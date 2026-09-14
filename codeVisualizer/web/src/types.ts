export type SerializedValue =
  | null
  | boolean
  | number
  | string
  | SerializedValue[]
  | { [key: string]: SerializedValue };

export interface ProblemData {
  title: string;
  title_slug: string;
  difficulty: string;
  question_id: string;
  content_text: string;
  entrypoint: string | null;
  starter_code: string | null;
  sample_args: unknown[][];
  source_url: string;
}

export interface TraceEvent {
  seq: number;
  type: "call" | "line" | "state" | "return" | "exception";
  line: number | null;
  source: string;
  function: string;
  depth: number;
  locals_before?: Record<string, SerializedValue>;
  locals_after?: Record<string, SerializedValue>;
  changed: string[];
  return_value?: SerializedValue;
  exception?: string;
  operation?: string;
  operation_index?: number;
  operation_args?: SerializedValue;
}

export interface TraceRun {
  status: string;
  entrypoint: string | null;
  entrypoint_source?: string;
  entrypoint_kind?: "function" | "design";
  result: SerializedValue;
  stdout: string;
  error: string | null;
  events: TraceEvent[];
  event_count: number;
  sandbox_mode: string;
}

export interface TraceResponse {
  candidate: TraceRun;
  reference: TraceRun | null;
  comparison: {
    matches: boolean;
    candidate_result: SerializedValue;
    reference_result: SerializedValue;
  } | null;
}
