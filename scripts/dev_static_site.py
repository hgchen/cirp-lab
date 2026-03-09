#!/usr/bin/env python3

from __future__ import annotations

import argparse
import functools
import http.server
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT_DIR / "dist"
BUILD_SCRIPT = ROOT_DIR / "scripts" / "build_static_site.sh"
WATCH_DIRS = [
    ROOT_DIR / "images",
]
WATCH_FILES = [
    ROOT_DIR / "index.html",
    ROOT_DIR / "members.md",
    ROOT_DIR / "news.md",
    ROOT_DIR / "publications.bib",
    ROOT_DIR / "README.md",
    BUILD_SCRIPT,
]
IGNORE_DIRS = {".git", "dist", "__pycache__"}
IGNORE_SUFFIXES = {".DS_Store", ".swp", ".tmp"}


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


def iter_watch_paths() -> list[Path]:
    paths: list[Path] = []

    for file_path in WATCH_FILES:
        if file_path.exists():
            paths.append(file_path)

    for watch_dir in WATCH_DIRS:
        if not watch_dir.exists():
            continue
        for path in watch_dir.rglob("*"):
            if not path.is_file():
                continue
            if any(part in IGNORE_DIRS for part in path.parts):
                continue
            if path.name in IGNORE_SUFFIXES:
                continue
            paths.append(path)

    return sorted(set(paths))


def snapshot() -> dict[Path, float]:
    state: dict[Path, float] = {}
    for path in iter_watch_paths():
        try:
            state[path] = path.stat().st_mtime_ns
        except FileNotFoundError:
            continue
    return state


def run_build() -> bool:
    try:
        subprocess.run(
            ["bash", str(BUILD_SCRIPT)],
            cwd=ROOT_DIR,
            check=True,
        )
        print(f"[dev] build complete at {time.strftime('%H:%M:%S')}", flush=True)
        return True
    except subprocess.CalledProcessError as error:
        print(f"[dev] build failed with exit code {error.returncode}", file=sys.stderr, flush=True)
        return False


def serve(port: int) -> tuple[http.server.ThreadingHTTPServer, threading.Thread]:
    handler = functools.partial(NoCacheHandler, directory=str(DIST_DIR))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def watch_loop(interval: float) -> None:
    previous = snapshot()
    while True:
        time.sleep(interval)
        current = snapshot()
        if current != previous:
            changed = sorted(
                {str(path.relative_to(ROOT_DIR)) for path in set(previous) ^ set(current)}
                | {
                    str(path.relative_to(ROOT_DIR))
                    for path in set(previous) & set(current)
                    if previous[path] != current[path]
                }
            )
            if changed:
                print("[dev] changes detected:", ", ".join(changed), flush=True)
            run_build()
            previous = current


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve the CIRP Lab static site with auto rebuild.")
    parser.add_argument("--port", type=int, default=8000, help="Port to serve the site on")
    parser.add_argument("--interval", type=float, default=0.8, help="Polling interval in seconds")
    args = parser.parse_args()

    if not BUILD_SCRIPT.exists():
        print("[dev] build script not found", file=sys.stderr)
        return 1

    if not run_build():
        return 1

    server, _thread = serve(args.port)
    print(f"[dev] serving {DIST_DIR} at http://127.0.0.1:{args.port}", flush=True)
    print("[dev] save files and refresh the browser to see updates", flush=True)

    def shutdown(_signum: int, _frame: object) -> None:
        print("\n[dev] shutting down", flush=True)
        server.shutdown()
        server.server_close()
        raise SystemExit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        watch_loop(args.interval)
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    raise SystemExit(main())
