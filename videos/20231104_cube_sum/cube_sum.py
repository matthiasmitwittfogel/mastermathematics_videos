# Copyright (c) 2026 matthiasmitwittfogel
# Licensed under the Custom Educational License.
# See LICENSE file for details.

"""Visual derivation of 1^3 + 2^3 + ... + n^3 using geometric squares."""

import math

from manim import (
    BLACK, BLUE, PURE_RED, RED, WHITE, YELLOW,
    Scene, config,
    MathTex, Text, Square, Line, Polygon,
    BraceBetweenPoints, Difference, Intersection,
    GrowFromEdge, Create, Write, Rotate,
    UP, DOWN, LEFT, RIGHT, PI, UL, UR, DL, DR,
)

try:
    from manim_voiceover import VoiceoverScene
    _HAS_VOICEOVER = True
except ImportError:
    _HAS_VOICEOVER = False

if _HAS_VOICEOVER:
    from manim_voiceover.services.azure import AzureService
    _Base = VoiceoverScene
else:
    _Base = Scene

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
config.background_color = BLACK

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SIDE_LEN = 0.3
SQUARE_COLOR = BLUE
SQUARE_OPACITY = 0.5
STROKE_WIDTH = 0.1


# ---------------------------------------------------------------------------
# Voiceover fallback
# ---------------------------------------------------------------------------
class _DummyTracker:
    duration = 2.0

    def __enter__(self):
        return self

    def __exit__(self, *_):
        pass


