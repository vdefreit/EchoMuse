"""Pure decision logic for the bare ``stop`` playback kill word.

The stop classifier is separate from the normal wake word and is consulted
only while assistant audio is playing. Its 0.65 cutoff and 0.03 immediate
margin follow the model's reference implementation; borderline scores need
two adjacent 80 ms frames to filter isolated TV/noise spikes.
"""

from __future__ import annotations

from typing import NamedTuple

STOP_THRESHOLD = 0.65
IMMEDIATE_MARGIN = 0.03


class StopDecision(NamedTuple):
    fired: bool
    note: str


def decide(*, score: float, prev_score: float,
           threshold: float = STOP_THRESHOLD) -> StopDecision:
    """Return whether this frame should hard-stop the current playback."""
    if score <= threshold:
        return StopDecision(False, "")
    if score >= threshold + IMMEDIATE_MARGIN:
        return StopDecision(
            True, f"score={score:.3f} >= {threshold + IMMEDIATE_MARGIN:.2f}"
        )
    if prev_score > threshold:
        return StopDecision(
            True,
            f"scores {prev_score:.3f}/{score:.3f} — two consecutive "
            f"frames > {threshold:.2f}",
        )
    return StopDecision(False, "")
