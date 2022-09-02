#!/usr/bin/env python3

import unittest

from src.replace_all import replace_all

import contextlib

from io import StringIO


class TestReplaceAll(unittest.TestCase):
    basic_cases = (
        ("empty string; empty replacements", "", {}, ""),
        ("empty string; non-empty replacements", "", {"a": "b"}, ""),
        ("non-empty string; empty replacements", "a", {}, "a"),
        ("non-empty string; irrelevant replacements", "a", {"b": "d"}, "a"),
        ("single", "a", {"a": "b"}, "b"),
        ("single prefix", "ab", {"a": "b"}, "bb"),
        ("single suffix", "ba", {"a": "b"}, "bb"),
        ("single middle", "bab", {"a": "b"}, "bbb"),
        ("single repeat", "aa", {"a": "b"}, "bb"),
        ("single repeat prefix", "aac", {"a": "b"}, "bbc"),
        ("single repeat suffix", "caa", {"a": "b"}, "cbb"),
        ("single repeat middle", "caac", {"a": "b"}, "cbbc"),
        ("single repeat ends", "aca", {"a": "b"}, "bcb"),
        ("multiple all", "ac", {"a": "b", "c": "d"}, "bd"),
        ("multiple prefix", "ace", {"a": "b", "c": "d"}, "bde"),
        ("multiple suffix", "eac", {"a": "b", "c": "d"}, "ebd"),
        ("multiple ends", "aec", {"a": "b", "c": "d"}, "bed"),
        ("multiple middle", "eacf", {"a": "b", "c": "d"}, "ebdf"),
        ("long replacement", "abc", {"ab": "bc"}, "bcc"),
        ("shortening", "aa", {"aa": "a"}, "a"),
        ("lengthening", "a", {"a": "aa"}, "aa"),
        ("duplicate", "aa", {"a": "aa"}, "aaaa"),
        ("ambiguous", "aaa", {"aa": "b"}, "ba"),
        (
            "ascii",
            "Hello, world!",
            {"Hello": "Goodbye", "world": "friend"},
            "Goodbye, friend!",
        ),
        ("unicode", "こんにちは", {"こん": "今", "にち": "日"}, "今日は"),
        (
            "long",
            "an interpreted, interactive, object-oriented programming language",
            {"in": "IN", "a": "ä"},
            "än INterpreted, INteräctive, object-oriented progrämmINg länguäge",
        ),
    )

    def test_basic(self):
        for name, s, replacements, expected in self.basic_cases:
            with self.subTest(name=name):
                actual = replace_all(s, replacements)
                self.assertEqual(actual, expected)

    def test_doc(self):
        s = "an interpreted, interactive, object-oriented programming language"
        expected = "a magical, amazing, user-friendly programming language"
        actual = replace_all(
            s,
            {
                "an ": "a ",
                "interpreted": "magical",
                "interactive": "amazing",
                "object-oriented": "user-friendly",
            },
        )
        self.assertEqual(actual, expected)

    def test_paragraph(self):
        s = unittest.__doc__
        replacements = {
            "assert": "try",
            "Python": "Jython",
            "THE AUTHOR SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT\nLIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A\nPARTICULAR PURPOSE.  ": "x",
        }
        expected = s
        for old, new in replacements.items():
            while old in expected:
                expected = expected.replace(old, new)

        actual = replace_all(s, replacements)
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
