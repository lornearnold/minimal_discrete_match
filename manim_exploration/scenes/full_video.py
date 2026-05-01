"""Stitched master scene: every storyboard beat in order.

Each subscene's `construct` is invoked against this scene's `self`, with
`self.clear()` between beats so we don't carry mobjects forward. Render
with:

    uv run manim -pql scenes/full_video.py FullStory
"""

from __future__ import annotations

from manim import FadeOut, Scene, config

from _common import BACKGROUND
from continuum_reveal import DefiningG
from defining_s import DefiningS
from pile_to_gsd import PileToGSD
from quantity_ratio import QuantityRatio
from ratios import MassRatios, VolumeRatios
from rounding import ReducingError, RoundingApproach  # noqa: F401
from sieve_stack import SieveStack, transition_to_piles
from spanned_integer import SpannedIntegerApproach, SpannedIntegerError
from verification import Verification

config.background_color = BACKGROUND
config.frame_rate = 30


SCENES = [
    SieveStack,
    PileToGSD,
    DefiningG,
    DefiningS,
    MassRatios,
    VolumeRatios,
    QuantityRatio,
    # RoundingApproach removed: redundant with ReducingError's iter-1 setup.
    ReducingError,
    SpannedIntegerApproach,
    SpannedIntegerError,
    Verification,
]


class FullStory(Scene):
    def construct(self):
        for i, scene_cls in enumerate(SCENES):
            if scene_cls is PileToGSD and hasattr(self, "cloud"):
                # Bridge from SieveStack: don't clear — slide particles into
                # pile bands and morph sieve front edges into datums, then
                # run PileToGSD with its own setup skipped.
                transition_to_piles(self, self)
                self._skip_pile_setup = True
                try:
                    scene_cls.construct(self)
                finally:
                    self._skip_pile_setup = False
            elif scene_cls is DefiningG and hasattr(self, "axes"):
                # Seamless handoff from PileToGSD: keep particles + bars,
                # ContinuumReveal layers more particles on top.
                self._skip_continuum_setup = True
                try:
                    scene_cls.construct(self)
                finally:
                    self._skip_continuum_setup = False
            else:
                scene_cls.construct(self)

            if i < len(SCENES) - 1:
                next_cls = SCENES[i + 1]
                seamless = (
                    (scene_cls is SieveStack and next_cls is PileToGSD)
                    or (scene_cls is PileToGSD and next_cls is DefiningG)
                    or (scene_cls is QuantityRatio and next_cls is ReducingError)
                    or (scene_cls is ReducingError
                        and next_cls is SpannedIntegerApproach)
                    or (scene_cls is SpannedIntegerApproach
                        and next_cls is SpannedIntegerError)
                )
                if seamless:
                    continue
                # Fade out current state instead of cutting to black, so the
                # transition between scenes reads as a soft hand-off.
                if self.mobjects:
                    self.play(
                        *[FadeOut(m) for m in list(self.mobjects)],
                        run_time=0.35,
                    )
