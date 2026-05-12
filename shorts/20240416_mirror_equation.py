# Copyright (c) 2026 matthiasmitwittfogel
# Licensed under the Custom Educational License.
# See LICENSE file for details.

"""Scene showing mirror-symmetric perfect squares."""

from manim import (
    BLACK,
    CounterclockwiseTransform,
    DOWN,
    LEFT,
    Line,
    MathTex,
    ORIGIN,
    RIGHT,
    Scene,
    UP,
    Write,
    config,
)


# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
config.background_color = BLACK
config.pixel_width = 2160
config.pixel_height = 3840


class SeriesSumFromOneOver3(Scene):
    """Demonstrate mirrored square equations."""

    MIRROR_LINE_EXTENT = 10
    FONT_SIZE = 60
    FONT_SIZE_SMALL = 55
    EDGE_SHIFT = 3

    def _mirror_pair(self, left_tex, right_tex, y_shift, font_size, left_align, right_align):
        """Write a left equation and transform a copy into its mirrored right form."""
        eq = MathTex(left_tex, font_size=font_size).shift(y_shift).align_to(left_align, RIGHT)
        eq_ = MathTex(right_tex, font_size=font_size).shift(y_shift).align_to(right_align, LEFT)
        self.play(Write(eq))
        self.play(CounterclockwiseTransform(eq.copy(), eq_))
        return eq, eq_

    def construct(self):
        # --- Mirror axis ----------------------------------------------------------
        self.add(
            Line(
                start=ORIGIN + DOWN * self.MIRROR_LINE_EXTENT,
                end=ORIGIN + UP * self.MIRROR_LINE_EXTENT,
            )
        )

        # --- First pair (defines edge alignment) ----------------------------------
        eq1 = (
            MathTex(r"10^2=100", font_size=self.FONT_SIZE)
            .shift(UP * self.MIRROR_LINE_EXTENT)
            .to_edge(LEFT)
            .shift(RIGHT * self.EDGE_SHIFT)
        )
        eq1_ = (
            MathTex(r"001=01^2", font_size=self.FONT_SIZE)
            .shift(UP * self.MIRROR_LINE_EXTENT)
            .to_edge(RIGHT)
            .shift(LEFT * self.EDGE_SHIFT)
        )
        self.play(Write(eq1))
        self.play(CounterclockwiseTransform(eq1.copy(), eq1_))

        # --- Subsequent pairs -----------------------------------------------------
        eq2, eq2_ = self._mirror_pair(
            r"11^2=121", r"121=11^2", UP * 8, self.FONT_SIZE, eq1, eq1_
        )
        eq3, eq3_ = self._mirror_pair(
            r"12^2=144", r"441=21^2", UP * 6, self.FONT_SIZE, eq2, eq2_
        )
        eq4, eq4_ = self._mirror_pair(
            r"13^2=169", r"961=31^2", UP * 4, self.FONT_SIZE, eq3, eq3_
        )
        eq5, _ = self._mirror_pair(
            r"102^2=10404", r"40401=201^2", UP * 2, self.FONT_SIZE, eq4, eq4_
        )

        # NOTE: from pair 6 onward left alignment stays on eq5 and right on eq4_
        self._mirror_pair(
            r"103^2=10609", r"90601=301^2", ORIGIN, self.FONT_SIZE, eq5, eq4_
        )
        self._mirror_pair(
            r"1002^2=1004004", r"4004001=2001^2", DOWN * 2, self.FONT_SIZE, eq5, eq4_
        )
        self._mirror_pair(
            r"1003^2=1006009", r"9006001=3001^2", DOWN * 4, self.FONT_SIZE, eq5, eq4_
        )
        self._mirror_pair(
            r"10002^2=100040004",
            r"400040001=20001^2",
            DOWN * 6,
            self.FONT_SIZE_SMALL,
            eq5,
            eq4_,
        )
        self._mirror_pair(
            r"10003^2=100060009",
            r"900060001=30001^2",
            DOWN * 8,
            self.FONT_SIZE_SMALL,
            eq5,
            eq4_,
        )

        self.wait(3)
