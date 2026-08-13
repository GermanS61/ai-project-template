#!/usr/bin/env python3
"""Validate relative Markdown link targets and GitHub-style heading anchors."""

from __future__ import annotations

import html
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[2]
FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
ATX_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
SETEXT_RE = re.compile(r"^\s{0,3}(?:=+|-+)\s*$")
EXPLICIT_ANCHOR_RE = re.compile(r"<a\s+(?:[^>]*?\s)?(?:id|name)=[\"']([^\"']+)[\"'][^>]*>", re.IGNORECASE)
INLINE_CODE_RE = re.compile(r"(`+)([^\n]*?)\1")
HTML_TAG_RE = re.compile(r"<[^>]+>")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
MARKDOWN_LINK_TEXT_RE = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")


def markdown_files() -> list[Path]:
    result = subprocess.run(
        [
            "git",
            "-C",
            str(ROOT),
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "*.md",
            "*.markdown",
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return [ROOT / line for line in result.stdout.splitlines() if line]


def mask_preserving_newlines(value: str) -> str:
    return "".join("\n" if character == "\n" else " " for character in value)


def strip_blockquote_prefix(line: str) -> tuple[str, int, int]:
    position = 0
    depth = 0

    while position < len(line):
        marker_start = position
        spaces = 0
        while position < len(line) and line[position] == " " and spaces < 3:
            position += 1
            spaces += 1
        if position >= len(line) or line[position] != ">":
            position = marker_start
            break

        depth += 1
        position += 1
        if position < len(line) and line[position] in " \t":
            position += 1

    return line[position:], depth, position


def remove_html_comments(text: str) -> str:
    return HTML_COMMENT_RE.sub(lambda match: mask_preserving_newlines(match.group(0)), text)


def remove_fenced_code(text: str) -> str:
    output: list[str] = []
    fence_character: str | None = None
    fence_length = 0
    fence_quote_depth = 0

    for line in text.splitlines(keepends=True):
        content, quote_depth, _ = strip_blockquote_prefix(line)
        match = FENCE_RE.match(content)
        if fence_character is not None and quote_depth < fence_quote_depth:
            fence_character = None
            fence_length = 0
            fence_quote_depth = 0
        if fence_character is None and match:
            marker = match.group(1)
            fence_character = marker[0]
            fence_length = len(marker)
            fence_quote_depth = quote_depth
            output.append("\n" if line.endswith("\n") else "")
            continue

        if fence_character is not None:
            if match:
                marker = match.group(1)
                trailing = content[match.end() :].strip()
                if (
                    quote_depth >= fence_quote_depth
                    and marker[0] == fence_character
                    and len(marker) >= fence_length
                    and not trailing
                ):
                    fence_character = None
                    fence_length = 0
                    fence_quote_depth = 0
            output.append("\n" if line.endswith("\n") else "")
            continue

        output.append(line)

    return "".join(output)


def github_slug(value: str) -> str:
    value = MARKDOWN_LINK_TEXT_RE.sub(r"\1", value)
    value = HTML_TAG_RE.sub("", value)
    value = html.unescape(value).replace("`", "").lower()
    slug: list[str] = []
    for character in value:
        category = unicodedata.category(character)
        if character.isspace():
            slug.append("-")
        elif character in "-_" or character.isalnum() or category.startswith("M"):
            slug.append(character)
    return "".join(slug)


def anchors_in(text: str) -> set[str]:
    text = remove_fenced_code(remove_html_comments(text))
    anchors = set(EXPLICIT_ANCHOR_RE.findall(text))
    occurrences: dict[str, int] = {}
    previous_line: str | None = None
    previous_quote_depth: int | None = None

    for raw_line in text.splitlines():
        line, quote_depth, _ = strip_blockquote_prefix(raw_line)
        match = ATX_HEADING_RE.match(line)
        heading = match.group(1) if match else None
        is_setext = bool(
            heading is None
            and previous_line
            and previous_quote_depth == quote_depth
            and SETEXT_RE.match(line)
        )
        if is_setext:
            heading = previous_line.strip()

        if heading:
            base = github_slug(heading)
            duplicate_number = occurrences.get(base, 0)
            anchor = base if duplicate_number == 0 else f"{base}-{duplicate_number}"
            occurrences[base] = duplicate_number + 1
            anchors.add(anchor)

        previous_line = line if line.strip() and match is None and not is_setext else None
        previous_quote_depth = quote_depth if previous_line else None

    return anchors


def anchors_for(path: Path) -> set[str]:
    return anchors_in(path.read_text(encoding="utf-8"))


def exact_path(path: Path) -> Path | None:
    try:
        relative = path.resolve().relative_to(ROOT.resolve())
    except ValueError:
        return None

    current = ROOT
    for part in relative.parts:
        if not current.is_dir():
            return None
        names = {child.name: child for child in current.iterdir()}
        if part not in names:
            return None
        current = names[part]
    return current


def clean_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    return re.sub(r"\\([\\()`*_{}\[\]<>#+.!-])", r"\1", target)


def is_escaped(text: str, position: int) -> bool:
    backslashes = 0
    position -= 1
    while position >= 0 and text[position] == "\\":
        backslashes += 1
        position -= 1
    return backslashes % 2 == 1


def find_closing_bracket(text: str, opening: int) -> int | None:
    depth = 0
    position = opening

    while position < len(text):
        character = text[position]
        if character == "\\" and position + 1 < len(text):
            position += 2
            continue
        if character == "[":
            depth += 1
        elif character == "]":
            depth -= 1
            if depth == 0:
                return position
        position += 1
    return None


def skip_whitespace(text: str, position: int) -> int:
    while position < len(text) and text[position].isspace():
        position += 1
    return position


def parse_title_and_close(text: str, position: int) -> int | None:
    position = skip_whitespace(text, position)
    if position < len(text) and text[position] == ")":
        return position + 1
    if position >= len(text) or text[position] not in "\"'(":
        return None

    opener = text[position]
    closer = ")" if opener == "(" else opener
    position += 1
    while position < len(text):
        if text[position] == "\\" and position + 1 < len(text):
            position += 2
            continue
        if text[position] == closer:
            position = skip_whitespace(text, position + 1)
            return position + 1 if position < len(text) and text[position] == ")" else None
        position += 1
    return None


def parse_inline_destination(text: str, opening: int) -> tuple[str, int] | None:
    position = skip_whitespace(text, opening + 1)

    if position < len(text) and text[position] == "<":
        start = position + 1
        position = start
        while position < len(text):
            if text[position] == "\\" and position + 1 < len(text):
                position += 2
                continue
            if text[position] == ">":
                end = parse_title_and_close(text, position + 1)
                return (clean_target(text[start:position]), end) if end is not None else None
            if text[position] == "\n":
                return None
            position += 1
        return None

    start = position
    depth = 0
    while position < len(text):
        character = text[position]
        if character == "\\" and position + 1 < len(text):
            position += 2
            continue
        if character == "(":
            depth += 1
        elif character == ")":
            if depth == 0:
                return clean_target(text[start:position]), position + 1
            depth -= 1
        elif character.isspace() and depth == 0:
            end = parse_title_and_close(text, position)
            return (clean_target(text[start:position]), end) if end is not None else None
        position += 1
    return None


def parse_definition_destination(value: str) -> str | None:
    position = skip_whitespace(value, 0)
    if position >= len(value):
        return None

    if value[position] == "<":
        start = position + 1
        position = start
        while position < len(value):
            if value[position] == "\\" and position + 1 < len(value):
                position += 2
                continue
            if value[position] == ">":
                return clean_target(value[start:position])
            if value[position] == "\n":
                return None
            position += 1
        return None

    start = position
    depth = 0
    while position < len(value):
        character = value[position]
        if character == "\\" and position + 1 < len(value):
            position += 2
            continue
        if character == "(":
            depth += 1
        elif character == ")":
            if depth == 0:
                return None
            depth -= 1
        elif character.isspace() and depth == 0:
            break
        position += 1
    if depth != 0:
        return None
    return clean_target(value[start:position])


def normalize_reference_label(label: str) -> str:
    label = re.sub(r"\\([!\"#$%&'()*+,./:;<=>?@\[\\\]^_`{|}~-])", r"\1", label)
    return " ".join(html.unescape(label).split()).casefold()


def reference_definitions(
    text: str,
) -> tuple[dict[str, str], list[tuple[int, str]], list[tuple[int, int]]]:
    definitions: dict[str, str] = {}
    targets: list[tuple[int, str]] = []
    spans: list[tuple[int, int]] = []
    offset = 0

    for line_number, raw_line in enumerate(text.splitlines(keepends=True), start=1):
        line, _, _ = strip_blockquote_prefix(raw_line)
        leading_spaces = len(line) - len(line.lstrip(" "))
        if leading_spaces <= 3:
            content = line[leading_spaces:]
            if content.startswith("["):
                closing = find_closing_bracket(content, 0)
                if closing is not None and content[closing + 1 :].startswith(":"):
                    label = normalize_reference_label(content[1:closing])
                    target = parse_definition_destination(content[closing + 2 :])
                    if label and target is not None:
                        definitions.setdefault(label, target)
                        targets.append((line_number, target))
                        spans.append((offset, offset + len(raw_line)))
        offset += len(raw_line)

    return definitions, targets, spans


def mask_spans(text: str, spans: list[tuple[int, int]]) -> str:
    if not spans:
        return text
    characters = list(text)
    for start, end in spans:
        for position in range(start, end):
            if characters[position] != "\n":
                characters[position] = " "
    return "".join(characters)


def analyze_links(text: str) -> tuple[list[tuple[int, str]], list[tuple[int, str]]]:
    visible = remove_fenced_code(remove_html_comments(text))
    visible = INLINE_CODE_RE.sub(lambda match: mask_preserving_newlines(match.group(0)), visible)
    definitions, targets, definition_spans = reference_definitions(visible)
    searchable = mask_spans(visible, definition_spans)
    undefined: list[tuple[int, str]] = []
    position = 0

    while position < len(searchable):
        if searchable[position] != "[" or is_escaped(searchable, position):
            position += 1
            continue

        closing = find_closing_bracket(searchable, position)
        if closing is None:
            position += 1
            continue

        following = closing + 1
        if following < len(searchable) and searchable[following] == "(":
            parsed = parse_inline_destination(searchable, following)
            if parsed is not None:
                target, end = parsed
                targets.append((searchable.count("\n", 0, position) + 1, target))
                position = end
                continue
        elif following < len(searchable) and searchable[following] == "[":
            reference_closing = find_closing_bracket(searchable, following)
            if reference_closing is not None:
                raw_label = searchable[following + 1 : reference_closing]
                if not raw_label:
                    raw_label = searchable[position + 1 : closing]
                normalized = normalize_reference_label(raw_label)
                if normalized and normalized not in definitions:
                    undefined.append(
                        (searchable.count("\n", 0, position) + 1, raw_label)
                    )
                position = reference_closing + 1
                continue

        position = closing + 1

    return sorted(targets, key=lambda item: item[0]), undefined


def targets_in(text: str) -> list[tuple[int, str]]:
    return analyze_links(text)[0]


def undefined_references_in(text: str) -> list[tuple[int, str]]:
    return analyze_links(text)[1]


def validate_target(
    source: Path,
    line_number: int,
    target: str,
    anchor_cache: dict[Path, set[str]],
) -> str | None:
    if not target or target.startswith("//"):
        return None

    split = urlsplit(target)
    if split.scheme or split.netloc:
        return None

    decoded_path = unquote(split.path)
    fragment = unquote(split.fragment)
    if decoded_path.startswith("/"):
        return None

    candidate = source if not decoded_path else source.parent / decoded_path
    resolved = exact_path(candidate)
    if resolved is None:
        return f"{source.relative_to(ROOT).as_posix()}:{line_number}: target does not exist: {target}"

    anchor_file = resolved
    if resolved.is_dir():
        readme = exact_path(resolved / "README.md")
        if fragment and readme is None:
            return f"{source.relative_to(ROOT).as_posix()}:{line_number}: directory has no README.md for anchor: {target}"
        if readme is not None:
            anchor_file = readme

    if fragment and anchor_file.suffix.lower() in {".md", ".markdown"}:
        anchors = anchor_cache.setdefault(anchor_file, anchors_for(anchor_file))
        if fragment not in anchors:
            return f"{source.relative_to(ROOT).as_posix()}:{line_number}: anchor does not exist: {target}"

    return None


def main() -> int:
    errors: list[str] = []
    anchor_cache: dict[Path, set[str]] = {}
    files = markdown_files()
    checked_targets = 0

    for source in files:
        text = source.read_text(encoding="utf-8")
        targets, undefined_references = analyze_links(text)
        for line_number, target in targets:
            checked_targets += 1
            error = validate_target(source, line_number, target, anchor_cache)
            if error:
                errors.append(error)
        for line_number, label in undefined_references:
            errors.append(
                f"{source.relative_to(ROOT).as_posix()}:{line_number}: "
                f"undefined reference link: [{label}]"
            )

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1

    print(
        f"Checked {checked_targets} Markdown link targets and anchors "
        f"in {len(files)} files."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
