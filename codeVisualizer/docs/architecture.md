# Architecture and roadmap

## Implemented vertical slice

1. The web client sends a public LeetCode URL to the API.
2. The API extracts the problem slug and requests public metadata from LeetCode GraphQL.
3. The client sends code, entry point, and one editable argument set to the execution API.
4. The API uses the Docker runner image when available, otherwise a labeled development-only
   subprocess.
5. The runner validates imports, adapts LeetCode data structures, and records calls, executed
   lines, completed state changes, returns, and exceptions.
6. The client animates this normalized event list and renders a structure-aware tree view.

Stateful LeetCode design problems are also detected from their operation sequence. The runner
constructs the main class, replays each method call on the same instance, tags trace events with
their owning operation, and returns the usual LeetCode result array. LFU Cache has a dedicated
frequency-bucket visualization.

The trace uses separate `line` and `state` events. `line` means the interpreter is about to
execute that source line. `state` appears after the line finishes when a tracked value changed.
This distinction preserves chronological correctness when a line contains a recursive call.

## Next stages

1. Add array, pointer, stack, queue, map, and set renderers.
2. Add recursion-tree rendering independent of input data structure.
3. Add graph, grid, linked-list, and DP-table renderers.
4. Generate small editable edge cases from the imported constraints.
5. Add multi-case execution and earliest semantic divergence between candidate and reference.
6. Add grounded natural-language narration, session persistence, and JSON export/import.

The execution trace remains the source of truth. Generated explanations may describe a trace
event but must not create variable values or control-flow events that the runner did not record.
