#!/usr/bin/env python3
"""Regression tests for the repository Markdown link checker."""

from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

import check_markdown_links as checker


class MarkdownLinkCheckerTests(unittest.TestCase):
    def run_main(self, root: Path, files: list[Path]) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            mock.patch.object(checker, "ROOT", root),
            mock.patch.object(checker, "markdown_files", return_value=files),
            redirect_stdout(stdout),
            redirect_stderr(stderr),
        ):
            result = checker.main()
        return result, stdout.getvalue(), stderr.getvalue()

    def test_gfm_footnote_definition_is_not_a_link_target(self) -> None:
        text = "Text with a footnote.[^1]\n\n[^1]: Footnote explanation.\n"

        targets, undefined = checker.analyze_links(text)

        self.assertEqual([], targets)
        self.assertEqual([], undefined)

    def test_inline_link_inside_gfm_footnote_body_is_checked(self) -> None:
        text = "[^note]: See [the guide](docs/guide.md) for details.\n"

        targets, undefined = checker.analyze_links(text)

        self.assertEqual([(1, "docs/guide.md")], targets)
        self.assertEqual([], undefined)

    def test_regular_reference_definition_is_still_checked(self) -> None:
        text = "Read [the guide][guide].\n\n[guide]: docs/guide.md\n"

        targets, undefined = checker.analyze_links(text)

        self.assertEqual([(3, "docs/guide.md")], targets)
        self.assertEqual([], undefined)

    def test_escaped_caret_reference_is_not_treated_as_a_footnote(self) -> None:
        text = "Read [the note][\\^note].\n\n[\\^note]: docs/note.md\n"

        targets, undefined = checker.analyze_links(text)

        self.assertEqual([(3, "docs/note.md")], targets)
        self.assertEqual([], undefined)

    def test_bom_does_not_hide_first_heading_anchor(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "source.md"
            target = root / "target.md"
            source.write_text(
                "[First section](target.md#first-section)\n",
                encoding="utf-8-sig",
            )
            target.write_text("# First Section\n", encoding="utf-8-sig")

            result, stdout, stderr = self.run_main(root, [source, target])

        self.assertEqual(0, result, stderr)
        self.assertIn("Checked 1 Markdown link targets", stdout)
        self.assertEqual("", stderr)

    def test_invalid_utf8_source_is_reported_and_other_files_continue(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            invalid = root / "invalid.md"
            valid = root / "valid.md"
            invalid.write_bytes(b"# \xc7\xe0\xe3\xee\xeb\xee\xe2\xee\xea\n")
            valid.write_text("[Missing](missing.md)\n", encoding="utf-8")

            result, _, stderr = self.run_main(root, [invalid, valid])

        self.assertEqual(1, result)
        self.assertIn("invalid.md: is not valid UTF-8", stderr)
        self.assertIn("valid.md:1: target does not exist: missing.md", stderr)
        self.assertNotIn("Traceback", stderr)

    def test_invalid_utf8_anchor_target_is_reported_and_links_continue(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "source.md"
            target = root / "target.md"
            source.write_text(
                "[Bad anchor](target.md#heading)\n[Missing](missing.md)\n",
                encoding="utf-8",
            )
            target.write_bytes(b"# \xc7\xe0\xe3\xee\xeb\xee\xe2\xee\xea\n")

            result, _, stderr = self.run_main(root, [source])

        self.assertEqual(1, result)
        self.assertIn("cannot validate anchor target.md#heading", stderr)
        self.assertIn("target.md: is not valid UTF-8", stderr)
        self.assertIn("source.md:2: target does not exist: missing.md", stderr)
        self.assertNotIn("Traceback", stderr)


if __name__ == "__main__":
    unittest.main()
