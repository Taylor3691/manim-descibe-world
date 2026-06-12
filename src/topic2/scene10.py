from pathlib import Path

from manim import *

from video_mobject import VideoMobject, create_video_stage_frame


VIDEO_DIR = Path("assets/videos")


def resolve_video_path(name):
    path = VIDEO_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing video asset: {path}")
    return path


def fit_video_preserving_aspect(video, frame, padding=0.06):
    video.move_to(frame.get_center())
    scale_factor = min(
        (frame.width - padding) / video.width,
        (frame.height - padding) / video.height,
    )
    video.scale(scale_factor)
    video.pause()


def create_video_grid_panel(video_name, center, scene, width=4.25, height=2.25):
    frame = create_video_stage_frame(width=width, height=height, center=center)
    video = VideoMobject(resolve_video_path(video_name), loop=True)
    video.set_time_source(lambda: scene.time)
    fit_video_preserving_aspect(video, frame, padding=0.04)
    return Group(frame, video), video


def create_table_of_contents():
    title = Tex(
        r"\textbf{Physics-Grounded World Models}",
        font_size=48,
    ).to_edge(UP)

    circle_1 = Circle(radius=0.35, color=BLUE_D, stroke_width=3)
    text_1 = Tex("1", font_size=36, color=WHITE).move_to(circle_1)
    group_1 = VGroup(circle_1, text_1)

    circle_2 = Circle(radius=0.35, color=GREEN_D, stroke_width=3)
    text_2 = Tex("2", font_size=36, color=WHITE).move_to(circle_2)
    group_2 = VGroup(circle_2, text_2)

    circle_3 = Circle(radius=0.35, color=RED_D, stroke_width=3)
    text_3 = Tex("3", font_size=36, color=WHITE).move_to(circle_3)
    group_3 = VGroup(circle_3, text_3)

    circles_group = VGroup(group_1, group_2, group_3).arrange(RIGHT, buff=3.0)
    circles_group.move_to(ORIGIN + UP * 0.8)

    line_1_2 = Line(
        group_1.get_center() + RIGHT * 0.4,
        group_2.get_center() + LEFT * 0.4,
        color=WHITE,
        stroke_width=2.5,
    )
    line_2_3 = Line(
        group_2.get_center() + RIGHT * 0.4,
        group_3.get_center() + LEFT * 0.4,
        color=WHITE,
        stroke_width=2.5,
    )

    label_1 = Tex("Generation", font_size=36, color=WHITE)
    label_1.next_to(group_1, DOWN, buff=0.35)

    label_2 = Tex("Interaction", font_size=36, color=WHITE)
    label_2.next_to(group_2, DOWN, buff=0.35)

    label_3 = Tex("Evaluation", font_size=36, color=WHITE)
    label_3.next_to(group_3, DOWN, buff=0.35)

    toc = VGroup(
        title,
        group_1,
        group_2,
        group_3,
        line_1_2,
        line_2_3,
        label_1,
        label_2,
        label_3,
    )
    return {
        "toc": toc,
        "title": title,
        "circle_1": circle_1,
        "text_1": text_1,
        "circle_2": circle_2,
        "text_2": text_2,
        "circle_3": circle_3,
        "text_3": text_3,
        "group_1": group_1,
        "group_2": group_2,
        "group_3": group_3,
        "line_1_2": line_1_2,
        "line_2_3": line_2_3,
        "label_1": label_1,
        "label_2": label_2,
        "label_3": label_3,
    }


class Scene10(Scene):
    def construct(self):
        title = Tex(
            r"\textbf{Diverse Physics in Interactions}",
            font_size=48,
        ).to_edge(UP, buff=0.35)

        video_names = [
            "venice.mp4",
            "boat_river.mp4",
            "cloth_hang.mp4",
            "smoke_can.mp4",
            "flower_wind.mp4",
            "snow_man.mp4",
        ]

        panels = []
        videos = []
        for index, video_name in enumerate(video_names):
            row = index // 3
            col = index % 3
            center = RIGHT * ((col - 1) * 4.35) + UP * (0.95 - row * 2.55)
            panel, video = create_video_grid_panel(video_name, center, self)
            panels.append(panel)
            videos.append(video)

        frames = VGroup(*(panel[0] for panel in panels))
        video_group = Group(*videos)

        self.play(Write(title), run_time=1.0)
        self.wait(0.35)
        self.play(
            LaggedStart(
                *[FadeIn(frame, shift=UP * 0.1) for frame in frames],
                lag_ratio=0.08,
            ),
            run_time=0.85,
        )
        self.play(
            *[FadeIn(video) for video in videos],
            run_time=0.75,
        )

        for video in videos:
            video.play()

        self.wait(18.0)

        for video in videos:
            video.pause()

        self.play(
            FadeOut(title),
            FadeOut(frames),
            FadeOut(video_group),
            run_time=0.8,
        )

        for video in videos:
            video.close()

        self.clear()

        toc_parts = create_table_of_contents()
        self.play(
            FadeIn(toc_parts["title"]),
            FadeIn(toc_parts["group_1"]),
            FadeIn(toc_parts["label_1"]),
            Create(toc_parts["line_1_2"]),
            FadeIn(toc_parts["group_2"]),
            FadeIn(toc_parts["label_2"]),
            Create(toc_parts["line_2_3"]),
            FadeIn(toc_parts["group_3"]),
            FadeIn(toc_parts["label_3"]),
            run_time=1.2,
        )
        self.wait(18.0)

        self.play(
            toc_parts["label_3"].animate.scale(1.4).set_weight(BOLD),
            toc_parts["text_3"].animate.scale(1.2).set_weight(BOLD).set_color(BLACK),
            toc_parts["circle_3"].animate.set_fill(RED_D, opacity=1),
            toc_parts["title"].animate.set_opacity(0.3),
            toc_parts["circle_1"].animate.set_stroke(opacity=0.3),
            toc_parts["text_1"].animate.set_opacity(0.3),
            toc_parts["circle_2"].animate.set_stroke(opacity=0.3),
            toc_parts["text_2"].animate.set_opacity(0.3),
            toc_parts["label_1"].animate.set_opacity(0.3),
            toc_parts["label_2"].animate.set_opacity(0.3),
            toc_parts["line_1_2"].animate.set_opacity(0.3),
            toc_parts["line_2_3"].animate.set_opacity(0.3),
            run_time=1.2,
        )

        self.wait(1.0)
