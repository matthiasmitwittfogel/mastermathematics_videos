# Copyright (c) 2026 matthiasmitwittfogel
# Licensed under the Custom Educational License.
# See LICENSE file for details.

"""Visual proof that 1 + 3 + 5 + … + (2n-1) = n² via square packing."""

import math

import numpy as np

from manim import (
    BLACK,
    BLUE,
    BraceBetweenPoints,
    Create,
    DOWN,
    LEFT,
    MathTex,
    PURPLE,
    RED,
    ReplacementTransform,
    RIGHT,
    Rotate,
    Succession,
    Scene,
    FadeOut,
    Square,
    UP,
    VGroup,
    WHITE,
    Write,
    YELLOW,
    config,
)

# configs
config.background_color = BLACK
config.pixel_width = 360
config.pixel_height = 640

SIDE_LEN = 0.5
FORMULA_SHIFT = UP * 8


class Sum2N_1(Scene):
    """Animate the sum of odd integers forming successively larger squares."""

    def _create_squares(self, *squares):
        """Play Create animation for the given squares with fixed run_time."""
        self.play(*[Create(s) for s in squares], run_time=0.2)

    def _next_layer(self, prev_layer):
        """Copy a layer and shift it down by one square length."""
        return prev_layer.copy().shift(DOWN * SIDE_LEN)

    def _extend_sides(self, center_group, template):
        """Return center, left and right squares for the next layer."""
        left = template.copy().next_to(center_group, LEFT, buff=0)
        right = template.copy().next_to(center_group, RIGHT, buff=0)
        return center_group, left, right

    def _add_rotated_layer(self, source_group, color, prev_formula, multiplier, anchor):
        """Rotate a copy of source_group, shift it right, and update the formula."""
        new_group = source_group.copy().set_fill(color)
        self.play(Rotate(new_group, about_point=anchor.get_center(), angle=math.pi / 2))
        self.play(new_group.animate.shift(np.array([anchor.side_length, 0, 0])))
        new_formula = MathTex(
            rf"{multiplier}\cdot(1+3+5+...+(2n-1))"
        ).scale(1.5).shift(FORMULA_SHIFT)
        self.play(ReplacementTransform(prev_formula, new_formula))
        return new_group, new_formula

    def construct(self):
        # === Formula introduction ===
        formula = MathTex("1+3+5+...+(2n-1)").scale(1.5).shift(FORMULA_SHIFT)
        final_formula = formula.copy()
        self.play(Write(formula), run_time=1)
        question_mark = MathTex("?", font_size=96, color=RED).next_to(formula, DOWN * 5)
        self.play(Succession(Create(question_mark), FadeOut(question_mark)))

        # === Build square layers ===
        # Layer 1
        square_1 = Square(
            side_length=SIDE_LEN,
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.5,
        )
        # Layer 2
        square_2 = square_1.copy().next_to(square_1, DOWN, buff=0)
        square_3 = square_2.copy().next_to(square_2, LEFT, buff=0)
        square_4 = square_3.copy().next_to(square_2, RIGHT, buff=0)
        # Layers 3-7
        square_5, square_6, square_7 = self._extend_sides(
            self._next_layer(VGroup(square_2, square_3, square_4)), square_3
        )
        square_8, square_9, square_10 = self._extend_sides(
            self._next_layer(VGroup(square_7, square_6, square_5)), square_3
        )
        square_11, square_12, square_13 = self._extend_sides(
            self._next_layer(VGroup(square_8, square_9, square_10)), square_3
        )
        square_14, square_15, square_16 = self._extend_sides(
            self._next_layer(VGroup(square_11, square_13, square_12)), square_3
        )
        square_17, square_18, square_19 = self._extend_sides(
            self._next_layer(VGroup(square_14, square_15, square_16)), square_3
        )

        # === Animate square creation ===
        self._create_squares(square_1)
        self._create_squares(square_2, square_3, square_4)
        self._create_squares(square_5, square_6, square_7)
        self._create_squares(square_8, square_9, square_10)
        self._create_squares(square_11, square_12, square_13)
        self._create_squares(square_14, square_15, square_16)
        self._create_squares(square_17, square_18, square_19)

        # === Labels ===
        txt1 = MathTex("1").next_to(square_1, UP)
        brace = BraceBetweenPoints(
            [
                square_18.get_center()[0] - square_18.side_length / 2,
                square_18.get_center()[1],
                square_18.get_center()[2],
            ],
            [
                square_19.get_center()[0] + square_19.side_length / 2,
                square_19.get_center()[1],
                square_19.get_center()[2],
            ],
        ).shift(DOWN * 0.5)
        txt2 = MathTex("2n-1").next_to(brace, DOWN)
        self.play(Create(txt1))
        self.play(Create(brace))
        self.play(Create(txt2))

        self.remove(txt1)
        all_group = VGroup(
            square_1,
            square_2,
            square_3,
            square_4,
            square_5,
            square_6,
            square_7,
            square_9,
            square_10,
            square_8,
            square_13,
            square_12,
            square_11,
            square_16,
            square_15,
            square_14,
            square_17,
            square_18,
            square_19,
        )

        # === Rotated copies ===
        all_group_copy1, formula1 = self._add_rotated_layer(
            all_group, RED, formula, 2, square_1
        )
        all_group_copy2, formula2 = self._add_rotated_layer(
            all_group_copy1, YELLOW, formula1, 3, square_1
        )
        _, formula3 = self._add_rotated_layer(
            all_group_copy2, PURPLE, formula2, 4, square_1
        )

        # === Vertical brace ===
        brace2 = BraceBetweenPoints(
            [
                square_18.get_center()[0],
                square_18.get_center()[1] + square_18.side_length * 13.5,
                square_18.get_center()[2],
            ],
            [
                square_18.get_center()[0],
                square_18.get_center()[1] - square_18.side_length / 2,
                square_18.get_center()[2],
            ],
        ).shift(LEFT)
        self.play(Create(brace2))
        txt3 = MathTex("2n", sheen_direction=UP).next_to(brace2, LEFT)
        self.play(Write(txt3))

        # === Final formula derivation ===
        equal_sign = MathTex("=").scale(1.5).shift(UP * 6 + LEFT * 4)
        self.play(Write(equal_sign), run_time=0.5)
        txt4 = txt3.copy()
        self.play(txt4.animate.scale(1.5).next_to(equal_sign, RIGHT))
        dot_sign = MathTex(r"\cdot").scale(1.5).next_to(txt4, RIGHT)
        self.play(Write(dot_sign), run_time=0.1)
        txt5 = txt2.copy()
        self.play(txt5.animate.scale(1.5).next_to(dot_sign, RIGHT))

        group_ans = VGroup(txt5, dot_sign, txt4)

        final_ans = MathTex(r"n^2").scale(1.5).next_to(equal_sign, RIGHT)
        self.play(
            ReplacementTransform(formula3, final_formula),
            ReplacementTransform(group_ans, final_ans),
            run_time=2,
        )

        self.wait(4)
