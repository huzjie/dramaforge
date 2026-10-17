"""Speaker identity: embeddings, library, multi-speaker scene planning."""
from .speaker import Speaker
from .embedding import speaker_embedding, speaker_similarity
from .library import SpeakerLibrary

__all__ = [
    "Speaker",
    "speaker_embedding",
    "speaker_similarity",
    "SpeakerLibrary",
]
