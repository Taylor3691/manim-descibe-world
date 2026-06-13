from manim import *

class IMMFlexibleJumps(Scene):
    def construct(self):
        # === Setup ===
        # Title
        title = Text("IMM: Flexible jumps between timesteps", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.4)

        # Three nodes
        def make_node(label):
            circle = Circle(radius=0.4, color=BLUE_C, fill_opacity=0.3, stroke_width=3)
            text = MathTex(label, font_size=32, color=WHITE)
            return VGroup(circle, text)

        x_t = make_node("x_t")
        x_r = make_node("x_r")
        x_s = make_node("x_s")

        nodes = VGroup(x_t, x_r, x_s).arrange(RIGHT, buff=2.5)
        nodes.shift(UP * 0.3)

        # Noise level labels
        more_noisy = Text("more noisy", font_size=22, color=WHITE)
        more_noisy.next_to(x_t, DOWN, buff=0.3)

        less_noisy = Text("less noisy", font_size=22, color=WHITE)
        less_noisy.next_to(x_s, DOWN, buff=0.3)

        # Captions
        caption1 = Text("IMM learns transitions from one noise level to another.", font_size=22)
        caption1.to_edge(DOWN, buff=0.4)

        caption2 = Text("The model conditions on both source and target timesteps.", font_size=22)
        caption2.next_to(caption1, DOWN, buff=0.2)

        # === Phase 1: Intro ===
        self.play(
            FadeIn(title, shift=DOWN * 0.2),
            FadeIn(nodes, scale=0.8),
            run_time=2
        )
        self.wait(1)

        # === Phase 2: Label noise levels ===
        self.play(
            FadeIn(more_noisy, shift=UP * 0.1),
            FadeIn(less_noisy, shift=UP * 0.1),
            FadeIn(caption1, shift=UP * 0.1),
            run_time=1.5
        )
        self.wait(0.5)

        # === Phase 3: Direct jump ===
        direct_arrow = Arrow(
            x_t.get_top() + UP * 0.7,
            x_s.get_top() + UP * 0.7,
            color=ORANGE,
            buff=0.2,
            stroke_width=5
        )
        direct_label = Text("Direct jump", font_size=22, color=ORANGE)
        direct_label.next_to(direct_arrow, UP, buff=0.15)

        self.play(Create(direct_arrow), run_time=1.2)
        self.play(FadeIn(direct_label), run_time=0.6)
        self.wait(0.2)

        # === Phase 4: Two-step path ===
        path1 = Arrow(
            x_t.get_bottom() + DOWN * 0.8,
            x_r.get_bottom() + DOWN * 0.8,
            color=ORANGE,
            buff=0.2,
            stroke_width=5
        )
        path2 = Arrow(
            x_r.get_bottom() + DOWN * 0.8,
            x_s.get_bottom() + DOWN * 0.8,
            color=ORANGE,
            buff=0.2,
            stroke_width=5
        )
        path_group = VGroup(path1, path2)
        path_label = Text("Via intermediate step", font_size=22, color=ORANGE)
        path_label.next_to(path_group, DOWN, buff=0.15)

        self.play(Create(path1), run_time=1)
        self.play(Create(path2), run_time=1)
        self.play(FadeIn(path_label), run_time=0.5)
        self.wait(0.5)

        # === Phase 5: Highlight both ===
        self.play(
            direct_arrow.animate.set_stroke(width=9),
            path1.animate.set_stroke(width=9),
            path2.animate.set_stroke(width=9),
            run_time=0.6
        )
        self.play(
            direct_arrow.animate.set_stroke(width=5),
            path1.animate.set_stroke(width=5),
            path2.animate.set_stroke(width=5),
            run_time=0.6
        )
        self.wait(0.8)

        # === Phase 6: Caption addition ===
        self.play(FadeIn(caption2, shift=UP * 0.1), run_time=1.5)
        self.wait(0.5)

        # === Phase 7: End ===
        self.wait(1)
