from pathlib import Path

import cv2
import numpy as np
from manim import *

from video_mobject import VideoMobject, create_video_stage_frame


IMAGE_DIR = Path("assets/images")
VIDEO_DIR = Path("assets/videos")
WORKFLOW_GAP = 0.98
ARROW_PAD = 0.16


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


def fit_image_to_box(image, width, height):
    image.set_width(width)
    if image.height > height:
        image.set_height(height)
    return image


def fit_video_preserving_aspect(video, frame, padding=0.08):
    video.move_to(frame.get_center())
    scale_factor = min(
        (frame.width - padding) / video.width,
        (frame.height - padding) / video.height,
    )
    video.scale(scale_factor)
    video.pause()


class CroppedVideoMobject(ImageMobject):
    def __init__(self, filename, horizontal_crop=0.16, **kwargs):
        self.filename = str(filename)
        self.loop = kwargs.pop("loop", False)
        self.horizontal_crop = horizontal_crop
        self.cap = cv2.VideoCapture(self.filename)
        if not self.cap.isOpened():
            raise FileNotFoundError(f"Cannot open video file: {self.filename}")

        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.duration = self.frame_count / self.fps if self.fps > 0 else 0
        self.time_source = None
        self.scene_start_time = 0.0
        self.paused_video_time = 0.0
        self.is_playing = False
        self.current_frame_idx = 0
        self.last_rendered_index = -1
        self.last_frame = np.zeros((4, 4, 4), dtype=np.uint8)

        first_frame = self._seek_and_read(0)
        super().__init__(first_frame, **kwargs)
        self.add_updater(self._video_updater)

    def _crop_frame(self, frame):
        crop_pixels = int(frame.shape[1] * self.horizontal_crop)
        if crop_pixels <= 0 or crop_pixels * 2 >= frame.shape[1]:
            return frame
        return frame[:, crop_pixels:-crop_pixels, :]

    def _seek_and_read(self, index):
        index = max(0, min(index, max(0, self.frame_count - 1)))
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, index)
        self.current_frame_idx = index
        ok, frame = self.cap.read()
        if not ok:
            return self.last_frame
        rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        cropped = np.ascontiguousarray(self._crop_frame(rgba))
        self.last_frame = cropped
        self.last_rendered_index = index
        self.current_frame_idx = index + 1
        return self.last_frame

    def _read_until(self, target_index):
        target_index = max(0, min(target_index, max(0, self.frame_count - 1)))
        if target_index < self.last_rendered_index:
            return self._seek_and_read(target_index)

        if target_index >= self.current_frame_idx + 8:
            return self._seek_and_read(target_index)

        while self.current_frame_idx <= target_index:
            ok, frame = self.cap.read()
            if not ok:
                return self.last_frame
            rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            self.last_frame = np.ascontiguousarray(self._crop_frame(rgba))
            self.last_rendered_index = self.current_frame_idx
            self.current_frame_idx += 1

        return self.last_frame

    def set_time_source(self, time_source):
        self.time_source = time_source

    def _current_scene_time(self):
        if self.time_source is None:
            return 0.0
        return float(self.time_source())

    def _current_video_time(self, scene_time=None):
        if scene_time is None:
            scene_time = self._current_scene_time()
        if self.is_playing:
            return max(0.0, scene_time - self.scene_start_time)
        return self.paused_video_time

    def _video_updater(self, mobject, dt):
        if self.duration <= 0:
            return

        t = self._current_video_time()
        if self.loop:
            t = t % self.duration
        else:
            t = min(t, self.duration)

        frame_index = min(int(t * self.fps), max(0, self.frame_count - 1))
        if not self.is_playing and frame_index == self.last_rendered_index:
            return

        mobject.pixel_array = self._read_until(frame_index)

        if not self.loop and t >= self.duration:
            self.paused_video_time = self.duration
            self.is_playing = False

    def play(self):
        scene_time = self._current_scene_time()
        self.scene_start_time = scene_time - self.paused_video_time
        self.is_playing = True

    def pause(self):
        self.paused_video_time = self._current_video_time()
        self.is_playing = False

    def close(self):
        self.remove_updater(self._video_updater)
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def __deepcopy__(self, memo):
        copied = CroppedVideoMobject(
            self.filename,
            horizontal_crop=self.horizontal_crop,
            loop=self.loop,
        )
        copied.time_source = self.time_source
        copied.scene_start_time = self.scene_start_time
        copied.paused_video_time = self.paused_video_time
        copied.is_playing = self.is_playing
        copied.become(self)
        return copied


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


