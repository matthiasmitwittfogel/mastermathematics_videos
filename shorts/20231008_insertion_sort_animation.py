# Copyright (c) 2026 matthiasmitwittfogel
# Licensed under the Custom Educational License.
# See LICENSE file for details.

"""Animation demonstrating the insertion sort algorithm."""

from manim import (
    BLACK,
    BLUE,
    Circle,
    DOWN,
    GrowFromCenter,
    LEFT,
    Rectangle,
    RED,
    RIGHT,
    Scene,
    Text,
    UP,
    VGroup,
    Wiggle,
    config,
)


# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
config.pixel_width = 360
config.pixel_height = 640


class InsertSort(Scene):
    """Visualise insertion sort with animated bars."""

    VALUES = [10, 8, 2, 9, 1, 6, 3, 5, 7, 4]
    START_Y = 6.5
    Y_STEP = 1.5
    X_OFFSET = -4.0
    BAR_WIDTH_FACTOR = 2.0
    BAR_HEIGHT = 1.0
    CIRCLE_RADIUS = 0.2
    CIRCLE_OFFSET = LEFT * 5
    RUN_TIME = 0.5
    WIGGLE_RUN_TIME = 1.0
    TITLE_FONT_SIZE = 64
    ROUND_FONT_SIZE = 150
    ROUND_STROKE_WIDTH = 5
    TITLE_RECT_WIDTH = 11.0
    TITLE_RECT_HEIGHT = 1.8

    def _show_round(self, title):
        """Display and remove a round title."""
        txt = Text(
            title,
            font_size=self.ROUND_FONT_SIZE,
            color=RED,
            stroke_width=self.ROUND_STROKE_WIDTH,
        )
        self.play(GrowFromCenter(txt))
        self.remove(txt)

    def _shift_values(self, value_direction_pairs, run_time=None):
        """Shift a set of (value, direction) pairs simultaneously."""
        if run_time is None:
            run_time = self.RUN_TIME
        animations = []
        for value, direction in value_direction_pairs:
            idx = self.values.index(value)
            animations.append(
                VGroup(self.rect_objs[idx], self.txt_objs[idx]).animate.shift(direction)
            )
        self.play(*animations, run_time=run_time)

    def _wiggle_value(self, value, run_time=None):
        """Wiggle the bar/text pair for a given value."""
        if run_time is None:
            run_time = self.WIGGLE_RUN_TIME
        idx = self.values.index(value)
        self.play(
            Wiggle(VGroup(self.rect_objs[idx], self.txt_objs[idx])),
            run_time=run_time,
        )

    def _move_circle_down(self, circle):
        """Move the tracker circle down one step."""
        self.play(
            circle.animate.shift(DOWN * self.Y_STEP),
            run_time=self.RUN_TIME,
        )

    def construct(self):
        # --- Title ----------------------------------------------------------------
        self.add(
            Text("Insertion Sort Algorithm", font_size=self.TITLE_FONT_SIZE).move_to(
                [0, 9, 0]
            )
        )
        self.add(
            Rectangle(
                width=self.TITLE_RECT_WIDTH,
                height=self.TITLE_RECT_HEIGHT,
                stroke_color=BLACK,
                fill_color=RED,
                fill_opacity=0.4,
            ).move_to([0, 9, 0])
        )

        # --- Build bars -----------------------------------------------------------
        self.txt_objs = []
        self.rect_objs = []
        y = self.START_Y
        for value in self.VALUES:
            x = self.X_OFFSET + value / self.BAR_WIDTH_FACTOR
            self.txt_objs.append(Text(str(value)).move_to([x, y, 0]))
            self.rect_objs.append(
                Rectangle(
                    width=value,
                    height=self.BAR_HEIGHT,
                    fill_color=BLUE,
                    fill_opacity=0.4,
                ).move_to([x, y, 0])
            )
            y -= self.Y_STEP

        self.add(*self.txt_objs, *self.rect_objs)
        self.values = self.VALUES  # local alias for helpers

        # --- First Round ----------------------------------------------------------
        self._show_round("First Round")

        circle = Circle(
            radius=self.CIRCLE_RADIUS,
            color=RED,
            fill_color=RED,
            fill_opacity=1,
        ).next_to(self.rect_objs[self.values.index(8)], self.CIRCLE_OFFSET)
        self.add(circle)

        self._shift_values([(8, LEFT), (10, LEFT)])
        self._shift_values([(8, UP * self.Y_STEP), (10, DOWN * self.Y_STEP)])
        self._shift_values([(8, RIGHT), (10, RIGHT)])

        # --- Second Round ---------------------------------------------------------
        self._show_round("Second Round")

        self._move_circle_down(circle)

        self._shift_values([(2, LEFT), (10, LEFT)])
        self._shift_values([(8, LEFT)])

        self._shift_values([
            (2, UP * self.Y_STEP * 2),
            (8, DOWN * self.Y_STEP),
            (10, DOWN * self.Y_STEP),
        ])

        self._shift_values([(2, RIGHT), (8, RIGHT), (10, RIGHT)])

        # --- Third Round ----------------------------------------------------------
        self._show_round("Third Round")

        self._move_circle_down(circle)

        self._shift_values([(9, LEFT), (10, LEFT)])
        self._shift_values([(8, LEFT)])
        self._wiggle_value(8)
        self._shift_values([(8, RIGHT)])

        self._shift_values([
            (9, UP * self.Y_STEP),
            (10, DOWN * self.Y_STEP),
        ])
        self._shift_values([(9, RIGHT), (10, RIGHT)])

        # --- Forth Round ----------------------------------------------------------
        self._show_round("Forth Round")

        self._move_circle_down(circle)

        self._shift_values([(1, LEFT), (10, LEFT)])
        self._shift_values([(9, LEFT)])
        self._shift_values([(8, LEFT)])
        self._shift_values([(2, LEFT)])

        self._shift_values([
            (1, UP * self.Y_STEP * 4),
            (2, DOWN * self.Y_STEP),
            (8, DOWN * self.Y_STEP),
            (9, DOWN * self.Y_STEP),
            (10, DOWN * self.Y_STEP),
        ])

        self._shift_values([
            (1, RIGHT),
            (2, RIGHT),
            (8, RIGHT),
            (9, RIGHT),
            (10, RIGHT),
        ])

        # --- Fifth Round ----------------------------------------------------------
        self._show_round("Fifth Round")

        self._move_circle_down(circle)

        self._shift_values([(6, LEFT), (10, LEFT)])
        self._shift_values([(9, LEFT)])
        self._shift_values([(8, LEFT)])
        self._shift_values([(2, LEFT)])
        self._wiggle_value(2)
        self._shift_values([(2, RIGHT)])

        self._shift_values([
            (6, UP * self.Y_STEP * 3),
            (10, DOWN * self.Y_STEP),
            (8, DOWN * self.Y_STEP),
            (9, DOWN * self.Y_STEP),
        ])

        self._shift_values([
            (6, RIGHT),
            (10, RIGHT),
            (8, RIGHT),
            (9, RIGHT),
        ])

        # --- Sixth Round ----------------------------------------------------------
        self._show_round("Sixth Round")

        self._move_circle_down(circle)

        self._shift_values([(3, LEFT), (10, LEFT)])
        self._shift_values([(9, LEFT)])
        self._shift_values([(8, LEFT)])
        self._shift_values([(6, LEFT)])
        self._shift_values([(2, LEFT)])
        self._wiggle_value(2)
        self._shift_values([(2, RIGHT)])

        self._shift_values([
            (3, UP * self.Y_STEP * 4),
            (10, DOWN * self.Y_STEP),
            (8, DOWN * self.Y_STEP),
            (9, DOWN * self.Y_STEP),
            (6, DOWN * self.Y_STEP),
        ])

        self._shift_values([
            (3, RIGHT),
            (10, RIGHT),
            (8, RIGHT),
            (9, RIGHT),
            (6, RIGHT),
        ])

        # --- Seventh Round --------------------------------------------------------
        self._show_round("Seventh Round")

        self._move_circle_down(circle)

        self._shift_values([(5, LEFT), (10, LEFT)])
        self._shift_values([(9, LEFT)])
        self._shift_values([(8, LEFT)])
        self._shift_values([(6, LEFT)])
        self._shift_values([(3, LEFT)])
        self._wiggle_value(3)
        self._shift_values([(3, RIGHT)])

        self._shift_values([
            (5, UP * self.Y_STEP * 4),
            (10, DOWN * self.Y_STEP),
            (8, DOWN * self.Y_STEP),
            (9, DOWN * self.Y_STEP),
            (6, DOWN * self.Y_STEP),
        ])

        self._shift_values([
            (5, RIGHT),
            (10, RIGHT),
            (8, RIGHT),
            (9, RIGHT),
            (6, RIGHT),
        ])

        # --- Eighth Round ---------------------------------------------------------
        self._show_round("Eighth Round")

        self._move_circle_down(circle)

        self._shift_values([(7, LEFT), (10, LEFT)])
        self._shift_values([(9, LEFT)])
        self._shift_values([(8, LEFT)])
        self._shift_values([(6, LEFT)])
        self._wiggle_value(6)
        self._shift_values([(6, RIGHT)])

        self._shift_values([
            (7, UP * self.Y_STEP * 3),
            (10, DOWN * self.Y_STEP),
            (8, DOWN * self.Y_STEP),
            (9, DOWN * self.Y_STEP),
        ])

        self._shift_values([
            (7, RIGHT),
            (10, RIGHT),
            (8, RIGHT),
            (9, RIGHT),
        ])

        # --- Ninth Round ----------------------------------------------------------
        self._show_round("Ninth Round")

        self._move_circle_down(circle)

        self._shift_values([(4, LEFT), (10, LEFT)])
        self._shift_values([(9, LEFT)])
        self._shift_values([(8, LEFT)])
        self._shift_values([(7, LEFT)])
        self._shift_values([(6, LEFT)])
        self._shift_values([(5, LEFT)])
        self._shift_values([(3, LEFT)])
        self._wiggle_value(3)
        self._shift_values([(3, RIGHT)])

        self._shift_values([
            (4, UP * self.Y_STEP * 6),
            (10, DOWN * self.Y_STEP),
            (8, DOWN * self.Y_STEP),
            (9, DOWN * self.Y_STEP),
            (7, DOWN * self.Y_STEP),
            (6, DOWN * self.Y_STEP),
            (5, DOWN * self.Y_STEP),
        ])

        self._shift_values([
            (7, RIGHT),
            (10, RIGHT),
            (8, RIGHT),
            (9, RIGHT),
            (6, RIGHT),
            (5, RIGHT),
            (4, RIGHT),
        ])

        # --- Finish ---------------------------------------------------------------
        self._show_round("Finish")

        self.remove(circle)

        self.wait(3)
