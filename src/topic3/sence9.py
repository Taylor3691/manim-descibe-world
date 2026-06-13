from manim import *

class DDIMSubOptimal(Scene):
    def construct(self):
        # Color scheme
        BLUE_COLOR = "#4A90D9"
        RED_COLOR = "#E74C3C"
        YELLOW_COLOR = "#F39C12"
        
        # === Phase 1: Title Fade-in ===
        title = Text("Why is DDIM sub-optimal?", font_size=44, color=WHITE)
        title.to_edge(UP, buff=0.6)
        
        self.play(FadeIn(title, shift=DOWN, run_time=2))
        self.wait(0.3)
        
        # === Phase 2: Build Denoising Chain ===
        # Node labels - using MathTex for subscript notation
        node_labels = [
            Text("Noise", font_size=22, color=BLUE_COLOR),
            MathTex("x_t", font_size=36, color=BLUE_COLOR),
            MathTex("x_{t-1}", font_size=36, color=BLUE_COLOR),
            MathTex("x_{t-2}", font_size=36, color=BLUE_COLOR),
            Text("...", font_size=36, color=BLUE_COLOR),
            MathTex("x_0", font_size=36, color=BLUE_COLOR),
            Text("Image", font_size=22, color=BLUE_COLOR),
        ]
        
        # Create nodes with rounded boxes
        nodes = VGroup()
        for label in node_labels:
            box = RoundedRectangle(
                height=0.75,
                width=max(label.get_width() + 0.4, 1.2),
                corner_radius=0.15,
                color=BLUE_COLOR,
                stroke_width=2.5,
                fill_color=BLUE_COLOR,
                fill_opacity=0.15
            )
            label.move_to(box.get_center())
            node = VGroup(box, label)
            nodes.add(node)
        
        # Arrange nodes horizontally
        nodes.arrange(RIGHT, buff=0.5)
        nodes.move_to([0, 0.3, 0])
        
        # Scale to fit if too wide
        if nodes.get_width() > 13:
            scale_factor = 13 / nodes.get_width()
            nodes.scale(scale_factor)
            nodes.move_to([0, 0.3, 0])
        
        # Create arrows
        arrows = VGroup()
        for i in range(len(nodes) - 1):
            arrow = Arrow(
                nodes[i].get_right(),
                nodes[i+1].get_left(),
                color=BLUE_COLOR,
                buff=0.05,
                stroke_width=3.5,
                max_tip_length_to_length_ratio=0.2,
                tip_length=0.18
            )
            arrows.add(arrow)
        
        # Animate nodes appearing sequentially
        self.play(
            LaggedStart(
                *[FadeIn(node, scale=0.7) for node in nodes],
                lag_ratio=0.3
            ),
            run_time=5
        )
        self.play(
            LaggedStart(
                *[GrowFromPoint(arrow, arrow.get_start()) for arrow in arrows],
                lag_ratio=0.2
            ),
            run_time=3
        )
        self.wait(0.3)
        
        # === Phase 3: First Caption ===
        caption1 = Text(
            "DDIM relies on many sequential refinement steps.",
            font_size=24,
            color=WHITE
        )
        caption1.next_to(nodes, DOWN, buff=0.6)
        
        self.play(FadeIn(caption1, run_time=2))
        self.wait(0.3)
        
        # === Phase 4: Highlight Middle Section ===
        # Highlight nodes 2-5 (x_{t-1}, x_{t-2}, ..., x_0)
        highlight_target = VGroup(nodes[2], nodes[3], nodes[4], nodes[5])
        highlight = SurroundingRectangle(
            highlight_target,
            color=YELLOW_COLOR,
            buff=0.25,
            stroke_width=4
        )
        
        self.play(Create(highlight, run_time=2))
        # Pulse the highlight
        self.play(
            highlight.animate.set_stroke(width=6),
            rate_func=there_and_back,
            run_time=1
        )
        self.wait(0.2)
        
        # === Phase 5: Second Caption ===
        caption2 = Text(
            "Even with a strong model, inference still requires multiple steps.",
            font_size=24,
            color=WHITE
        )
        caption2.next_to(caption1, DOWN, buff=0.3)
        
        self.play(FadeIn(caption2, run_time=2))
        self.wait(0.3)
        
        # === Phase 6: Warning Label ===
        warning_text = Text(
            "Sub-optimal inference efficiency",
            font_size=22,
            color=RED_COLOR,
            weight=BOLD
        )
        warning_box = SurroundingRectangle(
            warning_text,
            color=RED_COLOR,
            buff=0.2,
            stroke_width=2.5,
        )
        warning_box.set_fill(RED_COLOR, opacity=0.15)
        warning = VGroup(warning_box, warning_text)
        warning.next_to(nodes[-1], UP, buff=0.4)
        # Keep within screen
        if warning.get_right()[0] > 6.5:
            warning.shift(LEFT * (warning.get_right()[0] - 6.5))
        if warning.get_left()[0] < -6.5:
            warning.shift(RIGHT * (-6.5 - warning.get_left()[0]))
        
        # Scale-up appearance with flash
        self.play(
            FadeIn(warning, scale=0.5),
            run_time=1
        )
        # Flash effect
        self.play(
            warning.animate.scale(1.15),
            rate_func=there_and_back,
            run_time=0.7
        )
        self.wait(1)
        
        # === Phase 7: Dim Chain ===
        chain_elements = VGroup(nodes, arrows, highlight)
        self.play(
            chain_elements.animate.set_opacity(0.35),
            run_time=2.5
        )
        self.wait(1.5)
