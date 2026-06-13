from manim import *
import numpy as np

class MMDAlignsDistributions(Scene):
    def construct(self):
        np.random.seed(42)

        # === Title ===
        title = Text("MMD aligns the distributions", font_size=42, weight=BOLD)
        title.to_edge(UP, buff=0.4)

        # === Point clouds ===
        def make_cloud(cx, n=40, spread=0.75, color=BLUE_D):
            dots = VGroup()
            for _ in range(n):
                ox = np.random.uniform(-spread, spread)
                oy = np.random.uniform(-spread, spread)
                dot = Dot([cx + ox, oy, 0], radius=0.05,
                          color=color, fill_opacity=0.9)
                dots.add(dot)
            return dots

        cloud_a = make_cloud(-3.5, color=BLUE_D)
        cloud_b = make_cloud(3.5, color=TEAL_D)

        # Cloud labels
        label_a = Text("Distribution A", font_size=22, color=BLUE_D)
        label_a.next_to(cloud_a, DOWN, buff=0.4)
        label_b = Text("Distribution B", font_size=22, color=TEAL_D)
        label_b.next_to(cloud_b, DOWN, buff=0.4)

        # === MMD indicator (double-headed arrow) ===
        mmd_arrow = DoubleArrow(
            [-2.2, 0, 0], [2.2, 0, 0],
            color=RED_E, stroke_width=8, buff=0
        )
        mmd_text = Text("MMD", font_size=30, color=RED_E, weight=BOLD)
        mmd_text.next_to(mmd_arrow, UP, buff=0.15)

        # Mismatch label (above MMD text)
        mismatch_large = Text("Large mismatch", font_size=22, color=RED_E, weight=BOLD)
        mismatch_large.next_to(mmd_text, UP, buff=0.2)

        # === Bottom caption ===
        bottom = Text(
            "Train the model so different paths produce matching distributions.",
            font_size=20
        )
        bottom.to_edge(DOWN, buff=0.4)

        # === Phase 1: Intro ===
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=1.2)
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in cloud_a], lag_ratio=0.02),
            LaggedStart(*[FadeIn(d, scale=0.5) for d in cloud_b], lag_ratio=0.02),
            FadeIn(label_a, shift=UP * 0.2),
            FadeIn(label_b, shift=UP * 0.2),
            run_time=2
        )
        self.wait(0.3)

        # === Phase 2: Draw MMD indicator ===
        self.play(
            GrowFromCenter(mmd_arrow),
            FadeIn(mmd_text),
            run_time=2.5
        )
        self.wait(0.3)

        # === Phase 3: Large mismatch label ===
        self.play(FadeIn(mismatch_large, shift=UP * 0.2), run_time=1.5)
        self.wait(0.3)

        # === Phase 4: Optimization (clouds move, arrow shrinks, color: red -> green) ===
        new_arrow = DoubleArrow(
            [-1, 0, 0], [1, 0, 0],
            color=GREEN_E, stroke_width=8, buff=0
        )
        new_mmd_text = Text("MMD", font_size=30, color=GREEN_E, weight=BOLD)
        new_mmd_text.next_to(new_arrow, UP, buff=0.15)

        self.play(
            cloud_a.animate.shift(RIGHT * 1.5),
            cloud_b.animate.shift(LEFT * 1.5),
            Transform(mmd_arrow, new_arrow),
            Transform(mmd_text, new_mmd_text),
            run_time=4
        )
        self.wait(0.3)

        # === Phase 5: Small mismatch label (cross-fade) ===
        mismatch_small = Text("Small mismatch", font_size=22, color=GREEN_E, weight=BOLD)
        mismatch_small.move_to(mismatch_large.get_center())

        self.play(
            FadeOut(mismatch_large),
            FadeIn(mismatch_small),
            run_time=1.5
        )
        self.wait(0.3)

        # === Phase 6: Conclusion ===
        self.play(FadeIn(bottom, shift=UP * 0.2), run_time=2.5)
        self.wait(1.5)
