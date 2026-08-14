#!/usr/bin/env python3
"""Regression tests for the repository's high-confidence secret scanner."""

from __future__ import annotations

import io
import json
import os
import subprocess
import unittest
from unittest import mock

import check_secrets


class SecretLineTests(unittest.TestCase):
    def test_reviewer_placeholders_are_ignored(self) -> None:
        placeholders = [
            "".join(
                (
                    "DATABASE_URL=",
                    "postgresql://",
                    "user:",
                    "password@",
                    "localhost:5432/app_dev",
                )
            ),
            "".join(("OPENAI_API_KEY=", "sk", "-your-openai-key-goes-here")),
            "".join(("ANTHROPIC_API_KEY=", "sk", "-ant-", "x" * 24)),
            "".join(("AXIOMA_API_KEY=", "${", "AXIOMA_API_KEY", "}")),
            "".join(("SERVICE_TOKEN=", "<", "service-token", ">")),
            "".join(("SECRET_KEY=", "change", "-me-in-production")),
        ]

        for line in placeholders:
            with self.subTest(line=line):
                self.assertEqual(check_secrets.scan_line(line), [])

        findings: set[tuple[str, int, str]] = set()
        check_secrets.scan_content(
            "synthetic.env.example",
            ("\n".join(placeholders) + "\n").encode("utf-8"),
            findings,
        )
        self.assertEqual(findings, set())

    def test_loopback_demo_urls_are_ignored(self) -> None:
        urls = [
            "".join(
                (
                    "DATABASE_URL=",
                    "postgresql://",
                    "user:",
                    "password@",
                    "127.0.0.1:5432/app_dev",
                )
            ),
            "".join(
                (
                    "DATABASE_URL=",
                    "postgresql://",
                    "user:",
                    "password@",
                    "[::1]:5432/app_dev",
                )
            ),
        ]

        for line in urls:
            with self.subTest(line=line):
                self.assertEqual(check_secrets.scan_line(line), [])

    def test_real_signature_is_detected(self) -> None:
        token = "".join(("sk", "-", "A1b2C3d4E5f6G7h8I9j0K1l2"))
        findings = check_secrets.scan_line("".join(("OPENAI_API_KEY=", token)))

        self.assertIn("OpenAI API key", findings)

    def test_hex_assignments_do_not_depend_on_entropy(self) -> None:
        values = [
            "".join(("dead", "beef")) * 4,
            "".join(("0123456789abcdef", "0123456789abcdef", "01234567")),
        ]

        for value in values:
            with self.subTest(length=len(value)):
                self.assertIn(
                    "high-entropy secret assignment",
                    check_secrets.scan_line("".join(("API_KEY=", value))),
                )

    def test_letters_only_high_entropy_assignment_is_detected(self) -> None:
        value = "".join(("QwErTyUiOpAsD", "fGhJkLzXcVbNm"))

        self.assertIn(
            "high-entropy secret assignment",
            check_secrets.scan_line("".join(("API_KEY=", value))),
        )

    def test_placeholder_words_embedded_in_real_values_do_not_bypass_scan(self) -> None:
        values = [
            "".join(("my", "test", "ActualSecret", "123ABC")),
            "".join(("9z8Y7x6W5v4U3t2S1r0Qabc", "xxx", "DEF123")),
        ]

        for value in values:
            with self.subTest(value=value):
                self.assertIn(
                    "high-entropy secret assignment",
                    check_secrets.scan_line("".join(("PASSWORD=", value))),
                )

    def test_angle_wrapped_real_values_do_not_bypass_scan(self) -> None:
        values = [
            "".join(("<", "deadbeef" * 5, ">")),
            "".join(("<", "A7b9Q2w4E6r8T0y1U3i5O7p9", ">")),
        ]

        for value in values:
            with self.subTest(value=value):
                self.assertIn(
                    "high-entropy secret assignment",
                    check_secrets.scan_line("".join(("API_KEY=", value))),
                )

    def test_localhost_text_inside_external_hostname_does_not_bypass_scan(self) -> None:
        value = "".join(
            (
                "postgresql://",
                "user:",
                "S3cr3tValue@",
                "localhost.evil.example/db",
            )
        )

        self.assertIn(
            "high-entropy secret assignment",
            check_secrets.scan_line("".join(("DATABASE_URL=", value))),
        )

    def test_multiple_assignments_on_one_line_are_all_scanned(self) -> None:
        first = "".join(("dead", "beef")) * 4
        second = "".join(("QwErTyUiOpAsD", "fGhJkLzXcVbNm"))
        line = "".join(("API_KEY=", first, ", TOKEN=", second))

        findings = check_secrets.scan_line(line)

        self.assertEqual(findings.count("high-entropy secret assignment"), 2)


class HistoryRangeTests(unittest.TestCase):
    def test_push_event_builds_before_after_range_without_event_file(self) -> None:
        before = "1" * 40
        after = "2" * 40
        event = json.dumps({"before": before, "after": after})

        with (
            mock.patch.dict(
                os.environ,
                {"GITHUB_EVENT_NAME": "push", "GITHUB_EVENT_PATH": "unused.json"},
            ),
            mock.patch.object(check_secrets.Path, "read_text", return_value=event),
        ):
            result = check_secrets.event_revision_range()

        self.assertEqual(result, f"{before}..{after}")

    def test_missing_push_before_falls_back_to_after_with_warning(self) -> None:
        before = "1" * 40
        after = "2" * 40
        cat_file_result = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout=f"{before} missing\n".encode("ascii"),
            stderr=b"",
        )

        with (
            mock.patch.dict(os.environ, {"GITHUB_EVENT_NAME": "push"}),
            mock.patch.object(
                check_secrets.subprocess, "run", return_value=cat_file_result
            ) as run,
            mock.patch("sys.stderr", new_callable=io.StringIO) as stderr,
        ):
            result = check_secrets.available_history_range(f"{before}..{after}")

        self.assertEqual(result, after)
        self.assertIn("before object is unavailable", stderr.getvalue())
        run.assert_called_once()

    def test_available_push_before_preserves_range(self) -> None:
        before = "1" * 40
        after = "2" * 40
        cat_file_result = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout=f"{before} commit\n".encode("ascii"),
            stderr=b"",
        )

        with (
            mock.patch.dict(os.environ, {"GITHUB_EVENT_NAME": "push"}),
            mock.patch.object(
                check_secrets.subprocess, "run", return_value=cat_file_result
            ),
        ):
            result = check_secrets.available_history_range(f"{before}..{after}")

        self.assertEqual(result, f"{before}..{after}")

    def test_git_failure_remains_fail_closed(self) -> None:
        before = "1" * 40
        after = "2" * 40
        failure = subprocess.CalledProcessError(128, ["git", "cat-file"])

        with (
            mock.patch.dict(os.environ, {"GITHUB_EVENT_NAME": "push"}),
            mock.patch.object(check_secrets.subprocess, "run", side_effect=failure),
        ):
            with self.assertRaises(subprocess.CalledProcessError):
                check_secrets.available_history_range(f"{before}..{after}")


if __name__ == "__main__":
    unittest.main()
