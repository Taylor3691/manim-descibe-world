from pathlib import Path

import numpy as np
from manim import *

from video_mobject import (
    VideoMobject,
    create_video_stage_frame,
    fit_video_to_frame,
    freeze_video_frame,
)


def create_fontawesome_times_icon(color=RED, font_size=22):
    template = TexTemplate()
    template.add_to_preamble(r"\usepackage{fontawesome5}")
    return Tex(
        r"\faTimes",
        tex_template=template,
        font_size=font_size,
        color=color,
    )


class Scene2(Scene):
    def construct(self):
        label_font_size = 32

        slot_left = LEFT * 4.25
        slot_mid = ORIGIN
        slot_right = RIGHT * 4.25

        title = Tex(
            r"\textbf{Pixel Generation as World Models: }",
            r"\textbf{Challenges}",
        ).scale(0.9).to_edge(UP)
        title[1].set_color(RED)
        self.play(Write(title))
        self.wait(8)

        cup_path = Path("assets/images/cup.png")
        cup_group = ImageMobject(str(cup_path)).scale_to_fit_height(2.0).move_to(LEFT * 2.7)

        action_text = Tex(r'"Push cup to right by $10$cm"', font_size=34).next_to(cup_group, DOWN, buff=1)
        left_prompt_group = Group(cup_group, action_text)

        video_model_box = Rectangle(width=2.8, height=1.3, color=BLUE, fill_opacity=0.2).move_to(RIGHT * 2.4)
        video_model_text = Text("Video Model", font_size=28).move_to(video_model_box.get_center())
        ai_box = VGroup(video_model_box, video_model_text)
        ai_box.set_y(left_prompt_group.get_center()[1])

        arrow_style = {
            "color": YELLOW,
            "stroke_width": 3,
            "tip_shape": StealthTip,
            "max_tip_length_to_length_ratio": 0.1,
        }
        arrow = Arrow(start=cup_group.get_right(), end=video_model_box.get_left(), buff=0.18, **arrow_style)
        action_to_model_arrow = Arrow(
            start=action_text.get_right() + RIGHT * 0.1,
            end=video_model_box.get_left() + DOWN * 0.25,
            buff=0.15,
            **arrow_style,
        )

        self.play(FadeIn(cup_group, shift=UP * 0.5), Write(action_text))
        self.play(GrowArrow(arrow), GrowArrow(action_to_model_arrow), FadeIn(ai_box))
        self.wait(0.5)

        think_box_path = Path("assets/images/think-box.png")
        think_box_image = ImageMobject(str(think_box_path)).scale_to_fit_width(1.9)
        think_box_image.next_to(video_model_box, UP, buff=0.18)
        question_mark = Text("???", color=BLACK, font_size=36, weight=BOLD).move_to(think_box_image.get_center())
        think_group = Group(think_box_image, question_mark)

        self.play(FadeIn(think_box_image), Write(question_mark))
        self.wait(1)

        challenge_1_group = Group(cup_group, action_text, arrow, action_to_model_arrow, ai_box, think_group)
        self.play(challenge_1_group.animate.scale(0.44).move_to(slot_left), run_time=0.75)

        frame_1 = SurroundingRectangle(challenge_1_group, color=WHITE, buff=0.15, stroke_width=1.5)
        label_1_icon = create_fontawesome_times_icon(color=RED, font_size=label_font_size)
        label_1_text = Tex("Precise Action Control", font_size=label_font_size, color=WHITE)
        label_1 = VGroup(label_1_icon, label_1_text).arrange(RIGHT, buff=0.12).next_to(frame_1, UP, buff=0.12)
        challenge_1_slot = Group(challenge_1_group, frame_1, label_1)

        self.play(Create(frame_1), Write(label_1))

        wolf_video_path = Path("assets/videos/wolfs-chasing.mp4")
        wolf_video = VideoMobject(wolf_video_path)
        wolf_video.set_time_source(lambda: self.time)

        wolf_video_frame = create_video_stage_frame()
        fit_video_to_frame(wolf_video, wolf_video_frame, padding=0.18)

        self.play(FadeOut(challenge_1_slot), FadeIn(wolf_video_frame), FadeIn(wolf_video), run_time=0.8)
        wolf_video.play()
        self.wait(wolf_video.duration)
        wolf_video.pause()

        challenge_2_group = Group(wolf_video_frame, wolf_video)
        frame_2 = frame_1.copy().move_to(slot_mid)

        target_challenge_2 = challenge_2_group.copy()
        inner_target_w = frame_2.width - 0.3
        inner_target_h = frame_2.height - 0.3
        target_challenge_2.scale_to_fit_width(inner_target_w)
        if target_challenge_2.height > inner_target_h:
            target_challenge_2.scale_to_fit_height(inner_target_h)
        target_challenge_2.move_to(slot_mid)

        self.play(Transform(challenge_2_group, target_challenge_2), run_time=0.75)

        label_2_text = Tex(
            "Physical Consistency",
            font_size=label_font_size,
            color=WHITE,
        )
        label_2_icon = create_fontawesome_times_icon(color=RED, font_size=label_font_size)
        label_2 = VGroup(label_2_icon, label_2_text).arrange(RIGHT, buff=0.12).next_to(frame_2, UP, buff=0.12)

        self.play(Create(frame_2), Write(label_2), FadeIn(challenge_1_slot))

        wolf_video.stop()

        wolf_still = freeze_video_frame(wolf_video)
        self.remove(wolf_video)
        self.add(wolf_still)
        challenge_2_group = Group(wolf_video_frame, wolf_still)

        challenge_2_slot = Group(challenge_2_group, frame_2, label_2)

        self.play(
            FadeOut(challenge_1_slot),
            FadeOut(challenge_2_group),
            FadeOut(frame_2),
            FadeOut(label_2),
            run_time=0.7,
        )
        wolf_video.close()

        fulcrum_point = DOWN * 1.0

        pivot = Triangle(color=GRAY_C, fill_opacity=1).scale(0.34)
        pivot.move_to(fulcrum_point)

        pivot_top = pivot.get_top()
        beam = Line(LEFT * 2.2, RIGHT * 2.2, color=GRAY_D, stroke_width=8)
        beam.move_to(np.array([pivot_top[0], pivot_top[1], 0]))

        plate_offset = 0.48
        left_anchor = beam.get_start()
        right_anchor = beam.get_end()

        left_plate_bar = Line(
            left_anchor + UP * plate_offset + LEFT * 0.65,
            left_anchor + UP * plate_offset + RIGHT * 0.65,
            color=WHITE,
            stroke_width=4,
        )
        right_plate_bar = Line(
            right_anchor + UP * plate_offset + LEFT * 0.65,
            right_anchor + UP * plate_offset + RIGHT * 0.65,
            color=WHITE,
            stroke_width=4,
        )

        left_stem = Line(left_plate_bar.get_center(), left_anchor, color=GRAY_B, stroke_width=5)
        right_stem = Line(right_plate_bar.get_center(), right_anchor, color=GRAY_B, stroke_width=5)

        left_plate = VGroup(left_stem, left_plate_bar)
        right_plate = VGroup(right_stem, right_plate_bar)

        lever_group = VGroup(beam, left_plate, right_plate)
        dynamic_group = VGroup(lever_group)

        self.play(FadeIn(pivot, shift=UP * 0.1), Create(lever_group), run_time=1.1)

        box_w = 2.2
        box_h = 1.2
        box_font_size = 24
        box_color_left = GREEN_D
        box_color_right = RED_D

        cg_rect = Rectangle(width=box_w, height=box_h, color=box_color_left, fill_opacity=0.28)
        cg_rect.set_stroke(color=box_color_left, width=2)
        cg_text = Paragraph(
            "Computer",
            "Graphics",
            alignment="center",
            font_size=box_font_size,
            color=WHITE,
            weight=BOLD,
            line_spacing=0.9,
        )
        cg_box = VGroup(cg_rect, cg_text)
        cg_text.move_to(cg_rect.get_center())

        cg_target = left_plate_bar.get_center() + UP * (cg_box.height / 2 + 0.02)
        cg_box.move_to(cg_target + UP * 1.35)

        self.play(FadeIn(cg_box, shift=UP * 0.25), run_time=0.45)
        self.play(cg_box.animate.move_to(cg_target), run_time=1.2, rate_func=smooth)
        dynamic_group.add(cg_box)
        self.wait(0.2)

        nn_rect = Rectangle(width=box_w, height=box_h, color=box_color_right, fill_opacity=0.28)
        nn_rect.set_stroke(color=box_color_right, width=2)
        nn_text = Paragraph(
            "Video",
            "Model",
            alignment="center",
            font_size=box_font_size,
            color=WHITE,
            weight=BOLD,
            line_spacing=0.9,
        )
        nn_box = VGroup(nn_rect, nn_text)
        nn_text.move_to(nn_rect.get_center())

        nn_target = right_plate_bar.get_center() + UP * (nn_box.height / 2 + 0.02)
        nn_box.move_to(nn_target + UP * 1.3)

        self.play(FadeIn(nn_box, shift=UP * 0.3), run_time=0.25)
        self.play(nn_box.animate.move_to(nn_target), run_time=0.42, rate_func=rush_into)
        dynamic_group.add(nn_box)

        self.play(
            Rotate(dynamic_group, angle=-32 * DEGREES, about_point=beam.get_center()),
            run_time=0.42,
            rate_func=rush_from,
        )
        self.play(
            Rotate(dynamic_group, angle=8 * DEGREES, about_point=beam.get_center()),
            run_time=0.22,
            rate_func=smooth,
        )
        self.play(
            Rotate(dynamic_group, angle=-4 * DEGREES, about_point=beam.get_center()),
            run_time=0.2,
            rate_func=smooth,
        )

        self.wait(0.4)

        challenge_3_group = Group(pivot, dynamic_group)
        frame_3 = frame_1.copy().move_to(slot_right)

        target_challenge_3 = challenge_3_group.copy()
        target_challenge_3.scale_to_fit_width(frame_3.width - 0.3)
        if target_challenge_3.height > frame_3.height - 0.3:
            target_challenge_3.scale_to_fit_height(frame_3.height - 0.3)
        target_challenge_3.move_to(slot_right)

        self.play(Transform(challenge_3_group, target_challenge_3), run_time=0.75)

        label_3_text = Tex(
            "Efficiency",
            font_size=label_font_size,
            color=WHITE,
        )
        label_3_icon = create_fontawesome_times_icon(color=RED, font_size=label_font_size)
        label_3 = VGroup(label_3_icon, label_3_text).arrange(RIGHT, buff=0.12).next_to(frame_3, UP, buff=0.12)

        self.play(Create(frame_3), Write(label_3), FadeIn(challenge_1_slot), FadeIn(challenge_2_slot))
        self.wait(4)
