"""Stitched 5-scene master for the 1-minute poster video.

Soft FadeOut between Scenes 1→2, 2→3, and 4→5. The Scene 3 → Scene 4
hand-off is custom (no fade-out): Scene 4 picks up the volume sieve
stack from Scene 3 and slides it right while the mass figure appears.

Render with:

    uv run manim -ql scenes/poster_scene.py PosterVersion
"""

from __future__ import annotations

from manim import FadeOut, Scene, config

from _common import BACKGROUND
from scene1_title import TitleQuestion
# from scene2_mass import TotalMassRatios
# from scene3_volume import VolumeRatios
# from scene4_quantity import QuantityRatios
# from scene5_verification import VerificationUsage

config.background_color = BACKGROUND
config.frame_rate = 30


class PosterVersion(Scene):
    def construct(self):
        # Scene 1
        TitleQuestion.construct(self)
        self._fade_all(0.4)

    def _fade_all(self, run_time: float = 0.4) -> None:
        if self.mobjects:
            self.play(
                *[FadeOut(m) for m in list(self.mobjects)],
                run_time=run_time,
            )
