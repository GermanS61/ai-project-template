#!/usr/bin/env python3
"""Detect high-confidence secrets in files included in the repository."""

from __future__ import annotations

import ipaddress
import json
import math
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[2]
ALLOW_MARKER = "secret-scan:" + " allow"
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
SIGNATURES = (
    (
        "private key",
        re.compile(
            r"-----BEGIN (?:(?:OPENSSH |RSA |EC |DSA |ENCRYPTED )?PRIVATE KEY|"
            r"PGP PRIVATE KEY BLOCK)-----"
        ),
    ),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,255}\b")),
    (
        "GitHub fine-grained token",
        re.compile(r"\bgithub_pat_[A-Za-z0-9_]{50,255}\b"),
    ),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("GitLab token", re.compile(r"\bglpat-[0-9A-Za-z_-]{20,255}\b")),
    ("npm token", re.compile(r"\bnpm_[0-9A-Za-z]{36}\b")),
    (
        "OpenAI API key",
        re.compile(r"\bsk-(?!ant-)(?:proj-|svcacct-)?[0-9A-Za-z_-]{20,255}\b"),
    ),
    (
        "Anthropic API key",
        re.compile(r"\bsk-ant-[0-9A-Za-z_-]{20,255}\b"),
    ),
    ("PyPI token", re.compile(r"\bpypi-[0-9A-Za-z_-]{50,255}\b")),
    ("SendGrid API key", re.compile(r"\bSG\.[0-9A-Za-z_-]{20,}\.[0-9A-Za-z_-]{20,}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{20,255}\b")),
    ("Stripe live key", re.compile(r"\b(?:sk|rk)_live_[0-9A-Za-z]{16,255}\b")),
)
ASSIGNMENT_RE = re.compile(
    r"(?ix)"
    r"[\"']?"
    r"(?:api[_-]?key|access[_-]?key|auth[_-]?token|bearer[_-]?token|"
    r"client[_-]?secret|private[_-]?key|secret(?:[_-]?key)?|password|passwd|token|"
    r"database[_-]?url|connection[_-]?(?:string|uri)|dsn)"
    r"[\"']?\s*[:=]\s*"
    r"(?:\"(?P<double>[^\"\r\n]{8,})\"|'(?P<single>[^'\r\n]{8,})'|"
    r"(?P<bare>[^\s,;]{8,}))"
)
SAFE_VALUES = {
    "changeme",
    "dummy",
    "example",
    "fake",
    "placeholder",
    "redacted",
    "replace",
    "sample",
    "test",
    "insert_api_key_here",
    "replace_with_your_api_key",
    "your_api_key",
    "your_api_key_here",
    "your_password",
    "your_password_here",
    "your_secret",
    "your_secret_here",
    "your_token",
    "your_token_here",
}
ENV_REFERENCE_RE = re.compile(r"^\$\{[A-Za-z_][A-Za-z0-9_]*\}$")
ANGLE_VALUE_RE = re.compile(r"^<(?P<inner>[^<>\r\n]+)>$")
PLACEHOLDER_SEGMENTS = {
    "anthropic",
    "api",
    "aws",
    "change",
    "credential",
    "credentials",
    "dummy",
    "example",
    "fake",
    "github",
    "gitlab",
    "goes",
    "google",
    "here",
    "in",
    "insert",
    "key",
    "me",
    "npm",
    "openai",
    "password",
    "passwd",
    "placeholder",
    "production",
    "pypi",
    "redacted",
    "replace",
    "sample",
    "secret",
    "sendgrid",
    "service",
    "slack",
    "stripe",
    "test",
    "token",
    "value",
    "with",
    "xxx",
    "your",
}
PLACEHOLDER_MARKERS = {
    "change",
    "dummy",
    "example",
    "fake",
    "here",
    "insert",
    "placeholder",
    "redacted",
    "replace",
    "sample",
    "test",
    "xxx",
    "your",
}
ANGLE_PLACEHOLDER_MARKERS = PLACEHOLDER_MARKERS | {
    "credential",
    "credentials",
    "key",
    "password",
    "secret",
    "token",
}
SIGNATURE_PREFIX_RE = re.compile(
    r"(?i)^(?:gh[pousr]_|github_pat_|(?:AKIA|ASIA)|AIza|glpat-|npm_|"
    r"sk-(?:ant-|proj-|svcacct-)?|pypi-|SG\.|xox[baprs]-|(?:sk|rk)_live_)"
)
HEX_SECRET_RE = re.compile(r"(?i)^[0-9a-f]{32,}$")
DEMO_LOCAL_CREDENTIALS = {
    ("demo", "demo"),
    ("test", "test"),
    ("user", "password"),
    ("username", "password"),
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


def event_revision_range() -> str | None:
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        return None

    try:
        event = json.loads(Path(event_path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise RuntimeError(f"cannot read GitHub event payload: {error}") from error

    event_name = os.environ.get("GITHUB_EVENT_NAME")
    if event_name == "pull_request":
        try:
            return f"{event['pull_request']['base']['sha']}..{event['pull_request']['head']['sha']}"
        except (KeyError, TypeError) as error:
            raise RuntimeError("pull_request event has no base/head SHA") from error

    if event_name == "push":
        before = event.get("before")
        after = event.get("after")
        if not isinstance(after, str) or not after:
            raise RuntimeError("push event has no after SHA")
        if isinstance(before, str) and before.strip("0"):
            return f"{before}..{after}"
        return after

    return None


def git_object_type(object_id: str) -> str | None:
    result = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "cat-file",
            "--batch-check=%(objectname) %(objecttype)",
        ],
        input=f"{object_id}\n".encode("ascii"),
        check=True,
        capture_output=True,
    )
    fields = result.stdout.decode("ascii", errors="strict").strip().split()
    if len(fields) == 2 and fields[0] == object_id and fields[1] == "missing":
        return None
    if len(fields) != 2:
        raise RuntimeError(f"unexpected git cat-file output for {object_id!r}")
    return fields[1]


def available_history_range(revision_range: str) -> str:
    """Fall back to reachable push history only when its before object is absent."""
    if os.environ.get("GITHUB_EVENT_NAME") != "push" or ".." not in revision_range:
        return revision_range

    before, after = revision_range.split("..", maxsplit=1)
    before_type = git_object_type(before)
    if before_type is None:
        print(
            "WARNING: push before object is unavailable; scanning all history "
            f"reachable from {after} instead. Unreachable rewritten history cannot "
            "be verified by this checkout.",
            file=sys.stderr,
        )
        return after
    if before_type != "commit":
        raise RuntimeError(
            f"push before object {before!r} has unexpected type {before_type!r}"
        )
    return revision_range


def changed_history_blobs(revision_range: str) -> list[tuple[str, bytes]]:
    objects = subprocess.run(
        ["git", "-C", str(ROOT), "-c", "core.quotePath=false", "rev-list", "--objects", revision_range],
        check=True,
        capture_output=True,
    ).stdout.splitlines()
    object_paths: dict[bytes, str] = {}
    object_ids: list[bytes] = []

    for entry in objects:
        object_id, separator, raw_path = entry.partition(b" ")
        if not object_id:
            continue
        object_ids.append(object_id)
        if separator and raw_path:
            object_paths.setdefault(object_id, raw_path.decode("utf-8", errors="replace"))

    if not object_ids:
        return []

    type_result = subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "--batch-check=%(objectname) %(objecttype)"],
        input=b"\n".join(object_ids) + b"\n",
        check=True,
        capture_output=True,
    )
    object_types = {
        object_id: object_type
        for object_id, object_type in (
            line.split(maxsplit=1) for line in type_result.stdout.splitlines()
        )
    }

    blobs: list[tuple[str, bytes]] = []
    for object_id, path in object_paths.items():
        if object_types.get(object_id) != b"blob" or Path(path).suffix.lower() in BINARY_SUFFIXES:
            continue
        data = subprocess.run(
            ["git", "-C", str(ROOT), "cat-file", "blob", object_id.decode("ascii")],
            check=True,
            capture_output=True,
        ).stdout
        blobs.append((path, data))
    return blobs


