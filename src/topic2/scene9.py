from pathlib import Path

import numpy as np
from PIL import Image
from manim import *

from video_mobject import VideoMobject, create_video_stage_frame, freeze_video_frame


IMAGE_DIR = Path("assets/images")
VIDEO_DIR = Path("assets/videos")


def resolve_image_path(name):
    path = IMAGE_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing image asset: {path}")
    return path


def resolve_video_path(name):
    path = VIDEO_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing video asset: {path}")
    return path


def fit_video_preserving_aspect(video, frame, padding=0.12):
    video.move_to(frame.get_center())
    scale_factor = min(
        (frame.width - padding) / video.width,
        (frame.height - padding) / video.height,
    )
    video.scale(scale_factor)
    video.pause()


def create_video_panel(video_name, label, center):
    frame = create_video_stage_frame(width=4.2, height=2.8, center=center)
    video = VideoMobject(resolve_video_path(video_name), loop=False)
    video.set_time_source(lambda: 0)
    fit_video_preserving_aspect(video, frame, padding=0.1)

    label_mob = Tex(label, font_size=29, color=WHITE)
    label_mob.next_to(frame, DOWN, buff=0.18)

    return frame, video, label_mob


def create_looping_video_panel(video_name, label, center, scene, width=3.2, height=1.75):
    frame = create_video_stage_frame(width=width, height=height, center=center)
    video = VideoMobject(resolve_video_path(video_name), loop=True)
    video.set_time_source(lambda: scene.time)
    fit_video_preserving_aspect(video, frame, padding=0.0)

    label_mob = Tex(label, font_size=28, color=WHITE)
    label_mob.next_to(frame, DOWN, buff=0.14)
    return frame, video, label_mob


def fit_image_to_box(image, width, height):
    image.set_width(width)
    if image.height > height:
        image.set_height(height)
    return image


def create_image_panel(name, label, width=3.1, max_height=1.82, font_size=28):
    image = ImageMobject(str(resolve_image_path(name)))
    fit_image_to_box(image, width, max_height)
    image.set_z_index(1)

    label_mob = Tex(label, font_size=font_size, color=WHITE)
    label_mob.next_to(image, DOWN, buff=0.16)
    label_mob.set_z_index(3)
    return Group(image, label_mob)


def create_soft_edge_image(name, width=2.42, edge_size=25):
    image = Image.open(resolve_image_path(name)).convert("RGBA")
    w, h = image.size
    edge_size = max(1, int(edge_size))

    x = np.minimum(np.arange(w), np.arange(w)[::-1]) / edge_size
    y = np.minimum(np.arange(h), np.arange(h)[::-1]) / edge_size
    mask = np.clip(np.minimum(y[:, None], x[None, :]), 0, 1)
    mask = mask * mask * (3 - 2 * mask)

    alpha = Image.fromarray(np.uint8(mask * 255), mode="L")
    image.putalpha(alpha)

    image_mobject = ImageMobject(np.asarray(image))
    image_mobject.set_width(width)
    image_mobject.set_z_index(0)
    return image_mobject


def make_cube_scene_panel(image_name, label):
    cube_width = 2.25
    cube_height = 1.48
    front_pad = 0.08

    image = create_soft_edge_image(
        image_name,
        width=(cube_width + front_pad) * 1.08,
        edge_size=150,
    )
    image.move_to(ORIGIN + RIGHT * 0.16 + UP * 0.1)

    front = Rectangle(
        width=cube_width + front_pad,
        height=cube_height + front_pad,
        color=WHITE,
        stroke_width=2.0,
    ).move_to(ORIGIN)
    front.set_z_index(4)

    offset = RIGHT * 0.34 + UP * 0.28
    side_edges = VGroup()
    for corner in [front.get_corner(UL), front.get_corner(UR), front.get_corner(DR), front.get_corner(DL)]:
        edge = DashedLine(
            corner,
            corner + offset,
            color=GRAY_B,
            stroke_width=1.8,
            dash_length=0.06,
            dashed_ratio=0.55,
        )
        edge.set_z_index(3)
        side_edges.add(edge)

    label_mob = Tex(label, font_size=28, color=WHITE)
    label_mob.next_to(front, DOWN, buff=0.14)
    label_mob.set_z_index(5)
    return Group(side_edges, image, front, label_mob)


