from pathlib import Path

from manim import *


IMAGE_DIR = Path("assets/images")


def resolve_image_path(name):
    path = IMAGE_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing image asset: {path}")
    return path


def fit_image_to_box(image, width, height):
    image.set_width(width)
    if image.height > height:
        image.set_height(height)
    return image


def make_arrow(start, end, stroke_width=3.2):
    arrow = Arrow(
        start=start,
        end=end,
        buff=0,
        color=WHITE,
        stroke_width=stroke_width,
        tip_shape=StealthTip,
        tip_length=0.13,
        max_tip_length_to_length_ratio=0.12,
        max_stroke_width_to_length_ratio=10,
    )
    arrow.set_z_index(5)
    return arrow


def create_benchmark_flow():
    benchmark = Tex(r"\textbf{Existing benchmark}", font_size=32, color=WHITE)
    benchmark.move_to(LEFT * 2.65)

    small_text = Tex(
        r"\textbf{Small}",
        r"\textbf{ scenes only}",
        font_size=31,
        color=WHITE,
    )
    small_text[0].set_color(YELLOW)

    models_text = Tex(
        r"\textbf{Can't evaluate }",
        r"\textbf{$3$D/$4$D}",
        r"\textbf{ models}",
        font_size=31,
        color=WHITE,
    )
    models_text[1].set_color(YELLOW)

    label_left_x = 0.35
    branch_y = 0.36
    small_text.move_to([label_left_x + small_text.width / 2, branch_y, 0])
    models_text.move_to([label_left_x + models_text.width / 2, -branch_y, 0])

    arrow_start = benchmark.get_right() + RIGHT * 0.2
    arrow_end_x = label_left_x - 0.22
    arrow_up = make_arrow(
        arrow_start,
        [arrow_end_x, branch_y, 0],
        stroke_width=3.0,
    )
    arrow_down = make_arrow(
        arrow_start,
        [arrow_end_x, -branch_y, 0],
        stroke_width=3.0,
    )

    flow = VGroup(benchmark, arrow_up, arrow_down, small_text, models_text)
    if flow.width > config.frame_width - 1.0:
        flow.scale_to_fit_width(config.frame_width - 1.0)
    return flow


def create_semantic_prompt_panel():
    prompt_lines = VGroup(
        Tex(r"\textit{``A tranquil tableau}", font_size=30, color=WHITE),
        Tex(r"\textit{of an ancient\ldots The scene}", font_size=30, color=WHITE),
        Tex(r"\textit{captures a sense of \ldots''}", font_size=30, color=WHITE),
    ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)

    label = Tex(r"\textbf{Semantic Prompt}", font_size=30, color=WHITE)
    label.next_to(prompt_lines, DOWN, buff=0.42)

    panel = VGroup(prompt_lines, label)
    panel.set_z_index(2)
    return panel


def create_world_panel():
    image = ImageMobject(str(resolve_image_path("tableau.png")))
    fit_image_to_box(image, width=5.65, height=3.25)
    image.set_z_index(2)

    border = Rectangle(
        width=image.width,
        height=image.height,
        color=WHITE,
        stroke_width=1.2,
    ).move_to(image)
    border.set_z_index(3)

    label = Tex(r"\textbf{A World of Multiple Scenes}", font_size=30, color=WHITE)
    label.next_to(image, DOWN, buff=0.34)
    label.set_z_index(4)

    return Group(image, border, label)


def create_problem_box():
    problem = VGroup(
        Tex(r"\textbf{Problem: Semantic prompt only. }", font_size=32, color=WHITE),
        Tex(r"\textbf{No spatial prompts.}", font_size=32, color=YELLOW),
    ).arrange(RIGHT, buff=0.12)

    if problem.width > config.frame_width - 1.45:
        problem.scale_to_fit_width(config.frame_width - 1.45)

    frame = SurroundingRectangle(
        problem,
        color=WHITE,
        buff=0.18,
        stroke_width=2.0,
    )
    return VGroup(frame, problem)


def create_fontawesome_icon(icon_command, color=WHITE, font_size=34):
    template = TexTemplate()
    template.add_to_preamble(r"\usepackage{fontawesome5}")
    return Tex(
        icon_command,
        tex_template=template,
        font_size=font_size,
        color=color,
    )


def create_metric_box(label, icon_command, width=3.15, height=1.15):
    box = RoundedRectangle(
        corner_radius=0.04,
        width=width,
        height=height,
        color=WHITE,
        stroke_width=2.6,
        fill_opacity=0,
    )
    icon = create_fontawesome_icon(icon_command, color=WHITE, font_size=34)
    text = Tex(rf"\textbf{{{label}}}", font_size=35, color=WHITE)
    content = VGroup(icon, text).arrange(RIGHT, buff=0.24)
    content.move_to(box.get_center())
    return VGroup(box, content)


