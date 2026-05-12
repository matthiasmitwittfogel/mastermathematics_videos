# Copyright (c) 2026 matthiasmitwittfogel
# Licensed under the Custom Educational License.
# See LICENSE file for details.

"""Visual proof that 1+2+3+...+n+...+3+2+1 = n²."""

from manim import (
    BLACK,
    BraceBetweenPoints,
    Create,
    DOWN,
    FadeOut,
    GREEN,
    LEFT,
    MathTex,
    PI,
    PURPLE,
    RED,
    RIGHT,
    Rotate,
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
RUN_T = 0.2
SIDE_LEN = 0.5


class SumFrom1ToNTo1(Scene):
    """Build a staircase of squares, mirror it, and show it forms an n×n square."""

    def _create_row(self, prev_rect_1, prev_rect_2, label_text):
        """Add a new row below prev_rect_1 using a copied VGroup for the right side."""
        rect_1 = Square(side_length=SIDE_LEN, fill_color=PURPLE, fill_opacity=0.5).next_to(prev_rect_1, DOWN, buff=0)
        rect_2 = VGroup(prev_rect_1, prev_rect_2).copy().next_to(rect_1, RIGHT, buff=0)
        self.play(Create(rect_1), Create(rect_2), run_time=RUN_T)
        txt = MathTex(label_text).next_to(rect_1, LEFT)
        self.add(txt)
        return rect_1, rect_2, txt

    def _create_mirror_row(self, source_group, shift_amount):
        """Copy a labelled row, shift it downward, and tint it green."""
        row = source_group.copy().shift(shift_amount).set_fill(GREEN)
        self.play(Create(row), run_time=RUN_T)
        return row

    def construct(self):
        # --- Title and question -----------------------------------------------
        formula = MathTex("1+2+3+...+n+...+3+2+1").scale(1.5).shift(UP * 8)
        self.play(Write(formula), run_time=1)
        question_mark = MathTex("?", font_size=96, color=RED).next_to(formula, DOWN * 5)
        self.play(Succession(Create(question_mark), FadeOut(question_mark)), run_time=1)

        # --- Build staircase rows ---------------------------------------------
        rect1 = Square(side_length=SIDE_LEN, fill_color=PURPLE, fill_opacity=0.5).move_to(LEFT * 4 + UP * 6)
        self.play(Create(rect1), run_time=RUN_T)
        txt1 = MathTex("1").next_to(rect1, LEFT)
        self.add(txt1)

        # Row 2 is special: its right half is just a copy of its left half
        rect2_1 = Square(side_length=SIDE_LEN, fill_color=PURPLE, fill_opacity=0.5).next_to(rect1, DOWN, buff=0)
        rect2_2 = rect2_1.copy().next_to(rect2_1, RIGHT, buff=0)
        self.play(Create(rect2_2), Create(rect2_1), run_time=RUN_T)
        txt2 = MathTex("2").next_to(rect2_1, LEFT)
        self.add(txt2)

        rect3_1, rect3_2, txt3 = self._create_row(rect2_1, rect2_2, "3")
        rect4_1, rect4_2, txt4 = self._create_row(rect3_1, rect3_2, "4")
        rect5_1, rect5_2, txt5 = self._create_row(rect4_1, rect4_2, "5")
        rect6_1, rect6_2, txt6 = self._create_row(rect5_1, rect5_2, "6")
        rect7_1, rect7_2, txt7 = self._create_row(rect6_1, rect6_2, "7")
        rect8_1, rect8_2, txt8 = self._create_row(rect7_1, rect7_2, "...")
        rect9_1, rect9_2, txt9 = self._create_row(rect8_1, rect8_2, "n-1")

        # Row n is tinted green
        rectn_1 = (
            Square(side_length=SIDE_LEN, fill_color=PURPLE, fill_opacity=0.5)
            .next_to(rect9_1, DOWN, buff=0)
            .set_fill(GREEN)
        )
        rectn_2 = VGroup(rect9_1, rect9_2).copy().next_to(rectn_1, RIGHT, buff=0).set_fill(GREEN)
        self.play(Create(rectn_1), Create(rectn_2), run_time=RUN_T)
        txtn = MathTex("n").next_to(rectn_1, LEFT)
        self.add(txtn)

        # --- Mirror rows below ------------------------------------------------
        self._create_mirror_row(VGroup(rect9_1, rect9_2, txt9), DOWN)
        self._create_mirror_row(VGroup(rect8_1, rect8_2, txt8), DOWN * 2)
        self._create_mirror_row(VGroup(rect7_1, rect7_2, txt7), DOWN * 3)
        self._create_mirror_row(VGroup(rect6_1, rect6_2, txt6), DOWN * 4)
        self._create_mirror_row(VGroup(rect5_1, rect5_2, txt5), DOWN * 5)
        self._create_mirror_row(VGroup(rect4_1, rect4_2, txt4), DOWN * 6)
        self._create_mirror_row(VGroup(rect3_1, rect3_2, txt3), DOWN * 7)
        self._create_mirror_row(VGroup(rect2_1, rect2_2, txt2), DOWN * 8)
        self._create_mirror_row(VGroup(rect1, txt1), DOWN * 9)

        # --- Clean up labels and reposition -----------------------------------
        self.remove(txt1, txt2, txt3, txt4, txt5, txt6, txt7, txt8, txt9)
        up_group = VGroup(
            rect1, rect2_1, rect2_2, rect3_1, rect3_2,
            rect4_1, rect4_2, rect5_1, rect5_2, rect6_1,
            rect6_2, rect7_1, rect7_2, rect8_1, rect8_2,
            rect9_1, rect9_2,
        )

        self.play(up_group.animate.shift(RIGHT * 5))
        self.play(up_group.animate.shift(DOWN * 10 / 2))
        self.play(Rotate(up_group, PI / 2))
        self.play(up_group.animate.shift(LEFT * 4.5))

        # --- Braces and final result ------------------------------------------
        down_brace = BraceBetweenPoints(
            LEFT * 4 + RIGHT * 0.25 + DOWN * 4,
            RIGHT + RIGHT * 0.25 + DOWN * 4,
        ).shift(LEFT * 0.5 + UP * 0.5)
        right_brace = BraceBetweenPoints(
            RIGHT * 1.2 + DOWN * 3.5 + UP * 0.25,
            RIGHT * 1.2 + UP * 1.5 + UP * 0.25,
        )

        self.add(down_brace)
        down_num = MathTex("n").next_to(down_brace, DOWN)
        self.play(Write(down_num))
        self.add(right_brace)
        right_num = MathTex("n").next_to(right_brace, RIGHT)
        self.play(Write(right_num))

        equal = MathTex("=").scale(1.5).move_to(UP * 6 + LEFT * 5.5)
        self.play(Write(equal))
        n_ = down_num.copy().scale(1.5)
        self.play(n_.animate.next_to(equal, RIGHT))
        dot = MathTex(r"\cdot").scale(1.5).next_to(n_, RIGHT)
        self.add(dot)
        self.play(right_num.copy().scale(1.5).animate.next_to(dot, RIGHT))

        result = MathTex("=n^2").scale(1.5).move_to(UP * 4 + LEFT * 5)
        self.play(Write(result))

        self.wait(4)
