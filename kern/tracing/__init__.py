"""
Kern Tracing Module

This module provides OpenTelemetry-based tracing capabilities for Kern agents.
It uses the openinference-instrumentation-kern package for automatic instrumentation
and provides a custom DatabaseSpanExporter to store traces in the Kern database.
"""

from kern.tracing.exporter import DatabaseSpanExporter
from kern.tracing.setup import setup_tracing

__all__ = ["DatabaseSpanExporter", "setup_tracing"]
