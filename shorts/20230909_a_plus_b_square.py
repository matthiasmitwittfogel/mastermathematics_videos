# Copyright (c) 2026 matthiasmitwittfogel
# Licensed under the Custom Educational License.
# See LICENSE file for details.

"""Visual proof of (a+b)^2 = a^2 + 2ab + b^2."""

from manim import (
    BLACK,
    BLUE,
    Create,
    DashedLine,
    DOWN,
    DrawBorderThenFill,
    FadeOut,
    GREEN,
    LEFT,
    Line,
    MathTex,
    RED,
    Rectangle,
    RIGHT,
    Scene,
    Square,
    Succession,
    TransformMatchingTex,
    UP,
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
config.pixel_width = 2160
config.pixel_height = 3840

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
SCALE_VALUE = 1.5
OPACITY_VAL = 0.5


class APlusBSquare(Scene):
    """Draw a square of side (a+b) and decompose it into four rectangles."""

    def _create_labeled_line(self, start, end, color, label_text, label_dir):
        """Create a line with a scaled MathTex label next to it."""
        line = Line(start=start, end=end, color=color)
        label = MathTex(label_text).next_to(line, label_dir).scale(SCALE_VALUE)
        return line, label

    def _draw_rect_group(self, shape, label_a, label_b, position):
        """Draw a filled shape, move label_a to its centre, add a dot, then move label_b."""
        self.play(DrawBorderThenFill(shape), run_time=0.5)
        self.play(label_a.animate.move_to(position))
        dot = MathTex(r"\cdot ").next_to(label_a, RIGHT)
        self.add(dot)
        self.play(label_b.animate.next_to(dot, RIGHT))
        return VGroup(label_a, dot, label_b)

    def construct(self):
        # --- Intro formula ----------------------------------------------------
        formula1 = MathTex(r"(a+b)^{2}=?", color=BLUE).scale(4)
        self.play(Succession(Create(formula1), FadeOut(formula1)), run_time=2)

        # --- Outer square edges -----------------------------------------------
        line1, label1 = self._create_labeled_line([-5, 5, 0], [1, 5, 0], RED, "a", UP)
        self.play(Create(line1))
        self.add(label1)

        line2, label2 = self._create_labeled_line(line1.end, [5, 5, 0], GREEN, "b", UP)
        self.play(Create(line2))
        self.add(label2)

        line3, label3 = self._create_labeled_line(line2.end, [5, -1, 0], RED, "a", RIGHT)
        self.play(Create(line3))
        self.add(label3)

        line4, label4 = self._create_labeled_line(line3.end, [5, -5, 0], GREEN, "b", RIGHT)
        self.play(Create(line4))
        self.add(label4)

        line5, label5 = self._create_labeled_line(line4.end, [1, -5, 0], GREEN, "b", DOWN)
        self.play(Create(line5))
        self.add(label5)

        line6, label6 = self._create_labeled_line(line5.end, [-5, -5, 0], RED, "a", DOWN)
        self.play(Create(line6))
        self.add(label6)

        line7, label7 = self._create_labeled_line(line6.end, [-5, -1, 0], GREEN, "b", LEFT)
        self.play(Create(line7))
        self.add(label7)

        line8, label8 = self._create_labeled_line(line7.end, [-5, 5, 0], RED, "a", LEFT)
        self.play(Create(line8))
        self.add(label8)

        # --- Build expanded formula -------------------------------------------
        formula_part1 = MathTex("(").scale(SCALE_VALUE).move_to([-5, 10, 0])
        self.play(Write(formula_part1))
        formula_part2 = label1.copy()
        self.play(formula_part2.animate.scale(SCALE_VALUE).next_to(formula_part1))
        formula_part3 = MathTex("+").scale(SCALE_VALUE).next_to(formula_part2, RIGHT)
        self.play(Write(formula_part3))
        formula_part4 = label2.copy()
        self.play(formula_part4.animate.scale(SCALE_VALUE).next_to(formula_part3, RIGHT))
        formula_part5 = MathTex(r")\cdot(").scale(SCALE_VALUE).next_to(formula_part4, RIGHT)
        self.play(Write(formula_part5))
        formula_part6 = label3.copy()
        self.play(formula_part6.animate.scale(SCALE_VALUE).next_to(formula_part5, RIGHT))
        formula_part7 = MathTex("+").scale(SCALE_VALUE).next_to(formula_part6, RIGHT)
        self.play(Write(formula_part7))
        formula_part8 = label4.copy()
        self.play(formula_part8.animate.scale(SCALE_VALUE).next_to(formula_part7, RIGHT))
        formula_part9 = MathTex(")").scale(SCALE_VALUE).next_to(formula_part8, RIGHT)
        self.play(Write(formula_part9))

        # --- Collapse back to squared form ------------------------------------
        formula_part5_ = MathTex(r")^{2}").scale(SCALE_VALUE).next_to(formula_part4, RIGHT)
        self.play(
            *[FadeOut(mob) for mob in [formula_part6, formula_part7, formula_part8, formula_part9]],
            TransformMatchingTex(formula_part5, formula_part5_),
            run_time=2,
        )

        equal = MathTex("=").scale(SCALE_VALUE).move_to([-5, 8, 0])
        self.play(Write(equal))

        # --- Dashed dividing lines --------------------------------------------
        dash_line1 = DashedLine(start=line8.start, end=line3.end)
        dash_line2 = DashedLine(start=line1.end, end=line5.end)
        self.play(Create(dash_line1), Create(dash_line2))

        # --- Four inner rectangles --------------------------------------------
        rect1 = Square(side_length=6, fill_color=RED, fill_opacity=OPACITY_VAL).move_to([-2, 2, 0])
        group1 = self._draw_rect_group(rect1, label8, label1, [-2, 2, 0])

        rect2 = Rectangle(width=4, height=6, fill_color=GREEN, fill_opacity=OPACITY_VAL).move_to([3, 2, 0])
        group2 = self._draw_rect_group(rect2, label2, label3, [3, 2, 0])

        rect3 = Square(side_length=4, fill_color=YELLOW, fill_opacity=OPACITY_VAL).move_to([3, -3, 0])
        group3 = self._draw_rect_group(rect3, label4, label5, [3, -3, 0])

        rect4 = Rectangle(width=6, height=4, fill_color=BLUE, fill_opacity=OPACITY_VAL).move_to([-2, -3, 0])
        group4 = self._draw_rect_group(rect4, label6, label7, [-2, -3, 0])

        # --- Arrange groups next to equals ------------------------------------
        self.play(group1.animate.scale(1).next_to(equal, RIGHT))
        plus1 = MathTex(" + ").next_to(group1, RIGHT * 1.5).scale(SCALE_VALUE)
        self.add(plus1)
        self.play(group2.animate.scale(1).next_to(plus1, RIGHT * 1.5))
        plus2 = plus1.copy().next_to(group2, RIGHT * 1.5)
        self.add(plus2)
        self.play(group3.animate.scale(1).next_to(plus2, RIGHT * 1.5))
        plus3 = plus2.copy().next_to(group3, RIGHT * 1.5)
        self.add(plus3)
        self.play(group4.animate.scale(1).next_to(plus3, RIGHT * 1.5))

        # --- Final simplified result ------------------------------------------
        equal_ = MathTex("=").scale(SCALE_VALUE).move_to([-5, 6, 0])
        result = MathTex(r"a^2 + 2ab + b^2", color=WHITE).scale(SCALE_VALUE).next_to(equal_, RIGHT)
        self.add(equal_)
        self.play(Write(result))

        self.wait(4)
