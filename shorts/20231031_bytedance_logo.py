# Copyright (c) 2026 matthiasmitwittfogel
# Licensed under the Custom Educational License.
# See LICENSE file for details.

"""Scene that constructs the TikTok logo from mathematical formulas."""

import math

import numpy as np
from manim import (
    BLACK,
    BLUE,
    Axes,
    Circle,
    Create,
    DashedLine,
    Difference,
    DOWN,
    FadeIn,
    FadeOut,
    GrowFromEdge,
    Intersection,
    LEFT,
    Line,
    MathTex,
    NumberPlane,
    ORIGIN,
    PI,
    PURE_RED,
    Rectangle,
    RED,
    RemoveTextLetterByLetter,
    RIGHT,
    Scene,
    Square,
    Text,
    Uncreate,
    Unwrite,
    UP,
    VGroup,
    WHITE,
    Write,
    YELLOW,
    AddTextLetterByLetter,
    AnnularSector,
    config,
)


# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
config.background_color = BLACK
config.pixel_width = 2160
config.pixel_height = 3840


class ByteDanceLogo(Scene):
    """Draw the TikTok logo using mathematical formulas."""

    # Timing
    RUN_TIME = 0.5
    UNWRITE_RUN_TIME = 0.1
    UNCREATE_RUN_TIME = 1.5
    FADEOUT_RUN_TIME = 0.2

    # Geometry constants
    CIRCLE1_CENTER = 4 * DOWN + 3 * LEFT
    CIRCLE3_CENTER = UP * 4 + RIGHT * 4
    LINE_Y_EXTENT = 17
    LINE_HORIZ_Y = 4
    RECT1_WIDTH = 1.2
    RECT1_HEIGHT = 4
    RECT1_SHIFT = np.array([-1.6, -2, 0])
    RECT2_WIDTH = 2
    RECT2_HEIGHT = 8
    SHIFT_A = RIGHT * 2 + UP
    SHIFT_B = LEFT * 0.6 + UP * 0.6
    SECTOR_INNER = 2
    SECTOR_OUTER = 4
    SECTOR2_INNER = 3
    SECTOR2_OUTER = 5
    SECTOR2_ANGLE = PI / 2
    SECTOR2_START_ANGLE = PI

    # Formula font sizes
    FORMULA_LARGE = 65
    FORMULA_SMALL = 50

    txt_list = [
        Text("How to use", font_size=80, fill_opacity=1),
        Text("math formulas", font_size=80, fill_opacity=1, color=RED),
        Text("to draw", font_size=80, fill_opacity=1),
        Text("TikTok logo", font_size=96, fill_opacity=1, color=BLUE),
    ]

    plane = NumberPlane(
        x_range=[-7, 7, 2],
        y_range=(-8, 16, 2),
        x_length=14,
        y_length=24,
    )

    axes = Axes(
        x_range=[-7, 7, 2],
        y_range=(-8, 16, 2),
        x_length=14,
        y_length=24,
        x_axis_config={"unit_size": 1},
        y_axis_config={"unit_size": 1},
        color=YELLOW,
    ).add_coordinates()

    def show_beginning_text(self):
        """Type out the opening title cards."""
        self.play(AddTextLetterByLetter(self.txt_list[0].move_to(UP * 4)))
        self.play(AddTextLetterByLetter(self.txt_list[1].move_to(UP * 2)))
        self.play(AddTextLetterByLetter(self.txt_list[2].move_to(ORIGIN)))
        self.play(AddTextLetterByLetter(self.txt_list[3].move_to(DOWN * 2)))

    def remove_beginning_text(self):
        """Erase the opening title cards."""
        self.play(RemoveTextLetterByLetter(self.txt_list[0]), run_time=0.2)
        self.play(RemoveTextLetterByLetter(self.txt_list[1]), run_time=0.2)
        self.play(RemoveTextLetterByLetter(self.txt_list[2]), run_time=0.2)
        self.play(RemoveTextLetterByLetter(self.txt_list[3]), run_time=0.2)

    def _write(self, mobject):
        """Helper: Write an object with the standard run time."""
        self.play(Write(mobject), run_time=self.RUN_TIME)

    def _create(self, mobject):
        """Helper: Create an object."""
        self.play(Create(mobject))

    def _unwrite(self, mobject):
        """Helper: Unwrite an object quickly."""
        self.play(Unwrite(mobject), run_time=self.UNWRITE_RUN_TIME)

    def _add_line(self, start, end, shift=None):
        """Helper: create a white line, optionally shift it, add it, and return it."""
        line = Line(start, end, color=WHITE)
        if shift is not None:
            line.shift(shift)
        self.add(line)
        return line

    def _white_intersection(self, mobject_a, mobject_b):
        """Helper: Intersection with white fill."""
        return Intersection(
            mobject_a,
            mobject_b,
            fill_color=WHITE,
            color=WHITE,
            fill_opacity=1,
        )

    def construct(self):
        self.show_beginning_text()
        self.remove_beginning_text()

        # --- Grid & axes --------------------------------------------------------
        self.play(FadeIn(self.plane), run_time=self.RUN_TIME)
        self.play(FadeIn(self.axes), run_time=self.RUN_TIME)

        # --- Left circles & formulas --------------------------------------------
        formula1 = MathTex(
            r"(x+3)^2+y^2=16", font_size=self.FORMULA_LARGE, color=YELLOW
        ).move_to(UP * 0.5 + 3 * LEFT)
        self._write(formula1)

        circle1 = Circle(radius=4, color=WHITE).move_to(self.CIRCLE1_CENTER)
        self._create(circle1)

        circle2 = Circle(radius=2, color=WHITE).move_to(self.CIRCLE1_CENTER)
        formula2 = MathTex(
            r"(x+3)^2+y^2=4", font_size=self.FORMULA_LARGE, color=YELLOW
        ).next_to(circle2, UP)
        self._write(formula2)
        self._create(circle2)

        # --- Vertical dashed lines -----------------------------------------------
        line1 = DashedLine(
            start=LEFT * 1 + DOWN * self.LINE_Y_EXTENT,
            end=LEFT * 1 + UP * self.LINE_Y_EXTENT,
            color=WHITE,
        )
        formula3 = MathTex(
            "x=-1", font_size=self.FORMULA_LARGE, color=YELLOW
        ).next_to(line1, LEFT * 2).shift(UP * 6)
        self._write(formula3)
        self._create(line1)

        line2 = DashedLine(
            start=DOWN * self.LINE_Y_EXTENT + RIGHT,
            end=UP * self.LINE_Y_EXTENT + RIGHT,
            color=WHITE,
        )
        formula4 = MathTex(
            "x=1", font_size=self.FORMULA_LARGE, color=YELLOW
        ).next_to(line2, RIGHT * 2).shift(UP * 8)
        self._write(formula4)
        self._create(line2)

        line3 = DashedLine(
            start=LEFT * 10 + UP * self.LINE_HORIZ_Y,
            end=RIGHT * 10 + UP * self.LINE_HORIZ_Y,
            color=WHITE,
        )
        formula5 = MathTex(
            "y=8", font_size=self.FORMULA_LARGE, color=YELLOW
        ).next_to(line3, DOWN)
        self._write(formula5)
        self._create(line3)

        # --- Unwrite left formulas -----------------------------------------------
        self.play(
            Unwrite(formula5),
            Unwrite(formula4),
            Unwrite(formula3),
            Unwrite(formula2),
            Unwrite(formula1),
        )

        # --- Right circles & formulas --------------------------------------------
        circle3 = Circle(radius=5, color=WHITE).move_to(self.CIRCLE3_CENTER)
        formula6 = MathTex(
            r"(x-4)^2+(y-8)^2=25",
            font_size=self.FORMULA_SMALL,
            color=YELLOW,
        ).next_to(circle3, UP).shift(LEFT)
        self._write(formula6)
        self._create(circle3)
        self._unwrite(formula6)

        circle4 = Circle(radius=3, color=WHITE).move_to(self.CIRCLE3_CENTER)
        formula7 = MathTex(
            r"(x-4)^2+(y-8)^2=9",
            font_size=self.FORMULA_SMALL,
            color=YELLOW,
        ).next_to(circle4, UP).shift(LEFT)
        self._write(formula7)
        self._create(circle4)
        self._unwrite(formula7)

        # --- Additional dashed lines ---------------------------------------------
        line4 = DashedLine(
            start=DOWN * self.LINE_Y_EXTENT + RIGHT * 4,
            end=UP * self.LINE_Y_EXTENT + RIGHT * 4,
            color=WHITE,
        )
        formula8 = MathTex(
            r"x=4", font_size=self.FORMULA_SMALL, color=YELLOW
        ).next_to(line4, RIGHT).shift(DOWN * 5)
        self._write(formula8)
        self._create(line4)

        line5 = DashedLine(
            start=DOWN * self.LINE_Y_EXTENT + LEFT * 2.2,
            end=UP * self.LINE_Y_EXTENT + LEFT * 2.2,
            color=WHITE,
        )
        formula9 = MathTex(
            r"x=-2.2", font_size=self.FORMULA_SMALL, color=YELLOW
        ).next_to(line5, LEFT).shift(DOWN * 5)
        self._write(formula9)
        self._create(line5)

        # --- Line segments -------------------------------------------------------
        line5_part = self._add_line(
            [-2.2, math.sqrt(4 - math.pow(-2.2 + 3, 2)), 0],
            [-2.2, math.sqrt(16 - math.pow(-2.2 + 3, 2)), 0],
            shift=DOWN * 4,
        )
        line1_part = self._add_line([-1, -4, 0], [-1, 4, 0])
        line2_part = self._add_line([1, -4, 0], [1, 4, 0])
        line3_part = self._add_line([-1, 4, 0], [1, 4, 0])
        line4_part = self._add_line([4, 1, 0], [4, -1, 0])

        # --- Remove dashed construction lines ------------------------------------
        self.play(
            Uncreate(line5),
            Uncreate(line1),
            Uncreate(line2),
            Uncreate(line3),
            Uncreate(line4),
            run_time=self.UNCREATE_RUN_TIME,
        )
        self.remove(formula8, formula9)

        # --- Red left part -------------------------------------------------------
        circle1_ = circle1.copy().set_color(PURE_RED)
        circle2_ = circle2.copy().set_color(PURE_RED)
        intersection1 = Difference(
            circle1_,
            circle2_,
            fill_color=PURE_RED,
            fill_opacity=1,
            color=PURE_RED,
            stroke_color=PURE_RED,
        )
        rect1 = Rectangle(
            width=self.RECT1_WIDTH,
            height=self.RECT1_HEIGHT,
            fill_color=PURE_RED,
            color=PURE_RED,
            fill_opacity=1,
        ).shift(self.RECT1_SHIFT)
        diff1 = Difference(
            intersection1,
            rect1,
            color=PURE_RED,
            fill_color=PURE_RED,
            fill_opacity=1,
        )
        self.play(FadeIn(diff1), run_time=2)

        rect2 = Rectangle(
            width=self.RECT2_WIDTH,
            height=self.RECT2_HEIGHT,
            fill_color=PURE_RED,
            color=PURE_RED,
            fill_opacity=1,
        )
        self.play(GrowFromEdge(rect2, UP), run_time=1)

        self.remove(circle1, circle2)

        # --- Red right part ------------------------------------------------------
        intersection2 = Difference(
            circle3,
            circle4,
            fill_color=PURE_RED,
            fill_opacity=1,
            color=PURE_RED,
        )
        square = Square(side_length=5, fill_color=WHITE, fill_opacity=1).shift(
            RIGHT * 1.5 + UP * 1.5
        )
        diff2 = Intersection(
            intersection2,
            square,
            fill_color=PURE_RED,
            color=PURE_RED,
            fill_opacity=1,
        )
        self.play(FadeIn(diff2))
        self.play(Uncreate(circle4), Uncreate(circle3), run_time=self.RUN_TIME)

        self.remove(line4_part, line3_part, line5_part, line2_part, line1_part)

        # --- Compose logo --------------------------------------------------------
        group = VGroup(diff2, diff1, rect2).set_color(PURE_RED)

        rect_a = Rectangle(width=2, height=8).shift(self.SHIFT_A)
        rect_b = rect_a.copy().shift(self.SHIFT_B)
        intersect_1 = self._white_intersection(rect_b, rect_a)

        sector = AnnularSector(
            inner_radius=self.SECTOR_INNER,
            outer_radius=self.SECTOR_OUTER,
            angle=2 * PI,
            color=WHITE,
            fill_opacity=1,
        ).move_to(self.CIRCLE1_CENTER)
        rect_c = Rectangle(
            width=self.RECT1_WIDTH,
            height=self.RECT1_HEIGHT,
            fill_color=WHITE,
            color=WHITE,
            fill_opacity=1,
        ).shift(self.RECT1_SHIFT)
        diff_a = Difference(
            sector,
            rect_c,
            fill_color=WHITE,
            color=WHITE,
            fill_opacity=1,
        ).shift(self.SHIFT_A)
        diff_b = diff_a.copy().shift(self.SHIFT_B)
        inter_a_b = self._white_intersection(diff_a, diff_b)

        sector_1 = AnnularSector(
            inner_radius=self.SECTOR2_INNER,
            outer_radius=self.SECTOR2_OUTER,
            angle=self.SECTOR2_ANGLE,
            start_angle=self.SECTOR2_START_ANGLE,
            color=WHITE,
            fill_opacity=1,
        )
        sector_2 = sector_1.copy().shift(self.SHIFT_B)
        inter_c_d = self._white_intersection(sector_2, sector_1).shift(
            UP * 5 + RIGHT * 6
        )

        blue = group.copy().set_color(r"#00FFFF")

        inter = Intersection(
            group, blue, color=WHITE, fill_opacity=1, fill_color=WHITE
        )
        self.add(inter)

        self.play(blue.animate.shift(self.SHIFT_A).shift(self.SHIFT_B))

        self.play(group.animate.shift(self.SHIFT_A))

        self.play(FadeIn(intersect_1), FadeIn(inter_a_b), FadeIn(inter_c_d))

        self.play(FadeOut(self.axes), run_time=self.FADEOUT_RUN_TIME)
        self.play(FadeOut(self.plane), run_time=self.FADEOUT_RUN_TIME)

        self.wait(3)
