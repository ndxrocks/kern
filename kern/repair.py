"""JSON extraction, repair, and LaTeX protection for small model outputs."""

from __future__ import annotations

import json
import re

from json_repair import repair_json

# LaTeX commands whose first letter conflicts with JSON escape sequences.
# Sorted longest-first so the regex alternation matches greedily.
_LATEX_ESCAPE_CMDS = sorted(
    [
        "text", "textbf", "textit", "textrm", "textsc", "times", "theta",
        "tan", "tanh", "to", "top", "triangle", "tilde",
        "nu", "nabla", "neg", "neq", "notin", "newline", "not", "notag",
        "beta", "bar", "binom", "boldsymbol", "big", "bigl", "bigr",
        "bigm", "bmod", "bot", "boxed",
        "frac", "forall", "flat",
        "rho", "right", "rightarrow", "rm", "ref",
    ],
    key=len,
    reverse=True,
)
_LATEX_FIX = re.compile(
    r"(?<!\\)\\(?=" + "|".join(_LATEX_ESCAPE_CMDS) + r"(?![a-zA-Z]))"
)


def protect_latex(text: str) -> str:
    """Double backslashes before LaTeX commands to prevent JSON escape corruption."""
    return _LATEX_FIX.sub(r"\\\\", text)


def extract_json(text: str) -> dict | None:
    """Extract and repair JSON from an LLM response.

    Handles: markdown code blocks, leading/trailing text, LaTeX commands,
    malformed JSON (via json_repair).
    """
    text = text.strip()

    # Extract from code block first
    match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if match:
        text = match.group(1).strip()

    # Find JSON start
    start_idx = text.find("{")
    if start_idx < 0:
        return None
    if start_idx > 0:
        text = text[start_idx:]

    # Protect LaTeX from JSON escape interpretation
    text = protect_latex(text)

    try:
        repaired = repair_json(text)
        return json.loads(repaired)
    except Exception:
        return None
