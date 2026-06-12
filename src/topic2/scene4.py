from pathlib import Path

from manim import *


class Scene4(Scene):
    def construct(self):
        # Title
        title = Tex(r"\textbf{Interactive 3D World Generation}").to_edge(UP)
        self.play(Write(title))

        # LEFT SIDE (1/4 of screen, divided into 2 parts)
        left_center = LEFT * 5.3

        # Left top part: user-control.png + "User Control" text
        user_control_path = Path("assets/images/user-control.png")
        user_control_img = ImageMobject(str(user_control_path)).scale_to_fit_height(0.8)
        user_control_text = Text("User Control", font_size=24).next_to(user_control_img, DOWN, buff=0.3)
        user_control_group = Group(user_control_img, user_control_text).arrange(DOWN, buff=0.2)
        user_control_group.move_to(left_center + UP * 1.5)

        # Left bottom part: input-image.png + "Input Image" text
        input_image_path = Path("assets/images/input-image.png")
        input_image_img = ImageMobject(str(input_image_path)).scale_to_fit_height(2.5)
        input_image_text = Text("Input Image", font_size=24).next_to(input_image_img, DOWN, buff=0.3)
        input_image_group = Group(input_image_img, input_image_text).arrange(DOWN, buff=0.2)
        input_image_group.move_to(left_center + DOWN * 1.5)

        # Group left elements
        left_group = Group(user_control_group, input_image_group)

        # RIGHT SIDE
        right_center = RIGHT * 2

        # Arrow pointing right (centered vertically, positioned between left and right groups)
        arrow_center = LEFT * 3.4
        arrow_style = {
            "color": YELLOW,
            "stroke_width": 8,
            "tip_shape": StealthTip,
            "max_tip_length_to_length_ratio": 0.15,
        }
        arrow = Arrow(
            start=arrow_center + LEFT * 0.3,
            end=arrow_center + RIGHT * 0.3,
            buff=0,
            **arrow_style,
        )
        arrow.set_stroke(width=8)

        # 3D scenes image
        scenes_3d_path = Path("assets/images/3d-scenes.png")
        scenes_3d_img = ImageMobject(str(scenes_3d_path)).scale_to_fit_height(3.2)
        scenes_3d_img.move_to(right_center + DOWN * 0.3)
        scenes_3d_text = Tex(r"Generated $3$D Scenes", font_size=32).next_to(scenes_3d_img, DOWN, buff=0.3)

        right_group = Group(arrow, scenes_3d_img, scenes_3d_text)

        # Citation text at bottom right corner
        citation_text = Tex(r"[\textbf{WonderWorld}, Yu \textit{et al.}, CVPR'$25$]", font_size=22, color=GRAY)

        # Animate the scene
        self.play(
            FadeIn(input_image_img, shift=LEFT * 0.3),
            Write(input_image_text),
            run_time=1.2,
        )

        self.wait(0.8)

        self.play(
            FadeIn(user_control_img, shift=LEFT * 0.3),
            Write(user_control_text),
            run_time=1.2,
        )

        self.play(
            GrowArrow(arrow),
            run_time=0.7,
        )

        self.play(
            FadeIn(scenes_3d_img, shift=RIGHT * 0.3),
            Write(scenes_3d_text),
            Write(citation_text.to_corner(DOWN + RIGHT)),
            run_time=0.8,
        )

        self.wait(7.5)
