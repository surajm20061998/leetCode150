import type { TraceEvent } from "../types";

function activeStack(events: TraceEvent[], step: number) {
  const stack: { name: string; depth: number }[] = [];
  for (const event of events.slice(0, step + 1)) {
    if (event.type === "call") {
      while (stack.length && stack[stack.length - 1].depth >= event.depth) stack.pop();
      stack.push({ name: event.function, depth: event.depth });
    } else if (event.type === "return") {
      let index = -1;
      for (let cursor = stack.length - 1; cursor >= 0; cursor -= 1) {
        if (stack[cursor].depth === event.depth) {
          index = cursor;
          break;
        }
      }
      if (index >= 0) stack.splice(index);
    }
  }
  return stack;
}

interface TimelineProps {
  events: TraceEvent[];
  step: number;
  playing: boolean;
  onStep: (step: number) => void;
  onPlaying: (playing: boolean) => void;
}

export function Timeline({ events, step, playing, onStep, onPlaying }: TimelineProps) {
  const stack = activeStack(events, step);
  return (
    <div className="timeline-shell">
      <div className="transport">
        <button onClick={() => onStep(0)} disabled={step === 0} aria-label="First step">↤</button>
        <button onClick={() => onStep(Math.max(0, step - 1))} disabled={step === 0} aria-label="Previous step">←</button>
        <button className="play" onClick={() => onPlaying(!playing)} aria-label={playing ? "Pause" : "Play"}>
          {playing ? "Ⅱ" : "▶"}
        </button>
        <button onClick={() => onStep(Math.min(events.length - 1, step + 1))} disabled={step === events.length - 1} aria-label="Next step">→</button>
        <button onClick={() => onStep(events.length - 1)} disabled={step === events.length - 1} aria-label="Last step">↦</button>
      </div>
      <div className="scrubber">
        <input
          type="range"
          min="0"
          max={Math.max(0, events.length - 1)}
          value={step}
          onChange={(event) => onStep(Number(event.target.value))}
          aria-label="Trace step"
        />
        <span>{step + 1} / {events.length}</span>
      </div>
      <div className="call-stack" aria-label="Call stack">
        <span className="stack-label">Call stack</span>
        {stack.length ? stack.map((item, index) => (
          <span className="stack-frame" key={`${item.depth}-${index}`}>{item.name}</span>
        )) : <span className="muted">—</span>}
      </div>
    </div>
  );
}
