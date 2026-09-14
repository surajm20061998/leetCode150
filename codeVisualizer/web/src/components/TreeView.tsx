import type { SerializedValue, TraceEvent } from "../types";

type RecordValue = Record<string, SerializedValue>;

function isRecord(value: SerializedValue | undefined): value is RecordValue {
  return Boolean(value && typeof value === "object" && !Array.isArray(value));
}

function isTreeNode(value: SerializedValue | undefined): value is RecordValue {
  return isRecord(value) && value.$type === "TreeNode";
}

function findTree(value: SerializedValue | undefined): RecordValue | null {
  if (isTreeNode(value)) return value;
  if (Array.isArray(value)) {
    for (const child of value) {
      const found = findTree(child);
      if (found) return found;
    }
  } else if (isRecord(value)) {
    for (const child of Object.values(value)) {
      const found = findTree(child);
      if (found) return found;
    }
  }
  return null;
}

function TreeNodeVisual({ node, activeId }: { node: RecordValue; activeId?: string }) {
  const attrs = isRecord(node.attrs) ? node.attrs : {};
  const left = isTreeNode(attrs.left) ? attrs.left : null;
  const right = isTreeNode(attrs.right) ? attrs.right : null;
  const id = typeof node.$id === "string" ? node.$id : undefined;
  const val = attrs.val ?? "?";
  return (
    <div className="tree-subtree">
      <div className={`tree-node ${id === activeId ? "current" : ""}`}>{String(val)}</div>
      {(left || right) && (
        <div className="tree-children">
          <div className={`tree-child ${left ? "has-node" : ""}`}>
            {left ? <TreeNodeVisual node={left} activeId={activeId} /> : <span className="tree-null">∅</span>}
          </div>
          <div className={`tree-child ${right ? "has-node" : ""}`}>
            {right ? <TreeNodeVisual node={right} activeId={activeId} /> : <span className="tree-null">∅</span>}
          </div>
        </div>
      )}
    </div>
  );
}

export function TreeView({ events, current }: { events: TraceEvent[]; current: TraceEvent }) {
  const initialLocals = events.find((event) => findTree(event.locals_after as SerializedValue))?.locals_after;
  const currentTree = findTree(current.locals_after as SerializedValue);
  const tree = findTree(initialLocals as SerializedValue) || currentTree;
  const activeId = typeof currentTree?.$id === "string" ? currentTree.$id : undefined;

  if (!tree) {
    return (
      <div className="empty-visual">
        <span className="empty-glyph">⌁</span>
        <p>No tree structure in this frame.</p>
        <small>The generic state inspector is still tracking every variable.</small>
      </div>
    );
  }
  return (
    <div className="tree-canvas">
      <TreeNodeVisual node={tree} activeId={activeId} />
    </div>
  );
}
