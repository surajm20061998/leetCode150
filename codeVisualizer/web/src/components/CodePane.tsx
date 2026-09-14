interface CodePaneProps {
  code: string;
  activeLine?: number | null;
}

export function CodePane({ code, activeLine }: CodePaneProps) {
  return (
    <div className="code-pane" aria-label="Executed source code">
      {code.split("\n").map((line, index) => {
        const lineNumber = index + 1;
        return (
          <div
            className={`code-line ${activeLine === lineNumber ? "active" : ""}`}
            key={lineNumber}
          >
            <span className="line-number">{lineNumber}</span>
            <code>{line || " "}</code>
          </div>
        );
      })}
    </div>
  );
}
