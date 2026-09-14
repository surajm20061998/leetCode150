"""Execute and trace one LeetCode-style Python solution.

The process accepts a JSON payload on stdin and emits one JSON document on stdout.
It is deliberately self-contained so the same file can run inside the Docker sandbox.
"""

from __future__ import annotations

import ast
import bisect
import builtins
import collections
import contextlib
import functools
import heapq
import inspect
import io
import itertools
import json
import math
import operator
import sys
import traceback
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple


MAX_EVENTS = 4_000
MAX_ITEMS = 40
MAX_DEPTH = 5
ALLOWED_IMPORTS = {
    "bisect",
    "collections",
    "functools",
    "heapq",
    "itertools",
    "math",
    "operator",
    "typing",
}


class TraceLimitExceeded(RuntimeError):
    pass


class TreeNode:
    def __init__(self, val: int = 0, left: Optional["TreeNode"] = None, right: Optional["TreeNode"] = None):
        self.val = val
        self.left = left
        self.right = right


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next


class Node:
    def __init__(self, val: int = 0, neighbors: Optional[list["Node"]] = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def build_tree(values: list[Any]) -> Optional[TreeNode]:
    if not values or values[0] is None:
        return None
    nodes = [None if value is None else TreeNode(value) for value in values]
    children = iter(nodes[1:])
    for node in nodes:
        if node is None:
            continue
        node.left = next(children, None)
        node.right = next(children, None)
    return nodes[0]


def build_linked_list(values: list[Any]) -> Optional[ListNode]:
    sentinel = ListNode()
    tail = sentinel
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return sentinel.next


def build_graph(adjacency: list[list[int]]) -> Optional[Node]:
    if not adjacency:
        return None
    nodes = [Node(index + 1) for index in range(len(adjacency))]
    for index, neighbors in enumerate(adjacency):
        nodes[index].neighbors = [nodes[value - 1] for value in neighbors]
    return nodes[0]


class Snapshotter:
    def __init__(self) -> None:
        self._object_ids: dict[int, str] = {}
        self._next_object_id = 1

    def _stable_id(self, value: Any) -> str:
        identity = id(value)
        if identity not in self._object_ids:
            self._object_ids[identity] = f"obj-{self._next_object_id}"
            self._next_object_id += 1
        return self._object_ids[identity]

    def value(self, value: Any, depth: int = 0, path: Optional[set[int]] = None) -> Any:
        if value is None or isinstance(value, (bool, int, float, str)):
            if isinstance(value, str) and len(value) > 300:
                return value[:300] + "…"
            return value
        if depth >= MAX_DEPTH:
            return {"$truncated": type(value).__name__}
        path = set() if path is None else path
        identity = id(value)
        if identity in path:
            return {"$ref": self._stable_id(value)}
        next_path = path | {identity}

        if isinstance(value, (list, tuple)):
            items = [self.value(item, depth + 1, next_path) for item in value[:MAX_ITEMS]]
            if len(value) > MAX_ITEMS:
                items.append({"$more": len(value) - MAX_ITEMS})
            return items if isinstance(value, list) else {"$type": "tuple", "items": items}
        if isinstance(value, (set, frozenset)):
            ordered = sorted(value, key=repr)
            return {
                "$type": "set",
                "items": [self.value(item, depth + 1, next_path) for item in ordered[:MAX_ITEMS]],
            }
        if isinstance(value, dict):
            items = list(value.items())[:MAX_ITEMS]
            return {
                "$type": "dict",
                "entries": [
                    [self.value(key, depth + 1, next_path), self.value(item, depth + 1, next_path)]
                    for key, item in items
                ],
            }
        if isinstance(value, collections.deque):
            return {
                "$type": "deque",
                "items": [self.value(item, depth + 1, next_path) for item in list(value)[:MAX_ITEMS]],
            }
        if isinstance(value, (TreeNode, ListNode, Node)) or hasattr(value, "__dict__"):
            public = {
                key: item
                for key, item in vars(value).items()
                if not key.startswith("_")
            }
            return {
                "$id": self._stable_id(value),
                "$type": type(value).__name__,
                "attrs": {
                    key: self.value(item, depth + 1, next_path)
                    for key, item in list(public.items())[:MAX_ITEMS]
                },
            }
        if callable(value):
            return {"$type": "callable", "name": getattr(value, "__name__", type(value).__name__)}
        return {"$type": type(value).__name__, "repr": repr(value)[:300]}

    def locals(self, values: dict[str, Any]) -> dict[str, Any]:
        return {
            key: self.value(value)
            for key, value in values.items()
            if not key.startswith("__") and not inspect.ismodule(value)
        }


class TraceCollector:
    def __init__(self, code: str) -> None:
        self.lines = code.splitlines()
        self.events: list[dict[str, Any]] = []
        self.pending: dict[int, dict[str, Any]] = {}
        self.snapshotter = Snapshotter()
        self.current_operation: str | None = None
        self.current_operation_index: int | None = None
        self.current_operation_args: Any = None

    def _depth(self, frame: Any) -> int:
        depth = 0
        cursor = frame.f_back
        while cursor:
            if cursor.f_code.co_filename == "<candidate>":
                depth += 1
            cursor = cursor.f_back
        return depth

    def _source(self, line: Optional[int]) -> str:
        if line is None or line < 1 or line > len(self.lines):
            return ""
        return self.lines[line - 1].strip()

    def _append(self, event: dict[str, Any]) -> None:
        if len(self.events) >= MAX_EVENTS:
            raise TraceLimitExceeded(f"Trace exceeded {MAX_EVENTS} events")
        event["seq"] = len(self.events)
        if self.current_operation is not None:
            event["operation"] = self.current_operation
            event["operation_index"] = self.current_operation_index
            event["operation_args"] = self.snapshotter.value(self.current_operation_args)
        self.events.append(event)

    def _finish_pending(self, frame: Any) -> None:
        pending = self.pending.pop(id(frame), None)
        if pending is None:
            return
        after = self.snapshotter.locals(frame.f_locals)
        before = pending.get("locals_before", {})
        changed = sorted(
            key for key in set(before) | set(after) if before.get(key) != after.get(key)
        )
        if changed:
            self._append(
                {
                    "type": "state",
                    "line": pending["line"],
                    "source": pending["source"],
                    "function": pending["function"],
                    "depth": pending["depth"],
                    "locals_before": before,
                    "locals_after": after,
                    "changed": changed,
                }
            )

    def trace(self, frame: Any, event: str, arg: Any):
        if frame.f_code.co_filename != "<candidate>":
            return self.trace

        if event == "call":
            self._append(
                {
                    "type": "call",
                    "line": frame.f_lineno,
                    "source": self._source(frame.f_lineno),
                    "function": frame.f_code.co_name,
                    "depth": self._depth(frame),
                    "locals_after": self.snapshotter.locals(frame.f_locals),
                    "changed": [],
                }
            )
        elif event == "line":
            self._finish_pending(frame)
            item = {
                "type": "line",
                "line": frame.f_lineno,
                "source": self._source(frame.f_lineno),
                "function": frame.f_code.co_name,
                "depth": self._depth(frame),
                "locals_before": self.snapshotter.locals(frame.f_locals),
                "locals_after": self.snapshotter.locals(frame.f_locals),
                "changed": [],
            }
            self._append(item)
            self.pending[id(frame)] = {
                "line": item["line"],
                "source": item["source"],
                "function": item["function"],
                "depth": item["depth"],
                "locals_before": item["locals_before"],
            }
        elif event == "return":
            self._finish_pending(frame)
            self._append(
                {
                    "type": "return",
                    "line": frame.f_lineno,
                    "source": self._source(frame.f_lineno),
                    "function": frame.f_code.co_name,
                    "depth": self._depth(frame),
                    "return_value": self.snapshotter.value(arg),
                    "locals_after": self.snapshotter.locals(frame.f_locals),
                    "changed": [],
                }
            )
        elif event == "exception":
            exc_type, exc_value, _ = arg
            self._append(
                {
                    "type": "exception",
                    "line": frame.f_lineno,
                    "source": self._source(frame.f_lineno),
                    "function": frame.f_code.co_name,
                    "depth": self._depth(frame),
                    "exception": f"{exc_type.__name__}: {exc_value}",
                    "locals_after": self.snapshotter.locals(frame.f_locals),
                    "changed": [],
                }
            )
        return self.trace


def validate_source(code: str) -> ast.Module:
    if "```" in code:
        raise ValueError("Remove the Markdown ``` fences and paste only Python code")
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [alias.name.split(".")[0] for alias in node.names]
            if isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module.split(".")[0]]
            rejected = [name for name in names if name not in ALLOWED_IMPORTS]
            if rejected:
                raise ValueError(f"Import not allowed in visualizer: {', '.join(rejected)}")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in {"open", "eval", "exec", "compile", "input", "breakpoint", "__import__"}:
                raise ValueError(f"Call not allowed in visualizer: {node.func.id}")
    return tree


