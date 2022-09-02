#!/usr/bin/env python3

from typing import Iterable, Optional, Mapping, Tuple


class Trie(object):
    @classmethod
    def fromReplacements(cls, replacements: Iterable[Tuple[str, str]]) -> "Trie":
        t = Trie()
        t.add_all(replacements)
        return t

    def __init__(self):
        self.children = {}
        self.replacement = None

    def __contains__(self, c: str) -> bool:
        return c in self.children

    def __getitem__(self, c: str) -> Optional["Trie"]:
        return self.children.get(c, None)

    def __str__(self) -> str:
        return self._str()

    def _str(self, depth=0) -> str:
        if self.children:
            return "\n".join(
                "\n".join(
                    (
                        ("  " * depth)
                        + c
                        + (f": {t.replacement}" if t.replacement else ""),
                        t._str(depth=depth + 1),
                    )
                )
                for c, t in self.children.items()
            )
        elif depth == 0:
            return self.replacement or ""
        return ""

    def _check(self, c: str) -> None:
        if c not in self:
            self.children[c] = Trie()

    def add(self, old: str, new: str) -> None:
        current = self
        for c in old:
            current._check(c)
            current = current.children[c]
        current.replacement = new

    def add_all(self, replacements: Iterable[Tuple[str, str]]) -> None:
        for old, new in replacements:
            self.add(old, new)


def replace_all(s: str, replacements: Mapping[str, str]):
    trie = Trie.fromReplacements(replacements.items())
    current = trie
    start = 0
    out = s
    offset = 0
    for i, c in enumerate(s):
        current = current[c]
        if current:
            if current.replacement:
                out = "".join(
                    (out[: offset + start], current.replacement, out[offset + i + 1 :])
                )
                offset += len(current.replacement) - (i + 1 - start)
                start = i + 1
                current = trie
        else:
            start = i + 1
            current = trie
    return out
