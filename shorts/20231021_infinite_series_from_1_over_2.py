# Copyright (c) 2026 matthiasmitwittfogel
# Licensed under the Custom Educational License.
# See LICENSE file for details.

"""Visual proof that the infinite series 1/2 + 1/4 + 1/8 + ... equals 1."""

from manim import (
    BLACK,
    BLUE,
    Create,
    DashedLine,
    DOWN,
    FadeOut,
    GrowFromEdge,
    LEFT,
    MathTex,
    ORIGIN,
    Polygon,
    RED,
    RIGHT,
    Scene,
    Succession,
    UP,
    WHITE,
    Write,
    YELLOW,
    config,
)

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
config.background_color = BLACK
config.pixel_width = 2160
config.pixel_height = 3840

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
BL = [-4, -4, 0]
BR = [4, -4, 0]
TL = [-4, 4, 0]


class SeriesSumFromOneOver8(Scene):
    """Animated geometric proof of the 1/2 + 1/4 + 1/8 + ... = 1 identity."""

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------
    def _add_triangle_slice(self, line_start, line_end, vertices, color, grow_edge,
                            formula_subobj, term_scale=None):
        """Draw a dashed divider and grow a coloured triangle with its series term."""
        line = DashedLine(start=line_start, end=line_end, color=WHITE)
        self.play(Create(line))

        triangle = Polygon(*vertices, color=color, fill_color=color, fill_opacity=0.5)
        self.play(GrowFromEdge(triangle, grow_edge))

        term = formula_subobj.copy()
        if term_scale is not None:
            self.play(term.animate.scale(term_scale).move_to(triangle.get_center_of_mass()))
        else:
            self.play(term.animate.move_to(triangle.get_center_of_mass()))
        return line, triangle, term

    def construct(self):
        # --- Formula & question mark -----------------------------------------
        formula = (
            MathTex(
                r"\frac{1}{2}", r"+", r"\frac{1}{4}", r"+", r"\frac{1}{8}", r"+",
                r"\frac{1}{16}", r"+", r"\frac{1}{32}", r"+", r"\frac{1}{64}", r"+", r"..."
            )
            .scale(1.5)
            .shift(UP * 9)
        )
        self.play(Write(formula), run_time=1)

        question_mark = MathTex("?", font_size=200, color=RED).next_to(formula, DOWN * 10)
        self.play(Succession(Create(question_mark), FadeOut(question_mark)))

        # --- Base right triangle ---------------------------------------------
        triangle = Polygon(BL, BR, TL, color=WHITE)
        self.play(Create(triangle), run_time=1)

        label1 = MathTex(r"\sqrt{2} ", font_size=80, color=BLUE).next_to(triangle, LEFT, buff=0.3)
        label2 = label1.copy().next_to(triangle, DOWN, buff=0.3)
        label3 = MathTex("2", color=BLUE, font_size=80).next_to(triangle, RIGHT, buff=0.2).shift(LEFT * 3)
        self.add(label3, label2, label1)

        # --- Recursive triangular slices -------------------------------------
        line1, triangle1, _ = self._add_triangle_slice(
            BL, ORIGIN, [BL, TL, ORIGIN], BLUE, LEFT,
            formula[0]
        )

        line2, triangle2, _ = self._add_triangle_slice(
            ORIGIN, [0, -4, 0], [ORIGIN, DOWN * 4, BL], YELLOW, DOWN,
            formula[2]
        )

        line3, triangle3, _ = self._add_triangle_slice(
            [0, -4, 0], [2, -2, 0], [[0, -4, 0], [2, -2, 0], ORIGIN], BLUE, LEFT,
            formula[4]
        )

        line4, triangle4, _ = self._add_triangle_slice(
            [2, -2, 0], [2, -4, 0], [[2, -2, 0], [2, -4, 0], [0, -4, 0]], YELLOW, DOWN,
            formula[6], term_scale=0.5
        )

        line5, triangle5, _ = self._add_triangle_slice(
            [2, -4, 0], [3, -3, 0], [[3, -3, 0], [2, -4, 0], [2, -2, 0]], BLUE, LEFT,
            formula[8], term_scale=1 / 3
        )

        line6, triangle6, _ = self._add_triangle_slice(
            [3, -3, 0], [3, -4, 0], [[3, -3, 0], [3, -4, 0], [2, -4, 0]], YELLOW, DOWN,
            formula[10], term_scale=0.25
        )

        # --- Remaining small triangle and overlay ----------------------------
        triangle7 = Polygon([3, -3, 0], [3, -4, 0], [4, -4, 0],
                            color=BLUE, fill_color=BLUE, fill_opacity=0.5)
        self.play(GrowFromEdge(triangle7, LEFT))
        self.play(formula[12].copy().animate.scale(1 / 3).move_to(triangle7.get_center_of_mass()))

        triangle_ = Polygon(BL, BR, TL, color=RED, fill_color=RED, fill_opacity=0.8)
        self.play(GrowFromEdge(triangle_, LEFT))

        # --- Equation --------------------------------------------------------
        equal = MathTex("=").scale(1.5).align_to(formula, LEFT).shift(UP * 7)
        self.play(Write(equal))

        self.play(label1.animate.next_to(equal, RIGHT))
        dot = MathTex(r"\cdot").next_to(label1, RIGHT)
        self.add(dot)

        self.play(label2.animate.next_to(dot, RIGHT))
        div = MathTex(r"{\div} 2", font_size=80, color=BLUE).next_to(label2, RIGHT)
        self.play(Write(div))

        result = MathTex("=1", color=RED).scale(1.5).align_to(equal, LEFT).shift(UP * 5)
        self.play(Write(result))

        self.wait(3)
