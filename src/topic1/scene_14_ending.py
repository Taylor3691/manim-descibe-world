"""
SCENE 14 — Ending
Time: 39:15–40:00

Single frame → expanding branching universe → slow camera pull back → title fade-in.
End slowly with silence before fade-out.
"""

from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from topic1.shared_styles import *


class Scene14Ending(Scene):
    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self):
        # ── Start with a single frame ──
        single_frame = Rectangle(
            width=2.0, height=1.13,
            color=DATA_COLOR, fill_opacity=0.15, stroke_width=2,
        )
        frame_glow = Rectangle(
            width=2.2, height=1.33,
            color=DATA_COLOR, fill_opacity=0.05, stroke_width=0,
        ).move_to(single_frame)

        self.play(
            FadeIn(frame_glow),
            FadeIn(single_frame, scale=0.5),
            run_time=1.0,
        )
        self.wait(0.5)

        # ── Expand into branching universe ──
        # Generate a tree of branches emanating from the frame
        branches = VGroup()
        branch_dots = VGroup()
        rng = np.random.RandomState(42)

        def create_branches(origin, angle, depth, max_depth, parent_color):
            if depth >= max_depth:
                return
            n_children = rng.randint(2, 4)
            for _ in range(n_children):
                child_angle = angle + rng.uniform(-PI / 4, PI / 4)
                length = rng.uniform(0.5, 1.2) * (1.0 - depth * 0.15)
                end = origin + np.array([
                    length * np.cos(child_angle),
                    length * np.sin(child_angle),
                    0,
                ])

                color_frac = min(1.0, depth / max_depth + rng.uniform(-0.1, 0.1))
                color = interpolate_color(
                    ManimColor(AGENT_COLOR),
                    ManimColor(LATENT_COLOR),
                    color_frac,
                )

                line = Line(
                    origin, end,
                    color=color,
                    stroke_width=max(0.5, 2.5 - depth * 0.4),
                    stroke_opacity=max(0.2, 0.8 - depth * 0.15),
                )
                branches.add(line)

                dot = Dot(
                    end, radius=max(0.02, 0.06 - depth * 0.008),
                    color=color,
                    fill_opacity=max(0.2, 0.7 - depth * 0.1),
                )
                branch_dots.add(dot)

                create_branches(end, child_angle, depth + 1, max_depth, color)

        # Create branches in multiple directions
        for base_angle in np.linspace(0, TAU, 6, endpoint=False):
            create_branches(
                ORIGIN, base_angle,
                depth=0, max_depth=4,
                parent_color=DATA_COLOR,
            )

        # Animate branches growing outward
        self.play(
            single_frame.animate.scale(0.3).set_opacity(0.3),
            frame_glow.animate.scale(0.3).set_opacity(0),
            run_time=0.5,
        )

        # Show branches in waves by distance from center
        branches_sorted = sorted(
            branches, key=lambda b: np.linalg.norm(b.get_start())
        )
        dots_sorted = sorted(
            branch_dots, key=lambda d: np.linalg.norm(d.get_center())
        )

        self.play(
            LaggedStart(
                *[Create(b) for b in branches_sorted],
                lag_ratio=0.008,
            ),
            LaggedStart(
                *[FadeIn(d, scale=0.3) for d in dots_sorted],
                lag_ratio=0.008,
            ),
            run_time=3.0,
        )

        self.wait(0.5)

        # ── Slow camera pull back (scale down everything) ──
        universe = VGroup(single_frame, frame_glow, branches, branch_dots)
        self.play(
            universe.animate.scale(0.6),
            run_time=2.0,
            rate_func=smooth,
        )

        # ── Final title fade-in ──
        title_line1 = Text(
            "Scaling Foundation World Models",
            font_size=36, color=TEXT_PRIMARY, weight=BOLD,
        )
        title_line2 = Text(
            "as a Path to Embodied AGI",
            font_size=32, color=HIGHLIGHT_COLOR, weight=BOLD,
        )
        title_group = VGroup(title_line1, title_line2).arrange(DOWN, buff=0.3)

        # Position title below the universe
        title_group.move_to(DOWN * 2.5)

        # Decorative elements
        top_line = Line(LEFT * 3, RIGHT * 3, color=AGENT_COLOR, stroke_width=1)
        top_line.next_to(title_group, UP, buff=0.3)
        bot_line = Line(LEFT * 3, RIGHT * 3, color=LATENT_COLOR, stroke_width=1)
        bot_line.next_to(title_group, DOWN, buff=0.3)

        self.play(
            FadeIn(title_line1, shift=UP * 0.2),
            Create(top_line),
            run_time=1.2,
        )
        self.play(
            FadeIn(title_line2, shift=UP * 0.2),
            Create(bot_line),
            run_time=1.0,
        )

        # Long pause — allow silence
        self.wait(3)

        # ── Fade everything out slowly ──
        self.play(
            *[FadeOut(mob, run_time=2.0) for mob in self.mobjects],
        )

        # Final black
        self.wait(1)
