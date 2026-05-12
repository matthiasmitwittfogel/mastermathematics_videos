# Copyright (c) 2026 matthiasmitwittfogel
# Licensed under the Custom Educational License.
# See LICENSE file for details.

"""Visual proof that 1 + 2 + … + n = n(n+1)/2 via geometric rearrangement."""

import numpy as np

from manim import (
    BLACK,
    BLUE,
    BraceBetweenPoints,
    Create,
    DOWN,
    DrawBorderThenFill,
    FadeIn,
    FadeOut,
    FadeTransform,
    LEFT,
    Line,
    MathTex,
    PI,
    Rectangle,
    RED,
    RIGHT,
    Scene,
    Transform,
    TransformMatchingTex,
    UP,
    WHITE,
    Write,
    config,
)

# configs
config.background_color = BLACK
config.pixel_width = 2160
config.pixel_height = 3840


class SumFrom1ToN(Scene):
    """Animate Gauss's formula by merging two staircases into a rectangle."""

    def construct(self):
        # === Formula introduction ===
        isolate_tex = ["1+2+3+4+5+6+...+n"]
        formula = MathTex(
            "1+2+3+4+5+6+...+n",
            color=BLUE,
            substrings_to_isolate=isolate_tex,
        ).scale(1.5)
        self.play(Write(formula), run_time=2)
        question_mark = MathTex("=?", color=RED).scale(1.5).next_to(formula, DOWN * 3)
        self.play(Create(question_mark))
        self.wait(1)
        self.play(FadeOut(question_mark))

        self.play(formula.animate.move_to(UP * 9))

        # === Left staircase ===
        line_group = [
            Line(start=[-5, 6 - i * 0.12, 0], end=[-5 + 0.1 * i, 6 - i * 0.12, 0])
            for i in range(50)
        ]
        for line in line_group:
            self.play(Create(line), run_time=0.03)

        left_brace = BraceBetweenPoints(
            line_group[0].start,
            line_group[49].start,
            color=BLUE,
            sharpness=0.5,
        )
        left_brace_label = MathTex("n", color=BLUE).next_to(left_brace, LEFT).rotate(PI / 2)

        bottom_brace = BraceBetweenPoints(
            line_group[49].start,
            line_group[49].end,
            color=BLUE,
            sharpness=0.5,
        )
        bottom_brace_label = MathTex("n", color=BLUE).next_to(bottom_brace, DOWN)

        self.play(FadeIn(left_brace_label), FadeIn(left_brace))
        self.play(FadeIn(bottom_brace), FadeIn(bottom_brace_label))

        # === Right staircase ===
        line_group1 = [
            Line(start=[5 - 0.1 * i, -6 + i * 0.12, 0], end=[5, -6 + i * 0.12, 0])
            for i in range(50)
        ]
        for line in line_group1:
            self.play(Create(line), run_time=0.03)

        right_brace = BraceBetweenPoints(
            line_group1[0].end,
            line_group1[49].end,
            color=BLUE,
            sharpness=0.5,
        )
        right_brace_label = MathTex("n", color=BLUE).next_to(right_brace, RIGHT).rotate(PI / 2)

        up_brace = BraceBetweenPoints(
            line_group1[49].end,
            line_group1[49].start,
            color=BLUE,
            sharpness=0.5,
        )
        up_brace_label = MathTex("n", color=BLUE).next_to(up_brace, UP)

        self.play(FadeIn(right_brace_label), FadeIn(right_brace))
        self.play(FadeIn(up_brace), FadeIn(up_brace_label))

        # === Merge staircases into rectangle ===
        bottom_brace_label_ = MathTex("n+1", color=BLUE).next_to([0, -3, 0], DOWN * 1.5)
        up_brace_label_ = MathTex("n+1", color=BLUE).next_to([0, 3, 0], UP * 1.5)

        SHIFT_A = np.array([5.0 / 2, -6.0 / 2, 0])
        SHIFT_B = np.array([-5.0 / 2, 6.0 / 2, 0])

        self.play(
            *[g.animate.shift(SHIFT_A) for g in line_group],
            left_brace.animate.shift(SHIFT_A),
            left_brace_label.animate.shift(SHIFT_A),
            bottom_brace.animate.shift(SHIFT_A),
            FadeTransform(bottom_brace_label, bottom_brace_label_),
            *[g1.animate.shift(SHIFT_B) for g1 in line_group1],
            right_brace.animate.shift(SHIFT_B),
            right_brace_label.animate.shift(SHIFT_B),
            FadeTransform(up_brace_label, up_brace_label_),
            up_brace.animate.shift(SHIFT_B),
        )

        # === Rectangle and answer ===
        rect = Rectangle(width=5, height=6, fill_color=WHITE, fill_opacity=0.5)
        self.play(DrawBorderThenFill(rect, run_time=1))
        self.remove(*line_group, *line_group1)

        equal = MathTex("=").scale(1.5).move_to(UP * 7).align_to(formula, LEFT)
        self.add(equal)
        isolate_tex1 = ["(n+1)"]
        answer = MathTex(
            r"n\times (n+1)",
            color=BLUE,
            substrings_to_isolate=isolate_tex1,
        ).scale(1.5).next_to(equal, RIGHT)
        answer1 = MathTex(
            r"\frac{n\times (n+1)}{2}",
            color=BLUE,
        ).scale(1.5).next_to(equal, RIGHT)
        formula1 = MathTex(
            r"2\times (1+2+3+4+5+6+...+n)",
            color=BLUE,
            substrings_to_isolate=isolate_tex,
        ).scale(1.5).move_to(UP * 9)

        self.play(Write(answer), TransformMatchingTex(formula, formula1), run_time=3)

        self.play(
            Create(Line(start=[0, -3, 0], end=[0, 3, 0])), color=RED
        )
        self.add(
            Rectangle(width=5 / 2, height=6, fill_color=WHITE, fill_opacity=0.5).shift(
                np.array([5 / 4.0, 0, 0])
            )
        )

        self.remove(
            left_brace,
            left_brace_label,
            bottom_brace,
            bottom_brace_label,
            bottom_brace_label_,
        )

        up_brace_half = BraceBetweenPoints([5 / 2.0, 3, 0], [0, 3, 0])
        up_brace_label_half = MathTex(r"\frac{n+1}{2}", color=BLUE).next_to(up_brace_half, UP)

        self.play(
            FadeOut(rect),
            Transform(up_brace, up_brace_half),
            Transform(up_brace_label_, up_brace_label_half),
            run_time=3,
        )
        self.play(
            TransformMatchingTex(formula1, formula),
            TransformMatchingTex(answer, answer1),
            run_time=3,
        )

        self.wait(5)