def create_image_panel(name, label, width=1.8125, max_height=1.8125):
    image = ImageMobject(str(resolve_image_path(name)))
    fit_image_to_box(image, width, max_height)
    image.set_z_index(2)

    border = Rectangle(
        width=image.width,
        height=image.height,
        color=WHITE,
        stroke_width=0.9,
    ).move_to(image)
    border.set_z_index(3)

    label_mob = Tex(label, font_size=27, color=WHITE)
    label_mob.next_to(image, DOWN, buff=0.12)
    label_mob.set_z_index(4)

    return Group(image, border, label_mob)


def create_stacked_inputs():
    gaussian_panel = create_image_panel("3dgs.png", r"$3$D Gaussian")
    material_panel = create_image_panel("material.png", "Material Field")
    inputs = Group(gaussian_panel, material_panel).arrange(DOWN, buff=0.34)
    return inputs


def create_text_box(text, width=2.15, height=1.0, font_size=25, color=BLUE_D):
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


def create_fontawesome_warning_icon(color=YELLOW):
    template = TexTemplate()
    template.add_to_preamble(r"\usepackage{fontawesome5}")
    return Tex(
        r"\faExclamationTriangle",
        tex_template=template,
        font_size=45,
        color=color,
    )


def create_next_state():
    label = Tex(r"Next state \\ $x_{t+1}$", font_size=35, color=WHITE)
    return label


def create_video_panel(video_name, width=3.15, height=2.32):
    frame = create_video_stage_frame(width=width, height=height, center=ORIGIN)
    video = CroppedVideoMobject(resolve_video_path(video_name), horizontal_crop=0.16, loop=True)
    video.set_time_source(lambda: 0)
    video.scale_to_fit_height(frame.height - 0.08)
    video.move_to(frame.get_center())
    video.pause()
    return Group(frame, video), video


