# Copyright (c) 2026 matthiasmitwittfogel
# Licensed under the Custom Educational License.
# See LICENSE file for details.

"""Express love through mathematical formulas."""

from manim import (
    BLACK, RED, WHITE,
    config, Scene,
    Text, NumberPlane, Axes,
    ParametricFunction, ImplicitFunction, MathTex,
    AddTextLetterByLetter, RemoveTextLetterByLetter,
    Write, Create, Uncreate, FadeOut,
    ORIGIN, UP, DOWN, RIGHT,
    random_bright_color,
)
import numpy as np
import math

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
config.background_color = BLACK


# ---------------------------------------------------------------------------
# Scene
# ---------------------------------------------------------------------------
class MathLove(Scene):
    """Draw a heart-shaped 'LOVE' using parametric and implicit functions."""

    def construct(self):
        # --- Opening text ---------------------------------------------------
        text = Text(
            "How to express love through mathematical formulas?",
            font_size=30,
            fill_opacity=1,
        ).move_to(ORIGIN)
        for letter in text:
            letter.set_color(random_bright_color())
        self.play(AddTextLetterByLetter(text))
        self.play(RemoveTextLetterByLetter(text), run_time=1)

        # --- Coordinate systems ---------------------------------------------
        plane = NumberPlane()
        axes = Axes()
        self.add(axes)
        self.add(plane)

        # --- Curve 1: y = 1/(x+6) -------------------------------------------
        def curve1_fn(x):
            return np.array([x, 1 / (x + 6), 0])

        curve1 = ParametricFunction(
            curve1_fn,
            t_range=np.array([-5.9, -4]),
            color=RED,
        )

        formula1 = MathTex(
            r"y=\frac{1}{x+6}",
            color=WHITE,
            font_size=40,
        ).next_to(curve1, DOWN).shift(UP)
        self.play(Write(formula1))
        self.play(Create(curve1))

        # --- Curve 2: Circle (x+2)^2+(y-2)^2=2 ------------------------------
        curve2 = ImplicitFunction(
            lambda x, y: pow(x + 2, 2) + pow(y - 2, 2) - 2,
            color=RED,
        )
        formula2 = MathTex(
            r"(x+2)^2+(y-2)^2=2",
            color=WHITE,
            font_size=40,
        ).next_to(curve2, DOWN).shift(UP * 3)
        self.play(Write(formula2))
        self.play(Create(curve2))

        # --- Curve 3 & 4: y=|2x-2|+1 (V-shape) -----------------------------
        def curve3_fn(x):
            return np.array([x, -2 * x, 0])

        def curve4_fn(x):
            return np.array([x, 2 * x, 0])

        curve3 = ParametricFunction(
            curve3_fn,
            color=RED,
            t_range=np.array([0, 1]),
        ).shift(UP * 3)
        curve4 = ParametricFunction(
            curve4_fn,
            color=RED,
            t_range=np.array([1, 2]),
        ).shift(DOWN)
        formula3 = MathTex(
            "y=|2x-2|+1",
            color=WHITE,
            font_size=40,
        ).next_to(curve4, DOWN)
        self.play(Write(formula3))
        self.play(Create(curve3))
        self.play(Create(curve4))

        # --- Curve 5: x = -3sin(3|y-2|)+6 -----------------------------------
        curve5 = ImplicitFunction(
            lambda x, y: -3 * math.sin(math.fabs(3 * (y - 2))) - x + 6,
            y_range=[1, 3],
            color=RED,
        )
        formula5 = MathTex(
            r"x=-3sin(3|y-2|+6)",
            color=WHITE,
            font_size=40,
        ).next_to(curve5, DOWN).shift(UP)
        self.play(Write(formula5))
        self.play(Create(curve5))

        # --- Curve 6: y = x^4 - 3 -------------------------------------------
        def curve6_fn(x):
            return np.array([x, x ** 4 - 3, 0])

        curve6 = ImplicitFunction(
            lambda x, y: y - math.pow(x, 4) + 3,
            color=RED,
            y_range=[-3, 0],
        )

        curve6_1 = ParametricFunction(
            curve6_fn,
            color=RED,
            t_range=np.array([-1.2, 1.2]),
        )
        curve6_1_backup = ParametricFunction(
            curve6_fn,
            t_range=np.array([-2, 2]),
            color=WHITE,
        )

        formula6 = MathTex(
            r"y=x^4-3",
            color=WHITE,
            font_size=40,
        ).next_to(curve6, RIGHT)

        self.play(Write(formula6))
        self.play(Create(curve6_1_backup))
        self.add(curve6_1)
        self.play(Uncreate(curve6_1_backup))

        self.remove(formula6, formula5, formula3, formula2, formula1)
        self.play(FadeOut(plane), FadeOut(axes))

        self.wait(3)
