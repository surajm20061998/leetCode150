import { useEffect, useMemo, useState } from "react";
import { fetchProblem, runTrace } from "./api";
import { CodePane } from "./components/CodePane";
import { Inspector } from "./components/Inspector";
import { Timeline } from "./components/Timeline";
import { StructureView } from "./components/StructureView";
import type { ProblemData, TraceResponse } from "./types";

const DEMO_URL = "https://leetcode.com/problems/diameter-of-binary-tree/";
const DEMO_CODE = `class Solution:
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
        return answer`;

function json(value: unknown) {
  return JSON.stringify(value, null, 2);
}

export default function App() {
  const [url, setUrl] = useState(DEMO_URL);
  const [problem, setProblem] = useState<ProblemData | null>(null);
  const [code, setCode] = useState(DEMO_CODE);
  const [referenceCode, setReferenceCode] = useState("");
  const [showReference, setShowReference] = useState(false);
  const [argsText, setArgsText] = useState("[[1, 2, 3, 4, 5]]");
  const [trace, setTrace] = useState<TraceResponse | null>(null);
  const [step, setStep] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [loadingProblem, setLoadingProblem] = useState(false);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [problemOpen, setProblemOpen] = useState(false);

  const events = trace?.candidate.events || [];
  const current = events[step];

  useEffect(() => {
    if (!playing || events.length === 0) return;
    const timer = window.setInterval(() => {
      setStep((currentStep) => {
        if (currentStep >= events.length - 1) {
          setPlaying(false);
          return currentStep;
        }
        return currentStep + 1;
      });
    }, 650);
    return () => window.clearInterval(timer);
  }, [playing, events.length]);

  useEffect(() => {
    const handler = (event: KeyboardEvent) => {
      if (!events.length || ["INPUT", "TEXTAREA"].includes((event.target as HTMLElement)?.tagName)) return;
      if (event.key === "ArrowRight") setStep((value) => Math.min(events.length - 1, value + 1));
      if (event.key === "ArrowLeft") setStep((value) => Math.max(0, value - 1));
      if (event.key === " ") {
        event.preventDefault();
        setPlaying((value) => !value);
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [events.length]);

  const statusLabel = useMemo(() => {
    if (!trace) return null;
    if (trace.comparison) return trace.comparison.matches ? "Outputs match" : "Outputs differ";
    return trace.candidate.status === "completed" ? "Trace complete" : trace.candidate.status;
  }, [trace]);

  async function importProblem() {
    setLoadingProblem(true);
    setError(null);
    try {
      const data = await fetchProblem(url);
      setProblem(data);
      if (data.sample_args.length) setArgsText(json(data.sample_args[0]));
      setProblemOpen(true);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Could not import the problem");
    } finally {
      setLoadingProblem(false);
    }
  }

  async function visualize() {
    setError(null);
    setRunning(true);
    setPlaying(false);
    try {
      const args = JSON.parse(argsText);
      if (!Array.isArray(args)) throw new Error("Test arguments must be a JSON array");
      const result = await runTrace({
        code,
        reference_code: showReference ? referenceCode : undefined,
        entrypoint: problem?.entrypoint || undefined,
        args,
      });
      setTrace(result);
      setStep(0);
      if (!result.candidate.events.length && result.candidate.error) setError(result.candidate.error);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Could not create the trace");
    } finally {
      setRunning(false);
    }
  }

  return (
    <div className="app">
      <header className="topbar">
        <a className="brand" href="#top" aria-label="Trace home">
          <span className="brand-mark">tr</span>
          <span>trace</span>
        </a>
        <span className="tagline">See the algorithm, not just the answer.</span>
        <div className="shortcut-hint"><kbd>←</kbd><kbd>→</kbd> step · <kbd>space</kbd> play</div>
      </header>

      <main id="top">
        <section className="hero">
          <div>
            <span className="eyebrow">Python algorithm visualizer</span>
            <h1>Walk through the part<br />your brain keeps skipping.</h1>
            <p>Import a LeetCode problem, paste your solution, and inspect each real state change.</p>
          </div>
          <div className="url-card">
            <label htmlFor="problem-url">LeetCode problem URL</label>
            <div className="url-row">
              <input id="problem-url" value={url} onChange={(event) => setUrl(event.target.value)} />
              <button className="secondary" onClick={importProblem} disabled={loadingProblem}>
                {loadingProblem ? "Importing…" : "Import"}
              </button>
            </div>
            <small>Public problems are loaded directly from LeetCode.</small>
          </div>
        </section>

        {error && <div className="error-banner"><span>!</span>{error}</div>}

        {problem && (
          <section className="problem-card">
            <button className="problem-summary" onClick={() => setProblemOpen(!problemOpen)}>
              <span className="problem-number">{problem.question_id.padStart(4, "0")}</span>
              <span className="problem-title">{problem.title}</span>
              <span className={`difficulty ${problem.difficulty.toLowerCase()}`}>{problem.difficulty}</span>
              <span className="chevron">{problemOpen ? "−" : "+"}</span>
            </button>
            {problemOpen && <pre className="problem-copy">{problem.content_text}</pre>}
          </section>
        )}

        <section className="setup-grid">
          <div className="editor-card">
            <div className="card-heading">
              <div><span className="step-number">01</span><h2>Your solution</h2></div>
              <span className="language-pill">Python 3</span>
            </div>
            <textarea
              className="solution-editor"
              aria-label="Python solution"
              value={code}
              onChange={(event) => setCode(event.target.value)}
              spellCheck={false}
            />
          </div>

          <div className="configuration-card">
            <div className="card-heading">
              <div><span className="step-number">02</span><h2>Visualize</h2></div>
              <span className="auto-pill">entry point auto-detected</span>
            </div>
            <div className="ready-card">
              <span className="ready-icon">✓</span>
              <div>
                <strong>{problem ? "Problem and example ready" : "Demo example ready"}</strong>
                <small>{problem?.entrypoint || "The runnable method will be detected from your code."}</small>
              </div>
            </div>
            <div className="example-picker">
              <span>Test case</span>
              <div className="example-options">
                {(problem?.sample_args.length ? problem.sample_args : [[[1, 2, 3, 4, 5]]]).map((sample, index) => (
                  <button
                    className={argsText === json(sample) ? "selected" : ""}
                    key={index}
                    onClick={() => setArgsText(json(sample))}
                  >
                    Example {index + 1}
                  </button>
                ))}
              </div>
              <pre className="argument-preview">{argsText}</pre>
            </div>
            <details className="advanced-settings">
              <summary>Advanced settings</summary>
              <div className="advanced-content">
                <label>Custom arguments <span className="label-note">JSON array</span>
                  <textarea value={argsText} onChange={(event) => setArgsText(event.target.value)} spellCheck={false} />
                </label>
                <label className="toggle-row">
                  <input type="checkbox" checked={showReference} onChange={(event) => setShowReference(event.target.checked)} />
                  <span><strong>Compare with a reference solution</strong><small>Run the same input and compare outputs.</small></span>
                </label>
                {showReference && (
                  <textarea
                    className="reference-editor"
                    aria-label="Reference Python solution"
                    value={referenceCode}
                    onChange={(event) => setReferenceCode(event.target.value)}
                    spellCheck={false}
                  />
                )}
              </div>
            </details>
            <button className="primary" onClick={visualize} disabled={running || !code.trim()}>
              <span>{running ? "Tracing…" : "Visualize execution"}</span><span>↗</span>
            </button>
          </div>
        </section>

        {trace && events.length > 0 && current && (
          <section className="trace-section">
            <div className="trace-heading">
              <div><span className="eyebrow">Execution trace</span><h2>{problem?.title || trace.candidate.entrypoint}</h2></div>
              <div className="run-badges">
                <span className={`run-status ${trace.comparison && !trace.comparison.matches ? "mismatch" : ""}`}>{statusLabel}</span>
                <span>{trace.candidate.entrypoint} · auto-detected</span>
                <span className={`sandbox-badge ${trace.candidate.sandbox_mode === "docker" ? "safe" : "local"}`}>{trace.candidate.sandbox_mode}</span>
                <span>{events.length} events</span>
              </div>
            </div>
            {trace.comparison && (
              <div className={`comparison-banner ${trace.comparison.matches ? "match" : "mismatch"}`}>
                <strong>{trace.comparison.matches ? "Candidate matches reference" : "Candidate and reference differ"}</strong>
                <span>Your result: <code>{json(trace.comparison.candidate_result)}</code></span>
                <span>Reference: <code>{json(trace.comparison.reference_result)}</code></span>
              </div>
            )}
            <Timeline events={events} step={step} playing={playing} onStep={setStep} onPlaying={setPlaying} />
            <div className="trace-workspace">
              <div className="source-panel">
                <div className="panel-title"><span>Source</span><span>line {current.line || "—"}</span></div>
                <CodePane code={code} activeLine={current.line} />
              </div>
              <div className="visual-panel">
                <div className="panel-title"><span>Structure</span><span className="live-dot">live state</span></div>
                <StructureView events={events} current={current} />
              </div>
              <Inspector event={current} />
            </div>
            {(trace.candidate.stdout || trace.candidate.error) && (
              <div className="console-panel">
                <span>Console</span><pre>{trace.candidate.error || trace.candidate.stdout}</pre>
              </div>
            )}
          </section>
        )}
      </main>
      <footer><span>trace / code visualizer</span><span>Built for the “wait, why did that happen?” moment.</span></footer>
    </div>
  );
}
