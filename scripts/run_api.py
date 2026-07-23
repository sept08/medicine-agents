from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    environment = os.environ.copy()
    environment.setdefault(
        "MEDICINE_AGENTS_DATA_DIR", str(ROOT / "data" / "runtime")
    )
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "medicine_agents.interfaces.api:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
        ],
        cwd=ROOT,
        env=environment,
        check=False,
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())