def shannon_entropy(value: str) -> float:
    counts = Counter(value)
    length = len(value)
    return -sum((count / length) * math.log2(count / length) for count in counts.values())


def signature_payload(value: str) -> str:
    match = SIGNATURE_PREFIX_RE.match(value)
    return value[match.end() :] if match else value


def is_repeated_filler(value: str) -> bool:
    compact = re.sub(r"[-_.]", "", value).lower()
    return len(compact) >= 8 and len(set(compact)) == 1


def is_local_demo_url(value: str) -> bool:
    try:
        parsed = urlsplit(value)
        hostname = parsed.hostname
        if not parsed.scheme or hostname is None or parsed.password is None:
            return False
    except ValueError:
        return False

    hostname = hostname.lower().rstrip(".")
    if hostname == "localhost":
        is_local = True
    else:
        try:
            is_local = ipaddress.ip_address(hostname).is_loopback
        except ValueError:
            is_local = False
    if not is_local:
        return False

    decoded_user = unquote(parsed.username or "").lower()
    decoded_pass = unquote(parsed.password).lower()
    return (decoded_user, decoded_pass) in DEMO_LOCAL_CREDENTIALS


def is_placeholder_phrase(value: str, markers: set[str]) -> bool:
    segments = re.findall(r"[a-z0-9]+", value.lower())
    return (
        bool(segments)
        and any(segment in markers for segment in segments)
        and all(segment in PLACEHOLDER_SEGMENTS for segment in segments)
    )


