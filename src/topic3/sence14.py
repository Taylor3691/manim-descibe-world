from manim import *
import numpy as np


class MMDAlignment(Scene):
    def construct(self):
        # ----- Color palette -----
        BLUE = "#1E88E5"
        ORANGE = "#FB8C00"
        RED = "#E53935"
        GREEN = "#43A047"

        # ----- Title -----
        title = Text("MMD aligns the distributions",
                     font_size=40, weight=BOLD)
        title.to_edge(UP, buff=0.4)

        # ----- Point clouds -----
        np.random.seed(7)
        cloud_a_center = LEFT * 3 + UP * 0.3
        cloud_b_center = RIGHT * 3 + UP * 0.3

        cloud_a = VGroup(*[
            Dot(
                cloud_a_center + np.array([
                    np.random.uniform(-0.8, 0.8),
                    np.random.uniform(-0.55, 0.55),
                    0
                ]),
                radius=0.07,
                color=BLUE
            )
            for _ in range(35)
        ])
        cloud_b = VGroup(*[
            Dot(
                cloud_b_center + np.array([
                    np.random.uniform(-0.8, 0.8),
                    np.random.uniform(-0.55, 0.55),
                    0
                ]),
                radius=0.07,
                color=ORANGE
            )
            for _ in range(35)
        ])

        # ----- MMD bracket helper -----
        def make_bracket(left_pt, right_pt, color):
            line = Line(left_pt, right_pt, color=color, stroke_width=6)
            tick_h = 0.18
            tick_l = Line(
                left_pt + UP * tick_h,
                left_pt + DOWN * tick_h,
                color=color, stroke_width=6
            )
            tick_r = Line(
                right_pt + UP * tick_h,
                right_pt + DOWN * tick_h,
                color=color, stroke_width=6
            )
            return VGroup(line, tick_l, tick_r)

        # ----- MMD indicator (initial: red, large) -----
        mmd_y = 0.3
        mmd_bracket = make_bracket(LEFT * 2.0 + UP * mmd_y,
                                    RIGHT * 2.0 + UP * mmd_y, RED)
        mmd_label = Text("MMD", font_size=30, color=RED, weight=BOLD)
        mmd_label.next_to(mmd_bracket, UP, buff=0.2)

        large_mismatch = Text("Large mismatch", font_size=22, color=RED)
        large_mismatch.next_to(mmd_bracket, DOWN, buff=0.35)

        # ----- MMD indicator (final: green, small) -----
        mmd_bracket_final = make_bracket(LEFT * 0.5 + UP * mmd_y,
                                          RIGHT * 0.5 + UP * mmd_y, GREEN)
        mmd_label_final = Text("MMD", font_size=30, color=GREEN, weight=BOLD)
        mmd_label_final.next_to(mmd_bracket_final, UP, buff=0.2)
        small_mismatch = Text("Small mismatch", font_size=22, color=GREEN)
        small_mismatch.next_to(mmd_bracket_final, DOWN, buff=0.35)

        # ----- Footer -----
        footer = Text(
            "Train the model so different paths produce matching distributions.",
            font_size=20
        )
        footer.to_edge(DOWN, buff=0.4)

        # ============ PHASE 1: Intro (~3s) ============
        self.play(
            FadeIn(title, shift=DOWN * 0.3),
            FadeIn(cloud_a),
            FadeIn(cloud_b),
            run_time=2
        )
        self.wait(1)

        # ============ PHASE 2: Draw MMD Indicator (~2s) ============
        self.play(
            Create(mmd_bracket),
            Write(mmd_label),
            run_time=1.5
        )
        self.wait(0.5)

        # ============ PHASE 3: Show Large Mismatch (~1s) ============
        self.play(FadeIn(large_mismatch, shift=UP * 0.2), run_time=1)
        self.wait(0.5)

        # ============ PHASE 4: Optimization (~5s) ============
        self.play(
            cloud_a.animate.shift(RIGHT * 1.5),
            cloud_b.animate.shift(LEFT * 1.5),
            Transform(mmd_bracket, mmd_bracket_final),
            Transform(mmd_label, mmd_label_final),
            FadeOut(large_mismatch),
            FadeIn(small_mismatch),
            run_time=4
        )
        self.wait(0.5)

        # ============ PHASE 5: Final Takeaway (~3s) ============
        self.play(FadeIn(footer, shift=UP * 0.3), run_time=1.5)
        self.wait(1.5)

        self.wait()