def infer_entrypoint(tree: ast.Module) -> str:
    solution_methods: list[str] = []
    functions: list[str] = []
    design_classes: list[str] = []
    helper_classes = {"ListNode", "TreeNode", "Node", "LinkedList", "DoublyLinkedList"}
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "Solution":
            solution_methods = [
                child.name
                for child in node.body
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and not child.name.startswith("_")
            ]
        elif isinstance(node, ast.ClassDef) and node.name not in helper_classes:
            public_methods = [
                child
                for child in node.body
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and not child.name.startswith("_")
            ]
            if public_methods:
                design_classes.append(node.name)
        elif isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            functions.append(node.name)
    if solution_methods:
        return f"Solution.{solution_methods[0]}"
    if functions:
        return functions[-1]
    if design_classes:
        return design_classes[-1]
    raise ValueError("Could not find a Solution method, standalone function, or design class")


def resolve_entrypoint(
    requested: str | None,
    tree: ast.Module,
    namespace: dict[str, Any],
) -> tuple[str, Any, str, str]:
    """Resolve a hidden problem hint first, then infer from the pasted source."""
    candidates = [item for item in (requested, infer_entrypoint(tree)) if item]
    for index, entrypoint in enumerate(dict.fromkeys(candidates)):
        if "." in entrypoint:
            class_name, method_name = entrypoint.split(".", 1)
            class_value = namespace.get(class_name)
            if class_value is None or not hasattr(class_value, method_name):
                continue
            instance = class_value()
            return entrypoint, getattr(instance, method_name), "problem hint" if index == 0 and requested else "source code", "function"
        target = namespace.get(entrypoint)
        if isinstance(target, type):
            return entrypoint, target, "input operations" if index == 0 and requested else "source code", "design"
        if callable(target):
            return entrypoint, target, "problem hint" if index == 0 and requested else "source code", "function"
    raise ValueError("Could not match the LeetCode method or infer a runnable function from the pasted code")