def is_obvious_placeholder(value: str) -> bool:
    stripped = value.strip()
    normalized = stripped.lower()
    if normalized in SAFE_VALUES or ENV_REFERENCE_RE.fullmatch(stripped):
        return True
    if is_local_demo_url(value):
        return True

    angle_match = ANGLE_VALUE_RE.fullmatch(stripped)
    if angle_match and is_placeholder_phrase(
        angle_match.group("inner"), ANGLE_PLACEHOLDER_MARKERS
    ):
        return True

    payload = signature_payload(stripped)
    if payload != stripped and is_repeated_filler(payload):
        return True

    return is_placeholder_phrase(payload, PLACEHOLDER_MARKERS)


def looks_like_real_secret(value: str) -> bool:
    if is_obvious_placeholder(value):
        return False
    stripped = value.strip()
    angle_match = ANGLE_VALUE_RE.fullmatch(stripped)
    candidate = angle_match.group("inner") if angle_match else stripped
    # This helper is called only for values captured under secret-like keys by
    # ASSIGNMENT_RE, where a long hexadecimal value is high-confidence even if
    # its observed entropy is low by chance.
    if HEX_SECRET_RE.fullmatch(candidate):
        return True
    if len(set(candidate)) < 5:
        return False
    return shannon_entropy(candidate) >= 3.5


def scan_line(line: str) -> list[str]:
    if ALLOW_MARKER in line.lower():
        return []

    findings = [
        name
        for name, pattern in SIGNATURES
        if any(
            not is_obvious_placeholder(match.group(0))
            for match in pattern.finditer(line)
        )
    ]
    for assignment in ASSIGNMENT_RE.finditer(line):
        value = next(
            group
            for group in (
                assignment.group("double"),
                assignment.group("single"),
                assignment.group("bare"),
            )
            if group is not None
        )
        if looks_like_real_secret(value):
            findings.append("high-entropy secret assignment")
    return findings


def scan_content(
    path: str,
    data: bytes,
    findings: set[tuple[str, int, str]],
) -> bool:
    # Secret formats are ASCII. Replacement decoding keeps those signatures
    # visible even when the surrounding file is not valid UTF-8.
    text = data.decode("utf-8", errors="replace")

    for line_number, line in enumerate(text.splitlines(), start=1):
        for rule in dict.fromkeys(scan_line(line)):
            findings.add((path, line_number, rule))
    return True


def main() -> int:
    findings: set[tuple[str, int, str]] = set()
    checked = 0

    for path in repository_files():
        if not path.is_file() or path.suffix.lower() in BINARY_SUFFIXES:
            continue

        relative = path.relative_to(ROOT).as_posix()
        if scan_content(relative, path.read_bytes(), findings):
            checked += 1

    revision_range = event_revision_range()
    if revision_range:
        revision_range = available_history_range(revision_range)
        for path, data in changed_history_blobs(revision_range):
            scan_content(path, data, findings)

    if findings:
        for path, line_number, rule in sorted(findings):
            print(f"ERROR: {path}:{line_number}: possible {rule}", file=sys.stderr)
        print(
            "Possible secrets found. Rotate real credentials before removing them; "
            f"mark a reviewed false positive with '{ALLOW_MARKER}'.",
            file=sys.stderr,
        )
        return 1

    print(f"Scanned {checked} repository files for high-confidence secrets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