def create_numbered_challenge(number, text, color=YELLOW):
    circle = Circle(radius=0.2, color=color, stroke_width=3)
    number_text = Tex(f"${number}$", font_size=32, color=WHITE).move_to(circle)
    label = Tex(text, font_size=32, color=WHITE)
    label.next_to(circle, RIGHT, buff=0.22)
    return VGroup(circle, number_text, label)


def make_arrow(start, end, stroke_width=3.2):
    arrow = Arrow(
        start=start,
        end=end,
        buff=0,
        color=WHITE,
        stroke_width=stroke_width,
        tip_shape=StealthTip,
        tip_length=0.12,
        max_tip_length_to_length_ratio=0.12,
        max_stroke_width_to_length_ratio=10,
    )
    arrow.set_z_index(5)
    return arrow


def make_dashed_arrow(start, end, stroke_width=2.6):
    arrow = make_arrow(start, end, stroke_width=stroke_width)
    dashed = DashedVMobject(arrow, num_dashes=18, dashed_ratio=0.62)
    dashed.set_z_index(4)
    return dashed


def make_curved_flow_arrow(start, end, angle=-TAU / 4, stroke_width=3.0, color=WHITE):
    arrow = CurvedArrow(
        start,
        end,
        angle=angle,
        color=color,
        stroke_width=stroke_width,
        tip_shape=StealthTip,
        tip_length=0.12,
    )
    arrow.set_z_index(6)
    return arrow


def create_text_box(text, width=2.55, height=1.22, font_size=30, color=BLUE_D):
    box = RoundedRectangle(
        corner_radius=0.06,
        width=width,
        height=height,
        color=color,
        fill_opacity=0.22,
        stroke_width=2.1,
    )
    label = Tex(text, font_size=font_size, color=WHITE)
    label.move_to(box.get_center())
    return VGroup(box, label)


def create_fontawesome_icon(icon_command, color=YELLOW, font_size=45):
    template = TexTemplate()
    template.add_to_preamble(r"\usepackage{fontawesome5}")
    return Tex(
        icon_command,
        tex_template=template,
        font_size=font_size,
        color=color,
    )


def add_left_icon_to_text_box(text_box, icon_command, color=YELLOW, font_size=34):
    icon = create_fontawesome_icon(icon_command, color=color, font_size=font_size)
    icon.move_to(text_box[0].get_left() + RIGHT * 0.36)
    text_box[1].shift(RIGHT * 0.34)
    icon.set_z_index(10)
    text_box.add(icon)
    return text_box


