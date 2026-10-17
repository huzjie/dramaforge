"""CPU reference backend: same pipeline, always obeys directives.

A "ground-truth" reference where skill is fixed at 1.0 -- useful as the gold
standard the mock backend is trained toward.
"""
from .registry import register_backend
from .mock import MockBackend


@register_backend("cpu")
class CpuBackend(MockBackend):
    name = "cpu"

    def __init__(self, config):
        super().__init__(config)
        self.skill = 1.0
