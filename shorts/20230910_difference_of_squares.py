# Copyright (c) 2026 matthiasmitwittfogel
# Licensed under the Custom Educational License.
# See LICENSE file for details.

"""Visual proof of the difference of squares: a² − b² = (a+b)(a−b)."""

import numpy as np

from manim import (
    BLACK,
    BLUE,
    BraceBetweenPoints,
    Create,
    DOWN,
    DrawBorderThenFill,
    FadeIn,
    GREEN,
    LEFT,
    Line,
    MarkupText,
    MathTex,
    PI,
    RED,
    Rectangle,
    ReplacementTransform,
    RIGHT,
    Rotate,
    Scene,
    Square,
    Text,
    Transform,
    UP,
    VGroup,
    config,
)

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
config.background_color = BLACK
config.pixel_width = 900
config.pixel_height = 1600
config.frame_width = 27
config.frame_height = 48

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
SCALE_VAL = 2


class DifferenceOfSquares(Scene):
    """Animate the geometric decomposition of a² − b²."""

    def _make_brace(self, p1, p2, label_text, label_dir):
        """Create a brace between two points with a scaled label."""
        brace = BraceBetweenPoints(p1, p2, color=BLUE, sharpness=0.5)
        label = MathTex(label_text, color=BLUE).scale(SCALE_VAL).next_to(brace, label_dir)
        return brace, label

    def construct(self):
        # --- Titles -----------------------------------------------------------
        title1 = Text(
            "Visual Proof",
            font_size=80,
            gradient=(RED, BLUE, GREEN),
        )
        title2 = MarkupText(
            '<span underline="single" underline_color="green">Difference of Squares</span>',
            gradient=(RED, BLUE, GREEN),
            font_size=80,
        ).next_to(title1, DOWN * 2)

        self.play(FadeIn(title1), FadeIn(title2))
        self.play(
            title1.animate.move_to([0, 10, 0]),
            title2.animate.move_to([[0, 8, 0]]),
        )

        # --- Large square a² --------------------------------------------------
        square_a = Square(side_length=8, fill_color=RED, fill_opacity=0.4, color=BLACK)
        self.play(Create(square_a))

        up_brace, up_brace_label = self._make_brace([4, 4, 0], [-4, 4, 0], "a", UP)
        self.play(Create(up_brace_label), Create(up_brace), run_time=1)

        left_brace, left_brace_label = self._make_brace([-4, 4, 0], [-4, -4, 0], "a", LEFT)
        self.play(Create(left_brace_label), Create(left_brace), run_time=1)

        group_a = VGroup(up_brace_label.copy(), left_brace_label.copy())
        a_square = MathTex(r"a^2", color=BLUE).scale(SCALE_VAL).move_to([-4, -8, 0])
        self.play(ReplacementTransform(group_a, a_square))

        # --- Inner square b² --------------------------------------------------
        square_b = Square(side_length=3, fill_color=GREEN, fill_opacity=0.4).move_to([-2.5, -2.5, 0])
        self.play(DrawBorderThenFill(square_b))

        left_brace_b, left_brace_b_label = self._make_brace([-4, -1, 0], [-4, -4, 0], "b", LEFT)
        left_brace_a_b, left_brace_a_b_label = self._make_brace([-4, 4, 0], [-4, -1, 0], "a-b", LEFT)
        self.play(
            Transform(left_brace, left_brace_a_b),
            Transform(left_brace_label, left_brace_a_b_label),
            Create(left_brace_b),
            Create(left_brace_b_label),
        )

        bottom_brace_b, bottom_brace_b_label = self._make_brace([-4, -4, 0], [-1, -4, 0], "b", DOWN)
        self.add(bottom_brace_b_label, bottom_brace_b)

        bottom_brace_a_b, bottom_brace_a_b_label = self._make_brace([-1, -4, 0], [4, -4, 0], "a-b", DOWN)
        self.add(bottom_brace_a_b_label, bottom_brace_a_b)

        group_b = VGroup(left_brace_b_label.copy(), bottom_brace_b_label.copy())

        equal_notation = MathTex("-", color=BLUE).scale(SCALE_VAL).next_to(a_square)
        self.add(equal_notation)
        b_square = MathTex(r"b^2 = ", color=BLUE).scale(SCALE_VAL).next_to(equal_notation, RIGHT)
        self.play(ReplacementTransform(group_b, b_square))

        # --- Cover b² and hide its braces -------------------------------------
        square_b_ = Square(
            side_length=4,
            fill_color=BLACK,
            stroke_color=BLACK,
            color=BLACK,
            fill_opacity=1,
        ).move_to([-3, -3, 0])
        self.add(square_b_)
        self.remove(bottom_brace_b, bottom_brace_b_label, left_brace_b_label, left_brace_b)

        # --- Cut line and new braces ------------------------------------------
        dot_line = Line(start=[-1, -1, 0], end=[4, -1, 0])
        self.play(Create(dot_line))

        right_b_brace, right_b_brace_label = self._make_brace([4, -4, 0], [4, -1, 0], "b", RIGHT)
        self.play(Create(right_b_brace_label), Create(right_b_brace))

        # --- Mask and rotate remaining strip ----------------------------------
        rect_mask = Rectangle(
            width=5,
            height=3,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_color=BLACK,
            color=BLACK,
        ).move_to([1.5, -2.5, 0])

        rect_tmp = Rectangle(
            width=5,
            height=3,
            fill_color=RED,
            fill_opacity=0.4,
            color=BLACK,
        ).move_to([-1 + 5 / 2.0, -4 + 3 / 2.0, 0])
        self.add(rect_mask)
        self.add(rect_tmp)

        self.remove(bottom_brace_a_b_label, bottom_brace_a_b, right_b_brace, right_b_brace_label)
        self.play(Rotate(rect_tmp, about_point=[4, -1, 0], angle=PI / 2))

        # --- Braces for rotated strip -----------------------------------------
        rect_tmp_up_brace, rect_tmp_up_brace_label = self._make_brace([7, -1, 0], [4, -1, 0], "b", UP)
        rect_tmp_right_brace, rect_tmp_right_brace_label = self._make_brace([7, -6, 0], [7, -1, 0], "a-b", RIGHT)
        self.add(rect_tmp_up_brace, rect_tmp_up_brace_label, rect_tmp_right_brace, rect_tmp_right_brace_label)

        # --- Move strip up and build formula ----------------------------------
        rect_tmp_group = VGroup(
            rect_tmp,
            rect_tmp_up_brace,
            rect_tmp_up_brace_label,
            rect_tmp_right_brace,
            rect_tmp_right_brace_label,
        )
        self.play(rect_tmp_group.animate.shift(np.array([0, 5, 0])))

        left_pan = MathTex("(", color=BLUE).scale(SCALE_VAL).next_to(b_square, RIGHT)
        self.add(left_pan)
        math_a = up_brace_label.copy()
        self.play(math_a.animate.next_to(left_pan, RIGHT))
        math_plus = MathTex("+", color=BLUE).scale(SCALE_VAL).next_to(math_a, RIGHT)
        self.add(math_plus)
        math_b = rect_tmp_up_brace_label.copy()
        self.play(math_b.animate.next_to(math_plus, RIGHT))
        right_pan = MathTex(r")(", color=BLUE).scale(SCALE_VAL).next_to(math_b, RIGHT)
        self.add(right_pan)
        math_a_b = left_brace_a_b_label.copy()
        self.play(math_a_b.animate.next_to(right_pan, RIGHT))

        self.add(MathTex(")", color=BLUE).scale(SCALE_VAL).next_to(math_a_b, RIGHT))

        self.wait(4)