class Scene9(Scene):
    def construct(self):
        # SCENE 9A
        title = Tex(
            r"\textbf{Challenge: }",
            r"\textbf{Multi-Physics}",
            r"\textbf{ Simulation is Hard}",
            font_size=40,
        ).to_edge(UP, buff=0.42)
        title[1].set_color(YELLOW)

        video_y = 0.75
        x_positions = [-4.32, 0, 4.32]
        panels = [
            create_video_panel("duck-1.mp4", "PhysGen", [x_positions[0], video_y, 0]),
            create_video_panel("duck-3.mp4", "Tora", [x_positions[1], video_y, 0]),
            create_video_panel("duck-4.mp4", "CogVideoX-12V", [x_positions[2], video_y, 0]),
        ]

        frames = VGroup(*(frame for frame, _video, _label in panels))
        videos = Group(*(video for _frame, video, _label in panels))
        labels = VGroup(*(label for _frame, _video, label in panels))

        challenge_1 = create_numbered_challenge(
            1,
            "Inaccurate Multi-Physics Simulation",
            color=YELLOW,
        )
        challenge_2 = create_numbered_challenge(
            2,
            "Missing Physical States",
            color=RED_D,
        )
        challenges = VGroup(challenge_1, challenge_2).arrange(RIGHT, buff=1.05)
        challenges.move_to(DOWN * 2.0)
        if challenges.width > config.frame_width - 0.8:
            challenges.scale_to_fit_width(config.frame_width - 0.8)
            challenges.move_to(DOWN * 2.0)

        for video in videos:
            video.set_time_source(lambda video=video: self.time)

        self.play(Write(title), run_time=1.0)
        self.wait(5.5)

        self.play(
            *[FadeIn(frame, shift=UP * 0.12) for frame in frames],
            run_time=1.0,
        )
        self.play(
            *[FadeIn(video) for video in videos],
            *[Write(label) for label in labels],
            run_time=0.9,
        )

        for video in videos:
            video.play()

        self.wait(8.0)
        self.play(
            FadeIn(VGroup(challenge_1[0], challenge_1[1]), scale=0.7),
            Write(challenge_1[2]),
            run_time=0.8,
        )
        self.wait(3.0)
        self.play(
            FadeIn(VGroup(challenge_2[0], challenge_2[1]), scale=0.7),
            Write(challenge_2[2]),
            run_time=0.8,
        )

        self.wait(5.0)

        for video in videos:
            video.pause()

        frozen_videos = Group(*(freeze_video_frame(video) for video in videos))
        self.add(*frozen_videos)
        self.remove(*videos)

        # SCENE 9B
        self.play(FadeOut(*self.mobjects), run_time=0.8)
        self.clear()

        for video in videos:
            video.close()

        title_9b = Tex(
            r"\textbf{Video model to improve multi-physics simulation?}",
            font_size=40,
        ).to_edge(UP, buff=0.45)

        physics_simulator = create_text_box(
            r"\textbf{Physics}\\\textbf{Simulator}",
            width=2.58,
            height=1.22,
            font_size=30,
            color=RED_D,
        ).move_to(LEFT * 2.7 + UP * 1.2)
        add_left_icon_to_text_box(
            physics_simulator,
            r"\faAtom",
            color=WHITE,
            font_size=42,
        )
        warning_icon = create_fontawesome_icon(
            r"\faExclamationTriangle",
            color=YELLOW,
            font_size=42,
        )
        warning_icon.move_to(physics_simulator[0].get_corner(UR) + UP * 0.05 + RIGHT * 0.05)
        warning_icon.set_z_index(20)

        video_generator = create_text_box(
            r"\textbf{Video}\\\textbf{Generator}",
            width=2.58,
            height=1.22,
            font_size=30,
            color=BLUE_D,
        ).move_to(RIGHT * 2.7 + UP * 1.2)
        add_left_icon_to_text_box(
            video_generator,
            r"\faPlayCircle",
            color=WHITE,
            font_size=42,
        )

        improvement_arrow = make_arrow(
            video_generator[0].get_left() + LEFT * 0.34,
            physics_simulator[0].get_right() + RIGHT * 0.34,
            stroke_width=3.3,
        )
        improvement_label = Tex(r"\textbf{improve?}", font_size=29, color=WHITE)
        improvement_label.next_to(improvement_arrow, UP, buff=0.18)

        rotate_icon = create_fontawesome_icon(
            r"\faSync",
            color=GREEN,
            font_size=46,
        )
        rotate_icon.move_to(improvement_arrow.get_center())
        rotate_icon.set_opacity(0)

        limitation_1 = create_numbered_challenge(
            1,
            "Cannot take actions as input",
            color=YELLOW,
        )
        limitation_2 = create_numbered_challenge(
            2,
            r"Too few \{Action, Video\} pairs",
            color=YELLOW,
        )
        limitations = VGroup(limitation_1, limitation_2).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        limitations.move_to(DOWN * 0.98)
        if limitations.width > config.frame_width - 1.0:
            limitations.scale_to_fit_width(config.frame_width - 1.0)
            limitations.move_to(DOWN * 0.98)

        lightbulb_icon = create_fontawesome_icon(
            r"\faLightbulb",
            color=YELLOW,
            font_size=42,
        )
        wonderplay_text = Tex(
            r"\textbf{WonderPlay: Using a Hybrid-model}",
            font_size=36,
            color=WHITE,
        )
        wonderplay = VGroup(lightbulb_icon, wonderplay_text).arrange(RIGHT, buff=0.28)
        wonderplay.next_to(limitation_2, DOWN, buff=0.6)

        self.wait(0.5)
        self.play(Write(title_9b), run_time=1.0)
        self.wait(1.0)
        self.play(
            FadeIn(physics_simulator, shift=RIGHT * 0.12),
            FadeIn(warning_icon, scale=1.35),
            FadeIn(video_generator, shift=LEFT * 0.12),
            run_time=1.2,
        )
        self.play(GrowArrow(improvement_arrow), Write(improvement_label), run_time=0.75)
        self.wait(11.0)
        self.play(
            FadeIn(VGroup(limitation_1[0], limitation_1[1]), scale=0.7),
            Write(limitation_1[2]),
            run_time=1.2,
        )
        self.wait(11.0)
        self.play(
            FadeIn(VGroup(limitation_2[0], limitation_2[1]), scale=0.7),
            Write(limitation_2[2]),
            run_time=1.2,
        )
        self.wait(3.0)
        self.play(
            FadeOut(improvement_arrow),
            FadeOut(improvement_label),
            run_time=0.5,
        )
        self.wait(0.5)
        self.add(rotate_icon)
        rotate_icon.set_opacity(1)
        self.play(
            Rotate(rotate_icon, angle=TAU, about_point=rotate_icon.get_center(), rate_func=linear),
            physics_simulator.animate.shift(RIGHT * 0.45),
            warning_icon.animate.shift(RIGHT * 0.45),
            video_generator.animate.shift(LEFT * 0.45),
            FadeIn(lightbulb_icon, scale=1.25),
            Write(wonderplay_text),
            run_time=1.0,
        )
        self.wait(5.0)

        # SCENE 9C
        title_9c = Tex(
            r"\textbf{WonderPlay}",
            r"\textbf{: Hybrid Generative Simulator}",
            font_size=40,
        ).to_edge(UP, buff=0.35)
        title_9c[0].set_color(YELLOW)

        simulator_panel = RoundedRectangle(
            corner_radius=0.04,
            width=3.6,
            height=5.25,
            color=WHITE,
            stroke_width=2.4,
            fill_opacity=0,
        ).move_to(DOWN * 0.12)
        simulator_title = Tex(r"\textbf{WonderPlay}", font_size=35, color=YELLOW)
        simulator_title.move_to(simulator_panel.get_top() + DOWN * 0.55)

        physics_target = simulator_panel.get_center() + UP * 0.82
        video_target = simulator_panel.get_center() + DOWN * 1.45

        input_panel = create_image_panel("smoke.png", "Input Image", width=3.18, max_height=1.7)
        input_panel.move_to(LEFT * 4.35 + UP * 1.35)

        scene_panel = make_cube_scene_panel("smoke.png", "3D Scene")
        scene_panel.move_to(LEFT * 4.35 + DOWN * 1.62)

        flags_x = input_panel[0].get_left()[0] - 0.42
        flags_arrow = make_curved_flow_arrow(
            [flags_x, (input_panel[0].get_bottom() + DOWN * 0.18)[1], 0],
            [flags_x, (scene_panel[2].get_top() + UP * 0.18)[1], 0],
            angle=TAU / 4,
            stroke_width=3.0,
        )
        flags_label = Tex(r"\textbf{FLAGS}", font_size=27, color=WHITE)
        flags_label.rotate(PI / 2)
        flags_label.next_to(flags_arrow, LEFT, buff=0.18)

        coarse_frame, coarse_video, coarse_label = create_looping_video_panel(
            "smoke-1.mp4",
            "Coarse Simulation",
            RIGHT * 4.45 + UP * 1.5,
            self,
        )
        generated_frame, generated_video, generated_label = create_looping_video_panel(
            "smoke-2.mp4",
            "Generated Video",
            RIGHT * 4.45 + DOWN * 1.72,
            self,
        )

        physics_to_coarse = make_dashed_arrow(
            physics_target + RIGHT * 1.42,
            coarse_frame.get_left() + LEFT * 0.16,
            stroke_width=2.5,
        )
        generator_to_generated = make_dashed_arrow(
            video_target + RIGHT * 1.42,
            generated_frame.get_left() + LEFT * 0.16,
            stroke_width=2.5,
        )

        physics_bottom = physics_target + DOWN * 0.61
        generator_top = video_target + UP * 0.61
        model_down_arrow = make_curved_flow_arrow(
            physics_bottom + LEFT * 0.28 + DOWN * 0.2,
            generator_top + LEFT * 0.28 + UP * 0.2,
            angle=TAU / 4,
            color=RED_D,
        )
        model_up_arrow = make_curved_flow_arrow(
            generator_top + RIGHT * 0.28 + UP * 0.2,
            physics_bottom + RIGHT * 0.28 + DOWN * 0.2,
            angle=TAU / 4,
            color=BLUE_D,
        )
        video_arrow_left_x = coarse_frame.get_center()[0] - 0.42
        video_arrow_right_x = coarse_frame.get_center()[0] + 0.42
        video_arrow_top_y = coarse_label.get_bottom()[1] - 0.26
        video_arrow_bottom_y = generated_frame.get_top()[1] + 0.28
        video_down_arrow = make_curved_flow_arrow(
            [video_arrow_left_x, video_arrow_top_y, 0],
            [video_arrow_left_x, video_arrow_bottom_y, 0],
            angle=TAU / 4,
            color=RED_D,
        )
        video_up_arrow = make_curved_flow_arrow(
            [video_arrow_right_x, video_arrow_bottom_y, 0],
            [video_arrow_right_x, video_arrow_top_y, 0],
            angle=TAU / 4,
            color=BLUE_D,
        )

        self.play(
            FadeOut(title_9b),
            FadeOut(warning_icon),
            FadeOut(rotate_icon),
            FadeOut(limitations),
            FadeOut(wonderplay),
            run_time=0.65,
        )
        self.wait(0.5)
        self.play(
            Write(title_9c),
            FadeIn(simulator_panel),
            Write(simulator_title),
            physics_simulator.animate.shift(physics_target - physics_simulator[0].get_center()),
            video_generator.animate.shift(video_target - video_generator[0].get_center()),
            run_time=1.0,
        )
        self.wait(5.0)
        self.play(
            FadeIn(input_panel, shift=RIGHT * 0.12),
            run_time=1.0,
        )
        self.wait(0.5)
        self.play(
            Create(flags_arrow),
            run_time=0.75,
        )
        self.play(
            Write(flags_label),
            FadeIn(scene_panel, shift=UP * 0.12),
            run_time=1.0,
        )
        self.wait(3.0)
        self.play(
            FadeIn(coarse_frame),
            FadeIn(coarse_video),
            Write(coarse_label),
            Create(physics_to_coarse),
            run_time=1.2,
        )
        coarse_video.play()
        self.wait(0.5)
        self.play(
            FadeOut(physics_to_coarse),
            run_time=0.45,
        )
        self.wait(10.0)
        self.play(
            Create(model_down_arrow),
            Create(video_down_arrow),
            run_time=0.75,
        )
        self.play(
            FadeIn(generated_frame),
            FadeIn(generated_video),
            Write(generated_label),
            Create(generator_to_generated),
            run_time=1.2,
        )
        generated_video.play()
        self.wait(0.5)
        self.play(
            FadeOut(generator_to_generated),
            run_time=0.45,
        )
        self.wait(1.0)
        self.play(
            Create(model_up_arrow),
            Create(video_up_arrow),
            run_time=0.75,
        )
        self.wait(0.5)

        refined_video = VideoMobject(resolve_video_path("smoke-2.mp4"), loop=True)
        refined_video.set_time_source(lambda: self.time)
        fit_video_preserving_aspect(refined_video, coarse_frame, padding=0.0)
        refined_label = Tex("Refined Simulation", font_size=28, color=WHITE)
        refined_label.move_to(coarse_label)

        self.play(
            FadeOut(coarse_video),
            FadeIn(refined_video),
            Transform(coarse_label, refined_label),
            run_time=0.65,
        )
        refined_video.play()
        self.wait(6.0)

        coarse_video.close()
        generated_video.close()
        refined_video.close()
