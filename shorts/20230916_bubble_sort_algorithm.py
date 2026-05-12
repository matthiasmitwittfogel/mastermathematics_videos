# Copyright (c) 2026 matthiasmitwittfogel
# Licensed under the Custom Educational License.
# See LICENSE file for details.

"""Bubble Sort algorithm visualization."""

from manim import (
    BLACK, GREEN, BLUE, PURPLE, RED,
    config, Scene,
    Text, Rectangle, VGroup, BraceBetweenPoints,
    FadeIn, GrowFromCenter,
)
import numpy as np

# =============================================================================
# Configuration
# =============================================================================
config.pixel_width = 360
config.pixel_height = 640

# =============================================================================
# Constants
# =============================================================================
BAR_HEIGHT = 1.0
BAR_SPACING = 1.5
START_Y = 6.5
START_X = -4

_SHIFT_DOWN = np.array([0, -BAR_SPACING, 0])
_SHIFT_UP = np.array([0, BAR_SPACING, 0])


# =============================================================================
# Scene
# =============================================================================
class BubbleSort(Scene):
    """Visualize the Bubble Sort algorithm with animated bar swapping."""

    def construct(self):
        # ── Title ────────────────────────────────────────────────────────────
        title = Text("Bubble Sort Algorithm", font_size=64).move_to([0, 9, 0])
        bg = Rectangle(
            width=title.width + 0.6,
            height=1.8,
            stroke_color=BLACK,
            fill_color=GREEN,
            fill_opacity=0.4,
        ).move_to([0, 9, 0])
        self.add(title, bg)

        # ── Build bars ───────────────────────────────────────────────────────
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

        # ── Brace ────────────────────────────────────────────────────────────
        brace = BraceBetweenPoints(
            [START_X, 7, 0],
            [START_X, 4.5, 0],
            color=PURPLE,
            sharpness=2.0,
            stroke_width=10,
        )

        # ── First Round ──────────────────────────────────────────────────────
        txt = Text("First Round", font_size=200, color=RED, stroke_width=5)
        self.play(FadeIn(brace), GrowFromCenter(txt))
        self.remove(txt)

        self.play(groups[values.index(10)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(8)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(groups[values.index(10)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(2)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(groups[values.index(10)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(9)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(groups[values.index(10)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(1)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(groups[values.index(10)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(6)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(groups[values.index(10)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(3)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(groups[values.index(10)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(5)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(groups[values.index(10)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(7)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(groups[values.index(10)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(4)].animate.shift(_SHIFT_UP))

        # ── Second Round ─────────────────────────────────────────────────────
        txt = Text("Second Round", font_size=200, color=RED, stroke_width=5)
        self.play(GrowFromCenter(txt))
        self.remove(txt)
        self.play(brace.animate.shift(np.array([0, BAR_SPACING * 8, 0])))
        self.play(groups[values.index(8)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(2)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(groups[values.index(9)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(1)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(groups[values.index(9)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(6)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(groups[values.index(9)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(3)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(groups[values.index(9)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(5)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(groups[values.index(9)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(7)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(groups[values.index(9)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(4)].animate.shift(_SHIFT_UP))

        # ── Third Round ──────────────────────────────────────────────────────
        txt = Text("Third Round", font_size=200, color=RED, stroke_width=5)
        self.play(GrowFromCenter(txt))
        self.remove(txt)
        self.play(brace.animate.shift(np.array([0, BAR_SPACING * 7, 0])))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(groups[values.index(8)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(1)].animate.shift(_SHIFT_UP))

        for val in [6, 3, 5, 7, 4]:
            self.play(brace.animate.shift(_SHIFT_DOWN))
            self.play(groups[values.index(8)].animate.shift(_SHIFT_DOWN),
                      groups[values.index(val)].animate.shift(_SHIFT_UP))

        # ── Forth Round ──────────────────────────────────────────────────────
        txt = Text("Forth Round", font_size=200, color=RED, stroke_width=5)
        self.play(GrowFromCenter(txt))
        self.remove(txt)
        self.play(brace.animate.shift(np.array([0, BAR_SPACING * 6, 0])))
        self.play(groups[values.index(2)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(1)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(groups[values.index(6)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(3)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(groups[values.index(6)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(5)].animate.shift(_SHIFT_UP))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(groups[values.index(7)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(4)].animate.shift(_SHIFT_UP))

        # ── Fifth Round ──────────────────────────────────────────────────────
        txt = Text("Fifth Round", font_size=200, color=RED, stroke_width=5)
        self.play(GrowFromCenter(txt))
        self.remove(txt)
        self.play(brace.animate.shift(np.array([0, BAR_SPACING * 5, 0])))

        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(brace.animate.shift(_SHIFT_DOWN))

        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(groups[values.index(6)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(4)].animate.shift(_SHIFT_UP))

        # ── Sixth Round ──────────────────────────────────────────────────────
        txt = Text("Sixth Round", font_size=200, color=RED, stroke_width=5)
        self.play(GrowFromCenter(txt))
        self.remove(txt)
        self.play(brace.animate.shift(np.array([0, BAR_SPACING * 4, 0])))

        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(groups[values.index(5)].animate.shift(_SHIFT_DOWN),
                  groups[values.index(4)].animate.shift(_SHIFT_UP))

        # ── Seventh Round ────────────────────────────────────────────────────
        txt = Text("Seventh Round", font_size=200, color=RED, stroke_width=5)
        self.play(GrowFromCenter(txt))
        self.remove(txt)
        self.play(brace.animate.shift(np.array([0, BAR_SPACING * 3, 0])))
        self.play(brace.animate.shift(_SHIFT_DOWN))
        self.play(brace.animate.shift(_SHIFT_DOWN))

        # ── Eighth Round ─────────────────────────────────────────────────────
        txt = Text("Eighth Round", font_size=200, color=RED, stroke_width=5)
        self.play(GrowFromCenter(txt))
        self.remove(txt)
        self.play(brace.animate.shift(np.array([0, BAR_SPACING * 2, 0])))
        self.play(brace.animate.shift(_SHIFT_DOWN))

        # ── Ninth Round ──────────────────────────────────────────────────────
        txt = Text("Ninth Round", font_size=200, color=RED, stroke_width=5)
        self.play(GrowFromCenter(txt))
        self.remove(txt)
        self.play(brace.animate.shift(np.array([0, BAR_SPACING * 1, 0])))

        self.remove(brace)

        self.wait(3)
