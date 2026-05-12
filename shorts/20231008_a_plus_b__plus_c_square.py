# Copyright (c) 2026 matthiasmitwittfogel
# Licensed under the Custom Educational License.
# See LICENSE file for details.

"""Visual derivation of (a+b+c)^2 by splitting a square into nine rectangles."""

import numpy as np
from manim import (
    BLACK,
    BLUE,
    BraceBetweenPoints,
    Create,
    DashedLine,
    FadeOut,
    GOLD,
    GREEN,
    GrowFromEdge,
    LEFT,
    Line,
    MathTex,
    ORANGE,
    PINK,
    Polygon,
    PURPLE,
    RED,
    RIGHT,
    Scene,
    Succession,
    Text,
    UP,
    DOWN,
    VGroup,
    WHITE,
    Write,
    YELLOW,
    config,
)

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
config.background_color = BLACK
config.pixel_width = 360
config.pixel_height = 640

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
OFFSET = np.array([-5, -4, 0])
LABEL_SCALE = 1
RUN_T = 0.2
NEW_RUN_T = 0.5


class APlusBPlusCSquare(Scene):
    """Decompose a square of side (a+b+c) to show the algebraic expansion."""

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------
    def _add_edge(self, start, end, color, label_text, label_dir, run_time):
        """Draw a solid border line and attach its label."""
        line = Line(start=start, end=end, color=color).shift(OFFSET)
        label = MathTex(label_text).next_to(line, label_dir).scale(LABEL_SCALE)
        self.play(Create(line), run_time=run_time)
        self.add(label)
        return line, label

    def _add_dashed_edge(self, start, end, color, label_text, label_dir, run_time):
        """Draw a dashed divider line and attach its label."""
        line = DashedLine(start=start, end=end, color=color).shift(OFFSET)
        label = MathTex(label_text).next_to(line, label_dir).scale(LABEL_SCALE)
        self.play(Create(line), run_time=run_time)
        self.add(label)
        return line, label

    def _fill_rect(self, corners, fill_color, grow_edge, center_label, dot_label,
                   side_label, run_time, last_run_time=None):
        """Grow a coloured rectangle and assemble its area label."""
        rect = Polygon(*corners, fill_color=fill_color, fill_opacity=0.5).shift(OFFSET)
        self.play(GrowFromEdge(rect, grow_edge), run_time=run_time)
        self.play(center_label.animate.move_to(rect.get_center()), run_time=run_time)
        dot = MathTex(r"\cdot").next_to(dot_label, RIGHT)
        self.add(dot)
        if last_run_time is not None:
            self.play(side_label.animate.next_to(dot, RIGHT), run_time=last_run_time)
        else:
            self.play(side_label.animate.next_to(dot, RIGHT))
        return rect, dot

    def construct(self):
        # --- Title & question ------------------------------------------------
        formula1 = MathTex(r"(a+b+c)^{2}", color=BLUE).scale(1.5)
        question = Text("?", color=RED).scale(3).next_to(formula1, DOWN * 2)
        self.play(Write(formula1))
        self.play(Succession(Create(question), FadeOut(question)))
        self.play(formula1.animate.shift(UP * 9 + LEFT * 4))

        # --- Top border ------------------------------------------------------
        line11, label11 = self._add_edge([0, 8, 0], [3, 8, 0], RED, "a", UP, RUN_T)
        line12, label12 = self._add_edge([3, 8, 0], [6, 8, 0], YELLOW, "b", UP, RUN_T)
        line13, label13 = self._add_edge([6, 8, 0], [8, 8, 0], BLUE, "c", UP, RUN_T)

        # --- Right border ----------------------------------------------------
        line21, label21 = self._add_edge([8, 8, 0], [8, 5, 0], RED, "a", RIGHT, RUN_T)
        line22, label22 = self._add_edge([8, 5, 0], [8, 2, 0], YELLOW, "b", RIGHT, RUN_T)
        _, label23 = self._add_edge([8, 2, 0], [8, 0, 0], BLUE, "c", RIGHT, RUN_T)

        # --- Bottom border ---------------------------------------------------
        line31, label31 = self._add_edge([8, 0, 0], [6, 0, 0], BLUE, "c", DOWN * 2, RUN_T)
        line32, label32 = self._add_edge([6, 0, 0], [3, 0, 0], YELLOW, "b", DOWN * 2, RUN_T)
        _, label33 = self._add_edge([3, 0, 0], [0, 0, 0], RED, "a", DOWN * 2, RUN_T)

        # --- Left border -----------------------------------------------------
        line41, label41 = self._add_edge([0, 0, 0], [0, 2, 0], BLUE, "c", LEFT * 2, RUN_T)
        _, label42 = self._add_edge([0, 2, 0], [0, 5, 0], YELLOW, "b", LEFT * 2, RUN_T)
        line43, label43 = self._add_edge([0, 5, 0], [0, 8, 0], RED, "a", LEFT * 2, RUN_T)

        # --- Horizontal dashed lines -----------------------------------------
        line51, label51 = self._add_dashed_edge([0, 5, 0], [3, 5, 0], RED, "a", DOWN, RUN_T)
        line52, label52 = self._add_dashed_edge([3, 5, 0], [6, 5, 0], YELLOW, "b", DOWN, RUN_T)
        line53, label53 = self._add_dashed_edge([6, 5, 0], [8, 5, 0], RED, "c", DOWN, RUN_T)

        line61, label61 = self._add_dashed_edge([0, 2, 0], [3, 2, 0], RED, "a", DOWN, RUN_T)
        line62, label62 = self._add_dashed_edge([3, 2, 0], [6, 2, 0], YELLOW, "b", DOWN, RUN_T)
        line63, label63 = self._add_dashed_edge([6, 2, 0], [8, 2, 0], RED, "c", DOWN, RUN_T)

        # --- Vertical dashed lines -------------------------------------------
        line71, label71 = self._add_dashed_edge([3, 8, 0], [3, 5, 0], RED, "a", RIGHT, RUN_T)
        _, label72 = self._add_dashed_edge([3, 5, 0], [3, 2, 0], YELLOW, "b", RIGHT, RUN_T)
        line73, label73 = self._add_dashed_edge([3, 2, 0], [3, 0, 0], RED, "c", RIGHT, RUN_T)

        line81, label81 = self._add_dashed_edge([6, 8, 0], [6, 5, 0], RED, "a", RIGHT, RUN_T)
        line82, label82 = self._add_dashed_edge([6, 5, 0], [6, 2, 0], YELLOW, "b", RIGHT, RUN_T)
        _, label83 = self._add_dashed_edge([6, 2, 0], [6, 0, 0], RED, "c", RIGHT, RUN_T)

        # --- Coloured rectangles ---------------------------------------------
        _, dot1 = self._fill_rect(
            (line11.start, line11.end, line71.end, line51.start),
            RED, LEFT, label11, label11, label71, NEW_RUN_T
        )
        subgroup1 = VGroup(label11, label71, dot1)

        _, dot2 = self._fill_rect(
            (line12.start, line12.end, line81.end, line52.start),
            ORANGE, LEFT, label12, label12, label81, NEW_RUN_T
        )
        subgroup2 = VGroup(label12, dot2, label81)

        _, dot3 = self._fill_rect(
            (line13.start, line13.end, line21.end, line53.start),
            YELLOW, LEFT, label13, label13, label21, NEW_RUN_T
        )
        subgroup3 = VGroup(label21, dot3, label13)

        _, dot4 = self._fill_rect(
            (line22.start, line22.end, line82.end, line82.start),
            GREEN, UP, label53, label53, label22, NEW_RUN_T
        )
        subgroup4 = VGroup(label22, dot4, label53)

        _, dot5 = self._fill_rect(
            (line52.start, line52.end, line62.end, line62.start),
            BLUE, RIGHT, label52, label52, label82, NEW_RUN_T
        )
        subgroup5 = VGroup(label82, label52, dot5)

        _, dot6 = self._fill_rect(
            (line51.start, line51.end, line61.end, line61.start),
            PURPLE, RIGHT, label51, label51, label72, NEW_RUN_T,
            last_run_time=None
        )
        subgroup6 = VGroup(label72, dot6, label51)

        _, dot7 = self._fill_rect(
            (line41.start, line41.end, line73.start, line73.end),
            WHITE, UP, label61, label61, label73, NEW_RUN_T,
            last_run_time=None
        )
        subgroup7 = VGroup(label73, label61, dot7)

        _, dot8 = self._fill_rect(
            (line62.start, line62.end, line32.start, line32.end),
            GOLD, LEFT, label62, label62, label83, NEW_RUN_T,
            last_run_time=None
        )
        subgroup8 = VGroup(label83, dot8, label62)

        _, dot9 = self._fill_rect(
            (line63.start, line63.end, line31.start, line31.end),
            PINK, LEFT, label63, label63, label23, NEW_RUN_T,
            last_run_time=None
        )
        subgroup9 = VGroup(label23, dot9, label63)

        # --- Bottom brace ----------------------------------------------------
        brace_down = BraceBetweenPoints(line41.start, line31.start).shift(OFFSET)
        self.play(Create(brace_down), run_time=NEW_RUN_T)
        down_plus1 = MathTex("+").next_to(label32, LEFT)
        down_plus2 = MathTex("+").next_to(label32, RIGHT)
        self.add(down_plus2, down_plus1)
        self.play(label33.animate.next_to(down_plus1, LEFT), run_time=NEW_RUN_T)
        self.play(label31.animate.next_to(down_plus2, RIGHT), run_time=NEW_RUN_T)

        # --- Left brace ------------------------------------------------------
        brace_left = BraceBetweenPoints(line43.end, line41.start).shift(OFFSET)
        self.play(Create(brace_left), run_time=NEW_RUN_T)
        left_plus1 = MathTex("+").next_to(label42, UP)
        left_plus2 = MathTex("+").next_to(label42, DOWN)
        self.add(left_plus2, left_plus1)
        self.play(label43.animate.next_to(left_plus1, UP), run_time=NEW_RUN_T)
        self.play(label41.animate.next_to(left_plus2, DOWN), run_time=NEW_RUN_T)

        # --- Equation assembly -----------------------------------------------
        equals1 = MathTex("=(").scale(1).move_to(LEFT * 6 + UP * 8)
        self.play(Create(equals1), run_time=NEW_RUN_T)
        group_left = VGroup(down_plus2, down_plus1, label31, label32, label33)
        self.play(group_left.animate.next_to(equals1, RIGHT))
        middle = MathTex(r")\cdot(").next_to(group_left)
        self.add(middle)

        self.play(label43.animate.next_to(middle, RIGHT), run_time=NEW_RUN_T)
        self.play(left_plus1.animate.next_to(label43, RIGHT), run_time=NEW_RUN_T)
        self.play(label42.animate.next_to(left_plus1, RIGHT), run_time=NEW_RUN_T)
        self.play(left_plus2.animate.next_to(label42, RIGHT), run_time=NEW_RUN_T)
        self.play(label41.animate.next_to(left_plus2, RIGHT), run_time=NEW_RUN_T)

        right = MathTex(")").next_to(label41, RIGHT)
        self.add(right)

        equals2 = MathTex("=").scale(1).align_to(equals1, LEFT).shift(UP * 7)
        self.add(equals2)
        self.play(subgroup1.animate.next_to(equals2, RIGHT), run_time=NEW_RUN_T)
        plus1 = MathTex("+").scale(1).next_to(subgroup1, RIGHT)
        self.add(plus1)
        self.play(subgroup2.animate.next_to(plus1, RIGHT), run_time=NEW_RUN_T)
        plus2 = plus1.copy().next_to(subgroup2, RIGHT)
        self.add(plus2)
        self.play(subgroup3.animate.next_to(plus2, RIGHT), run_time=NEW_RUN_T)
        plus3 = plus2.copy().next_to(subgroup3, RIGHT)
        self.add(plus3)
        self.play(subgroup4.animate.next_to(plus3, RIGHT), run_time=NEW_RUN_T)
        plus4 = plus3.copy().next_to(subgroup4, RIGHT)
        self.add(plus4)
        self.play(subgroup5.animate.next_to(plus4, RIGHT), run_time=NEW_RUN_T)
        plus5 = plus4.copy().next_to(subgroup5, RIGHT)
        self.add(plus5)
        self.play(subgroup6.animate.move_to(LEFT * 5 + UP * 6), run_time=NEW_RUN_T)
        plus6 = plus5.copy().next_to(subgroup6, RIGHT)
        self.add(plus6)
        self.play(subgroup7.animate.next_to(plus6, RIGHT), run_time=NEW_RUN_T)
        plus7 = plus6.copy().next_to(subgroup7, RIGHT)
        self.add(plus7)
        self.play(subgroup8.animate.next_to(plus7, RIGHT), run_time=NEW_RUN_T)
        plus8 = plus7.copy().next_to(subgroup8, RIGHT)
        self.add(plus8)
        self.play(subgroup9.animate.next_to(plus8, RIGHT), run_time=NEW_RUN_T)

        result = MathTex(
            r"=a^2+b^2+c^2+2ab+2ac+2bc",
            substrings_to_isolate=["a", "b", "c"]
        ).align_to(equals1, LEFT).shift(UP * 5)
        result.set_color_by_tex("a", RED)
        result.set_color_by_tex("b", YELLOW)
        result.set_color_by_tex("c", BLUE)
        self.play(Write(result))

        self.wait(4)
