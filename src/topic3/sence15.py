from manim import *
import numpy as np


class ColorThrough(Animation):
    """Smoothly transition a mobject's color through a list of color stops."""
    def __init__(self, mobject, colors, **kwargs):
        self.colors = colors
        self.n = max(len(colors) - 1, 1)
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha):
        if self.n == 0:
            self.mobject.set_color(self.colors[0])
            return
        idx = min(int(alpha * self.n), self.n - 1)
        local_alpha = alpha * self.n - idx
        self.mobject.set_color(
            interpolate_color(self.colors[idx], self.colors[idx + 1], local_alpha)
        )


class ArrowAlign(Animation):
    """Animate a DoubleArrow's endpoints and color together in one pass."""
    def __init__(self, arrow, target_start, target_end, colors, **kwargs):
        self.arrow = arrow
        self.target_start = np.array(target_start, dtype=float)
        self.target_end = np.array(target_end, dtype=float)
        self.original_start = np.array(arrow.get_start(), dtype=float)
        self.original_end = np.array(arrow.get_end(), dtype=float)
        self.colors = colors
        self.n = max(len(colors) - 1, 1)
        self.arrow_kwargs = {
            "stroke_width": arrow.stroke_width,
            "buff": arrow.buff,
            "tip_length": arrow.tip_length,
        }
        super().__init__(arrow, **kwargs)

    def interpolate_mobject(self, alpha):
        new_start = interpolate(self.original_start, self.target_start, alpha)
        new_end = interpolate(self.original_end, self.target_end, alpha)
        if self.n == 0:
            color = self.colors[0]
        else:
            idx = min(int(alpha * self.n), self.n - 1)
            local_alpha = alpha * self.n - idx
            color = interpolate_color(
                self.colors[idx], self.colors[idx + 1], local_alpha
            )
        new_arrow = DoubleArrow(
            start=new_start,
            end=new_end,
            color=color,
            **self.arrow_kwargs,
        )
        self.arrow.become(new_arrow)


class MMDSpec(Scene):
    def construct(self):
        # ===== Setup: title, point clouds, labels =====
        title = Text("MMD aligns the distributions", font_size=40, color=WHITE)
        title.to_edge(UP, buff=0.4)

        np.random.seed(42)
        cloud_A_dots = VGroup(*[
            Dot(
                point=np.array([
                    -3 + np.random.uniform(-0.3, 0.3),
                    np.random.uniform(-0.25, 0.25),
                    0
                ]),
                radius=0.07,
                color=BLUE,
                fill_opacity=1,
            )
            for _ in range(12)
        ])
        cloud_B_dots = VGroup(*[
            Dot(
                point=np.array([
                    3 + np.random.uniform(-0.3, 0.3),
                    np.random.uniform(-0.25, 0.25),
                    0
                ]),
                radius=0.07,
                color=ORANGE,
                fill_opacity=1,
            )
            for _ in range(12)
        ])

        label_A = Text("Distribution A", font_size=22, color=BLUE)
        label_A.next_to(cloud_A_dots, LEFT, buff=0.3)
        label_B = Text("Distribution B", font_size=22, color=ORANGE)
        label_B.next_to(cloud_B_dots, RIGHT, buff=0.3)

        # ===== Phase 1: Intro (~4s) =====
        self.play(
            FadeIn(title, shift=DOWN * 0.3),
            FadeIn(cloud_A_dots, shift=RIGHT * 0.3),
            FadeIn(cloud_B_dots, shift=LEFT * 0.3),
            FadeIn(label_A),
            FadeIn(label_B),
            run_time=2.5,
        )
        self.wait(1.5)

        # ===== Phase 2: Show MMD Indicator (~3s) =====
        right_A_x = -2.6
        left_B_x = 2.6

        mmd_arrow = DoubleArrow(
            start=np.array([right_A_x, 0, 0]),
            end=np.array([left_B_x, 0, 0]),
            color=RED,
            stroke_width=5,
            buff=0.15,
            tip_length=0.2,
        )
        mmd_label = Text("MMD", font_size=28, color=RED, weight=BOLD)
        mmd_label.next_to(mmd_arrow, UP, buff=0.15)

        mismatch_large = Text("Large mismatch", font_size=22, color=RED)
        mismatch_large.next_to(mmd_arrow, DOWN, buff=0.2)

        self.play(
            Create(mmd_arrow),
            Write(mmd_label),
            run_time=1.5,
        )
        self.play(
            FadeIn(mismatch_large, shift=UP * 0.2),
            run_time=1,
        )
        self.wait(0.5)

        # ===== Phase 3: Alignment Animation (~8s) =====
        target_A_x = -1.0
        target_B_x = 1.0
        shift_A = RIGHT * (target_A_x - (-3))
        shift_B = LEFT * (3 - target_B_x)

        target_start = np.array([target_A_x + 0.5, 0, 0])
        target_end = np.array([target_B_x - 0.5, 0, 0])

        # Use a temp arrow to position the "Small mismatch" label
        temp_arrow = DoubleArrow(
            start=target_start,
            end=target_end,
            color=GREEN,
            stroke_width=5,
            buff=0.15,
            tip_length=0.2,
        )
        mismatch_small = Text("Small mismatch", font_size=22, color=GREEN)
        mismatch_small.next_to(temp_arrow, DOWN, buff=0.2)

        color_stops = [RED, ORANGE, YELLOW, GREEN]
        self.play(
            cloud_A_dots.animate.shift(shift_A),
            cloud_B_dots.animate.shift(shift_B),
            label_A.animate.shift(shift_A),
            label_B.animate.shift(shift_B),
            ArrowAlign(mmd_arrow, target_start, target_end, color_stops),
            ColorThrough(mmd_label, color_stops),
            FadeOut(mismatch_large, shift=UP * 0.2),
            FadeIn(mismatch_small, shift=UP * 0.2),
            run_time=5.5,
        )
        self.wait(2.5)

        # ===== Phase 4: Conclusion (~3s) =====
        takeaway = Text(
            "Train the model so different paths produce matching distributions.",
            font_size=22,
            color=WHITE,
        )
        takeaway.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(takeaway, shift=UP * 0.3), run_time=1.5)
        self.wait(1.5)
