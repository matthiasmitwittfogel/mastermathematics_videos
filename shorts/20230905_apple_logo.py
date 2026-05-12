# Copyright (c) 2026 matthiasmitwittfogel
# Licensed under the Custom Educational License.
# See LICENSE file for details.

"""
Apple Logo drawn with mathematical formulas.

Original animation logic and visual output are preserved.
Code is reorganised for readability, naming consistency,
and reduced duplication.
"""

from manim import (
    BLACK, RED, GREEN, WHITE, BLUE,
    config, Scene,
    ParametricFunction, ImplicitFunction, ArcBetweenPoints,
    MathTex, Text, Dot, DecimalMatrix,
    Circle, Intersection,
    NumberPlane, Axes,
    Create, Uncreate, FadeIn, FadeOut,
    AddTextLetterByLetter, RemoveTextLetterByLetter,
    UP, DOWN, LEFT, RIGHT, ORIGIN,
)
import numpy as np
import math
from sympy import symbols, Eq, solve

# =============================================================================
# Configuration
# =============================================================================
config.background_color = BLACK
config.pixel_width = 720
config.pixel_height = 1280

X_SHIFT = 0
Y_SHIFT = -4


# =============================================================================
# Helpers
# =============================================================================
def _shifted(point):
    """Apply the global scene shift to a 3-D point."""
    return list(np.add(point, [X_SHIFT, Y_SHIFT, 0]))


def _point_label(point, decimals=2):
    """Build a DecimalMatrix label for a coordinate point."""
    return DecimalMatrix(
        [point],
        element_to_mobject_config={"num_decimal_places": decimals},
    ).scale(1)


# =============================================================================
# Curve A — Left parabola:  f(x) = 0.48 (x + 2.03)² + 0.01
# =============================================================================
def left_parabola(x):
    return np.array([
        x + X_SHIFT,
        0.48 * pow(x + 2.03, 2) + 0.01 + Y_SHIFT,
        0,
    ])


curve_a_full = ParametricFunction(
    left_parabola,
    t_range=np.array([-7, 7]),
    color=RED,
)
curve_a_title = MathTex(
    "f(x)=0.49(x+2.03)^{2}+0.01",
    fill_color=GREEN,
).move_to([-2, 11, 0]).scale(1)

point_2 = [-2.03, 0.48 * pow(-2.03 + 2.03, 2) + 0.01, 0]
point_2_label = _point_label(point_2)


# =============================================================================
# Curve B — Cosine wave:  g(x) = (1/3) cos(x) + 0.1577448
# =============================================================================
def cosine_wave(x):
    return np.array([
        x + X_SHIFT,
        1 / 3 * math.cos(x) + 0.1577448 + Y_SHIFT,
        0,
    ])


curve_b_full = ParametricFunction(
    cosine_wave,
    t_range=np.array([-7, 7]),
    color=RED,
)
curve_b_title = MathTex(
    r"g(x)=0.33cos(x)+0.16",
    fill_color=GREEN,
).move_to([0, -3, 0])

curve_b_seg = ParametricFunction(
    cosine_wave,
    t_range=np.array([-2.03, 2.03]),
    color=WHITE,
)

point_3 = [2.03, 1 / 3 * math.cos(2.03) + 0.1577448, 0]
point_3_label = _point_label(point_3)


# =============================================================================
# Curve C — Right parabola:  f(x) = 0.48 (x - 2.03)² + 0.01
# =============================================================================
def right_parabola(x):
    return np.array([
        x + X_SHIFT,
        0.48 * pow(x - 2.03, 2) + 0.01 + Y_SHIFT,
        0,
    ])


curve_c_full = ParametricFunction(
    right_parabola,
    t_range=np.array([-7, 7]),
    color=RED,
)
curve_c_title = MathTex(
    "f(x)=0.49(x-2.03)^{2}+0.01",
    fill_color=GREEN,
).move_to([2, 11, 0]).scale(1)


# =============================================================================
# Curve D — Circle:  (x - 5.58)² + (y - 5.34)² = 6.63
# =============================================================================
curve_d_full = ImplicitFunction(
    lambda x, y: pow(x - 5.58, 2) + pow(y - Y_SHIFT - 5.34, 2) - 6.63,
    x_range=[0, 7],
    color=RED,
)
curve_d_title = MathTex(
    "(x-5.58)^{2}+(y-5.34)^{2}=6.63",
    fill_color=GREEN,
).next_to([5.58 + X_SHIFT, 5.34 + Y_SHIFT, 0], LEFT)


