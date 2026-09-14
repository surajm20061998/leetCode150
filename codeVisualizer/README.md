# Trace — LeetCode Code Visualizer

Trace imports a public LeetCode problem from its URL, executes a pasted Python solution, and
turns the real runtime trace into an interactive walkthrough. The first vertical slice supports
source-line stepping, before/after local state, call-stack inspection, recursive tree traversal,
LeetCode `TreeNode`/`ListNode`/graph shims, and optional reference-solution comparison.

The entry point is automatic. LeetCode metadata is used as a hidden hint when a problem has been
imported; otherwise the runner detects the public `Solution` method or standalone function from
the pasted source. Raw arguments and reference comparison live under **Advanced settings**.

## Start locally

```bash
cd codeVisualizer
python3 -m venv .venv
.venv/bin/python -m pip install -r server/requirements.txt
cd web && npm install && cd ..
./run.sh
```

Open <http://localhost:5173>. The API runs on <http://127.0.0.1:8000>.

The interface opens with a working `diameterOfBinaryTree` example. Importing a LeetCode link
fills the title, description, entry point, and example arguments; it does not overwrite your
solution.

## Safer Docker execution

Without a runner image, development mode uses a restricted local subprocess and labels it in
the interface. Build the runner image to make Docker isolation the automatic default:

```bash
cd codeVisualizer
docker build -f docker/runner.Dockerfile -t code-visualizer-runner:latest .
```

Container runs have no network or repository mount, a read-only filesystem, a non-root user,
and CPU, memory, process, output, trace-count, and time limits. Set
`CODE_VISUALIZER_RUNNER_MODE=docker` to require Docker instead of allowing the development
fallback.

## Tests and production build

```bash
cd codeVisualizer
PYTHONPATH=. .venv/bin/python -m unittest discover -s tests -v
cd web && npm run build
```

## Current input contract

- Python `Solution` methods and standalone functions are supported.
- Stateful design classes such as `LFUCache` are auto-detected and replay LeetCode's
  `[operations, arguments]` input format.
- Test arguments must be a JSON array with one item per function parameter.
- Trees use LeetCode level-order arrays, such as `[[1, 2, 3, null, 4]]` for a one-argument
  method.
- Linked lists use arrays. Clone Graph uses an adjacency list.
- Common LeetCode typing names and algorithm modules are available automatically.
- External imports, filesystem access, `eval`, `exec`, `input`, and similar calls are rejected.

See [docs/architecture.md](docs/architecture.md) for the next implementation stages.
