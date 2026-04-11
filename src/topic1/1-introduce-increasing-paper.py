import os

from manim import *

class WorldModelScene(Scene):
    def construct(self):
        self.phase1_trend()
        self.wait(1)
        self.clear()

        self.phase2_world()
        self.wait(1)
        self.clear()

        self.phase3_agents()
        self.wait(2)

    # -------------------------
    # 📈 PHASE 1: TREND
    # -------------------------
    def phase1_trend(self):
        title = Text("Quá nhiều bài báo", font="Segoe UI").scale(0.7)
        title.to_edge(UP)

        axes = Axes(
            x_range=[2015, 2025, 1],
            y_range=[0, 0.25, 0.05],
            x_length=8,
            y_length=4,
            axis_config={"include_numbers": True},
        )

        labels = axes.get_axis_labels(x_label="Năm", y_label=r"\% Bài báo")

        # Fake data giống hình bạn
        years = [2015,2016,2017,2018,2019,2020,2021,2022,2023,2024]
        values = [0.06,0.05,0.03,0.05,0.06,0.055,0.07,0.085,0.15,0.23]

        graph = axes.plot_line_graph(
            x_values=years,
            y_values=values,
            add_vertex_dots=True,
        )

        self.play(Write(title))
        self.play(Create(axes), Write(labels))
        self.play(Create(graph), run_time=2)

        # highlight điểm cuối
        last_dot = graph["vertex_dots"][-1]
        self.play(Indicate(last_dot, scale_factor=2, color=YELLOW))


    # -------------------------
    # 🌍 PHASE 2: WORLD
    # -------------------------
    def phase2_world(self):
        text1 = Text("AI đã học cách trò chuyện").scale(0.8)
        text2 = Text("Giờ nó đang học cách xây dựng thực tại").scale(0.7).set_color(BLUE)

        text_group = VGroup(text1, text2).arrange(DOWN)
        text_group.to_edge(LEFT)

        world_box = RoundedRectangle(
            corner_radius=0.3,
            width=4,
            height=2,
            color=GREEN
        ).shift(RIGHT * 3)

        world_label = Text("Mô hình thế giới").scale(0.5).move_to(world_box.get_center())

        self.play(FadeIn(text1))
        self.play(Write(text2))
        self.play(FadeIn(world_box), Write(world_label))

        # hiệu ứng "world alive"
        self.play(world_box.animate.scale(1.1))
        self.play(world_box.animate.scale(1))

    # -------------------------
    # 🤖 PHASE 3: AGENTS + INFINITE WORLDS
    # -------------------------
    def phase3_agents(self):
        title = Text("Huấn luyện trong môi trường vô hạn").scale(0.7)
        title.to_edge(UP)

        agent = Dot(color=BLUE).scale(1.5)
        agent_label = Text("Tác tử").scale(0.4).next_to(agent, DOWN)

        self.play(Write(title))
        self.play(FadeIn(agent), Write(agent_label))

        # tạo world xung quanh
        worlds = VGroup()
        positions = [
            LEFT*3, RIGHT*3,
            UP*2, DOWN*2,
            LEFT*2+UP, RIGHT*2+DOWN
        ]

        for pos in positions:
            w = Circle(radius=0.5, color=GREEN).move_to(pos)
            worlds.add(w)

        self.play(LaggedStart(*[FadeIn(w) for w in worlds], lag_ratio=0.2))

        # agent đi qua các world
        for w in worlds:
            self.play(agent.animate.move_to(w.get_center()), run_time=0.5)

        # 🔥 expand thành nhiều world hơn (key idea)
        self.play(worlds.animate.scale(1.5))

        grid_worlds = VGroup(*[
            Circle(radius=0.3, color=GREEN)
            for _ in range(9)
        ]).arrange_in_grid(3,3).scale(1.2)

        self.play(Transform(worlds, grid_worlds))

        # text insight
        insight = Text("Thế giới vô hạn → tác tử mạnh hơn").scale(0.6).to_edge(DOWN)

        self.play(Write(insight))

        # agent move random (explore)
        for w in worlds:
            self.play(agent.animate.move_to(w.get_center()), run_time=0.3)


