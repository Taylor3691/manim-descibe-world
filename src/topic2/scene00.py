from manim import *


class Scene00(Scene):
    def construct(self):
        typing_sound = "assets/audio/typing-keyboard-asmr-1p5s.mp3"
        silence = "assets/audio/silence.wav"

        tutorial = Tex(
            r"Inspired by an invited talk: \textbf{From Video Generation to World Model}",
            font_size=34,
            color=WHITE,
        ).move_to(UP * 1.05)

        divider = Line(LEFT * 1.25, RIGHT * 1.25, color=GRAY_B, stroke_width=1.8)
        divider.move_to(UP * 0.45)

        subtitle = Tex(
            r"\textbf{Physics-Grounded World Models}",
            font_size=64,
            color=WHITE,
        ).move_to(DOWN * 0.15)

        self.add_sound(typing_sound, gain=12)
        self.add_sound(typing_sound, time_offset=1.9, gain=12)
        self.add_sound(silence, time_offset=4.2)
        self.play(Write(tutorial), run_time=1.5)
        self.wait(0.25)
        self.play(Create(divider), run_time=0.4)
        self.play(Write(subtitle), run_time=1.5)
        self.wait(1.0)
