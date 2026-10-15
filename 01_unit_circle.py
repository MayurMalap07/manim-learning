"""
Lesson 01 - Where does the sine wave come from?

A point goes around a circle of radius 1. Its HEIGHT at each angle is sin(theta).
If you plot that height against the angle, you get the sine wave.

Run:
    uv run manim -pql 01_unit_circle.py UnitCircleSine

New Manim ideas in this file
----------------------------
ValueTracker  : a single number you can animate (like a float field you tween in a game).
always_redraw : rebuilds an object every frame from the current values
                (like doing the work inside Update() instead of Start()).
"""

from manim import *
import numpy as np


class UnitCircleSine(Scene):
    def construct(self):
        # ---------- Layout ----------
        R = 1.5                          # 1 math unit = 1.5 screen units
        center = LEFT * 4                # circle sits on the left

        circle = Circle(radius=R, color=BLUE).move_to(center)
        x_axis_c = Line(center + LEFT * (R + 0.3), center + RIGHT * (R + 0.3), color=GREY)
        y_axis_c = Line(center + DOWN * (R + 0.3), center + UP * (R + 0.3), color=GREY)

        # Graph on the right. y_length = 3 * R so that "1" on the graph
        # is exactly the same height as the circle's radius.
        axes = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-1.5, 1.5, 1],
            x_length=6,
            y_length=3 * R,
            tips=False,
        ).move_to(RIGHT * 1.5)

        pi_label = MathTex(r"\pi").next_to(axes.c2p(PI, 0), DOWN)
        two_pi_label = MathTex(r"2\pi").next_to(axes.c2p(2 * PI, 0), DOWN)
        title = MathTex(r"y = \sin\theta", color=GREEN).next_to(axes, UP)

        self.play(Create(circle), Create(x_axis_c), Create(y_axis_c))
        self.play(Create(axes), Write(pi_label), Write(two_pi_label), Write(title))

        # ---------- The animated number ----------
        theta = ValueTracker(0)          # the angle, starts at 0

        def point_on_circle():
            t = theta.get_value()
            return center + R * np.array([np.cos(t), np.sin(t), 0])

        def point_on_graph():
            t = theta.get_value()
            return axes.c2p(t, np.sin(t))

        # ---------- Things that follow theta every frame ----------
        radius_line = always_redraw(
            lambda: Line(center, point_on_circle(), color=YELLOW)
        )
        # Green vertical line = the height of the point = sin(theta)
        height_line = always_redraw(
            lambda: Line(
                np.array([point_on_circle()[0], center[1], 0]),
                point_on_circle(),
                color=GREEN,
                stroke_width=6,
            )
        )
        circle_dot = always_redraw(lambda: Dot(point_on_circle(), color=YELLOW))
        graph_dot = always_redraw(lambda: Dot(point_on_graph(), color=GREEN))
        connector = always_redraw(
            lambda: DashedLine(point_on_circle(), point_on_graph(), color=GREY)
        )
        # The curve drawn so far: from 0 up to the current angle
        wave = always_redraw(
            lambda: axes.plot(
                np.sin,
                x_range=[0, max(theta.get_value(), 0.01)],
                color=GREEN,
            )
        )

        self.add(wave, radius_line, height_line, connector, circle_dot, graph_dot)

        # ---------- Run it: tween theta from 0 to 2*pi ----------
        self.play(theta.animate.set_value(2 * PI), run_time=8, rate_func=linear)
        self.wait()
