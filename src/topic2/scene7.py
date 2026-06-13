from pathlib import Path

from manim import *

from video_mobject import VideoMobject, create_video_stage_frame


VIDEO_DIR = Path("assets/videos")


def fit_video_preserving_aspect(video, frame, padding=0.14):
    video.move_to(frame.get_center())
    scale_factor = min(
        (frame.width - padding) / video.width,
        (frame.height - padding) / video.height,
    )
    video.scale(scale_factor)
    video.pause()


def create_table_of_contents():
    toc_title = Tex(
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

    label_1 = Text("Generation", font_size=26, color=WHITE)
    label_1.next_to(group_1, DOWN, buff=0.35)

    label_2 = Text("Interaction", font_size=26, color=WHITE)
    label_2.next_to(group_2, DOWN, buff=0.35)

    label_3 = Text("Evaluation", font_size=26, color=WHITE)
    label_3.next_to(group_3, DOWN, buff=0.35)

    return {
        "title": toc_title,
        "circle_1": circle_1,
        "text_1": text_1,
        "group_1": group_1,
        "circle_2": circle_2,
        "text_2": text_2,
        "group_2": group_2,
        "circle_3": circle_3,
        "text_3": text_3,
        "group_3": group_3,
        "line_1_2": line_1_2,
        "line_2_3": line_2_3,
        "label_1": label_1,
        "label_2": label_2,
        "label_3": label_3,
    }


def create_video_panel(video_name, label, center):
    frame = create_video_stage_frame(width=4.45, height=2.9, center=center)
    video = VideoMobject(VIDEO_DIR / f"{video_name}.mp4", loop=False)
    video.set_time_source(lambda: 0)
    fit_video_preserving_aspect(video, frame, padding=0.1)
    label_mob = Tex(label, font_size=30, color=WHITE)
    label_mob.next_to(frame, DOWN, buff=0.2)
    return frame, video, label_mob


def create_goal_text():
    goal_parts = VGroup(
        Tex(r"\textbf{Goal:} Predicting", font_size=32, color=WHITE),
        Tex("physical dynamics", font_size=32, color=YELLOW),
        Tex("of generated scenes under applied", font_size=32, color=WHITE),
        Tex(r"$3$D actions", font_size=32, color=YELLOW),
    )
    goal_parts.arrange(RIGHT, buff=0.08)
    if goal_parts.width > config.frame_width - 0.7:
        goal_parts.scale_to_fit_width(config.frame_width - 0.7)
    return goal_parts


class Scene7(Scene):
    def construct(self):
        # PART 1: TRANSITION

        toc = create_table_of_contents()

        self.play(
            FadeIn(toc["title"]),
            FadeIn(toc["group_1"]),
            FadeIn(toc["label_1"]),
            Create(toc["line_1_2"]),
            FadeIn(toc["group_2"]),
            FadeIn(toc["label_2"]),
            Create(toc["line_2_3"]),
            FadeIn(toc["group_3"]),
            FadeIn(toc["label_3"]),
            run_time=1.2,
        )
        self.wait(7.0)

        self.play(
            toc["label_2"].animate.scale(1.4).set_weight(BOLD),
            toc["text_2"].animate.scale(1.2).set_weight(BOLD).set_color(BLACK),
            toc["circle_2"].animate.set_fill(GREEN_D, opacity=1),
            toc["circle_1"].animate.set_stroke(opacity=0.3),
            toc["text_1"].animate.set_opacity(0.3),
            toc["circle_3"].animate.set_stroke(opacity=0.3),
            toc["text_3"].animate.set_opacity(0.3),
            toc["label_1"].animate.set_opacity(0.3),
            toc["label_3"].animate.set_opacity(0.3),
            toc["line_1_2"].animate.set_opacity(0.3),
            toc["line_2_3"].animate.set_opacity(0.3),
            run_time=1.2,
        )

        self.wait(1.5)

        self.play(FadeOut(*self.mobjects), run_time=0.8)
        self.clear()

        # PART 2: SCENE 7A

        title = Tex(
            r"\textbf{Generating Dynamic Scenes under Actions}",
            font_size=48,
        ).to_edge(UP, buff=0.5)

        goal = create_goal_text()
        goal.next_to(title, DOWN, buff=0.34)

        video_y = -0.48
        x_positions = [-4.58, 0, 4.58]
        panels = [
            create_video_panel("cloth_hang", "Wind Force Field", [x_positions[0], video_y, 0]),
            create_video_panel("jam_cake", "Gravity Field", [x_positions[1], video_y, 0]),
            create_video_panel("venice", "$3$D Force Field", [x_positions[2], video_y, 0]),
        ]
        frames = VGroup(*(frame for frame, _video, _label in panels))
        videos = Group(*(video for _frame, video, _label in panels))
        labels = VGroup(*(label for _frame, _video, label in panels))

        for video in videos:
            video.set_time_source(lambda video=video: self.time)

        self.play(Write(title), run_time=1.0)
        self.wait(0.4)
        self.play(Write(goal), run_time=1.0)
        self.wait(0.5)
        self.play(
            *[FadeIn(frame, shift=UP * 0.12) for frame in frames],
            run_time=0.7,
        )
        self.play(
            *[FadeIn(video) for video in videos],
            *[Write(label) for label in labels],
            run_time=0.8,
        )

        for video in videos:
            video.play()

        self.wait(min(8.0, *(video.duration for video in videos)))

        for video in videos:
            video.pause()

        self.wait(3.5)

        for video in videos:
            video.close()
