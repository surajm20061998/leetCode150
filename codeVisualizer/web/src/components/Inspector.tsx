import type { SerializedValue, TraceEvent } from "../types";

function display(value: SerializedValue | undefined) {
  if (typeof value === "string") return value;
  return JSON.stringify(value, null, 2);
}

function narration(event: TraceEvent) {
  if (event.type === "call") return `Enter ${event.function}(). Its arguments are now on the call stack.`;
  if (event.type === "return") return `${event.function}() returns ${display(event.return_value)}.`;
  if (event.type === "exception") return event.exception || "Execution raised an exception.";
  if (event.type === "state") {
    return `Line ${event.line} finished. It changed ${event.changed.join(", ")}.`;
  }
  if (event.changed.length) {
    return `Line ${event.line} executed. It changed ${event.changed.join(", ")}.`;
  }
  return `Next, execute line ${event.line} in ${event.function}().`;
}

export function Inspector({ event }: { event: TraceEvent }) {
  const locals = event.locals_after || {};
  return (
    <aside className="inspector">
      <section className="explanation-card">
        <div className="event-context">
          <span className={`event-tag ${event.type}`}>{event.type}</span>
          {event.operation && <span className="operation-tag">#{event.operation_index} {event.operation}</span>}
        </div>
        <p>{narration(event)}</p>
        {event.source && <code>{event.source}</code>}
      </section>

      <section>
        <div className="section-heading">
          <h3>Local state</h3>
          <span>{Object.keys(locals).length}</span>
        </div>
        <div className="variable-list">
          {Object.entries(locals).map(([name, value]) => (
            <div className={`variable ${event.changed.includes(name) ? "changed" : ""}`} key={name}>
              <div className="variable-name">
                <span>{name}</span>
                {event.changed.includes(name) && <small>changed</small>}
              </div>
              <pre>{display(value)}</pre>
            </div>
          ))}
          {!Object.keys(locals).length && <p className="muted">No local variables in this event.</p>}
        </div>
      </section>
    </aside>
  );
}
