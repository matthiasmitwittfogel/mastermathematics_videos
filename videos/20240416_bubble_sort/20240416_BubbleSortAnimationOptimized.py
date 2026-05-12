# Copyright (c) 2026 matthiasmitwittfogel
# Licensed under the Custom Educational License.
# See LICENSE file for details.

"""Optimized bubble sort animation with early termination."""

from manim import (
    BLACK, GREEN, BLUE, PURPLE, RED,
    config, Scene,
    Text, Rectangle, VGroup, BraceBetweenPoints,
    FadeIn, GrowFromCenter,
)
import numpy as np

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
config.pixel_width = 360
config.pixel_height = 640

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
BAR_HEIGHT = 1.0
BAR_SPACING = 1.5
START_Y = 6.5
START_X = -4

_SHIFT_DOWN = np.array([0, -BAR_SPACING, 0])
_SHIFT_UP = np.array([0, BAR_SPACING, 0])


# ---------------------------------------------------------------------------
# Scene
# ---------------------------------------------------------------------------
class BubbleSort(Scene):
    """Visualize the optimized Bubble Sort algorithm with animated bar swapping."""

    def construct(self):
        # --- Title ----------------------------------------------------------
        title = Text("Bubble Sort(optimized)", font_size=64).move_to([0, 9, 0])
        bg = Rectangle(
            width=title.width + 0.6,
            height=1.8,
            stroke_color=BLACK,
            fill_color=GREEN,
            fill_opacity=0.4,
        ).move_to([0, 9, 0])
        self.add(title, bg)

        # --- Build bars -----------------------------------------------------
        values = [10, 8, 2, 9, 1, 6, 3, 5, 7, 4]
        groups = []
        y_pos = START_Y
        for val in values:
            bar = Rectangle(
                width=val,
                height=BAR_HEIGHT,
                fill_color=BLUE,
                fill_opacity=0.4,
            ).move_to([START_X + val / 2.0, y_pos, 0])
            label = Text(str(val)).move_to([START_X + val / 2.0, y_pos, 0])
            groups.append(VGroup(bar, label))
            y_pos -= BAR_SPACING

        self.add(*groups)

        # --- Brace ----------------------------------------------------------
        brace = BraceBetweenPoints(
            [START_X, 7, 0],
            [START_X, 4.5, 0],
            color=PURPLE,
            sharpness=2.0,
            stroke_width=10,
        )

        # --- Loop 1 ---------------------------------------------------------
        txt = Text("Loop 1", font_size=200, color=RED, stroke_width=5)
        self.play(FadeIn(brace), GrowFromCenter(txt))
        self.remove(txt)

        self.play(groups[values.index(10)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(8)].animate.shift(_SHIFT_UP))

        # --- Loop 2 ---------------------------------------------------------
        txt = Text("Loop 2", font_size=200, color=RED, stroke_width=5)
        self.play(GrowFromCenter(txt))
        self.remove(txt)
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(groups[values.index(10)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(2)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_UP))
        self.play(groups[values.index(8)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(2)].animate.shift(_SHIFT_UP))

        # --- Loop 3 ---------------------------------------------------------
        txt = Text("Loop 3", font_size=200, color=RED, stroke_width=5)
        self.play(GrowFromCenter(txt))
        self.remove(txt)
        self.play(brace.animate.shift(np.array([0, -BAR_SPACING * 2, 0])))
        self.play(groups[values.index(10)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(9)].animate.shift(_SHIFT_UP))

        # --- Loop 4 ---------------------------------------------------------
        txt = Text("Loop 4", font_size=200, color=RED, stroke_width=5)
        self.play(GrowFromCenter(txt))
        self.remove(txt)
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(groups[values.index(10)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(1)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_UP))
        self.play(groups[values.index(9)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(1)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_UP))
        self.play(groups[values.index(8)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(1)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_UP))
        self.play(groups[values.index(2)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(1)].animate.shift(_SHIFT_UP))

        # --- Loop 5 ---------------------------------------------------------
        txt = Text("Loop 5", font_size=200, color=RED, stroke_width=5)
        self.play(GrowFromCenter(txt))
        self.remove(txt)
        self.play(brace.animate.shift(np.array([0, -BAR_SPACING * 4, 0])))
        self.play(groups[values.index(10)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(6)].animate.shift(_SHIFT_UP))

        self.play(brace.animate.shift(_SHIFT_UP))
        self.play(groups[values.index(9)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(6)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_UP))
        self.play(groups[values.index(8)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(6)].animate.shift(_SHIFT_UP))

        # --- Loop 6 ---------------------------------------------------------
        txt = Text("Loop 6", font_size=200, color=RED, stroke_width=5)
        self.play(GrowFromCenter(txt))
        self.remove(txt)
        self.play(brace.animate.shift(np.array([0, -BAR_SPACING * 3, 0])))
        self.play(groups[values.index(10)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(3)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_UP))
        self.play(groups[values.index(9)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(3)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_UP))
        self.play(groups[values.index(8)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(3)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_UP))
        self.play(groups[values.index(6)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(3)].animate.shift(_SHIFT_UP))

        # --- Loop 7 ---------------------------------------------------------
        txt = Text("Loop 7", font_size=200, color=RED, stroke_width=5)
        self.play(GrowFromCenter(txt))
        self.remove(txt)
        self.play(brace.animate.shift(np.array([0, -BAR_SPACING * 4, 0])))
        self.play(groups[values.index(10)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(5)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_UP))
        self.play(groups[values.index(9)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(5)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_UP))
        self.play(groups[values.index(8)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(5)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_UP))
        self.play(groups[values.index(6)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(5)].animate.shift(_SHIFT_UP))

        # --- Loop 8 ---------------------------------------------------------
        txt = Text("Loop 8", font_size=200, color=RED, stroke_width=5)
        self.play(GrowFromCenter(txt))
        self.remove(txt)
        self.play(brace.animate.shift(np.array([0, -BAR_SPACING * 4, 0])))
        self.play(groups[values.index(10)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(7)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_UP))
        self.play(groups[values.index(9)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(7)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_UP))
        self.play(groups[values.index(8)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(7)].animate.shift(_SHIFT_UP))

        # --- Loop 9 ---------------------------------------------------------
        txt = Text("Loop 9", font_size=200, color=RED, stroke_width=5)
        self.play(GrowFromCenter(txt))
        self.remove(txt)
        self.play(brace.animate.shift(np.array([0, -BAR_SPACING * 3, 0])))
        self.play(groups[values.index(10)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(4)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_UP))
        self.play(groups[values.index(9)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(4)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_UP))
        self.play(groups[values.index(8)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(4)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_UP))
        self.play(groups[values.index(7)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(4)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_UP))
        self.play(groups[values.index(6)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(4)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_UP))
        self.play(groups[values.index(5)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(4)].animate.shift(_SHIFT_UP))

        self.remove(brace)

        # --- Done -----------------------------------------------------------
        txt = Text("Done", font_size=150, color=RED, stroke_width=5)
        self.play(GrowFromCenter(txt))
        self.remove(txt)
        self.wait(3)
