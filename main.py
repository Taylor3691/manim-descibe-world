from manim import *

class Hello(Scene):
    def construct(self):
        text = Text("Hoàng Ngọc")
        self.play(Write(text))
        self.wait()