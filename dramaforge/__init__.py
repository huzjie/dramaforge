"""dramaforge - directable multi-speaker speech synthesis engine.

A zero-dependency reference implementation of the core mechanisms behind
**Fish Audio Drama 3** (an open-weight text-to-speech model with word-level
control over tone, emotion and voice shifts; multi-speaker scenes; and
natural-language direction via bracketed tags):

* **Natural-language direction**: a directive parser turns bracketed tags
  (``[emotion=angry]...[/emotion]``, ``[voice=alice]``) and plain-language
  instructions ("say the first line angrily, then switch to a warm tone")
  into structured, span-level ``Directive`` objects.

* **Word-level control**: the text is tokenized into words and each word picks
  up the attributes (emotion / voice / rate / pitch / emphasis) of the
  directive spans that cover it -- so a single sentence can flip emotion or
  speaker mid-word.

* **Multi-speaker scenes**: a ``SpeakerLibrary`` holds deterministic speaker
  embeddings; a scene planner assigns voices to spans and drives clean
  speaker hand-off (cross-fade rather than a hard cut).

* **RVQ audio codec**: a residual vector quantizer compresses acoustic frames
  into multi-level discrete codes, the same trick modern TTS codecs use to
  represent audio as a short token sequence.

Public API:
    from dramaforge import DramaEngine, Config, get_backend, synth
"""

__version__ = "0.1.0"

from .config import Config, load_config
from .engine import DramaEngine
from .backends import get_backend, list_backends

__all__ = [
    "Config",
    "load_config",
    "DramaEngine",
    "get_backend",
    "list_backends",
    "__version__",
]
