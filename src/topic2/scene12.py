from manim import *


def create_number_circle(number, color=BLUE_D):
    circle = Circle(radius=0.24, color=color, stroke_width=3.2)
    number_text = Tex(f"${number}$", font_size=34, color=WHITE).move_to(circle)
    return VGroup(circle, number_text)


def create_takeaway_label(number, text_parts, highlighted_indices):
    number_circle = create_number_circle(number, color=BLUE_D)
    label = Tex(*text_parts, font_size=35, color=WHITE)
    for index in highlighted_indices:
        label[index].set_color(YELLOW)

    row = VGroup(number_circle, label).arrange(RIGHT, buff=0.34, aligned_edge=DOWN)
    return row


def create_multiline_takeaway_label(number, lines):
    number_circle = create_number_circle(number, color=BLUE_D)
    label = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    row = VGroup(number_circle, label).arrange(RIGHT, buff=0.34, aligned_edge=UP)
    return row


def create_takeaway_messages():
    takeaway_1 = create_takeaway_label(
        1,
        (
            r"\textbf{$\mathbf{3}$D models}",
            r"\textbf{ excel at }",
            r"\textbf{static}",
            r"\textbf{ world generation.}",
        ),
        highlighted_indices=(0, 2),
    )
    takeaway_2_line_1 = Tex(
        r"\textbf{The best }",
        r"\textbf{open-source}",
        r"\textbf{ video models are}",
        font_size=35,
        color=WHITE,
    )
    takeaway_2_line_1[1].set_color(YELLOW)
    takeaway_2_line_2 = Tex(
        r"\textbf{as good as closed-source video models.}",
        font_size=35,
        color=WHITE,
    )
    takeaway_2 = create_multiline_takeaway_label(
        2,
        (takeaway_2_line_1, takeaway_2_line_2),
    )
    takeaway_3 = create_takeaway_label(
        3,
        (
            r"\textbf{Video models are weak in generating }",
            r"\textbf{larger worlds}",
            r"\textbf{.}",
        ),
        highlighted_indices=(1,),
    )

    messages = VGroup(takeaway_1, takeaway_2, takeaway_3).arrange(
        DOWN,
        aligned_edge=LEFT,
        buff=0.58,
    )
    if messages.width > config.frame_width - 1.0:
        messages.scale_to_fit_width(config.frame_width - 1.0)
    messages.move_to(DOWN * 0.25)
    return messages


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


class Scene12(Scene):
    def construct(self):
        title = Tex(
            r"\textbf{Evaluation: Takeaway Messages}",
            font_size=46,
        ).to_edge(UP, buff=0.42)

        messages = create_takeaway_messages()

        self.play(Write(title), run_time=1.2)
        self.wait(5.0)

        self.play(
            FadeIn(messages[0][0], scale=0.75),
            run_time=0.75,
        )
        self.play(
            Write(messages[0][1]),
            run_time=1.8,
        )
        self.wait(11.0)

        self.play(
            FadeIn(messages[1][0], scale=0.75),
            run_time=0.75,
        )
        self.play(
            Write(messages[1][1]),
            run_time=2.5,
        )
        self.wait(17.0)

        self.play(
            FadeIn(messages[2][0], scale=0.75),
            run_time=0.75,
        )
        self.play(
            Write(messages[2][1]),
            run_time=1.8,
        )
        self.wait(22.0)

        self.play(FadeOut(title), FadeOut(messages), run_time=0.8)
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
        self.wait(22.0)
