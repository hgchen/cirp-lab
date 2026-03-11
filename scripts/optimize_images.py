#!/usr/bin/env python3

from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


LARGE_IMAGE_BYTES = 1_000_000


@dataclass(frozen=True)
class Rule:
    max_edge: int
    output_suffix: str | None = None


SPECIFIC_RULES = {
    "images/bg_1.jpg": Rule(max_edge=1920),
    "images/bg_1.png": Rule(max_edge=1920, output_suffix=".jpg"),
    "images/uhm_logo.png": Rule(max_edge=512),
    "images/nsf_logo.png": Rule(max_edge=512),
}

PREFIX_RULES = [
    ("images/gallery/", Rule(max_edge=2000)),
    ("images/members/", Rule(max_edge=768)),
]


def available_tool() -> str | None:
    for name in ("ffmpeg", "sips"):
        if shutil.which(name):
            return name
    return None


def choose_rule(relative_path: str) -> Rule | None:
    if relative_path in SPECIFIC_RULES:
        return SPECIFIC_RULES[relative_path]
    for prefix, rule in PREFIX_RULES:
        if relative_path.startswith(prefix):
            return rule
    return None


def destination_path(source_path: Path, rule: Rule) -> Path:
    return source_path.with_suffix(rule.output_suffix) if rule.output_suffix else source_path


def ffmpeg_command(source_path: Path, output_path: Path, max_edge: int) -> list[str]:
    scale = (
        "scale="
        f"'if(gte(iw,ih),min({max_edge},iw),-2)':"
        f"'if(gte(iw,ih),-2,min({max_edge},ih))'"
    )
    command = [
        "ffmpeg",
        "-y",
        "-loglevel",
        "error",
        "-i",
        str(source_path),
        "-vf",
        scale,
    ]
    if output_path.suffix.lower() in {".jpg", ".jpeg"}:
        command.extend(["-q:v", "4"])
    elif output_path.suffix.lower() == ".png":
        command.extend(["-compression_level", "9"])
    command.append(str(output_path))
    return command


def sips_command(source_path: Path, output_path: Path, max_edge: int) -> list[str]:
    command = ["sips", "-Z", str(max_edge), str(source_path), "--out", str(output_path)]
    if output_path.suffix.lower() in {".jpg", ".jpeg"}:
        command[1:1] = ["-s", "format", "jpeg", "-s", "formatOptions", "82"]
    elif output_path.suffix.lower() == ".png":
        command[1:1] = ["-s", "format", "png"]
    return command


def rewrite_index_html(root_dir: Path) -> None:
    index_path = root_dir / "index.html"
    if not index_path.exists():
        return
    content = index_path.read_text(encoding="utf-8")
    updated = content.replace('url("images/bg_1.png")', 'url("images/bg_1.jpg")')
    if updated != content:
        index_path.write_text(updated, encoding="utf-8")


def optimize_image(tool: str, source_path: Path, rule: Rule) -> tuple[Path, int, int]:
    output_path = destination_path(source_path, rule)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_output = (
        output_path.with_name(f"{output_path.stem}.tmp{output_path.suffix}")
        if output_path == source_path
        else output_path
    )
    command = ffmpeg_command(source_path, temporary_output, rule.max_edge) if tool == "ffmpeg" else sips_command(source_path, temporary_output, rule.max_edge)
    original_size = source_path.stat().st_size
    subprocess.run(command, check=True)
    if temporary_output != output_path:
        temporary_output.replace(output_path)
    optimized_size = output_path.stat().st_size
    if output_path != source_path:
        source_path.unlink(missing_ok=True)
    return output_path, original_size, optimized_size


def main() -> int:
    root_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    images_dir = root_dir / "images"
    tool = available_tool()
    if not images_dir.exists():
        print(f"[images] skipped: {images_dir} does not exist")
        return 0
    if not tool:
        print("[images] skipped: neither ffmpeg nor sips is available")
        return 0

    rewrite_index_html(root_dir)

    optimized: list[tuple[str, str, int, int]] = []
    for source_path in sorted(path for path in images_dir.rglob("*") if path.is_file()):
        relative_path = source_path.relative_to(root_dir).as_posix()
        rule = choose_rule(relative_path)
        if not rule or source_path.stat().st_size <= LARGE_IMAGE_BYTES:
            continue
        try:
            output_path, original_size, optimized_size = optimize_image(tool, source_path, rule)
        except subprocess.CalledProcessError as error:
            print(f"[images] failed: {relative_path} ({error})", file=sys.stderr)
            continue
        optimized.append((relative_path, output_path.relative_to(root_dir).as_posix(), original_size, optimized_size))

    if optimized:
        print("[images] optimized oversized assets:")
        for source_rel, output_rel, original_size, optimized_size in optimized:
            print(
                f"  - {source_rel} -> {output_rel}: "
                f"{original_size / 1024:.0f}KB -> {optimized_size / 1024:.0f}KB"
            )
    else:
        print("[images] no oversized assets required optimization")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
