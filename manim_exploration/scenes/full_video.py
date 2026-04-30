"""Stitched master scene: every storyboard beat in order.

Each subscene's `construct` is invoked against this scene's `self`, with
`self.clear()` between beats so we don't carry mobjects forward. Render
with:

    uv run manim -pql scenes/full_video.py FullStory
"""

from __future__ import annotations

from manim import Scene, config

from _common import BACKGROUND
from continuum_reveal import DefiningG
from defining_s import DefiningS
from pile_to_gsd import PileToGSD
from quantity_ratio import QuantityRatio
from ratios import MassRatios, VolumeRatios
from rounding import ReducingError, RoundingApproach
from sieve_stack import SieveStack
from spanned_integer import SpannedIntegerApproach, SpannedIntegerError
from verification import Verification

config.background_color = BACKGROUND


SCENES = [
    SieveStack,
    PileToGSD,
    DefiningG,
    DefiningS,
    MassRatios,
    VolumeRatios,
    QuantityRatio,
    RoundingApproach,
    ReducingError,
    SpannedIntegerApproach,
    SpannedIntegerError,
    Verification,
]


class FullStory(Scene):
    def construct(self):
        for i, scene_cls in enumerate(SCENES):
            scene_cls.construct(self)
            if i < len(SCENES) - 1:
                self.clear()
                self.wait(0.4)
