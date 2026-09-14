import type { SerializedValue, TraceEvent } from "../types";
import { TreeView } from "./TreeView";

type RecordValue = Record<string, SerializedValue>;

function isRecord(value: SerializedValue | undefined): value is RecordValue {
  return Boolean(value && typeof value === "object" && !Array.isArray(value));
}

function findType(value: SerializedValue | undefined, type: string): RecordValue | null {
  if (!value) return null;
  if (isRecord(value) && value.$type === type) return value;
  if (Array.isArray(value)) {
    for (const child of value) {
      const found = findType(child, type);
      if (found) return found;
    }
  } else if (isRecord(value)) {
    for (const child of Object.values(value)) {
      const found = findType(child, type);
      if (found) return found;
    }
  }
  return null;
}

function attribute(object: RecordValue, name: string): SerializedValue | undefined {
  const attrs = isRecord(object.attrs) ? object.attrs : {};
  return attrs[name];
}

function dictEntries(value: SerializedValue | undefined): [SerializedValue, SerializedValue][] {
  if (!isRecord(value) || value.$type !== "dict" || !Array.isArray(value.entries)) return [];
  return value.entries.filter(
    (entry): entry is [SerializedValue, SerializedValue] => Array.isArray(entry) && entry.length === 2,
  );
}

function primitiveAttribute(object: SerializedValue, ...names: string[]): string | number | null {
  if (!isRecord(object)) return null;
  for (const name of names) {
    const value = attribute(object, name);
    if (typeof value === "string" || typeof value === "number") return value;
  }
  return null;
}

function CacheView({ cache, event }: { cache: RecordValue; event: TraceEvent }) {
  const capacity = primitiveAttribute(cache, "cap", "capacity");
  const minimumFrequency = primitiveAttribute(cache, "lfuCnt", "minFrequency");
  const mapValue = attribute(cache, "nodeMap") ?? attribute(cache, "values");
  const nodes = dictEntries(mapValue).map(([mapKey, nodeValue]) => {
    let node = nodeValue;
    if (isRecord(nodeValue) && nodeValue.$type === "tuple" && Array.isArray(nodeValue.items)) {
      node = nodeValue.items[0];
    }
    return {
      key: primitiveAttribute(node, "key") ?? (typeof mapKey === "number" || typeof mapKey === "string" ? mapKey : "?"),
      value: primitiveAttribute(node, "val", "value") ?? "?",
      frequency: primitiveAttribute(node, "freq", "frequency") ?? 1,
    };
  });
  const frequencies = [...new Set(nodes.map((node) => Number(node.frequency)))].sort((a, b) => a - b);

  return (
    <div className="cache-canvas">
      <div className="operation-heading">
        <span>Operation {typeof event.operation_index === "number" ? event.operation_index : "—"}</span>
        <strong>{event.operation || "LFUCache"}({Array.isArray(event.operation_args) ? event.operation_args.join(", ") : ""})</strong>
      </div>
      <div className="cache-metrics">
        <div><small>capacity</small><strong>{capacity ?? "—"}</strong></div>
        <div><small>size</small><strong>{nodes.length}</strong></div>
        <div className="minimum"><small>min frequency</small><strong>{minimumFrequency ?? "—"}</strong></div>
      </div>
      <div className="frequency-board">
        {frequencies.map((frequency) => (
          <div className={`frequency-lane ${String(minimumFrequency) === String(frequency) ? "active" : ""}`} key={frequency}>
            <div className="frequency-label"><span>frequency</span><strong>{frequency}</strong></div>
            <div className="cache-nodes">
              {nodes.filter((node) => Number(node.frequency) === frequency).map((node) => (
                <div className="cache-node" key={String(node.key)}>
                  <span>key {node.key}</span>
                  <strong>{node.value}</strong>
                  <small>{String(minimumFrequency) === String(frequency) ? "LFU bucket" : `seen ${frequency}×`}</small>
                </div>
              ))}
            </div>
          </div>
        ))}
        {!nodes.length && (
          <div className="empty-cache">
            <span>∅</span><strong>Cache is empty</strong><small>The constructor has not inserted any keys yet.</small>
          </div>
        )}
      </div>
    </div>
  );
}

export function StructureView({ events, current }: { events: TraceEvent[]; current: TraceEvent }) {
  let cache: RecordValue | null = null;
  for (let index = Math.min(current.seq, events.length - 1); index >= 0; index -= 1) {
    cache = findType(events[index].locals_after as SerializedValue, "LFUCache");
    if (cache) break;
  }
  if (cache) return <CacheView cache={cache} event={current} />;
  return <TreeView events={events} current={current} />;
}
