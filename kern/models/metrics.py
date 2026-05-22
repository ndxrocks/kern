"""Backward-compatible re-exports from kern.metrics.

All metric classes now live in kern.metrics.  This shim keeps
``from kern.models.metrics import Metrics`` working everywhere.
"""

from kern.metrics import (  # noqa: F401
    BaseMetrics,
    MessageMetrics,
    Metrics,
    ModelMetrics,
    ModelType,
    RunMetrics,
    SessionMetrics,
    ToolCallMetrics,
    accumulate_eval_metrics,
    accumulate_model_metrics,
    merge_background_metrics,
)

# Explicit re-export for type checkers
__all__ = [
    "BaseMetrics",
    "MessageMetrics",
    "Metrics",
    "ModelMetrics",
    "ModelType",
    "RunMetrics",
    "SessionMetrics",
    "ToolCallMetrics",
    "accumulate_eval_metrics",
    "accumulate_model_metrics",
    "merge_background_metrics",
]
