# Copyright (c) 2026 matthiasmitwittfogel
# Licensed under the Custom Educational License.
# See LICENSE file for details.

"""Visual proof that the sum 1/8 + 1/16 + 1/32 + ... equals 1/4."""

import math
from manim import (
    BLACK,
    BLUE,
    BraceBetweenPoints,
    Create,
    FadeOut,
    GREEN,
    GrowFromCenter,
    LEFT,
    MathTex,
    PI,
    Polygon,
    RED,
    RIGHT,
    Scene,
    Square,
    Succession,
    UP,
    DOWN,
    VGroup,
    WHITE,
    Write,
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
SQUARE_SIDE = 8
ROTATION_ANGLE = PI / 4
SCALE_FACTOR = 1 / math.sqrt(2)
RUN_TIME_SHORT = 0.5
FILL_COLOR = RED
FILL_OPACITY = 0.5

BL = [-4, -4, 0]
BR = [4, -4, 0]
TL = [-4, 4, 0]


class SeriesSumFromOneOver8(Scene):
    """Animated geometric decomposition showing the infinite series starting at 1/8 sums to 1/4."""

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------
    def _rotate_square(self, square, run_time):
        """Return a copy of *square* rotated by 45° and scaled by 1/√2."""
        new_square = square.copy()
        self.play(
            new_square.animate.rotate(ROTATION_ANGLE).scale(SCALE_FACTOR),
            run_time=run_time,
        )
        return new_square

    def _add_triangle(self, vertices, run_time, pre_shift=None):
        """Create a filled red triangle."""
        triangle = Polygon(*vertices, fill_color=FILL_COLOR, fill_opacity=FILL_OPACITY)
        if pre_shift is not None:
            triangle.shift(pre_shift)
        self.play(Create(triangle), run_time=run_time)
        return triangle

    def _add_labeled_triangle(self, vertices, formula_subobj, run_time,
                              term_scale=None, pre_shift=None):
        """Create a filled red triangle and place a (possibly scaled) formula term at its centroid."""
        triangle = self._add_triangle(vertices, run_time, pre_shift)
        term = formula_subobj.copy()
        if term_scale is not None:
            term.scale(term_scale)
        self.play(term.animate.move_to(triangle.get_center_of_mass()), run_time=run_time)
        return triangle, term

    def construct(self):
        # --- Formula & question mark -----------------------------------------
        formula = (
            MathTex(
                r"\frac{1}{8}", r"+", r"\frac{1}{16}", r"+", r"\frac{1}{32}", r"+",
                r"\frac{1}{64}", r"+", r"\frac{1}{128}", r"+", r"..."
            )
            .scale(1.5)
            .shift(UP * 8)
        )
        self.play(Write(formula), run_time=1)

        question_mark = MathTex("?", font_size=200, color=RED).next_to(formula, DOWN * 10)
        self.play(Succession(Create(question_mark), FadeOut(question_mark)))

        # --- Base square & braces --------------------------------------------
        square_1 = Square(side_length=SQUARE_SIDE)
        self.play(Create(square_1), run_time=RUN_TIME_SHORT)

        brace_left = BraceBetweenPoints(TL, BL)
        txt1 = MathTex("1").next_to(brace_left, LEFT)
        brace_down = BraceBetweenPoints(BL, BR)
        txt2 = txt1.copy().next_to(brace_down, DOWN)
        self.play(
            Create(brace_left),
            Create(txt1),
            Create(brace_down),
            Create(txt2),
            run_time=1,
        )

        # --- Rotating squares and labelled triangles -------------------------
        square_2 = self._rotate_square(square_1, RUN_TIME_SHORT)
        triangle1, f1 = self._add_labeled_triangle(
            [BL, [-4, 0, 0], [0, -4, 0]], formula[0], RUN_TIME_SHORT
        )

        square_3 = self._rotate_square(square_2, RUN_TIME_SHORT)
        triangle2, f2 = self._add_labeled_triangle(
            [[0, -4, 0], [-2, -2, 0], [2, -2, 0]],
            formula[2], RUN_TIME_SHORT, term_scale=0.8
        )

        square_4 = self._rotate_square(square_3, RUN_TIME_SHORT)
        triangle3, f3 = self._add_labeled_triangle(
            [[0, -2, 0], [2, 0, 0], [2, -2, 0]],
            formula[4], RUN_TIME_SHORT, term_scale=0.5
        )

        square_5 = self._rotate_square(square_4, RUN_TIME_SHORT)
        triangle4, f4 = self._add_labeled_triangle(
            [[1, 1, 0], [1, -1, 0], [2, 0, 0]],
            formula[6], RUN_TIME_SHORT, term_scale=0.4
        )

        square_6 = self._rotate_square(square_5, RUN_TIME_SHORT)
        triangle5, f5 = self._add_labeled_triangle(
            [[0, 1, 0], [1, 0, 0], [1, 1, 0]],
            formula[8], RUN_TIME_SHORT, term_scale=0.2
        )

        # --- Remaining small triangles (no labels) ---------------------------
        square_7 = self._rotate_square(square_6, RUN_TIME_SHORT)
        triangle6 = self._add_triangle(
            [[0, 1 / 2, 0], [1 / 2, 0, 0], [-1 / 2, 0, 0]],
            RUN_TIME_SHORT, pre_shift=UP / 2
        )

        square_8 = self._rotate_square(square_7, RUN_TIME_SHORT)
        triangle7 = self._add_triangle(
            [[0, 1 / 2, 0], [-1 / 2, 0, 0], [-1 / 2, 1 / 2, 0]], RUN_TIME_SHORT
        )

        square_9 = self._rotate_square(square_8, RUN_TIME_SHORT)
        triangle8 = self._add_triangle(
            [[-1 / 4, 1 / 4, 0], [-1 / 4, -1 / 4, 0], [-1 / 2, 0, 0]], RUN_TIME_SHORT
        )

        square10 = self._rotate_square(square_9, RUN_TIME_SHORT)
        triangle9 = self._add_triangle(
            [[-1 / 4, -1 / 4, 0], [0, -1 / 4, 0], [-1 / 4, 0, 0]], RUN_TIME_SHORT
        )

        # --- Group and rotate copies -----------------------------------------
        group1 = VGroup(
            triangle9, triangle8, triangle7, triangle6, triangle5,
            triangle4, triangle3, triangle2, triangle1, f1, f2, f3, f4, f5
        )
        group1_ = VGroup(
            triangle9, triangle8, triangle7, triangle6, triangle5,
            triangle4, triangle3, triangle2, triangle1
        )
        group2 = group1_.copy().set_fill(GREEN)
        self.play(group2.animate.rotate(PI / 2, about_point=[0, -2, 0]).shift((RIGHT + UP) * 2))

        group3 = group2.copy().set_fill(BLUE)
        self.play(group3.animate.rotate(PI / 2).shift(UP * 2.5 + LEFT * 0.5))

        group4 = group3.copy().set_fill(WHITE)
        self.play(group4.animate.rotate(PI / 2).shift(LEFT * 2.5 + DOWN * 0.5))

        # --- Clean up construction guides ------------------------------------
        self.remove(
            square10, square_9, square_8, square_7, square_6, square_5,
            square_4, square_3, square_2, square_1
        )
        self.remove(brace_down, brace_left, txt2, txt1)

        # --- Arrange quadrants -----------------------------------------------
        self.play(
            group4.animate.shift(LEFT * 2 + UP * 2),
            group3.animate.shift(RIGHT * 2 + UP * 2),
            group2.animate.shift(DOWN * 2 + RIGHT * 2),
            group1.animate.shift(LEFT * 2 + DOWN * 2)
        )

        # --- Final 1/4 labels ------------------------------------------------
        quarter_txt1 = MathTex(r"{{\frac{1}{4}}}").scale(5).move_to(group4.get_center())
        self.play(GrowFromCenter(quarter_txt1))
        quarter_txt2 = MathTex(r"{{\frac{1}{4}}}").scale(5).move_to(group3.get_center())
        self.play(GrowFromCenter(quarter_txt2))
        quarter_txt3 = MathTex(r"{{\frac{1}{4}}}").scale(5).move_to(group2.get_center())
        self.play(GrowFromCenter(quarter_txt3))
        quarter_txt4 = MathTex(r"{{\frac{1}{4}}}").scale(5).move_to(group1.get_center())
        self.play(GrowFromCenter(quarter_txt4))

        # --- Fade out three quadrants ----------------------------------------
        self.play(FadeOut(group4), FadeOut(quarter_txt1), run_time=0.5)
        self.play(FadeOut(group3), FadeOut(quarter_txt2), run_time=0.5)
        self.play(FadeOut(group2), FadeOut(quarter_txt3), run_time=0.5)

        # --- Equation --------------------------------------------------------
        eq = MathTex("=").scale(2).move_to(UP * 5 + LEFT * 5)
        self.play(Write(eq), run_time=0.5)

        self.play(quarter_txt4.animate.scale(1 / 5 * 2).set_color(RED).next_to(eq, RIGHT))

        self.wait(4)
