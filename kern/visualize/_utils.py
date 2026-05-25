"""Shared utilities for visualization modules."""

from __future__ import annotations


class _IdCounter:
    """Tiny mutable counter shared across recursive calls."""

    def __init__(self) -> None:
        self._n = 0

    def next(self, prefix: str = "n") -> str:
        self._n += 1
        return f"{prefix}{self._n}"


_SHAPE = {
    "step": ("[", "]"),
    "steps": ("[", "]"),
    "condition": ("{", "}"),
    "router": ("{", "}"),
    "loop": ("([", "])"),
    "parallel": ("([", "])"),
    "callable": ("[/", "/]"),
    "start": ("([", "])"),
    "end": ("([", "])"),
}


def _sanitize(text: str) -> str:
    """Escape characters that break Mermaid syntax."""
    return text.replace('"', "#quot;").replace("(", "#lpar;").replace(")", "#rpar;")
