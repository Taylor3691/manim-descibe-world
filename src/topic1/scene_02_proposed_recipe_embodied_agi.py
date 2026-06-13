"""
SCENE 2 - Proposed Recipe for Embodied AGI

Pre-train on all available data, then enter an endless loop:
generate diverse worlds/tasks, select the useful ones, and train again.
"""

from manim import *
import numpy as np
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from topic1.shared_styles import *


class Scene2_ProposedRecipeEmbodiedAGI(MovingCameraScene):
    def setup(self):
        self.camera.background_color = BG_COLOR

    def make_background(self):
        bg = Rectangle(width=30, height=12, stroke_width=0)
        bg.set_fill(BG_COLOR, opacity=1)

        grid = VGroup()
        for x in np.arange(-15, 15.5, 1.0):
            grid.add(Line([x, -6, 0], [x, 6, 0], color="#22304d", stroke_width=0.5, stroke_opacity=0.22))
        for y in np.arange(-6, 6.5, 1.0):
            grid.add(Line([-15, y, 0], [15, y, 0], color="#22304d", stroke_width=0.5, stroke_opacity=0.22))

        haze = VGroup(
            Rectangle(width=30, height=4.4, stroke_width=0, fill_color="#142a52", fill_opacity=0.18).shift(UP * 2.9),
            Rectangle(width=30, height=3.6, stroke_width=0, fill_color="#171333", fill_opacity=0.28).shift(DOWN * 3.3),
        )
        return VGroup(bg, haze, grid)

    def card(self, width, height, color, title, subtitle=None):
        shadow = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.18,
            stroke_width=0,
            fill_color=BLACK,
            fill_opacity=0.26,
        ).shift(DOWN * 0.06 + RIGHT * 0.06)
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.18,
            color=color,
            stroke_width=2.2,
            fill_color="#121a33",
            fill_opacity=0.82,
        )
        title_mob = Text(title, font_size=22, color=TEXT_PRIMARY, weight=BOLD)
        if subtitle:
            subtitle_mob = Text(subtitle, font_size=13, color=TEXT_DIM)
            text_group = VGroup(title_mob, subtitle_mob).arrange(DOWN, buff=0.13)
        else:
            text_group = VGroup(title_mob)
        text_group.move_to(box.get_top() + DOWN * 0.38)
        return VGroup(shadow, box, text_group)

    def robot_icon(self, scale=1.0):
        head = RoundedRectangle(
            width=0.58,
            height=0.42,
            corner_radius=0.09,
            color=AGENT_COLOR,
            fill_color="#0b5f80",
            fill_opacity=0.75,
            stroke_width=2,
        )
        body = RoundedRectangle(
            width=0.82,
            height=0.64,
            corner_radius=0.12,
            color=AGENT_COLOR,
            fill_color="#103c66",
            fill_opacity=0.78,
            stroke_width=2,
        ).next_to(head, DOWN, buff=0.08)
        eyes = VGroup(
            Dot(radius=0.035, color=WHITE).shift(LEFT * 0.12),
            Dot(radius=0.035, color=WHITE).shift(RIGHT * 0.12),
        ).move_to(head)
        antenna = VGroup(
            Line(head.get_top(), head.get_top() + UP * 0.18, color=AGENT_COLOR, stroke_width=2),
            Dot(head.get_top() + UP * 0.2, radius=0.035, color=HIGHLIGHT_COLOR),
        )
        arms = VGroup(
            Line(body.get_left() + UP * 0.1, body.get_left() + LEFT * 0.23 + DOWN * 0.05, color=AGENT_COLOR, stroke_width=3),
            Line(body.get_right() + UP * 0.1, body.get_right() + RIGHT * 0.23 + DOWN * 0.05, color=AGENT_COLOR, stroke_width=3),
        )
        legs = VGroup(
            Line(body.get_bottom() + LEFT * 0.18, body.get_bottom() + LEFT * 0.18 + DOWN * 0.18, color=AGENT_COLOR, stroke_width=3),
            Line(body.get_bottom() + RIGHT * 0.18, body.get_bottom() + RIGHT * 0.18 + DOWN * 0.18, color=AGENT_COLOR, stroke_width=3),
        )
        glow = Circle(radius=0.78, color=AGENT_COLOR, stroke_width=0, fill_opacity=0.11)
        return VGroup(glow, arms, legs, body, head, eyes, antenna).scale(scale)

    def data_icon(self, kind, color):
        if kind == "text":
            page = RoundedRectangle(width=0.7, height=0.55, corner_radius=0.04, color=color, fill_opacity=0.1, stroke_width=1.5)
            lines = VGroup(*[
                Line(page.get_left() + RIGHT * 0.12 + DOWN * y, page.get_right() + LEFT * 0.12 + DOWN * y, color=color, stroke_width=1.4)
                for y in [-0.13, 0.0, 0.13]
            ])
            return VGroup(page, lines)
        if kind == "code":
            box = RoundedRectangle(width=0.82, height=0.54, corner_radius=0.05, color=color, fill_opacity=0.1, stroke_width=1.5)
            code = Text("</>", font_size=18, color=color, weight=BOLD).move_to(box)
            return VGroup(box, code)
        if kind == "video":
            return make_film_strip(n_frames=3, frame_w=0.28, frame_h=0.18, spacing=0.05, color=color).scale(0.78)
        if kind == "game":
            frame = RoundedRectangle(width=0.76, height=0.5, corner_radius=0.04, color=color, fill_opacity=0.1, stroke_width=1.5)
            avatar = Dot(radius=0.05, color=AGENT_COLOR).move_to(frame.get_left() + RIGHT * 0.2 + DOWN * 0.05)
            block = Square(side_length=0.1, color=WORLD_COLOR, fill_opacity=0.7, stroke_width=0).move_to(frame.get_right() + LEFT * 0.18 + UP * 0.06)
            return VGroup(frame, avatar, block)
        frame = RoundedRectangle(width=0.7, height=0.52, corner_radius=0.04, color=color, fill_opacity=0.1, stroke_width=1.5)
        sun = Dot(radius=0.05, color=HIGHLIGHT_COLOR).move_to(frame.get_corner(UR) + LEFT * 0.16 + DOWN * 0.12)
        mountain = Polygon(frame.get_left() + DOWN * 0.19, frame.get_center() + UP * 0.07, frame.get_right() + DOWN * 0.19, color=color, fill_opacity=0.35, stroke_width=0)
        return VGroup(frame, mountain, sun)

    def capability_bar(self, width=1.75, label="Capability"):
        shell = RoundedRectangle(width=width, height=0.22, corner_radius=0.06, color=TEXT_DIM, fill_opacity=0.08, stroke_width=1)
        fill = RoundedRectangle(width=width, height=0.22, corner_radius=0.06, color=AGENT_COLOR, fill_color=AGENT_COLOR, fill_opacity=0.8, stroke_width=0)
        fill.stretch_to_fit_width(width * 0.22)
        fill.align_to(shell, LEFT)
        label_mob = Text(label, font_size=13, color=TEXT_DIM).next_to(shell, UP, buff=0.08)
        return VGroup(label_mob, shell, fill)

    def world_tile(self, kind, color):
        tile = RoundedRectangle(width=0.78, height=0.58, corner_radius=0.07, color=color, fill_color=color, fill_opacity=0.09, stroke_width=1.6)
        inside = VGroup()
        if kind == "maze":
            for x in [-0.18, 0.06, 0.25]:
                inside.add(Line([x, -0.19, 0], [x, 0.19, 0], color=color, stroke_width=2))
            inside.add(Line([-0.3, 0.02, 0], [0.22, 0.02, 0], color=color, stroke_width=2))
        elif kind == "city":
            for i, h in enumerate([0.22, 0.34, 0.18]):
                inside.add(Rectangle(width=0.14, height=h, color=color, fill_opacity=0.45, stroke_width=0).shift(RIGHT * (i - 1) * 0.17 + DOWN * (0.17 - h / 2)))
        elif kind == "lab":
            inside.add(Polygon(LEFT * 0.14 + UP * 0.18, RIGHT * 0.14 + UP * 0.18, RIGHT * 0.24 + DOWN * 0.18, LEFT * 0.24 + DOWN * 0.18, color=color, fill_opacity=0.35, stroke_width=1.2))
            inside.add(Line(UP * 0.18, UP * 0.29, color=color, stroke_width=2))
        elif kind == "forest":
            for x in [-0.2, 0, 0.2]:
                inside.add(Triangle(color=color, fill_opacity=0.45, stroke_width=0).scale(0.13).move_to(RIGHT * x + UP * 0.02))
                inside.add(Line(RIGHT * x + DOWN * 0.11, RIGHT * x + DOWN * 0.22, color=WORLD_COLOR, stroke_width=2))
        else:
            inside.add(Square(side_length=0.13, color=color, fill_opacity=0.55, stroke_width=0).shift(LEFT * 0.18))
            inside.add(Circle(radius=0.08, color=AGENT_COLOR, fill_opacity=0.8, stroke_width=0).shift(RIGHT * 0.15))
            inside.add(Line(LEFT * 0.3 + DOWN * 0.18, RIGHT * 0.3 + DOWN * 0.18, color=color, stroke_width=2))
        inside.move_to(tile)
        return VGroup(tile, inside)

    def funnel_icon(self):
        top = Polygon(LEFT * 0.48 + UP * 0.24, RIGHT * 0.48 + UP * 0.24, RIGHT * 0.17 + DOWN * 0.04, LEFT * 0.17 + DOWN * 0.04, color=HIGHLIGHT_COLOR, fill_opacity=0.18, stroke_width=2)
        stem = Polygon(LEFT * 0.12 + DOWN * 0.04, RIGHT * 0.12 + DOWN * 0.04, RIGHT * 0.05 + DOWN * 0.34, LEFT * 0.05 + DOWN * 0.34, color=HIGHLIGHT_COLOR, fill_opacity=0.35, stroke_width=2)
        beam = Triangle(color=HIGHLIGHT_COLOR, fill_opacity=0.13, stroke_width=0).scale(0.65).rotate(PI).shift(DOWN * 0.43)
        return VGroup(beam, top, stem)

    def construct(self):
        background = self.make_background()
        self.add(background)

        title = Text("Proposed Recipe for Embodied AGI", font_size=38, color=TEXT_PRIMARY, weight=BOLD)
        subtitle = Text("Công thức tổng quát: dữ liệu → thế giới → chọn lọc → huấn luyện", font_size=19, color=TEXT_DIM)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.16).to_edge(UP, buff=0.34)
        opener = Text("How can an agent keep improving after pre-training?", font_size=26, color=HIGHLIGHT_COLOR)
        opener_vi = Text("Làm sao agent tiếp tục giỏi hơn sau pre-training?", font_size=17, color=TEXT_DIM)
        opener_group = VGroup(opener, opener_vi).arrange(DOWN, buff=0.14).move_to(DOWN * 0.35)

        self.play(FadeIn(title, shift=DOWN * 0.12), Write(subtitle), run_time=1.5)
        self.play(FadeIn(opener_group, shift=UP * 0.16), run_time=0.9)
        self.wait(2.0)
        self.play(FadeOut(opener_group, shift=UP * 0.2), title_group.animate.scale(0.86).to_edge(UP, buff=0.25), run_time=1.1)

        pretrain_card = self.card(3.25, 3.15, AGENT_COLOR, "Step 1: Pre-train Agent", "Learn from all available data")
        pretrain_card.move_to(LEFT * 3.85 + DOWN * 0.2)
        robot = self.robot_icon(scale=0.78).move_to(pretrain_card[1].get_center() + DOWN * 0.1)
        cap = self.capability_bar(width=1.75).move_to(pretrain_card[1].get_bottom() + UP * 0.42)
        pretrain_group = VGroup(pretrain_card, robot, cap)

        data_kinds = ["text", "video", "image", "code", "game"]
        data_colors = [DATA_COLOR, AGENT_COLOR, WORLD_COLOR, LATENT_COLOR, ACTION_COLOR]
        data_starts = [
            LEFT * 6.7 + UP * 2.4,
            LEFT * 6.9 + DOWN * 1.7,
            LEFT * 4.1 + UP * 2.65,
            LEFT * 1.8 + DOWN * 1.85,
            LEFT * 1.6 + UP * 1.7,
        ]
        data_targets = [
            pretrain_card.get_center() + LEFT * 0.9 + UP * 0.88,
            pretrain_card.get_center() + LEFT * 0.95 + DOWN * 0.72,
            pretrain_card.get_center() + RIGHT * 0.87 + UP * 0.76,
            pretrain_card.get_center() + RIGHT * 0.82 + DOWN * 0.7,
            pretrain_card.get_center() + UP * 1.04,
        ]
        data_icons = VGroup()
        for kind, color, start in zip(data_kinds, data_colors, data_starts):
            icon = self.data_icon(kind, color).move_to(start)
            data_icons.add(icon)

        step_caption = Text("Step 1: Pre-train a capable agent from available data.", font_size=20, color=TEXT_PRIMARY)
        step_caption.to_edge(DOWN, buff=0.45)

        self.play(FadeIn(pretrain_card, shift=RIGHT * 0.25), FadeIn(robot, scale=0.7), FadeIn(cap), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(icon, scale=0.6) for icon in data_icons], lag_ratio=0.12), FadeIn(step_caption, shift=UP * 0.15), run_time=1.1)
        self.play(
            LaggedStart(*[icon.animate.move_to(target).scale(0.82) for icon, target in zip(data_icons, data_targets)], lag_ratio=0.08),
            cap[2].animate.stretch_to_fit_width(1.75 * 0.68).align_to(cap[1], LEFT),
            robot[0].animate.set_fill(opacity=0.24),
            run_time=2.0,
        )
        self.play(Indicate(robot, color=AGENT_COLOR, scale_factor=1.08), run_time=0.9)
        self.wait(1.0)

        loop_center = RIGHT * 3.25 + DOWN * 0.1
        loop_label = Text("Endless Improvement Loop", font_size=25, color=HIGHLIGHT_COLOR, weight=BOLD).move_to(loop_center + UP * 2.65)

        generate = self.card(2.45, 1.35, DATA_COLOR, "Generate Diverse Tasks").move_to(loop_center + UP * 1.25)
        select = self.card(2.45, 1.35, HIGHLIGHT_COLOR, "Select Interesting Ones").move_to(loop_center + DOWN * 0.55 + RIGHT * 1.95)
        train = self.card(2.45, 1.35, AGENT_COLOR, "Train Agent").move_to(loop_center + DOWN * 0.55 + LEFT * 1.95)
        loop_nodes = VGroup(generate, select, train)

        a1 = CurvedArrow(generate.get_right() + DOWN * 0.15, select.get_top() + LEFT * 0.2, angle=-TAU / 6, color=DATA_COLOR, stroke_width=3)
        a2 = CurvedArrow(select.get_left(), train.get_right(), angle=-TAU / 7, color=HIGHLIGHT_COLOR, stroke_width=3)
        a3 = CurvedArrow(train.get_top() + RIGHT * 0.2, generate.get_left() + DOWN * 0.15, angle=-TAU / 6, color=AGENT_COLOR, stroke_width=3)
        loop_arrows = VGroup(a1, a2, a3)

        connector = Arrow(pretrain_card.get_right() + RIGHT * 0.1, train.get_left() + LEFT * 0.15, color=ACTION_COLOR, stroke_width=3.2, buff=0.1)

        self.play(self.camera.frame.animate.move_to(RIGHT * 1.35).set(width=14.2), FadeOut(step_caption), run_time=1.4)
        self.play(GrowArrow(connector), FadeIn(loop_label, shift=DOWN * 0.15), run_time=0.7)
        self.play(FadeIn(generate, scale=0.92), run_time=0.6)

        worlds = VGroup()
        world_specs = [("maze", WORLD_COLOR), ("city", AGENT_COLOR), ("lab", LATENT_COLOR), ("forest", ACTION_COLOR), ("game", DATA_COLOR)]
        offsets = [LEFT * 0.78 + DOWN * 0.12, ORIGIN + DOWN * 0.12, RIGHT * 0.78 + DOWN * 0.12, LEFT * 0.38 + DOWN * 0.62, RIGHT * 0.38 + DOWN * 0.62]
        for (kind, color), offset in zip(world_specs, offsets):
            worlds.add(self.world_tile(kind, color).scale(0.48).move_to(generate.get_center() + offset))
        self.play(LaggedStart(*[FadeIn(w, scale=0.3) for w in worlds], lag_ratio=0.08), run_time=1.0)
        self.play(Create(a1), FadeIn(select, scale=0.92), run_time=0.7)

        funnel = self.funnel_icon().scale(0.74).move_to(select.get_center() + DOWN * 0.12)
        selected_worlds = VGroup(
            self.world_tile("city", HIGHLIGHT_COLOR).scale(0.42).move_to(select.get_center() + LEFT * 0.52 + DOWN * 0.28),
            self.world_tile("lab", HIGHLIGHT_COLOR).scale(0.42).move_to(select.get_center() + RIGHT * 0.52 + DOWN * 0.28),
        )
        dim_worlds = VGroup(
            self.world_tile("maze", TEXT_DIM).scale(0.34).move_to(select.get_center() + LEFT * 0.72 + UP * 0.1),
            self.world_tile("forest", TEXT_DIM).scale(0.34).move_to(select.get_center() + UP * 0.16),
            self.world_tile("game", TEXT_DIM).scale(0.34).move_to(select.get_center() + RIGHT * 0.72 + UP * 0.1),
        ).set_opacity(0.28)
        self.play(FadeIn(funnel, shift=DOWN * 0.12), FadeIn(dim_worlds), FadeIn(selected_worlds), run_time=1.0)
        self.play(LaggedStart(*[Indicate(w, color=HIGHLIGHT_COLOR, scale_factor=1.12) for w in selected_worlds], lag_ratio=0.12), run_time=0.9)
        self.play(Create(a2), FadeIn(train, scale=0.92), run_time=0.7)

        train_robot = self.robot_icon(scale=0.43).move_to(train.get_center() + LEFT * 0.48 + DOWN * 0.1)
        mini_world = self.world_tile("lab", HIGHLIGHT_COLOR).scale(0.44).move_to(train.get_center() + RIGHT * 0.5 + DOWN * 0.1)
        train_bar = self.capability_bar(width=1.35).scale(0.75).move_to(train.get_bottom() + UP * 0.26)
        self.play(FadeIn(train_robot), FadeIn(mini_world), FadeIn(train_bar), run_time=0.8)
        self.play(train_robot.animate.move_to(mini_world.get_center() + LEFT * 0.08).scale(0.78), train_bar[2].animate.stretch_to_fit_width(1.35 * 0.75 * 0.82).align_to(train_bar[1], LEFT), run_time=1.1)
        self.play(Create(a3), run_time=0.6)

        academic = VGroup(
            Text("Not every generated task is useful.", font_size=25, color=TEXT_PRIMARY, weight=BOLD),
            Text("Selection is part of intelligence.", font_size=25, color=HIGHLIGHT_COLOR, weight=BOLD),
            Text("Không phải mọi tác vụ được sinh ra đều hữu ích.\nBiết chọn lọc cũng là một phần của trí tuệ.", font_size=16, color=TEXT_DIM, line_spacing=1.15),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(academic, shift=UP * 0.2), run_time=0.8)
        self.wait(1.0)
        self.play(FadeOut(academic), run_time=0.5)

        labels = VGroup(
            Text("diversity", font_size=16, color=DATA_COLOR).next_to(generate, LEFT, buff=0.18),
            Text("challenge", font_size=16, color=WORLD_COLOR).next_to(generate, RIGHT, buff=0.18),
            Text("selection", font_size=16, color=HIGHLIGHT_COLOR).next_to(select, DOWN, buff=0.15),
            Text("learning", font_size=16, color=AGENT_COLOR).next_to(train, DOWN, buff=0.15),
        )
        self.play(self.camera.frame.animate.move_to(ORIGIN).set(width=14.2), FadeIn(labels, shift=UP * 0.08), run_time=1.3)

        flow_path = VMobject()
        flow_path.set_points_smoothly([
            generate.get_right() + DOWN * 0.15,
            select.get_top() + LEFT * 0.1,
            select.get_left(),
            train.get_right(),
            train.get_top() + RIGHT * 0.15,
            generate.get_left() + DOWN * 0.1,
        ])
        flow_dot = Dot(radius=0.07, color=HIGHLIGHT_COLOR)
        self.add(flow_dot)
        for _ in range(3):
            self.play(MoveAlongPath(flow_dot, flow_path), run_time=1.15, rate_func=linear)
        self.play(FadeOut(flow_dot), run_time=0.2)
        self.wait(0.4)

        final_diagram = VGroup(pretrain_group, data_icons, connector, loop_label, loop_nodes, loop_arrows, worlds, funnel, selected_worlds, dim_worlds, train_robot, mini_world, train_bar, labels)
        self.play(final_diagram.animate.set_opacity(0.28), title_group.animate.set_opacity(0.35), run_time=0.9)

        conclusion = VGroup(
            Text("Embodied AGI is not a single training run — it is a self-improving loop.", font_size=28, color=TEXT_PRIMARY, weight=BOLD),
            Text("Embodied AGI không chỉ là một lần huấn luyện, mà là một vòng lặp tự cải thiện.", font_size=18, color=TEXT_DIM),
        ).arrange(DOWN, buff=0.18).move_to(DOWN * 0.15)
        conclusion[0].set_width(min(conclusion[0].width, 12.4))
        conclusion[1].set_width(min(conclusion[1].width, 11.0))
        self.play(FadeIn(conclusion, shift=UP * 0.2), run_time=1.0)
        self.wait(4.0)
        self.play(FadeOut(VGroup(final_diagram, title_group, conclusion)), run_time=1.0)
