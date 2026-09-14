import type { ProblemData, TraceResponse } from "./types";

async function request<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || `Request failed with status ${response.status}`);
  }
  return data as T;
}

export function fetchProblem(url: string) {
  return request<ProblemData>("/api/problems/fetch", { url });
}

export function runTrace(body: {
  code: string;
  reference_code?: string;
  entrypoint?: string;
  args: unknown[];
}) {
  return request<TraceResponse>("/api/trace", body);
}