def adapt_argument(name: str, annotation: Any, value: Any, method_name: str) -> Any:
    annotation_name = str(annotation)
    if isinstance(value, list) and ("TreeNode" in annotation_name or name == "root"):
        return build_tree(value)
    if isinstance(value, list) and ("ListNode" in annotation_name or name == "head"):
        return build_linked_list(value)
    if (
        isinstance(value, list)
        and ("Node" in annotation_name or method_name == "cloneGraph")
        and all(isinstance(item, list) for item in value)
    ):
        return build_graph(value)
    return value


def safe_import(name: str, globals_: Any = None, locals_: Any = None, fromlist: Any = (), level: int = 0):
    root = name.split(".")[0]
    if root not in ALLOWED_IMPORTS:
        raise ImportError(f"Import not allowed in visualizer: {root}")
    return builtins.__import__(name, globals_, locals_, fromlist, level)


def execute(payload: dict[str, Any]) -> dict[str, Any]:
    code = payload.get("code", "")
    tree = validate_source(code)
    raw_args = payload.get("args", [])
    if not isinstance(raw_args, list):
        raise ValueError("args must be a JSON array")

    allowed_builtins = dict(vars(builtins))
    for name in ("open", "eval", "exec", "compile", "input", "breakpoint"):
        allowed_builtins.pop(name, None)
    allowed_builtins["__import__"] = safe_import

    namespace: dict[str, Any] = {
        "__builtins__": allowed_builtins,
        "__name__": "candidate_solution",
        "List": List,
        "Optional": Optional,
        "Dict": Dict,
        "Set": Set,
        "Tuple": Tuple,
        "TreeNode": TreeNode,
        "ListNode": ListNode,
        "Node": Node,
        "collections": collections,
        "defaultdict": collections.defaultdict,
        "deque": collections.deque,
        "Counter": collections.Counter,
        "heapq": heapq,
        "math": math,
        "bisect": bisect,
        "functools": functools,
        "itertools": itertools,
        "operator": operator,
    }
    # Use the real compile/exec outside the candidate's restricted builtins.
    compiled = compile(tree, "<candidate>", "exec")
    exec(compiled, namespace, namespace)

    operations_hint = None
    if (
        len(raw_args) == 2
        and isinstance(raw_args[0], list)
        and raw_args[0]
        and isinstance(raw_args[0][0], str)
    ):
        operations_hint = raw_args[0][0]
    entrypoint, target, entrypoint_source, entrypoint_kind = resolve_entrypoint(
        payload.get("entrypoint") or operations_hint, tree, namespace
    )
    method_name = entrypoint.rsplit(".", 1)[-1]

    collector = TraceCollector(code)
    stdout = io.StringIO()
    result: Any = None
    status = "completed"
    error = None
    try:
        with contextlib.redirect_stdout(stdout):
            sys.settrace(collector.trace)
            if entrypoint_kind == "design":
                if (
                    len(raw_args) != 2
                    or not isinstance(raw_args[0], list)
                    or not isinstance(raw_args[1], list)
                    or len(raw_args[0]) != len(raw_args[1])
                ):
                    raise ValueError(
                        "Design problems expect [operations, arguments], with matching list lengths"
                    )
                operations, operation_args = raw_args
                if not operations or operations[0] != entrypoint:
                    raise ValueError(f"The first operation must construct {entrypoint}")
                outputs: list[Any] = []
                instance = None
                for index, (operation, arguments) in enumerate(zip(operations, operation_args)):
                    if not isinstance(arguments, list):
                        raise ValueError(f"Arguments for operation {operation} must be a JSON array")
                    collector.current_operation = operation
                    collector.current_operation_index = index
                    collector.current_operation_args = arguments
                    if index == 0:
                        instance = target(*arguments)
                        outputs.append(None)
                    else:
                        if instance is None or not hasattr(instance, operation):
                            raise ValueError(f"{entrypoint} has no operation named {operation}")
                        outputs.append(getattr(instance, operation)(*arguments))
                result = outputs
            else:
                signature = inspect.signature(target)
                parameters = list(signature.parameters.values())
                if len(raw_args) != len(parameters):
                    raise ValueError(
                        f"{entrypoint} expects {len(parameters)} argument(s), received {len(raw_args)}"
                    )
                args = [
                    adapt_argument(parameter.name, parameter.annotation, value, method_name)
                    for parameter, value in zip(parameters, raw_args)
                ]
                result = target(*args)
    except TraceLimitExceeded as exc:
        status = "trace_limit"
        error = str(exc)
    except Exception as exc:  # The exception is returned as part of the trace result.
        status = "error"
        error = f"{type(exc).__name__}: {exc}"
    finally:
        sys.settrace(None)

    return {
        "status": status,
        "entrypoint": entrypoint,
        "entrypoint_source": entrypoint_source,
        "entrypoint_kind": entrypoint_kind,
        "result": collector.snapshotter.value(result),
        "stdout": stdout.getvalue()[-10_000:],
        "error": error,
        "events": collector.events,
        "event_count": len(collector.events),
    }


def main() -> None:
    try:
        payload = json.load(sys.stdin)
        output = execute(payload)
    except Exception as exc:
        output = {
            "status": "setup_error",
            "entrypoint": None,
            "result": None,
            "stdout": "",
            "error": f"{type(exc).__name__}: {exc}",
            "events": [],
            "event_count": 0,
        }
    json.dump(output, sys.stdout, separators=(",", ":"))


if __name__ == "__main__":
    main()
