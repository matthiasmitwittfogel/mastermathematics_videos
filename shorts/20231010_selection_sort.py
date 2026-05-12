# Copyright (c) 2026 matthiasmitwittfogel
# Licensed under the Custom Educational License.
# See LICENSE file for details.

"""Animation demonstrating the selection sort algorithm."""

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
    YELLOW,
    config,
)


# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
config.pixel_width = 360
config.pixel_height = 640


class SelectSort(Scene):
    """Visualise selection sort with animated bars."""

    VALUES = [10, 8, 2, 9, 1, 6, 3, 5, 7, 4]
    START_Y = 6.5
    Y_STEP = 1.5
    X_OFFSET = -4.0
    BAR_WIDTH_FACTOR = 2.0
    BAR_HEIGHT = 1.0
    CIRCLE_RADIUS = 0.2
    CIRCLE_OFFSET = LEFT * 5
    RUN_TIME = 0.4
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

    def construct(self):
        # --- Title ----------------------------------------------------------------
        title = Text(
            "Selection Sort Algorithm", font_size=self.TITLE_FONT_SIZE
        ).move_to([0, 9, 0])
        bg = Rectangle(
            width=title.width + 0.6,
            height=self.TITLE_RECT_HEIGHT,
            stroke_color=BLACK,
            fill_color=YELLOW,
            fill_opacity=0.4,
        ).move_to([0, 9, 0])
        self.add(title, bg)

        # --- Build bars -----------------------------------------------------------
        txt_objs = []
        rect_objs = []
        y = self.START_Y
        for value in self.VALUES:
            x = self.X_OFFSET + value / self.BAR_WIDTH_FACTOR
            txt_objs.append(Text(str(value)).move_to([x, y, 0]))
            rect_objs.append(
                Rectangle(
                    width=value,
                    height=self.BAR_HEIGHT,
                    fill_color=BLUE,
                    fill_opacity=0.4,
                ).move_to([x, y, 0])
            )
            y -= self.Y_STEP

        self.add(*txt_objs, *rect_objs)

        # --- Helpers --------------------------------------------------------------
        def move_rect(direction, index):
            self.play(
                VGroup(
                    rect_objs[self.VALUES.index(index)],
                    txt_objs[self.VALUES.index(index)],
                ).animate.shift(direction),
                run_time=self.RUN_TIME,
            )

        def wiggle_rect(index):
            self.play(
                Wiggle(
                    VGroup(
                        rect_objs[self.VALUES.index(index)],
                        txt_objs[self.VALUES.index(index)],
                    )
                ),
                run_time=self.WIGGLE_RUN_TIME,
            )

        # --- Tracker circle -------------------------------------------------------
        circle = Circle(
            radius=self.CIRCLE_RADIUS,
            color=RED,
            fill_color=RED,
            fill_opacity=1,
        ).next_to(rect_objs[self.VALUES.index(10)], self.CIRCLE_OFFSET)
        self.add(circle)

        # --- First Round ----------------------------------------------------------
        self._show_round("First Round")

        move_rect(LEFT, 10)
        move_rect(LEFT, 8)
        move_rect(RIGHT, 10)
        move_rect(LEFT, 2)
        move_rect(RIGHT, 8)
        move_rect(LEFT, 9)
        wiggle_rect(9)
        move_rect(RIGHT, 9)
        move_rect(LEFT, 1)
        move_rect(RIGHT, 2)
        move_rect(LEFT, 6)
        wiggle_rect(6)
        move_rect(RIGHT, 6)
        move_rect(LEFT, 3)
        wiggle_rect(3)
        move_rect(RIGHT, 3)
        move_rect(LEFT, 5)
        wiggle_rect(5)
        move_rect(RIGHT, 5)
        move_rect(LEFT, 7)
        wiggle_rect(7)
        move_rect(RIGHT, 7)
        move_rect(LEFT, 4)
        wiggle_rect(4)
        move_rect(RIGHT, 4)

        self.play(
            VGroup(
                rect_objs[self.VALUES.index(1)], txt_objs[self.VALUES.index(1)]
            ).animate.shift(UP * self.Y_STEP * 4),
            VGroup(
                rect_objs[self.VALUES.index(2)], txt_objs[self.VALUES.index(2)]
            ).animate.shift(DOWN * self.Y_STEP),
            VGroup(
                rect_objs[self.VALUES.index(9)], txt_objs[self.VALUES.index(9)]
            ).animate.shift(DOWN * self.Y_STEP),
            VGroup(
                rect_objs[self.VALUES.index(10)], txt_objs[self.VALUES.index(10)]
            ).animate.shift(DOWN * self.Y_STEP),
            VGroup(
                rect_objs[self.VALUES.index(8)], txt_objs[self.VALUES.index(8)]
            ).animate.shift(DOWN * self.Y_STEP),
            run_time=self.RUN_TIME,
        )
        move_rect(RIGHT, 1)

        # --- Second Round ---------------------------------------------------------
        self._show_round("Second Round")

        self.play(
            circle.animate.shift(DOWN * self.Y_STEP),
            run_time=self.RUN_TIME,
        )

        move_rect(LEFT, 10)
        move_rect(LEFT, 8)
        move_rect(RIGHT, 10)
        move_rect(LEFT, 2)
        move_rect(RIGHT, 8)
        move_rect(LEFT, 9)
        wiggle_rect(9)
        move_rect(RIGHT, 9)
        move_rect(LEFT, 6)
        wiggle_rect(6)
        move_rect(RIGHT, 6)
        move_rect(LEFT, 3)
        wiggle_rect(3)
        move_rect(RIGHT, 3)
        move_rect(LEFT, 5)
        wiggle_rect(5)
        move_rect(RIGHT, 5)
        move_rect(LEFT, 7)
        wiggle_rect(7)
        move_rect(RIGHT, 7)
        move_rect(LEFT, 4)
        wiggle_rect(4)
        move_rect(RIGHT, 4)

        self.play(
            VGroup(
                rect_objs[self.VALUES.index(2)], txt_objs[self.VALUES.index(2)]
            ).animate.shift(UP * self.Y_STEP * 2),
            VGroup(
                rect_objs[self.VALUES.index(10)], txt_objs[self.VALUES.index(10)]
            ).animate.shift(DOWN * self.Y_STEP),
            VGroup(
                rect_objs[self.VALUES.index(8)], txt_objs[self.VALUES.index(8)]
            ).animate.shift(DOWN * self.Y_STEP),
            run_time=self.RUN_TIME,
        )
        move_rect(RIGHT, 2)

        # --- Third Round ----------------------------------------------------------
        self._show_round("Third Round")

        self.play(
            circle.animate.shift(DOWN * self.Y_STEP),
            run_time=self.RUN_TIME,
        )

        move_rect(LEFT, 10)
        move_rect(LEFT, 8)
        move_rect(RIGHT, 10)
        move_rect(LEFT, 9)
        wiggle_rect(9)
        move_rect(RIGHT, 9)
        move_rect(LEFT, 6)
        move_rect(RIGHT, 8)
        move_rect(LEFT, 3)
        move_rect(RIGHT, 6)
        move_rect(LEFT, 5)
        wiggle_rect(5)
        move_rect(RIGHT, 5)
        move_rect(LEFT, 7)
        wiggle_rect(7)
        move_rect(RIGHT, 7)
        move_rect(LEFT, 4)
        wiggle_rect(4)
        move_rect(RIGHT, 4)

        self.play(
            VGroup(
                rect_objs[self.VALUES.index(3)], txt_objs[self.VALUES.index(3)]
            ).animate.shift(UP * self.Y_STEP * 4),
            VGroup(
                rect_objs[self.VALUES.index(10)], txt_objs[self.VALUES.index(10)]
            ).animate.shift(DOWN * self.Y_STEP),
            VGroup(
                rect_objs[self.VALUES.index(8)], txt_objs[self.VALUES.index(8)]
            ).animate.shift(DOWN * self.Y_STEP),
            VGroup(
                rect_objs[self.VALUES.index(9)], txt_objs[self.VALUES.index(9)]
            ).animate.shift(DOWN * self.Y_STEP),
            VGroup(
                rect_objs[self.VALUES.index(6)], txt_objs[self.VALUES.index(6)]
            ).animate.shift(DOWN * self.Y_STEP),
            run_time=self.RUN_TIME,
        )
        move_rect(RIGHT, 3)

        # --- Forth Round ----------------------------------------------------------
        self._show_round("Forth Round")

        self.play(
            circle.animate.shift(DOWN * self.Y_STEP),
            run_time=self.RUN_TIME,
        )

        move_rect(LEFT, 10)
        move_rect(LEFT, 8)
        move_rect(RIGHT, 10)
        move_rect(LEFT, 9)
        wiggle_rect(9)
        move_rect(RIGHT, 9)
        move_rect(LEFT, 6)
        move_rect(RIGHT, 8)
        move_rect(LEFT, 5)
        move_rect(RIGHT, 6)
        move_rect(LEFT, 7)
        wiggle_rect(7)
        move_rect(RIGHT, 7)
        move_rect(LEFT, 4)
        move_rect(RIGHT, 5)

        self.play(
            VGroup(
                rect_objs[self.VALUES.index(4)], txt_objs[self.VALUES.index(4)]
            ).animate.shift(UP * self.Y_STEP * 6),
            VGroup(
                rect_objs[self.VALUES.index(10)], txt_objs[self.VALUES.index(10)]
            ).animate.shift(DOWN * self.Y_STEP),
            VGroup(
                rect_objs[self.VALUES.index(8)], txt_objs[self.VALUES.index(8)]
            ).animate.shift(DOWN * self.Y_STEP),
            VGroup(
                rect_objs[self.VALUES.index(9)], txt_objs[self.VALUES.index(9)]
            ).animate.shift(DOWN * self.Y_STEP),
            VGroup(
                rect_objs[self.VALUES.index(6)], txt_objs[self.VALUES.index(6)]
            ).animate.shift(DOWN * self.Y_STEP),
            VGroup(
                rect_objs[self.VALUES.index(5)], txt_objs[self.VALUES.index(5)]
            ).animate.shift(DOWN * self.Y_STEP),
            VGroup(
                rect_objs[self.VALUES.index(7)], txt_objs[self.VALUES.index(7)]
            ).animate.shift(DOWN * self.Y_STEP),
            run_time=self.RUN_TIME,
        )
        move_rect(RIGHT, 4)

        # --- Fifth Round ----------------------------------------------------------
        self._show_round("Fifth Round")

        self.play(
            circle.animate.shift(DOWN * self.Y_STEP),
            run_time=self.RUN_TIME,
        )

        move_rect(LEFT, 10)
        move_rect(LEFT, 8)
        move_rect(RIGHT, 10)
        move_rect(LEFT, 9)
        wiggle_rect(9)
        move_rect(RIGHT, 9)
        move_rect(LEFT, 6)
        move_rect(RIGHT, 8)
        move_rect(LEFT, 5)
        move_rect(RIGHT, 6)
        move_rect(LEFT, 7)
        wiggle_rect(7)
        move_rect(RIGHT, 7)

        self.play(
            VGroup(
                rect_objs[self.VALUES.index(5)], txt_objs[self.VALUES.index(5)]
            ).animate.shift(UP * self.Y_STEP * 4),
            VGroup(
                rect_objs[self.VALUES.index(10)], txt_objs[self.VALUES.index(10)]
            ).animate.shift(DOWN * self.Y_STEP),
            VGroup(
                rect_objs[self.VALUES.index(8)], txt_objs[self.VALUES.index(8)]
            ).animate.shift(DOWN * self.Y_STEP),
            VGroup(
                rect_objs[self.VALUES.index(9)], txt_objs[self.VALUES.index(9)]
            ).animate.shift(DOWN * self.Y_STEP),
            VGroup(
                rect_objs[self.VALUES.index(6)], txt_objs[self.VALUES.index(6)]
            ).animate.shift(DOWN * self.Y_STEP),
            run_time=self.RUN_TIME,
        )
        move_rect(RIGHT, 5)

        # --- Sixth Round ----------------------------------------------------------
        self._show_round("Sixth Round")

        self.play(
            circle.animate.shift(DOWN * self.Y_STEP),
            run_time=self.RUN_TIME,
        )

        move_rect(LEFT, 10)
        move_rect(LEFT, 8)
        move_rect(RIGHT, 10)
        move_rect(LEFT, 9)
        wiggle_rect(9)
        move_rect(RIGHT, 9)
        move_rect(LEFT, 6)
        move_rect(RIGHT, 8)
        move_rect(LEFT, 7)
        wiggle_rect(7)
        move_rect(RIGHT, 7)

        self.play(
            VGroup(
                rect_objs[self.VALUES.index(6)], txt_objs[self.VALUES.index(6)]
            ).animate.shift(UP * self.Y_STEP * 3),
            VGroup(
                rect_objs[self.VALUES.index(10)], txt_objs[self.VALUES.index(10)]
            ).animate.shift(DOWN * self.Y_STEP),
            VGroup(
                rect_objs[self.VALUES.index(8)], txt_objs[self.VALUES.index(8)]
            ).animate.shift(DOWN * self.Y_STEP),
            VGroup(
                rect_objs[self.VALUES.index(9)], txt_objs[self.VALUES.index(9)]
            ).animate.shift(DOWN * self.Y_STEP),
            run_time=self.RUN_TIME,
        )
        move_rect(RIGHT, 6)

        # --- Seventh Round --------------------------------------------------------
        self._show_round("Seventh Round")

        self.play(
            circle.animate.shift(DOWN * self.Y_STEP),
            run_time=self.RUN_TIME,
        )

        move_rect(LEFT, 10)
        move_rect(LEFT, 8)
        move_rect(RIGHT, 10)
        move_rect(LEFT, 9)
        wiggle_rect(9)
        move_rect(RIGHT, 9)
        move_rect(LEFT, 7)
        move_rect(RIGHT, 8)

        self.play(
            VGroup(
                rect_objs[self.VALUES.index(7)], txt_objs[self.VALUES.index(7)]
            ).animate.shift(UP * self.Y_STEP * 3),
            VGroup(
                rect_objs[self.VALUES.index(10)], txt_objs[self.VALUES.index(10)]
            ).animate.shift(DOWN * self.Y_STEP),
            VGroup(
                rect_objs[self.VALUES.index(8)], txt_objs[self.VALUES.index(8)]
            ).animate.shift(DOWN * self.Y_STEP),
            VGroup(
                rect_objs[self.VALUES.index(9)], txt_objs[self.VALUES.index(9)]
            ).animate.shift(DOWN * self.Y_STEP),
            run_time=self.RUN_TIME,
        )
        move_rect(RIGHT, 7)

        # --- Eighth Round ---------------------------------------------------------
        self._show_round("Eighth Round")

        self.play(
            circle.animate.shift(DOWN * self.Y_STEP),
            run_time=self.RUN_TIME,
        )

        move_rect(LEFT, 10)
        move_rect(LEFT, 8)
        move_rect(RIGHT, 10)
        move_rect(LEFT, 9)
        wiggle_rect(9)
        move_rect(RIGHT, 9)

        self.play(
            VGroup(
                rect_objs[self.VALUES.index(8)], txt_objs[self.VALUES.index(8)]
            ).animate.shift(UP * self.Y_STEP),
            VGroup(
                rect_objs[self.VALUES.index(10)], txt_objs[self.VALUES.index(10)]
            ).animate.shift(DOWN * self.Y_STEP),
            run_time=self.RUN_TIME,
        )
        move_rect(RIGHT, 8)

        # --- Ninth Round ----------------------------------------------------------
        self._show_round("Ninth Round")

        self.play(
            circle.animate.shift(DOWN * self.Y_STEP),
            run_time=self.RUN_TIME,
        )

        move_rect(LEFT, 10)
        move_rect(LEFT, 9)
        move_rect(RIGHT, 10)

        self.play(
            VGroup(
                rect_objs[self.VALUES.index(9)], txt_objs[self.VALUES.index(9)]
            ).animate.shift(UP * self.Y_STEP),
            VGroup(
                rect_objs[self.VALUES.index(10)], txt_objs[self.VALUES.index(10)]
            ).animate.shift(DOWN * self.Y_STEP),
            run_time=self.RUN_TIME,
        )
        move_rect(RIGHT, 9)

        # --- Finish ---------------------------------------------------------------
        self._show_round("Finish")

        self.remove(circle)

        self.wait(3)
