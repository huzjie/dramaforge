"""Directable speech control: directives, tag parsing, natural-language parsing."""
from .directive import Directive, apply_directives
from .tags import parse_bracketed
from .parser import parse_natural, parse_text

__all__ = [
    "Directive",
    "apply_directives",
    "parse_bracketed",
    "parse_natural",
    "parse_text",
]
