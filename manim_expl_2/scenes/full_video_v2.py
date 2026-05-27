"""Stitched 5-scene master for the 1-minute poster video.

Soft FadeOut between Scenes 1→2, 2→3, and 4→5. The Scene 3 → Scene 4
hand-off is custom (no fade-out): Scene 4 picks up the volume sieve
stack from Scene 3 and slides it right while the mass figure appears.

Render with:

    uv run manim -ql scenes/full_video_v2.py FullStoryV2
"""

from __future__ import annotations

from manim import FadeOut, Scene, config

from _common import BACKGROUND
from scene1_title import TitleQuestion
from scene2_mass import TotalMassRatios
from scene3_volume import VolumeRatios
from scene4_quantity import QuantityRatios
from scene5_verification import VerificationUsage

config.background_color = BACKGROUND
config.frame_rate = 30


class FullStoryV2(Scene):
    def construct(self):
        # Scene 1
        TitleQuestion.construct(self)
        self._fade_all(0.4)

        # Scene 2
        TotalMassRatios.construct(self)
        self._fade_all(0.4)

        # Scene 3 — its construct stashes mobjects on `self`.
        VolumeRatios.construct(self)

        # Scene 3 → Scene 4 hand-off: don't fade. Scene 4 reads the
        # stashed mobjects (self._numerators, ._denominators, ._slashes,
        # ._sieve_dots, ._vector, ._zeta, ._title, ._dashed_lines,
        # ._solid_line) and animates the slide / fade-in itself.
        self._from_scene3 = True
        QuantityRatios.construct(self)
        self._from_scene3 = False
        self._fade_all(0.4)

        # Scene 5
        VerificationUsage.construct(self)

    def _fade_all(self, run_time: float = 0.4) -> None:
        if self.mobjects:
            self.play(
                *[FadeOut(m) for m in list(self.mobjects)],
                run_time=run_time,
            )
