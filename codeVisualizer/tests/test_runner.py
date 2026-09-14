import unittest

from runner.trace_runner import execute


DIAMETER_CODE = """class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        answer = 0
        def depth(node):
            nonlocal answer
            if not node:
                return 0
            left = depth(node.left)
            right = depth(node.right)
            answer = max(answer, left + right)
            return 1 + max(left, right)
        depth(root)
        return answer
"""

LFU_CODE = """class CacheNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.frequency = 1

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.values = {}
        self.clock = 0

    def get(self, key: int) -> int:
        if key not in self.values:
            return -1
        node, _ = self.values[key]
        node.frequency += 1
        self.clock += 1
        self.values[key] = (node, self.clock)
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
        if key in self.values:
            node, _ = self.values[key]
            node.value = value
            self.get(key)
            return
        if len(self.values) == self.capacity:
            victim = min(self.values, key=lambda item: (self.values[item][0].frequency, self.values[item][1]))
            del self.values[victim]
        self.clock += 1
        self.values[key] = (CacheNode(key, value), self.clock)
"""


class RunnerTests(unittest.TestCase):
    def test_traces_recursive_tree_solution(self):
        result = execute(
            {
                "code": DIAMETER_CODE,
                "entrypoint": "Solution.diameterOfBinaryTree",
                "args": [[1, 2, 3, 4, 5]],
            }
        )

        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["result"], 3)
        self.assertGreater(result["event_count"], 20)
        self.assertTrue(any(event["type"] == "call" and event["depth"] >= 3 for event in result["events"]))
        self.assertTrue(any(event["type"] == "state" and "answer" in event["changed"] for event in result["events"]))

    def test_nested_call_effect_appears_after_child_trace(self):
        result = execute(
            {
                "code": DIAMETER_CODE,
                "entrypoint": "Solution.diameterOfBinaryTree",
                "args": [[1, 2, 3]],
            }
        )
        root_call_line = next(
            event
            for event in result["events"]
            if event["type"] == "line" and event["source"] == "depth(root)"
        )
        root_call_effect = next(
            event
            for event in result["events"]
            if event["type"] == "state" and event["source"] == "depth(root)"
        )
        child_calls = [
            event for event in result["events"] if event["type"] == "call" and event["function"] == "depth"
        ]
        self.assertLess(root_call_line["seq"], child_calls[0]["seq"])
        self.assertGreater(root_call_effect["seq"], child_calls[-1]["seq"])

    def test_infers_solution_entrypoint(self):
        code = """class Solution:
    def twoSum(self, nums: List[int], target: int):
        seen = {}
        for i, number in enumerate(nums):
            if target - number in seen:
                return [seen[target - number], i]
            seen[number] = i
"""
        result = execute({"code": code, "args": [[2, 7, 11, 15], 9]})
        self.assertEqual(result["entrypoint"], "Solution.twoSum")
        self.assertEqual(result["entrypoint_source"], "source code")
        self.assertEqual(result["result"], [0, 1])

    def test_falls_back_to_source_when_problem_hint_does_not_match(self):
        code = "def solve(values):\n    return sum(values)"
        result = execute(
            {
                "code": code,
                "entrypoint": "Solution.someLeetCodeMethod",
                "args": [[1, 2, 3]],
            }
        )
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["entrypoint"], "solve")
        self.assertEqual(result["entrypoint_source"], "source code")
        self.assertEqual(result["result"], 6)

    def test_rejects_unsafe_import(self):
        result = None
        with self.assertRaisesRegex(ValueError, "Import not allowed"):
            result = execute({"code": "import os\ndef solve(): return os.getcwd()", "args": []})
        self.assertIsNone(result)

    def test_auto_detects_and_replays_design_class(self):
        operations = ["LFUCache", "put", "put", "get", "put", "get", "get"]
        arguments = [[2], [1, 1], [2, 2], [1], [3, 3], [2], [3]]
        result = execute({"code": LFU_CODE, "args": [operations, arguments]})

        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["entrypoint"], "LFUCache")
        self.assertEqual(result["entrypoint_kind"], "design")
        self.assertEqual(result["result"], [None, None, None, 1, None, -1, 3])
        self.assertTrue(any(event.get("operation") == "put" for event in result["events"]))
        self.assertTrue(any(event.get("operation_index") == 6 for event in result["events"]))

    def test_explains_markdown_fences(self):
        with self.assertRaisesRegex(ValueError, "Markdown"):
            execute({"code": "```python\ndef solve():\n    return 1\n```", "args": []})


if __name__ == "__main__":
    unittest.main()
