# Copyright (c) 2026 matthiasmitwittfogel
# Licensed under the Custom Educational License.
# See LICENSE file for details.

"""Visual proof that the series 1/3 + (1/3)^2 + (1/3)^3 + ... equals 1/2."""

from manim import (
    BLACK,
    BLUE,
    BraceBetweenPoints,
    Create,
    DashedLine,
    DOWN,
    DR,
    FadeOut,
    GrowFromCenter,
    GrowFromEdge,
    LEFT,
    MathTex,
    ORIGIN,
    PI,
    Polygon,
    PURE_RED,
    Rectangle,
    RED,
    RIGHT,
    Rotate,
    Scene,
    Square,
    Succession,
    Text,
    UL,
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
SQUARE_SIDE = 8
SEGMENT = 8 / 3
SEGMENT2 = 8 / 3 / 3
SEGMENT3 = 8 / 3 / 3 / 3
FILL_OPACITY = 0.4
FILL_COLOR = BLUE
RUN_T = 0.5

BL = [-4, -4, 0]
BR = [4, -4, 0]
TL = [-4, 4, 0]


class SeriesSumFromOneOver3(Scene):
    """Animated decomposition of the unit square showing the 1/3-series sums to 1/2."""

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------
    def _add_dashed_pair(self, start, end, shift_dir, shift_dist, reverse_order=False):
        """Create a dashed line and a shifted copy, preserving original play order."""
        line1 = DashedLine(start=start, end=end)
        line2 = line1.copy().shift(shift_dir * shift_dist)
        if reverse_order:
            self.play(Create(line2), Create(line1))
        else:
            self.play(Create(line1), Create(line2))
        return line1, line2

    def _add_formula_rect(self, shape, grow_edge, formula_subobj, term_scale=None):
        """Grow a filled shape and place a scaled formula term at its centroid."""
        self.play(GrowFromEdge(shape, grow_edge))
        term = formula_subobj.copy()
        if term_scale is not None:
            self.play(term.animate.scale(term_scale).move_to(shape.get_center_of_mass()))
        else:
            self.play(term.animate.move_to(shape.get_center_of_mass()))
        return term

    def construct(self):
        # --- Formula & question mark -----------------------------------------
        formula = (
            MathTex(
                r"\frac{1}{3}", r"+", r"(\frac{1}{3})^{2}", r"+", r"(\frac{1}{3})^{3}", r"+",
                r"(\frac{1}{3})^{4}", r"+", r"(\frac{1}{3})^{5}", r"+", r"..."
            )
            .scale(1.5)
            .shift(UP * 8)
        )
        self.play(Write(formula), run_time=1)

        question_mark = Text("?", font_size=100, color=RED).next_to(formula, DOWN * 10)
        self.play(Succession(Create(question_mark), FadeOut(question_mark)))

        # --- Base square & braces --------------------------------------------
        square_1 = Square(side_length=SQUARE_SIDE)
        self.play(Create(square_1), run_time=RUN_T)

        brace_left = BraceBetweenPoints(TL, BL)
        txt1 = MathTex("1").next_to(brace_left, LEFT)
        brace_down = BraceBetweenPoints(BL, BR)
        txt2 = txt1.copy().next_to(brace_down, DOWN)
        self.play(Create(brace_left), Create(txt1), Create(brace_down), Create(txt2), run_time=1)

        # --- Dashed divider lines --------------------------------------------
        line1_1, line1_2 = self._add_dashed_pair(
            [-4, SEGMENT / 2, 0], [4, SEGMENT / 2, 0], DOWN, SEGMENT
        )

        line2_1, line2_2 = self._add_dashed_pair(
            [-4 + SEGMENT, -4 + SEGMENT, 0], [-4 + SEGMENT, 4 - SEGMENT, 0], RIGHT, SEGMENT
        )

        line3_1, line3_2 = self._add_dashed_pair(
            [-4 + SEGMENT, -4 + SEGMENT + SEGMENT2, 0],
            [4 - SEGMENT, -4 + SEGMENT + SEGMENT2, 0],
            UP, SEGMENT2, reverse_order=True
        )

        line4_1, line4_2 = self._add_dashed_pair(
            [-4 + SEGMENT + SEGMENT2, -4 + SEGMENT + SEGMENT2, 0],
            [-4 + SEGMENT + SEGMENT2, -4 + SEGMENT + SEGMENT2 + SEGMENT2, 0],
            RIGHT, SEGMENT2, reverse_order=True
        )

        line_5_1, line_5_2 = self._add_dashed_pair(
            [-4 + SEGMENT + SEGMENT2, -4 + SEGMENT + SEGMENT2 + SEGMENT3 * 2, 0],
            [-4 + SEGMENT + SEGMENT2 * 2, -4 + SEGMENT + SEGMENT2 + SEGMENT3 * 2, 0],
            DOWN, SEGMENT3, reverse_order=True
        )

        # --- Coloured rectangles with series terms ---------------------------
        rect1 = Rectangle(
            width=SQUARE_SIDE, height=SEGMENT,
            fill_color=FILL_COLOR, fill_opacity=FILL_OPACITY, color=FILL_COLOR
        ).shift(SEGMENT * UP)
        formula1 = self._add_formula_rect(rect1, UP, formula[0])

        rect2 = Polygon(
            [-4, -SEGMENT / 2, 0], [-4, SEGMENT / 2, 0],
            [-4 + SEGMENT, SEGMENT / 2, 0], [-4 + SEGMENT, -SEGMENT / 2, 0],
            fill_color=FILL_COLOR, fill_opacity=FILL_OPACITY
        )
        formula2 = self._add_formula_rect(rect2, LEFT, formula[2])

        rect3 = Polygon(
            [-4 + SEGMENT, -4 + SEGMENT + SEGMENT2, 0],
            [4 - SEGMENT, -4 + SEGMENT + SEGMENT2, 0],
            [4 - SEGMENT, -4 + SEGMENT, 0],
            [-4 + SEGMENT, -4 + SEGMENT, 0],
            fill_opacity=FILL_OPACITY, fill_color=FILL_COLOR
        )
        formula3 = self._add_formula_rect(rect3, LEFT, formula[4], term_scale=0.5)

        rect4 = Polygon(
            [-4 + SEGMENT + SEGMENT2, -4 + SEGMENT + SEGMENT2, 0],
            [-4 + SEGMENT + SEGMENT2, -4 + SEGMENT + SEGMENT2 + SEGMENT2, 0],
            [-4 + SEGMENT, -4 + SEGMENT + SEGMENT2 + SEGMENT2, 0],
            [-4 + SEGMENT, -4 + SEGMENT + SEGMENT2, 0],
            fill_color=FILL_COLOR, fill_opacity=FILL_OPACITY
        ).shift(RIGHT * SEGMENT2 * 2)
        formula4 = self._add_formula_rect(rect4, DOWN, formula[6], term_scale=0.5)

        rect5 = Polygon(
            [-4 + SEGMENT + SEGMENT2, -4 + SEGMENT + SEGMENT2 + SEGMENT3 * 2, 0],
            [-4 + SEGMENT + SEGMENT2 * 2, -4 + SEGMENT + SEGMENT2 + SEGMENT3 * 2, 0],
            [-4 + SEGMENT + SEGMENT2 * 2, -4 + SEGMENT + SEGMENT2 + SEGMENT3, 0],
            [-4 + SEGMENT + SEGMENT2, -4 + SEGMENT + SEGMENT2 + SEGMENT3, 0],
            fill_opacity=FILL_OPACITY, fill_color=FILL_COLOR
        )
        formula5 = self._add_formula_rect(rect5, UP, formula[8], term_scale=0.25)

        # --- Central remaining term ------------------------------------------
        formula6 = formula[10].copy()
        self.play(formula6.animate.scale(1 / 4).move_to(ORIGIN))

        # --- Group and rotate ------------------------------------------------
        group1 = VGroup(rect5, rect4, rect3, rect2, rect1)
        group1_1 = VGroup(
            rect5, rect4, rect3, rect2, rect1,
            formula6, formula5, formula4, formula3, formula2, formula1
        )
        group2 = group1.copy().set_fill(PURE_RED)
        self.play(Rotate(group2, PI, about_point=ORIGIN))
        # self.play(group2.animate.rotate(PI, about_point=ORIGIN))

        # --- Clean up construction guides ------------------------------------
        self.remove(
            line1_1, line1_2, line2_2, line2_1, line3_1, line3_2,
            line4_2, line4_1, line_5_2, line_5_1, square_1
        )
        self.remove(brace_down, brace_left, txt2, txt1)
        self.play(group1_1.animate.shift(UL * 3), group2.animate.shift(DR * 3))

        # --- Result labels ---------------------------------------------------
        txt1_1 = MathTex(r"\frac{1}{2}").scale(3).move_to(group1_1.get_center())
        txt2_2 = txt1_1.copy().move_to(group2.get_center())
        self.play(GrowFromCenter(txt1_1), GrowFromCenter(txt2_2))

        self.play(FadeOut(group2), FadeOut(txt2_2), FadeOut(group1_1))

        # --- Final equation --------------------------------------------------
        equal = MathTex("=").scale(3).next_to(txt1_1, LEFT * 2)
        self.play(Write(equal))
        self.play(txt1_1.animate.next_to(equal, RIGHT))

        self.wait(3)