def create_metric_boxes():
    boxes = VGroup(
        create_metric_box("Controllability", r"\faSlidersH", width=3.35),
        create_metric_box("Quality", r"\faStar"),
        create_metric_box("Dynamics", r"\faSync"),
    ).arrange(RIGHT, buff=0.82)
    boxes.move_to(DOWN * 0.25)
    if boxes.width > config.frame_width - 0.8:
        boxes.scale_to_fit_width(config.frame_width - 0.8)
        boxes.move_to(DOWN * 0.25)
    return boxes


def create_worldscore_brace(start_point, end_point, direction, text, color, text_buff=0.28):
    brace = BraceBetweenPoints(
        start_point,
        end_point,
        direction=direction,
        color=color,
        sharpness=0.9,
    )
    label = Tex(text, font_size=36, color=color)
    label.next_to(brace, direction, buff=text_buff)
    return VGroup(brace, label)


def create_worldscore_metrics_scene():
    title = Tex(r"\textbf{WorldScore Metrics}", font_size=50, color=WHITE)
    title.to_edge(UP, buff=0.45)

    boxes = create_metric_boxes()

    static_brace = create_worldscore_brace(
        boxes[0][0].get_corner(UL) + LEFT * 0.05 + UP * 0.46,
        boxes[1][0].get_corner(UR) + RIGHT * 0.05 + UP * 0.46,
        UP,
        r"\textbf{WorldScore-Static}",
        BLUE,
        text_buff=0.22,
    )

    dynamic_brace = create_worldscore_brace(
        boxes[0][0].get_corner(DL) + LEFT * 0.05 + DOWN * 0.36,
        boxes[2][0].get_corner(DR) + RIGHT * 0.05 + DOWN * 0.36,
        DOWN,
        r"\textbf{WorldScore-Dynamic}",
        ORANGE,
        text_buff=0.22,
    )

    return {
        "title": title,
        "boxes": boxes,
        "static_brace": static_brace,
        "dynamic_brace": dynamic_brace,
    }


class Scene11(Scene):
    def construct(self):
        # SCENE 11A
        title = Tex(
            r"\textbf{Existing Evaluation is }",
            r"\textbf{Not Enough}",
            font_size=46,
        ).to_edge(UP, buff=0.38)
        title[1].set_color(YELLOW)

        benchmark_flow = create_benchmark_flow()
        benchmark_flow.next_to(title, DOWN, buff=0.45)

        semantic_prompt = create_semantic_prompt_panel()
        world_panel = create_world_panel()

        content = Group(semantic_prompt, world_panel).arrange(RIGHT, buff=1.3)
        content.move_to(DOWN * 0.45)
        if content.width > config.frame_width - 0.85:
            content.scale_to_fit_width(config.frame_width - 0.85)
            content.move_to(DOWN * 0.45)

        label_y = min(semantic_prompt[1].get_center()[1], world_panel[2].get_center()[1])
        semantic_prompt[1].set_y(label_y)
        world_panel[2].set_y(label_y)

        problem_box = create_problem_box()
        problem_box.to_edge(DOWN, buff=0.82)

        self.play(Write(title), run_time=1.0)
        self.wait(0.5)
        self.play(Write(benchmark_flow[0]), run_time=1.0)
        self.play(GrowArrow(benchmark_flow[1]), run_time=0.8)
        self.play(Write(benchmark_flow[3]), run_time=1.0)
        self.wait(0.5)
        self.play(GrowArrow(benchmark_flow[2]), run_time=0.8)
        self.play(Write(benchmark_flow[4]), run_time=1.0)
        self.wait(4.0)
        self.play(
            Write(semantic_prompt[0]),
            FadeIn(semantic_prompt[1], shift=UP * 0.08),
            run_time=1.2,
        )
        self.wait(3.0)
        self.play(
            FadeIn(world_panel[0], shift=UP * 0.12),
            FadeIn(world_panel[1]),
            Write(world_panel[2]),
            run_time=1.2,
        )
        self.wait(5.0)
        self.play(
            Create(problem_box[0]),
            Write(problem_box[1]),
            run_time=1.2,
        )
        self.wait(2.0)

        # SCENE 11B
        self.play(FadeOut(*self.mobjects), run_time=0.8)
        self.clear()

        metrics = create_worldscore_metrics_scene()
        boxes = metrics["boxes"]
        static_brace = metrics["static_brace"]
        dynamic_brace = metrics["dynamic_brace"]

        self.play(Write(metrics["title"]), run_time=1.0)
        self.wait(9.0)
        for box in boxes:
            self.play(
                FadeIn(box[0], shift=RIGHT * 0.18),
                FadeIn(box[1], shift=RIGHT * 0.18),
                run_time=1.0,
            )
            self.wait(3.5)
        self.wait(5.0)
        self.play(FadeIn(static_brace[0], shift=UP * 0.18), run_time=0.75)
        self.play(Write(static_brace[1]), run_time=1.0)
        self.wait(4.0)
        self.play(FadeIn(dynamic_brace[0], shift=DOWN * 0.18), run_time=0.75)
        self.play(Write(dynamic_brace[1]), run_time=1.0)
        self.wait(11.0)
