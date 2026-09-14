FROM python:3.12-slim

RUN useradd --create-home --uid 10001 runner
WORKDIR /runner
COPY runner/trace_runner.py /runner/trace_runner.py
USER runner
ENTRYPOINT ["python", "-I", "/runner/trace_runner.py"]
