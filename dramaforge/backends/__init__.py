"""Synthesis backends (mock, cpu) and registry."""
from .registry import register_backend, get_backend, list_backends

# explicit imports so the @register_backend decorators run
from . import mock, cpu  # noqa: F401

__all__ = ["register_backend", "get_backend", "list_backends"]