def _solve_point_4():
    """Intersection of Curve C (right parabola) and Curve D (circle)."""
    x, y = symbols("x y", real=True)
    eq1 = Eq(pow(x - 5.58, 2) + pow(y - 5.34, 2), 6.63)
    eq2 = Eq(0.48 * pow(x - 2.03, 2) + 0.01, y)
    results = solve((eq1, eq2), (x, y))

    point_4_x = point_4_y = 0.0
    for p in results:
        if p[0] < 6:
            point_4_x = float(p[0])
            point_4_y = float(p[1])
    return [point_4_x, point_4_y, 0]


point_4 = _solve_point_4()
point_4_label = _point_label(point_4)

curve_c_seg = ParametricFunction(
    right_parabola,
    t_range=np.array([point_3[0], point_4[0]]),
    color=WHITE,
)


# =============================================================================
# Curve E — Circle:  (x - 1.95)² + (y - 5.56)² = 9.14
# =============================================================================
curve_e_full = ImplicitFunction(
    lambda x, y: pow(x - 1.95, 2) + pow(y - Y_SHIFT - 5.56, 2) - 9.14,
    x_range=[-7, 7],
    y_range=[-8, 16],
    color=RED,
)
curve_e_title = MathTex(
    "(x-1.95)^{2}+(y-5.56)^{2}=9.14",
    fill_color=GREEN,
).next_to([1.95 + X_SHIFT, 5.56 + Y_SHIFT, 0], UP * 4)


def _solve_point_5():
    """Intersection of Curve D and Curve E."""
    x, y = symbols("x y", real=True)
    eq1 = Eq(pow(x - 5.58, 2) + pow(y - 5.34, 2), 6.63)
    eq2 = Eq(pow(x - 1.95, 2) + pow(y - 5.56, 2), 9.14)
    result = solve((eq1, eq2), (x, y))

    point = []
    for p in result:
        if p[1] > 5.34:
            point.append(float(p[0]))
            point.append(float(p[1]))
            point.append(0)
    return point


point_5 = _solve_point_5()
point_5_label = _point_label(point_5)

curve_d_seg = ImplicitFunction(
    lambda x, y: pow(x - 5.58, 2) + pow(y - Y_SHIFT - 5.34, 2) - 6.63,
    x_range=[0, 5],
    y_range=[point_4[1] + Y_SHIFT, point_5[1] + Y_SHIFT],
    color=WHITE,
)


# =============================================================================
# Curve F — Sine wave:  h(x) = 0.6 sin(x - 1.4) + 8.7
# =============================================================================
def sine_wave(x):
    return np.array([
        x + X_SHIFT,
        0.6 * math.sin(x - 1.4) + 8.7 + Y_SHIFT,
        0,
    ])


curve_f_full = ParametricFunction(
    sine_wave,
    t_range=np.array([-7, 7]),
    color=RED,
)
curve_f_title = MathTex(
    "h(x)=0.6sin(x-1.4)+8.7",
    fill_color=GREEN,
).next_to([2, 6, 0], UP)

point_6 = [0.85, 0.6 * math.sin(0.85 - 1.4) + 8.7, 0]
point_6_label = _point_label(point_6)

curve_e_seg = ImplicitFunction(
    lambda x, y: pow(x - 1.95, 2) + pow(y - Y_SHIFT - 5.56, 2) - 9.14,
    x_range=[point_6[0], point_5[0]],
    y_range=[Y_SHIFT + 5.56, 14],
    color=WHITE,
)


# =============================================================================
# Curve G — Circle:  (x + 1.95)² + (y - 5.56)² = 9.14
# =============================================================================
curve_g_full = ImplicitFunction(
    lambda x, y: pow(x + 1.95, 2) + pow(y - Y_SHIFT - 5.56, 2) - 9.14,
    x_range=[-7, 7],
    y_range=[-8, 16],
    color=RED,
)
curve_g_title = MathTex(
    "(x+1.95)^{2}+(y-5.56)^{2}=9.14",
    fill_color=GREEN,
).next_to([-1.95 + X_SHIFT, 5.56 + Y_SHIFT, 0], UP * 4)

point_7_x = math.sqrt(9.14 - (8.577 - 5.58) ** 2) + 0.18 - 1.95
point_7 = [point_7_x, 0.6 * math.sin(point_7_x - 1.4) + 8.7, 0]
point_7_label = _point_label(point_7)

curve_f_seg = ParametricFunction(
    sine_wave,
    t_range=np.array([point_7[0], point_6[0]]),
    color=WHITE,
)


