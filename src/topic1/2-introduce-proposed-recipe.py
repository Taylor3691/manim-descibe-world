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
        title = Text("Quá nhiều Paper").scale(0.7)
        title.to_edge(UP)

        axes = Axes(
            x_range=[2015, 2025, 1],
            y_range=[0, 0.25, 0.05],
            x_length=8,
            y_length=4,
            axis_config={"include_numbers": True},
        )

        labels = axes.get_axis_labels(x_label="Year", y_label=r"\% Papers")

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
        text1 = Text("AI learned to talk").scale(0.8)
        text2 = Text("Now it's learning to build reality").scale(0.7).set_color(BLUE)

        text_group = VGroup(text1, text2).arrange(DOWN)
        text_group.to_edge(LEFT)

        world_box = RoundedRectangle(
            corner_radius=0.3,
            width=4,
            height=2,
            color=GREEN
        ).shift(RIGHT * 3)

        world_label = Text("World Model").scale(0.5).move_to(world_box.get_center())

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
        title = Text("Training in Infinite Environments").scale(0.7)
        title.to_edge(UP)

        agent = Dot(color=BLUE).scale(1.5)
        agent_label = Text("Agent").scale(0.4).next_to(agent, DOWN)

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
        insight = Text("Infinite worlds → stronger agents").scale(0.6).to_edge(DOWN)

        self.play(Write(insight))

        # agent move random (explore)
        for w in worlds:
            self.play(agent.animate.move_to(w.get_center()), run_time=0.3)