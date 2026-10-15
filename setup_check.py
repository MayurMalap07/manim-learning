"""
setup_check.py - confirms your Manim setup works end to end.

Run from this folder:
    uv run manim -pql setup_check.py SetupCheck

-p  = play the video when done
-ql = quality low (fast). Use -qh for high quality later.
"""

from manim import *


class SetupCheck(Scene):
    def construct(self):
        # 1) Plain text  -> tests Pango (no LaTeX needed)
        title = Text("Setup check", font_size=48)
        title.to_edge(UP)                      # move to the top of the screen
        self.play(Write(title))

        # 2) Shapes + animation -> tests Cairo rendering + FFmpeg video
        square = Square(side_length=2, color=BLUE)
        circle = Circle(radius=1, color=PINK, fill_opacity=0.5)
        self.play(Create(square))
        self.play(square.animate.rotate(PI / 4))   # tween: rotate 45 degrees
        self.play(Transform(square, circle))       # morph square -> circle

        # 3) An equation -> tests LaTeX (MiKTeX) + dvisvgm
        #    r"..." is a raw string so Python leaves the backslashes for LaTeX.
        eq = MathTex(r"\oint_{\gamma} f(z)\,dz = 0", font_size=60)
        eq.next_to(square, DOWN, buff=0.6)          # place it under the circle
        self.play(Write(eq))

        # 4) Success message
        ok = Text("Everything works!", color=GREEN, font_size=36)
        ok.to_edge(DOWN)
        self.play(FadeIn(ok, shift=UP))
        self.wait()