# =============================================================================
# Curve H — Circle:  (x - 0.16)² + (y - 5.14)² = 26.68
# =============================================================================
curve_h_full = ImplicitFunction(
    lambda x, y: pow(x - 0.16, 2) + pow(y - Y_SHIFT - 5.14, 2) - 26.68,
    x_range=[-7, 7],
    y_range=[-8, 16],
    color=RED,
)
curve_h_title = MathTex(
    "(x-0.16)^{2}+(y-5.14)^{2}=26.68",
    fill_color=GREEN,
).next_to([0.16, 5.14, 0], UP)

point_8 = [-4.9, math.sqrt(9.14 - (-4.9 + 1.95) ** 2) + 5.56, 0]
point_8_label = _point_label(point_8)

curve_g_seg = ArcBetweenPoints(
    start=_shifted(point_7),
    end=_shifted(point_8),
    stroke_color=WHITE,
    radius=math.sqrt(9.14),
)

point_9 = [-point_4[0], -math.sqrt(26.68 - (-point_4[0] - 0.16) ** 2) + 5.14, 0]
point_9_label = _point_label(point_9)

curve_h_seg = ImplicitFunction(
    lambda x, y: pow(x - 0.16, 2) + pow(y - Y_SHIFT - 5.14, 2) - 26.68,
    x_range=[-7, 0],
    y_range=[point_9[1] + Y_SHIFT, point_8[1] + Y_SHIFT],
    color=WHITE,
)


# =============================================================================
# Final Curve A segment (closes the apple outline)
# =============================================================================
curve_a_seg = ParametricFunction(
    left_parabola,
    t_range=np.array([point_9[0], point_2[0]]),
    color=WHITE,
)