class Scene8(Scene):
    def construct(self):
        title = Tex(
            r"\textbf{Prior}",
            r"\textbf{ Physics-Grounded World Models}",
            font_size=44,
        ).to_edge(UP, buff=0.38)
        title[0].set_color(YELLOW)

        subtitle = Tex(
            r"Relying on ",
            r"physics simulation",
            r" to generate ",
            r"future dynamics",
            font_size=33,
            color=WHITE,
        )
        subtitle[1].set_color(BLUE)
        subtitle[3].set_color(BLUE)
        subtitle.next_to(title, DOWN, buff=0.28)

        inputs = create_stacked_inputs()
        simulator = create_text_box(
            r"\textbf{Physics}\\\textbf{Simulator}",
            width=1.72,
            height=1.15,
            font_size=28,
            color=GREEN_D,
        )
        action_label = Tex("Action", font_size=29, color=WHITE)
        action_label.next_to(simulator, DOWN, buff=1.05)
        action_arrow = make_arrow(
            action_label.get_top() + UP * 0.18,
            simulator[0].get_bottom() + DOWN * 0.18,
            stroke_width=3.0,
        )

        next_state = create_next_state()
        renderer = create_text_box(
            r"\textbf{Renderer}",
            width=1.7,
            height=0.95,
            font_size=29,
            color=BLUE_D,
        )
        plant_panel, plant_video = create_video_panel("plant.mp4")

        row_y = -0.62
        main_flow = Group(inputs, simulator, next_state, renderer, plant_panel)
        main_flow.arrange(RIGHT, buff=WORKFLOW_GAP)
        main_flow.move_to([0, row_y, 0])

        action_label.next_to(simulator, DOWN, buff=1.05)
        action_arrow.become(
            make_arrow(
                action_label.get_top() + UP * 0.18,
                simulator[0].get_bottom() + DOWN * 0.18,
                stroke_width=3.0,
            )
        )

        arrows = VGroup(
            make_arrow(
                inputs.get_right() + RIGHT * ARROW_PAD,
                simulator[0].get_left() + LEFT * ARROW_PAD,
            ),
            make_arrow(
                simulator[0].get_right() + RIGHT * ARROW_PAD,
                next_state.get_left() + LEFT * ARROW_PAD,
            ),
            make_arrow(
                next_state.get_right() + RIGHT * ARROW_PAD,
                renderer[0].get_left() + LEFT * ARROW_PAD,
            ),
            make_arrow(
                renderer[0].get_right() + RIGHT * ARROW_PAD,
                plant_panel[0].get_left() + LEFT * ARROW_PAD,
            ),
        )

        workflow = Group(
            inputs,
            simulator,
            action_label,
            action_arrow,
            next_state,
            renderer,
            plant_panel,
            arrows,
        )
        if workflow.width > config.frame_width - 0.75:
            workflow.scale_to_fit_width(config.frame_width - 0.75)
            workflow.move_to([0, row_y, 0])

        citation = Tex(
            r"[\textbf{PhysDreamer}, Zhang \textit{et al.}, ECCV'24]",
            font_size=24,
            color=WHITE,
        )
        citation.to_edge(RIGHT, buff=0.28).shift(DOWN * 2.85)

        red_simulator = create_text_box(
            r"\textbf{Physics}\\\textbf{Simulator}",
            width=1.72,
            height=1.15,
            font_size=28,
            color=RED_D,
        ).move_to(simulator)
        warning_icon = create_fontawesome_warning_icon(color=YELLOW)
        warning_icon.move_to(red_simulator[0].get_corner(UR) + UP * 0.06 + RIGHT * 0.06)
        warning_icon.set_z_index(20)

        self.play(Write(title), run_time=2.0)
        self.wait(1.0)
        self.play(Write(subtitle), run_time=2.0)
        self.wait(4.0)

        self.play(FadeIn(inputs, shift=UP * 0.12), Write(citation), run_time=1.2)
        self.wait(6.0)
        self.play(GrowArrow(arrows[0]), run_time=0.8)
        self.play(
            FadeIn(simulator, shift=RIGHT * 0.12),
            FadeIn(action_label, shift=UP * 0.08),
            GrowArrow(action_arrow),
            run_time=1.2,
        )
        self.wait(0.5)
        self.play(GrowArrow(arrows[1]), FadeIn(next_state, shift=RIGHT * 0.12), run_time=1.2)
        self.wait(3.0)
        self.play(GrowArrow(arrows[2]), FadeIn(renderer, shift=RIGHT * 0.12), run_time=0.8)
        self.play(
            GrowArrow(arrows[3]),
            FadeIn(plant_panel[0]),
            FadeIn(plant_panel[1]),
            run_time=1.2,
        )

        plant_video.set_time_source(lambda: self.time)
        plant_video.play()
        self.wait(min(2.0, plant_video.duration))
        plant_video.pause()

        glow_core = RoundedRectangle(
            corner_radius=0.06,
            width=simulator[0].width + 0.5,
            height=simulator[0].height + 0.5,
            color=RED_D,
            fill_opacity=0.06,
            stroke_width=0,
        ).move_to(simulator[0])
        glow_ring = RoundedRectangle(
            corner_radius=0.08,
            width=simulator[0].width + 0.2,
            height=simulator[0].height + 0.2,
            color=RED_D,
            fill_opacity=0,
            stroke_width=12,
        ).set_stroke(RED_D, width=12, opacity=0.35).move_to(simulator[0])
        glow_group = VGroup(glow_core, glow_ring)

        self.play(
            FadeIn(glow_group, scale=0.92),
            run_time=0.5,
            rate_func=smooth,
        )
        self.play(
            glow_ring.animate.scale(1.08).set_stroke(opacity=0.05),
            glow_core.animate.set_fill(opacity=0.12),
            FadeOut(glow_group, scale=1.05),
            FadeOut(simulator),
            FadeIn(red_simulator, scale=1.02),
            run_time=0.55,
            rate_func=smooth,
        )
        self.play(FadeIn(warning_icon, scale=1.5), run_time=0.35, rate_func=smooth)

        self.wait(1.0)
        plant_video.close()
