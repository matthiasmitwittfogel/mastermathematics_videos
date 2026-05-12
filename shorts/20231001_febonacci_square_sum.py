# Copyright (c) 2026 matthiasmitwittfogel
# Licensed under the Custom Educational License.
# See LICENSE file for details.

"""Visual proof that the sum of Fibonacci squares equals a product of consecutive Fibonacci numbers."""

from manim import (
    BLACK,
    BLUE,
    BraceBetweenPoints,
    Create,
    DOWN,
    FadeOut,
    LEFT,
    MathTex,
    RED,
    RIGHT,
    Scene,
    Square,
    Succession,
    UP,
    VGroup,
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
SIDE_LEN = 1


class FebonacciSquareSum(Scene):
    """Build a Fibonacci spiral of squares and show the area identity."""

    def _add_square_to_group(self, side_length, group, direction, formula, formula_index, scale_factor=None):
        """Create a square, animate its formula into place, tint the formula red, and add both to group."""
        square = Square(side_length=side_length, color=BLUE)
        if scale_factor is not None:
            square = square.scale(scale_factor)
        square = square.next_to(group, direction, buff=0)

        square_formula = formula.submobjects[formula_index].copy()
        self.play(Create(square))
        self.play(square_formula.animate.move_to(square.get_center()))
        formula.submobjects[formula_index].set_color(RED)
        group.add(square, square_formula)
        return square, square_formula

    def construct(self):
        # --- Formula and question ---------------------------------------------
        formula = MathTex(
            "1^2", "+", "1^2", "+", "2^2", "+", "3^2", "+", "5^2", "+",
            "8^2", "+", "13^2", "+", "21^2", "+", "34^2", "+", "55^2", "+", "89^2",
        ).scale(1).shift(UP * 8)
        final_formula = formula.copy()
        self.play(Write(formula), run_time=1)
        question_mark = MathTex("?", font_size=96, color=RED).next_to(formula, DOWN * 5)
        self.play(Succession(Create(question_mark), FadeOut(question_mark)))

        # --- First two squares (no group yet) ---------------------------------
        square_1 = Square(side_length=SIDE_LEN, color=BLUE)
        self.play(Create(square_1))

        square_1_formula = formula.submobjects[0].copy()
        self.play(square_1_formula.animate.move_to(square_1.get_center()))
        formula.submobjects[0].set_color(RED)

        square_2 = square_1.copy().next_to(square_1, DOWN, buff=0)
        self.play(Create(square_2))

        square_2_formula = formula.submobjects[2].copy()
        self.play(square_2_formula.animate.move_to(square_2.get_center()))
        formula.submobjects[2].set_color(RED)

        group = VGroup(square_1, square_1_formula, square_2, square_2_formula)

        # --- Remaining squares ------------------------------------------------
        square_3, _ = self._add_square_to_group(2, group, RIGHT, formula, 4)
        square_4, _ = self._add_square_to_group(3, group, DOWN, formula, 6)
        self.play(group.animate.shift(UP * 4 + LEFT * 4))

        square_5, _ = self._add_square_to_group(5, group, RIGHT, formula, 8)
        square_6, _ = self._add_square_to_group(8, group, DOWN, formula, 10)
        self.play(group.animate.scale(0.5).shift(LEFT * 3 + UP * 4))

        square_7, _ = self._add_square_to_group(13, group, RIGHT, formula, 12, scale_factor=0.5)
        square_8, _ = self._add_square_to_group(21, group, DOWN, formula, 14, scale_factor=0.5)
        self.play(group.animate.scale(0.3).shift(UP * 2 + LEFT * 2))

        square_9, _ = self._add_square_to_group(34, group, RIGHT, formula, 16, scale_factor=0.5 * 0.3)
        square_10, square_10_formula = self._add_square_to_group(55, group, DOWN, formula, 18, scale_factor=0.5 * 0.3)
        self.play(group.animate.scale(0.5).shift(LEFT * 4 + UP * 3))
        self.play(square_10_formula.animate.scale(2))

        square_11, _ = self._add_square_to_group(89, group, RIGHT, formula, 20, scale_factor=0.5 * 0.3 * 0.5)

        # --- Bottom braces ----------------------------------------------------
        brace1 = BraceBetweenPoints(
            group.get_center() + [-group.width / 2.0, -group.height / 2.0, 0],
            group.get_center() + [group.width / 2.0 - group.width * 89.0 / (55 + 89), -group.height / 2.0, 0],
        )
        txt1 = MathTex("55").next_to(brace1, DOWN)
        self.play(Create(brace1), Create(txt1))

        brace2 = BraceBetweenPoints(
            group.get_center() + [group.width / 2.0 - group.width * 89.0 / (55 + 89), -group.height / 2.0, 0],
            group.get_center() + [group.width / 2.0, -group.height / 2.0, 0],
        )
        txt2 = MathTex("89").next_to(brace2, DOWN)
        self.play(Create(brace2), Create(txt2))

        brace3 = BraceBetweenPoints(
            group.get_center() + [group.width / 2.0, -group.height / 2.0, 0],
            group.get_center() + [group.width / 2.0, group.height / 2.0, 0],
        )
        txt3 = MathTex("89").next_to(brace3, RIGHT)
        self.play(Create(brace3), Create(txt3))

        # --- Result formula ---------------------------------------------------
        equals = MathTex("=(").shift(UP * 6 + LEFT * 4)
        self.play(Write(equals))
        f1 = txt1.copy()
        self.play(Write(f1))
        self.play(f1.animate.next_to(equals, RIGHT))
        f2 = MathTex("+")
        self.play(f2.animate.next_to(f1, RIGHT))
        f3 = txt2.copy()
        self.play(f3.animate.next_to(f2, RIGHT))
        f4 = MathTex(r")\cdot").next_to(f3, RIGHT)
        self.add(f4)
        f5 = txt3.copy()
        self.play(f5.animate.next_to(f4, RIGHT))

        equals1 = MathTex("=").align_to(equals, LEFT).shift(UP * 4)
        self.play(Write(equals1))
        result = MathTex("12816").next_to(equals1, RIGHT)
        self.play(Write(result))

        self.wait(4)