# =============================================================================
# Scene
# =============================================================================
class AppleLogo(Scene):
    """Draw the Apple logo using parametric and implicit functions."""

    # ── Opening titles ───────────────────────────────────────────────────────
    txt_list = [
        Text("How to draw", font_size=80, fill_opacity=1),
        Text("The Apple logo", font_size=80, fill_opacity=1, color=RED),
        Text("Using", font_size=80, fill_opacity=1),
        Text("Mathematical Formulas", font_size=72, fill_opacity=1, color=BLUE),
    ]

    # ── Coordinate systems ───────────────────────────────────────────────────
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
    ).add_coordinates()

    def show_beginning_text(self):
        for txt in self.txt_list:
            txt.set_max_width(13)
        self.play(AddTextLetterByLetter(self.txt_list[0].move_to(UP * 4)))
        self.play(AddTextLetterByLetter(self.txt_list[1].move_to(UP * 2)))
        self.play(AddTextLetterByLetter(self.txt_list[2].move_to(ORIGIN)))
        self.play(AddTextLetterByLetter(self.txt_list[3].move_to(DOWN * 2)))

    def remove_beginning_text(self):
        self.play(RemoveTextLetterByLetter(self.txt_list[0]), run_time=0.2)
        self.play(RemoveTextLetterByLetter(self.txt_list[1]), run_time=0.2)
        self.play(RemoveTextLetterByLetter(self.txt_list[2]), run_time=0.2)
        self.play(RemoveTextLetterByLetter(self.txt_list[3]), run_time=0.2)

    def draw_leaf(self):
        """Draw the leaf from the intersection of two circles."""
        circle_small_1 = Circle(
            radius=math.sqrt(6.35),
            color=RED,
        ).move_to([2.31, 8.77 + Y_SHIFT, 0])
        circle_small_1_title = MathTex(
            "(x-2.3)^{2}+(y-8.77)^2=6.35",
            fill_color=GREEN,
        ).move_to(circle_small_1.get_center()).scale(1)

        circle_small_2 = Circle(
            radius=math.sqrt(5.58),
            color=RED,
        ).move_to([-0.23, 11.02 + Y_SHIFT, 0])
        circle_small_2_title = MathTex(
            "(x+0.3)^{2}+(y-11.01)^{2}=5.58",
            fill_color=GREEN,
        ).move_to(circle_small_2.get_center()).scale(1)

        intersect_small_12 = Intersection(
            circle_small_1, circle_small_2, color=WHITE,
        )

        self.add(circle_small_1_title)
        self.play(Create(circle_small_1))
        self.add(circle_small_2_title)
        self.play(Create(circle_small_2))

        self.play(Create(intersect_small_12))
        self.remove(circle_small_1_title)
        self.remove(circle_small_2_title)
        self.play(Uncreate(circle_small_1))
        self.play(Uncreate(circle_small_2))

    def construct(self):
        # ── Opening titles ───────────────────────────────────────────────────
        self.show_beginning_text()
        self.remove_beginning_text()

        # ── Coordinate systems ───────────────────────────────────────────────
        self.play(FadeIn(self.plane))
        self.play(FadeIn(self.axes))

        # ── Curve A (left parabola) ──────────────────────────────────────────
        self.add(curve_a_title)
        self.play(Create(curve_a_full), run_time=2)
        dot_2 = Dot(_shifted(point_2), color=GREEN)
        point_2_label.next_to(dot_2, DOWN)
        self.add(point_2_label)
        self.add(dot_2)
        self.remove(curve_a_title, dot_2, point_2_label)

        # ── Curve B (cosine wave) ────────────────────────────────────────────
        self.add(curve_b_title)
        self.play(Create(curve_b_full))
        dot_3 = Dot(_shifted(point_3), color=GREEN)
        point_3_label.next_to(dot_3, DOWN)
        self.add(dot_3, point_3_label)
        self.play(Create(curve_b_seg))
        self.remove(dot_3, curve_b_title, point_3_label)
        self.play(Uncreate(curve_b_full))

        # ── Curve C (right parabola) & Point 4 ───────────────────────────────
        self.add(curve_c_title)
        self.play(Create(curve_c_full))
        self.remove(curve_c_title)
        dot_4 = Dot(_shifted(point_4), color=GREEN)
        point_4_label.next_to(dot_4, LEFT)
        self.add(dot_4, point_4_label)
        self.play(Create(curve_c_seg))
        self.remove(dot_4, curve_d_title, point_4_label)
        self.play(Uncreate(curve_c_full))

        # ── Curve D (circle) & Curve E (circle) ──────────────────────────────
        self.add(curve_d_title)
        self.play(Create(curve_d_full))
        self.add(curve_e_title)
        self.play(Create(curve_e_full), run_time=2)
        dot_5 = Dot(_shifted(point_5), color=GREEN)
        point_5_label.next_to(dot_5, UP)
        self.add(point_5_label, dot_5)
        self.play(Create(curve_d_seg))
        self.remove(curve_d_title, dot_5, point_5_label)
        self.play(Uncreate(curve_d_full))

        # ── Curve F (sine wave) & Curve E segment ────────────────────────────
        self.add(curve_f_title)
        self.play(Create(curve_f_full))
        dot_6 = Dot(_shifted(point_6), color=GREEN)
        point_6_label.next_to(dot_6, UP)
        self.add(dot_6, point_6_label)
        self.play(Create(curve_e_seg))
        self.remove(curve_e_title)
        self.play(Uncreate(curve_e_full))
        self.remove(point_6_label, dot_6)

        # ── Curve G (circle) & Curve F segment ───────────────────────────────
        self.add(curve_g_title)
        self.play(Create(curve_g_full))
        dot_7 = Dot(_shifted(point_7), color=GREEN)
        point_7_label.next_to(dot_7, UP)
        self.add(dot_7, point_7_label)
        self.play(Create(curve_f_seg))
        self.remove(curve_f_title)
        self.play(Uncreate(curve_f_full))
        self.remove(point_7_label, dot_7)
        self.play(Uncreate(curve_f_full))
        self.remove(curve_f_title)

        # ── Curve H (circle) & Curve G segment ───────────────────────────────
        self.add(curve_h_title)
        self.play(Create(curve_h_full))
        dot_8 = Dot(_shifted(point_8), color=GREEN)
        self.add(dot_8)
        point_8_label.next_to(dot_8, UP)
        self.add(point_8_label)
        self.play(Create(curve_g_seg))
        self.remove(curve_g_title)
        self.play(Uncreate(curve_g_full))
        self.remove(point_8_label, dot_8)

        # ── Point 9 & Curve H segment ────────────────────────────────────────
        dot_9 = Dot(_shifted(point_9), color=GREEN)
        point_9_label.next_to(dot_9, RIGHT)
        self.add(dot_9, point_9_label)
        self.play(Create(curve_h_seg))
        self.play(Uncreate(curve_h_full))
        self.remove(curve_h_title)
        self.remove(point_9_label, dot_9)

        # ── Final Curve A segment (closes the outline) ───────────────────────
        self.play(Create(curve_a_seg))
        self.play(Uncreate(curve_a_full))

        # ── Leaf ─────────────────────────────────────────────────────────────
        self.draw_leaf()

        # ── Cleanup ──────────────────────────────────────────────────────────
        self.play(FadeOut(self.axes))
        self.play(FadeOut(self.plane))

        self.wait(2)
