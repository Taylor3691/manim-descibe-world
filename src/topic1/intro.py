from manim import *


class Scene00(Scene):
    def construct(self):
        typing_sound = "assets/audio/typing-keyboard-asmr-1p5s.mp3"
        silence = "assets/audio/silence.wav"

        tutorial_line1 = Tex(
            r"Inspired by an invited talk:",
            font_size=26,
            color=WHITE,
        )
        tutorial_line2 = Tex(
            r"\textbf{From Video Generation to World Model}",
            font_size=30,
            color=WHITE,
        )
        tutorial = VGroup(tutorial_line1, tutorial_line2).arrange(DOWN, buff=0.08)
        tutorial.move_to(UP * 0.75)

        divider = Line(LEFT * 1.25, RIGHT * 1.25, color=GRAY_B, stroke_width=1.8)
        divider.next_to(tutorial, DOWN, buff=0.25)

        subtitle_line1 = Tex(
            r"\textbf{Scaling Foundation World Model}",
            font_size=52,
            color=WHITE,
        )
        subtitle_line2 = Tex(
            r"\textbf{as a Path to Embodied AGI}",
            font_size=52,
            color=WHITE,
        )
        subtitle = VGroup(subtitle_line1, subtitle_line2).arrange(DOWN, buff=0.06)
        subtitle.next_to(divider, DOWN, buff=0.18)

        self.add_sound(typing_sound, gain=12)
        self.add_sound(typing_sound, time_offset=1.9, gain=12)
        self.add_sound(silence, time_offset=4.2)
        self.play(Write(tutorial), run_time=1.5)
        self.wait(0.25)
        self.play(Create(divider), run_time=0.4)
        self.play(Write(subtitle), run_time=1.5)
        self.wait(1.0)
