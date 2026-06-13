from manim import *

class DDIMtoIMM(Scene):
    def construct(self):
        BLUE = "#4A90D9"
        ORANGE = "#E67E22"
        GREEN = "#27AE60"

        # ============ Phase 1: Title ============
        title = Text("From DDIM to IMM", font_size=44, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.3)
        self.play(FadeIn(title, run_time=1.5))
        self.wait(0.5)

        # ============ Phase 2: DDIM Column ============
        ddim_header = Text("DDIM", font_size=38, color=BLUE, weight=BOLD)
        ddim_header.move_to(LEFT * 3.5 + UP * 2.4)

        chain = VGroup(
            MathTex("x_t"),
            MathTex("x_{t-1}"),
            MathTex("x_{t-2}"),
            MathTex(r"\dots"),
            MathTex("x_0"),
        ).set_color(BLUE)
        chain.arrange(RIGHT, buff=0.5)
        chain.move_to(LEFT * 3.5 + UP * 1.3)

        chain_arrows = VGroup()
        for i in range(len(chain) - 1):
            arr = Arrow(
                chain[i].get_right(), chain[i + 1].get_left(),
                buff=0.08, color=BLUE, stroke_width=4,
                max_tip_length_to_length_ratio=0.3,
            )
            chain_arrows.add(arr)

        b1 = Text("• Many sequential steps", font_size=22, color=BLUE)
        b2 = Text("• Less efficient inference", font_size=22, color=BLUE)
        ddim_bullets = VGroup(b1, b2).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        ddim_bullets.next_to(chain, DOWN, buff=0.6)
        ddim_bullets.set_x(ddim_header.get_x())

        self.play(Write(ddim_header), run_time=0.6)
        self.play(
            LaggedStart(*[FadeIn(n, scale=1.3) for n in chain], lag_ratio=0.15),
            run_time=1.3,
        )
        self.play(
            LaggedStart(
                *[GrowFromPoint(a, a.get_start()) for a in chain_arrows],
                lag_ratio=0.15,
            ),
            run_time=0.9,
        )
        self.play(
            LaggedStart(*[FadeIn(b, shift=RIGHT * 0.3) for b in ddim_bullets], lag_ratio=0.3),
            run_time=0.8,
        )
        self.wait(0.3)

        # ============ Phase 3: IMM Column ============
        imm_header = Text("IMM", font_size=38, color=ORANGE, weight=BOLD)
        imm_header.move_to(RIGHT * 3.5 + UP * 2.4)

        # --- IMM diagram group: two paths stacked vertically ---
        # Path 1: x_t -> x_s (direct, top)
        p1_a = MathTex("x_t").set_color(ORANGE)
        p1_b = MathTex("x_s").set_color(ORANGE)
        VGroup(p1_a, p1_b).arrange(RIGHT, buff=3.4)
        p1_arr = Arrow(
            p1_a.get_right(), p1_b.get_left(),
            buff=0.08, color=ORANGE, stroke_width=4,
        )
        path1 = VGroup(p1_a, p1_arr, p1_b)

        # Path 2: x_t -> x_r -> x_s (intermediate, bottom)
        p2_a = MathTex("x_t").set_color(ORANGE)
        p2_b = MathTex("x_r").set_color(ORANGE)
        p2_c = MathTex("x_s").set_color(ORANGE)
        VGroup(p2_a, p2_b, p2_c).arrange(RIGHT, buff=1.7)
        p2_arr1 = Arrow(
            p2_a.get_right(), p2_b.get_left(),
            buff=0.08, color=ORANGE, stroke_width=4,
            max_tip_length_to_length_ratio=0.3,
        )
        p2_arr2 = Arrow(
            p2_b.get_right(), p2_c.get_left(),
            buff=0.08, color=ORANGE, stroke_width=4,
            max_tip_length_to_length_ratio=0.3,
        )
        path2 = VGroup(p2_a, p2_arr1, p2_b, p2_arr2, p2_c)

        imm_diagram = VGroup(path1, path2).arrange(DOWN, buff=0.7)
        imm_diagram.move_to(RIGHT * 3.5 + UP * 0.6)

        # --- IMM bullet group: placed clearly below the diagram ---
        b3 = Text("• Flexible timestep jumps", font_size=20, color=ORANGE)
        b4 = Text("• Distributional consistency (MMD)", font_size=20, color=ORANGE)
        imm_bullets = VGroup(b3, b4).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        imm_bullets.next_to(imm_diagram, DOWN, buff=0.8)
        imm_bullets.set_x(imm_header.get_x())

        self.play(Write(imm_header), run_time=0.6)
        self.play(
            FadeIn(p1_a, scale=1.3), FadeIn(p1_b, scale=1.3),
            run_time=0.6,
        )
        self.play(GrowFromPoint(p1_arr, p1_arr.get_start()), run_time=0.5)
        self.play(
            LaggedStart(
                FadeIn(p2_a, scale=1.3),
                FadeIn(p2_b, scale=1.3),
                FadeIn(p2_c, scale=1.3),
                lag_ratio=0.2,
            ),
            run_time=0.9,
        )
        self.play(
            GrowFromPoint(p2_arr1, p2_arr1.get_start()),
            GrowFromPoint(p2_arr2, p2_arr2.get_start()),
            run_time=0.6,
        )
        self.play(
            LaggedStart(*[FadeIn(b, shift=RIGHT * 0.3) for b in imm_bullets], lag_ratio=0.3),
            run_time=0.8,
        )
        self.wait(0.3)

        # ============ Phase 4: Highlight Contrast ============
        self.play(Circumscribe(chain, color=YELLOW, run_time=1.0))
        self.wait(0.2)
        self.play(Circumscribe(imm_diagram, color=YELLOW, run_time=1.0))
        self.wait(0.2)

        # ============ Phase 5: Summary Box ============
        summary_box = RoundedRectangle(
            width=10, height=0.85, corner_radius=0.15,
            color=GREEN, fill_color=GREEN, fill_opacity=0.3,
        )
        summary_box.set_stroke(GREEN, width=3)
        summary_text = Text(
            "IMM aims for efficient few-step generation.",
            font_size=24, color=WHITE,
        )
        summary = VGroup(summary_box, summary_text)
        summary_text.move_to(summary_box.get_center())
        summary.move_to(DOWN * 2.8)

        self.play(FadeIn(summary, run_time=1.2))
        self.wait(0.4)

        # ============ Phase 6: Final Emphasis ============
        self.play(summary.animate.scale(1.12), run_time=0.3)
        self.play(summary.animate.scale(1 / 1.12), run_time=0.3)

        emphasis = Text("Efficient few-step generation", font_size=34,
                        color=GREEN, weight=BOLD)
        emphasis.next_to(summary, DOWN, buff=0.35)
        self.play(FadeIn(emphasis, shift=UP * 0.3, run_time=0.7))
        self.play(Indicate(emphasis, color=YELLOW, scale_factor=1.05), run_time=0.7)

        self.wait(2)