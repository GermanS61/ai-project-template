#!/usr/bin/env python3
"""Check repository text files for final newlines and trailing whitespace."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BINARY_SUFFIXES = {
    ".7z",
    ".avif",
    ".bmp",
    ".bz2",
    ".dll",
    ".doc",
    ".docx",
    ".dylib",
    ".eot",
    ".exe",
    ".gif",
    ".gz",
    ".ico",
    ".jpeg",
    ".jpg",
    ".mov",
    ".mp3",
    ".mp4",
    ".ogg",
    ".otf",
    ".pdf",
    ".png",
    ".ppt",
    ".pptx",
    ".rar",
    ".so",
    ".tar",
    ".tgz",
    ".tif",
    ".tiff",
    ".ttf",
    ".wav",
    ".webm",
    ".webp",
    ".woff",
    ".woff2",
    ".xls",
    ".xlsx",
    ".xz",
    ".zip",
}


def repository_files() -> list[Path]:
    result = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "-z",
        ],
        check=True,
        capture_output=True,
    )
    return [ROOT / Path(item.decode("utf-8")) for item in result.stdout.split(b"\0") if item]


def without_line_ending(line: bytes) -> bytes:
    if line.endswith(b"\r\n"):
        return line[:-2]
    if line.endswith((b"\n", b"\r")):
        return line[:-1]
    return line


def is_allowed_markdown_break(path: Path, line: bytes, trailing: bytes) -> bool:
    return path.suffix.lower() == ".md" and trailing == b"  " and bool(line[:-2].strip())


def main() -> int:
    errors: list[str] = []
    checked = 0

    for path in repository_files():
        if not path.is_file() or path.suffix.lower() in BINARY_SUFFIXES:
            continue

        data = path.read_bytes()
        if b"\0" in data[:8192]:
            continue

        relative = path.relative_to(ROOT).as_posix()
        try:
            data.decode("utf-8")
        except UnicodeDecodeError as error:
            errors.append(f"{relative}: is not valid UTF-8 ({error})")
            continue

        checked += 1
        if data.startswith(b"\xef\xbb\xbf"):
            errors.append(f"{relative}: UTF-8 BOM is not allowed")
        if data and not data.endswith(b"\n"):
            errors.append(f"{relative}: missing final newline")

        for line_number, raw_line in enumerate(data.splitlines(keepends=True), start=1):
            line = without_line_ending(raw_line)
            trailing = line[len(line.rstrip(b" \t")) :]
            if trailing and not is_allowed_markdown_break(path, line, trailing):
                errors.append(f"{relative}:{line_number}: trailing whitespace")

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1

    print(f"Checked EOF and whitespace in {checked} text files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