# ---------------------------------------------------------------------------
# Scene
# ---------------------------------------------------------------------------
class SubSum(_Base):
    """Geometric proof that 1^3 + 2^3 + ... + n^3 = (n(n+1)/2)^2."""

    USE_VOICEOVER = False

    def set_speech_service(self, service=None):
        if _HAS_VOICEOVER and self.USE_VOICEOVER:
            super().set_speech_service(service)

    def voiceover(self, text):
        if _HAS_VOICEOVER and self.USE_VOICEOVER:
            return super().voiceover(text)
        return _DummyTracker()

    def wait_until_bookmark(self, mark):
        if _HAS_VOICEOVER and self.USE_VOICEOVER:
            super().wait_until_bookmark(mark)

    def construct(self):
        if _HAS_VOICEOVER and self.USE_VOICEOVER:
            self.set_speech_service(
                AzureService(voice="zh-CN-YunxiNeural", style="newscast")
            )

        # --- Title formulas -------------------------------------------------
        formula1 = MathTex(r"1^3+2^3+3^3+4^3+...+n^3").scale(2 / 3).shift(UP * 3.2)

        with self.voiceover(
            "Visual proof: the sum of cubes from 1 to n."
        ) as tracker:
            self.play(Write(formula1), run_time=tracker.duration)

        formula2 = MathTex(
            "=1\\cdot1^2", "+", "2\\cdot2^2", "+",
            "3\\cdot3^2", "+", "4\\cdot4^2", "+",
            "...", "+", "n\\cdot n^2",
        ).scale(2 / 3).next_to(formula1, RIGHT)

        # --- Geometric squares ----------------------------------------------
        square_11 = Square(
            side_length=SIDE_LEN,
            fill_color=SQUARE_COLOR,
            fill_opacity=SQUARE_OPACITY,
            stroke_width=STROKE_WIDTH,
        ).shift(UP * 2 + LEFT * 3)
        square1s = [square_11]

        square_21 = Square(
            side_length=SIDE_LEN * 2,
            fill_color=SQUARE_COLOR,
            fill_opacity=SQUARE_OPACITY,
            stroke_width=STROKE_WIDTH,
        ).next_to(square_11, DOWN, buff=0).align_to(square_11, LEFT)
        square_22 = square_21.copy().shift(RIGHT * square_21.side_length)
        square2s = [square_21, square_22]

        square_31 = Square(
            side_length=SIDE_LEN * 3,
            fill_color=SQUARE_COLOR,
            fill_opacity=SQUARE_OPACITY,
            stroke_width=STROKE_WIDTH,
        ).next_to(square_21, DOWN, buff=0).align_to(square_21, LEFT)
        square_32 = square_31.copy().shift(RIGHT * square_31.side_length)
        square_33 = square_32.copy().shift(RIGHT * square_32.side_length)
        square3s = [square_31, square_32, square_33]

        square_41 = Square(
            side_length=SIDE_LEN * 4,
            fill_color=SQUARE_COLOR,
            fill_opacity=SQUARE_OPACITY,
            stroke_width=STROKE_WIDTH,
        ).next_to(square_31, DOWN, buff=0).align_to(square_31, LEFT)
        square_42 = square_41.copy().shift(RIGHT * square_41.side_length)
        square_43 = square_42.copy().shift(RIGHT * square_42.side_length)
        square_44 = square_43.copy().shift(RIGHT * square_43.side_length)
        square4s = [square_41, square_42, square_43, square_44]

        square_51 = Square(
            side_length=SIDE_LEN * 5,
            fill_color=SQUARE_COLOR,
            fill_opacity=SQUARE_OPACITY,
            stroke_width=STROKE_WIDTH,
        ).next_to(square_41, DOWN, buff=0).align_to(square_41, LEFT)
        square5s = [square_51]
        for i in range(1, 5):
            square5s.append(square_51.copy().shift(RIGHT * i * square_51.side_length))

        # --- Side labels ----------------------------------------------------
        mark1 = MathTex("1").next_to(square_11, LEFT).scale(1 / 2)
        mark2 = MathTex("2").next_to(square_21, LEFT).scale(1 / 2)
        mark3 = MathTex("3").next_to(square_31, LEFT).scale(1 / 2)
        mark4 = MathTex("4").next_to(square_41, LEFT).scale(1 / 2)
        mark_dot1 = Text("...").next_to(mark4, 2 * DOWN).scale(1 / 2)
        mark5 = MathTex("n").next_to(square_51, LEFT).scale(1 / 2)

        # --- Animation: step by step ----------------------------------------
        with self.voiceover(
            "First, let's break down 1 cubed as 1 times 1 squared, <bookmark mark='A'/> which equals the area of a square with side length 1."
        ) as tracker:
            self.play(formula1.animate.to_edge(LEFT))
            self.play(Write(formula2.submobjects[0].next_to(formula1, RIGHT)))
            self.add(formula2.submobjects[1].next_to(formula2.submobjects[0], RIGHT))
            self.wait_until_bookmark('A')
            self.play(GrowFromEdge(square_11, LEFT))
            self.add(mark1)

        with self.voiceover(
            "Then, 2 cubed becomes 2 times 2 squared, <bookmark mark='B'/> that is, the area of 2 squares with side length 2."
        ) as tracker:
            self.add(formula2.submobjects[2].next_to(formula2.submobjects[1], RIGHT))
            self.play(Write(formula2.submobjects[3].next_to(formula2.submobjects[2], RIGHT)))
            self.wait_until_bookmark('B')
            for sq in square2s:
                self.play(GrowFromEdge(sq, LEFT))
            self.add(mark2)

        with self.voiceover(
            "3 cubed equals 3 times 3 squared, <bookmark mark='C'/> which is the area of 3 squares with side length 3."
        ) as tracker:
            self.add(formula2.submobjects[4].next_to(formula2.submobjects[3], RIGHT))
            self.play(Write(formula2.submobjects[5].next_to(formula2.submobjects[4], RIGHT)))
            self.wait_until_bookmark("C")
            for sq in square3s:
                self.play(GrowFromEdge(sq, LEFT))
            self.add(mark3)

        with self.voiceover(
            "4 cubed equals 4 times 4 squared, <bookmark mark='D'/> equal to the area of 4 squares with side length 4."
        ) as tracker:
            self.add(formula2.submobjects[6].next_to(formula2.submobjects[5], RIGHT))
            self.play(Write(formula2.submobjects[7].next_to(formula2.submobjects[6], RIGHT)))
            self.wait_until_bookmark('D')
            for sq in square4s:
                self.play(GrowFromEdge(sq, LEFT))
            self.add(mark4)

        with self.voiceover(
            "And so on, <bookmark mark='E'/> up to n cubed, <bookmark mark='F'/> equal to n squares with side length n."
        ):
            self.add(formula2.submobjects[8].next_to(formula2.submobjects[7], RIGHT))
            self.add(formula2.submobjects[9].next_to(formula2.submobjects[8], RIGHT))
            self.add(formula2.submobjects[10].next_to(formula2.submobjects[9], RIGHT))
            self.wait_until_bookmark('E')
            self.play(Write(formula2.submobjects[10]))
            self.wait_until_bookmark('F')
            self.add(mark_dot1)
            for sq in square5s:
                self.play(GrowFromEdge(sq, LEFT), run_time=0.5)
            self.add(mark5)

        # --- Red line -------------------------------------------------------
        line = Line(
            start=square_11.get_corner(UL),
            end=square5s[4].get_corner(DR) + [square_51.side_length, 0, 0],
            color=RED,
            stroke_width=1,
        )
        line1 = Line(
            start=square5s[4].get_corner(DR) + [square_51.side_length, 0, 0],
            end=square5s[4].get_corner(DR),
            stroke_width=1,
        )
        with self.voiceover(
            "So the sum of cubes from 1 to n equals the total area of all these squares. How do we calculate it? <bookmark mark='G'/> We can draw a red line as shown,"
        ):
            self.wait_until_bookmark('G')
            self.play(Create(line))
            self.play(Create(line1))

        # --- Difference triangles -------------------------------------------
        triangle5 = Polygon(
            square5s[4].get_corner(DR) + [square_51.side_length, 0, 0],
            square_51.get_corner(DL),
            square_11.get_corner(UL),
            fill_color=BLUE,
            fill_opacity=0.5,
            stroke_width=0.1,
        )
        diffs = []
        all_squares = [square1s, square2s, square3s, square4s, square5s]
        for i, square_group in enumerate(all_squares):
            diffs.append(
                Difference(
                    square_group[i],
                    triangle5,
                    fill_color=PURE_RED,
                    fill_opacity=0.5,
                    stroke_width=0.1,
                )
            )

        intersects = []
        for square_group, diff in zip(all_squares, diffs):
            intersects.append(
                Intersection(
                    square_group[-1],
                    diff,
                    stroke_width=0.1,
                    fill_color=BLACK,
                    fill_opacity=1,
                    color=BLACK,
                    stroke_color=BLACK,
                )
            )
        self.add(*intersects)
        self.add(*diffs)

        with self.voiceover(
            "The red line creates n small red triangles above it. <bookmark mark='X'/> If we rotate each red triangle 180 degrees clockwise, all the square areas combine into one large triangle. So the sum of cubes equals the area of this large triangle."
        ):
            for d in diffs:
                self.play(Rotate(d, -PI, about_point=d.get_corner(DR)))
            self.remove(line, line1)

        # --- Braces ---------------------------------------------------------
        brace_left = BraceBetweenPoints(
            square_11.get_corner(UL),
            square_51.get_corner(DL),
        ).shift(LEFT)
        txt1 = MathTex(r"\frac{n(n+1)}{2}").next_to(brace_left, LEFT)
        brace_down = BraceBetweenPoints(
            square_51.get_corner(DL),
            square_51.get_corner(DL) + 6 * square_51.side_length * RIGHT,
        )
        txt2 = MathTex(r"n(n+1)").next_to(brace_down, DOWN)

        with self.voiceover(
            "The height of this large triangle equals the sum of the arithmetic sequence from 1 to n, that is <bookmark mark='H' /> n times n plus 1 divided by 2."
        ):
            self.play(Create(brace_left))
            self.wait_until_bookmark('H')
            self.play(Write(txt1))

        with self.voiceover(
            "The base of this large triangle <bookmark mark='I' /> equals n times n plus 1."
        ):
            self.play(Create(brace_down))
            self.wait_until_bookmark('I')
            self.play(Write(txt2))

        # --- Final result ---------------------------------------------------
        result_1 = Text("=Area(").scale(2 / 3).align_to(
            formula2.submobjects[10], LEFT
        ).shift(UP * 2 + LEFT * 2)
        final = MathTex(r"=(\frac{n(n+1)}{2})^2")

        with self.voiceover("So the area equals one half times base times height,"):
            self.play(Write(result_1), run_time=0.2)
            result1_2 = triangle5.copy()
            self.play(result1_2.animate.scale(1 / 10).next_to(result_1, RIGHT), run_time=0.5)
            result_2 = Text(")").scale(2 / 3).next_to(result1_2, RIGHT, buff=0.1)
            self.play(Write(result_2), run_time=0.2)
            result_3 = MathTex(r"=\frac{1}{2} \cdot ").align_to(result_1, LEFT).shift(UP)
            self.play(Write(result_3), run_time=0.2)
            result_4 = txt1.copy().scale(3 / 4).next_to(result_3, RIGHT)
            self.play(result_4.animate.scale(2 / 3).next_to(result_3, RIGHT), run_time=0.5)
            dot_4 = MathTex(r"\cdot").next_to(result_4, RIGHT)
            self.add(dot_4)
            result_5 = txt2.copy()
            self.play(result_5.animate.scale(2 / 3).next_to(dot_4, RIGHT), run_time=0.5)
            final.scale(4 / 5).align_to(result_3, LEFT).shift(DOWN * 0.5)

        with self.voiceover("The final result equals n times n plus 1, all squared, divided by 4."):
            self.play(Write(final))

        self.wait(3)
