from manim import *

config.background_color = WHITE


class TrilemmaVenn(Scene):
    def construct(self):
        # Title
        title = Text(
            "The trilemma of continuous generative models",
            font_size=44,
            color=BLACK,
        )
        title.to_edge(UP, buff=0.4)

        # Three circles for the Venn diagram
        radius = 2.05
        stroke_color = "#666666"

        top_circle = Circle(
            radius=radius,
            color=stroke_color,
            stroke_width=3,
            fill_color="#B0C4D8",
            fill_opacity=0.22,
        )
        top_circle.move_to([0, 1.05, 0])

        bl_circle = Circle(
            radius=radius,
            color=stroke_color,
            stroke_width=3,
            fill_color="#B8D0B0",
            fill_opacity=0.22,
        )
        bl_circle.move_to([-1.45, -0.45, 0])

        br_circle = Circle(
            radius=radius,
            color=stroke_color,
            stroke_width=3,
            fill_color="#E8C8A0",
            fill_opacity=0.22,
        )
        br_circle.move_to([1.45, -0.45, 0])

        # Internal labels
        label_top = Text(
            "Training stability",
            font_size=32,
            color="#1A2E5C",
        )
        label_top.move_to([0, 2.45, 0])

        label_bl = Text(
            "High quality\nsamples",
            font_size=30,
            color="#2D5F2D",
            line_spacing=0.9,
        )
        label_bl.move_to([-2.45, -1.5, 0])

        label_br = Text(
            "Efficient\ninference",
            font_size=30,
            color="#6B4423",
            line_spacing=0.9,
        )
        label_br.move_to([2.45, -1.5, 0])

        # External labels
        label_left = Text(
            "Diffusion Models",
            font_size=30,
            color=BLACK,
        )
        label_left.move_to([-5.3, 0.5, 0])

        label_right = Text(
            "VAEs, Normalizing\nFlows",
            font_size=30,
            color=BLACK,
            line_spacing=0.9,
        )
        label_right.move_to([5.3, 0.5, 0])

        label_bottom = Text(
            "GANs, Diffusion Distillation",
            font_size=30,
            color=BLACK,
        )
        label_bottom.move_to([0, -3.2, 0])

        # Arrows
        arrow_left = Arrow(
            start=[-3.8, 0.5, 0],
            end=[-1.0, 0.3, 0],
            color=BLACK,
            stroke_width=3,
            buff=0.1,
            max_tip_length_to_length_ratio=0.2,
        )

        arrow_right = Arrow(
            start=[3.8, 0.5, 0],
            end=[1.0, 0.3, 0],
            color=BLACK,
            stroke_width=3,
            buff=0.1,
            max_tip_length_to_length_ratio=0.2,
        )

        arrow_bottom = Arrow(
            start=[0, -2.85, 0],
            end=[0, -1.2, 0],
            color=BLACK,
            stroke_width=3,
            buff=0.1,
            max_tip_length_to_length_ratio=0.2,
        )

        # ---- Phase 1: Title fade in ----
        self.play(FadeIn(title), run_time=1.5)

        # ---- Phase 2: Draw circles one by one ----
        self.play(Create(top_circle), run_time=1.5)
        self.play(Create(bl_circle), run_time=1.5)
        self.play(Create(br_circle), run_time=1.5)

        # ---- Phase 3: Internal labels fade in ----
        self.play(
            FadeIn(label_top),
            FadeIn(label_bl),
            FadeIn(label_br),
            run_time=1.5,
        )

        # ---- Phase 4: External labels fade in ----
        self.play(
            FadeIn(label_left),
            FadeIn(label_right),
            FadeIn(label_bottom),
            run_time=1.5,
        )

        # ---- Phase 5: Draw arrows ----
        self.play(
            GrowFromPoint(arrow_left, arrow_left.get_start()),
            GrowFromPoint(arrow_right, arrow_right.get_start()),
            GrowFromPoint(arrow_bottom, arrow_bottom.get_start()),
            run_time=2,
        )

        # ---- Phase 6: Hold ----
        self.wait(2)