class DeepMindUsecaseScene(Scene):
    ASSET_DIR = os.path.join("src", "assets")
    INVESTOR_IMAGE = os.path.join(ASSET_DIR, "worldmodel_investor_trend.png")
    ARTICLE_IMAGE = os.path.join(ASSET_DIR, "worldmodel_media_collage.png")

    def construct(self):
        self.show_market_context()
        self.wait(0.6)
        self.clear()

        self.show_preferred_usecase()
        self.wait(1.5)

    def image_panel(self, image_path, title, width=5.3, height=3.0):
        frame = RoundedRectangle(corner_radius=0.16, width=width, height=height)
        frame.set_stroke(color=GRAY_B, width=2)
        frame.set_fill(color=BLACK, opacity=0.1)

        title_text = Text(title, font="Segoe UI", weight=MEDIUM).scale(0.38)
        title_text.next_to(frame, UP, buff=0.15)

        if os.path.exists(image_path):
            image = ImageMobject(image_path)
            image.set_width(width - 0.16)
            image.set_height(height - 0.16)
            image.move_to(frame.get_center())
            return VGroup(frame, image, title_text)

        placeholder = Text("Đặt ảnh vào: src/assets", font="Segoe UI").scale(0.34)
        placeholder2 = Text(os.path.basename(image_path), font="Consolas").scale(0.3)
        placeholder_group = VGroup(placeholder, placeholder2).arrange(DOWN, buff=0.12)
        placeholder_group.move_to(frame.get_center())

        return VGroup(frame, placeholder_group, title_text)

    def show_market_context(self):
        title = Text("World Model đang nóng lên", font="Segoe UI", weight=BOLD).scale(0.7)
        subtitle = Text(
            "A16Z, Lightspeed và nhiều ông lớn đang đầu tư mạnh",
            font="Segoe UI",
        ).scale(0.42)
        subtitle.set_color(GRAY_B)
        subtitle.next_to(title, DOWN, buff=0.15)

        panels = VGroup(
            self.image_panel(self.INVESTOR_IMAGE, "Xu hướng trên arXiv + bài toán thị trường"),
            self.image_panel(self.ARTICLE_IMAGE, "Truyền thông: AI xây dựng thế giới tương tác"),
        ).arrange(RIGHT, buff=0.45)
        panels.next_to(subtitle, DOWN, buff=0.45)

        experience = Text(
            "Ứng dụng 1: Trải nghiệm nhập vai giống game,"
            " người dùng chơi và làm đủ thứ mới.",
            font="Segoe UI",
        ).scale(0.45)
        experience.set_color(BLUE_B)
        experience.to_edge(DOWN)

        self.play(FadeIn(title, shift=UP * 0.2), FadeIn(subtitle, shift=UP * 0.2))
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in panels], lag_ratio=0.2))
        self.play(Write(experience))

    def show_preferred_usecase(self):
        title = Text("Ứng dụng speaker DeepMind thích hơn", font="Segoe UI", weight=BOLD).scale(0.68)
        title.to_edge(UP)

        note = Text(
            "Không chỉ tạo game cho người dùng -"
            " mà tạo vô hạn môi trường để huấn luyện tác tử.",
            font="Segoe UI",
        ).scale(0.42)
        note.set_color(YELLOW_D)
        note.next_to(title, DOWN, buff=0.18)

        data_box = RoundedRectangle(corner_radius=0.12, width=2.8, height=1.4, color=BLUE_D)
        data_box.set_fill(BLUE_E, opacity=0.45)
        data_box.to_edge(LEFT, buff=0.85).shift(UP * 0.5)
        data_label = Text("Dữ liệu offline", font="Consolas").scale(0.4).move_to(data_box)

        model_box = RoundedRectangle(corner_radius=0.12, width=3.2, height=1.6, color=GREEN_C)
        model_box.set_fill(GREEN_E, opacity=0.45)
        model_box.move_to(UP * 0.4)
        model_label = Text("Mô hình thế giới", font="Segoe UI", weight=BOLD).scale(0.46).move_to(model_box)

        arrow_data_to_model = Arrow(
            data_box.get_right(), model_box.get_left(), buff=0.15, stroke_width=4
        ).set_color(BLUE_C)

        seed_envs = VGroup(
            *[
                RoundedRectangle(corner_radius=0.08, width=1.2, height=0.75, color=TEAL_C)
                for _ in range(4)
            ]
        )
        for idx, env in enumerate(seed_envs):
            env.set_fill(TEAL_E, opacity=0.38)
            env.add(Text(f"E{idx + 1}", font="Consolas").scale(0.28).move_to(env))
        seed_envs.arrange_in_grid(rows=2, cols=2, buff=0.18)
        seed_envs.to_edge(RIGHT, buff=1.0).shift(UP * 0.5)

        arrow_model_to_env = Arrow(
            model_box.get_right(), seed_envs.get_left(), buff=0.16, stroke_width=4
        ).set_color(GREEN_C)

        agent = Dot(color=YELLOW, radius=0.09)
        agent_label = Text("Tác tử", font="Consolas").scale(0.32)
        agent.move_to(seed_envs[0].get_center() + DOWN * 0.02)
        agent_label.next_to(agent, DOWN, buff=0.08)

        self.play(FadeIn(title), FadeIn(note, shift=UP * 0.1))
        self.play(FadeIn(data_box), Write(data_label))
        self.play(GrowArrow(arrow_data_to_model), FadeIn(model_box), Write(model_label))
        self.play(GrowArrow(arrow_model_to_env), LaggedStart(*[FadeIn(e) for e in seed_envs], lag_ratio=0.15))
        self.play(FadeIn(agent), FadeIn(agent_label))

        for target in [seed_envs[1], seed_envs[3], seed_envs[2]]:
            self.play(agent.animate.move_to(target.get_center()), run_time=0.35)

        infinite_envs = VGroup(
            *[
                RoundedRectangle(corner_radius=0.06, width=0.75, height=0.45, color=TEAL_C)
                for _ in range(24)
            ]
        )
        for idx, env in enumerate(infinite_envs):
            env.set_fill(TEAL_E, opacity=0.35)
            if idx < 8:
                env.add(Text("E", font="Consolas").scale(0.2).move_to(env))
        infinite_envs.arrange_in_grid(rows=4, cols=6, buff=0.08)
        infinite_envs.move_to(seed_envs.get_center() + RIGHT * 0.1)

        infinity_text = Text("~ vô hạn môi trường", font="Segoe UI", weight=BOLD).scale(0.4)
        infinity_text.set_color(TEAL_B)
        infinity_text.next_to(infinite_envs, DOWN, buff=0.22)

        outcome = Text(
            "Tác tử được khám phá nhiều tình huống mới,"
            " vượt qua giới hạn của tập dữ liệu ban đầu.",
            font="Segoe UI",
        ).scale(0.4)
        outcome.set_color(YELLOW_B)
        outcome.to_edge(DOWN)

        self.play(ReplacementTransform(seed_envs, infinite_envs), FadeIn(infinity_text, shift=UP * 0.1))

        sample_points = [2, 7, 13, 19, 23]
        for idx in sample_points:
            self.play(agent.animate.move_to(infinite_envs[idx].get_center()), run_time=0.25)

        self.play(Write(outcome))