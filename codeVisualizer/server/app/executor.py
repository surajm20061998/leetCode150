from __future__ import annotations

import asyncio
import json
import os
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "runner" / "trace_runner.py"
IMAGE_NAME = os.getenv("CODE_VISUALIZER_RUNNER_IMAGE", "code-visualizer-runner:latest")
TIMEOUT_SECONDS = 5


async def _docker_available() -> bool:
    if not shutil.which("docker"):
        return False
    process = await asyncio.create_subprocess_exec(
        "docker",
        "image",
        "inspect",
        IMAGE_NAME,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL,
    )
    return await process.wait() == 0


async def _command() -> tuple[list[str], str]:
    configured = os.getenv("CODE_VISUALIZER_RUNNER_MODE", "auto").lower()
    use_docker = configured == "docker" or (configured == "auto" and await _docker_available())
    if use_docker:
        return (
            [
                "docker",
                "run",
                "--rm",
                "--interactive",
                "--network",
                "none",
                "--read-only",
                "--tmpfs",
                "/tmp:size=16m",
                "--memory",
                "256m",
                "--cpus",
                "0.75",
                "--pids-limit",
                "32",
                "--security-opt",
                "no-new-privileges",
                "--cap-drop",
                "ALL",
                IMAGE_NAME,
            ],
            "docker",
        )
    if configured == "docker":
        raise RuntimeError(f"Docker runner image {IMAGE_NAME} is not available")
    return ([shutil.which("python3") or "python3", "-I", str(RUNNER)], "local subprocess")


async def run_trace(payload: dict[str, Any]) -> dict[str, Any]:
    command, sandbox_mode = await _command()
    process = await asyncio.create_subprocess_exec(
        *command,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(
            process.communicate(json.dumps(payload).encode()),
            timeout=TIMEOUT_SECONDS,
        )
    except asyncio.TimeoutError:
        process.kill()
        await process.wait()
        return {
            "status": "timeout",
            "entrypoint": payload.get("entrypoint"),
            "result": None,
            "stdout": "",
            "error": f"Execution exceeded {TIMEOUT_SECONDS} seconds",
            "events": [],
            "event_count": 0,
            "sandbox_mode": sandbox_mode,
        }
    if process.returncode != 0:
        return {
            "status": "runner_error",
            "entrypoint": payload.get("entrypoint"),
            "result": None,
            "stdout": "",
            "error": stderr.decode(errors="replace")[-2_000:] or "Runner exited unexpectedly",
            "events": [],
            "event_count": 0,
            "sandbox_mode": sandbox_mode,
        }
    result = json.loads(stdout)
    result["sandbox_mode"] = sandbox_mode
    return result
