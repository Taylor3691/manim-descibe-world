"""
SCENE 1 — HOOK: "Can AI Learn a World?"
Time: 0:00–2:30

Rapid montage of video frames → freeze one → branch into futures → title reveal.
"""

from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from topic1.shared_styles import *


class Scene01Hook(Scene):
    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self):
        # ── Part 1: Rapid montage of "video frames" ──
        frame_labels = ["Platformer", "Robot", "Driving", "Internet Video"]
        colors = [ACTION_COLOR, AGENT_COLOR, WORLD_COLOR, DATA_COLOR]
        montage_frames = VGroup()

        for i, (lbl, c) in enumerate(zip(frame_labels, colors)):
            frame = Rectangle(
                width=2.8, height=1.6,
                color=c, fill_opacity=0.12, stroke_width=2,
            )
            frame_lbl = label_text(lbl, font_size=18, color=c).move_to(frame)
            # Add some visual noise (small rectangles inside to simulate content)
            noise = VGroup()
            rng = np.random.RandomState(42 + i)
            for _ in range(6):
                r = Rectangle(
                    width=rng.uniform(0.3, 0.8),
                    height=rng.uniform(0.15, 0.4),
                    color=c, fill_opacity=rng.uniform(0.05, 0.2),
                    stroke_width=0,
                )
                r.move_to(frame.get_center() + np.array([
                    rng.uniform(-1, 1), rng.uniform(-0.5, 0.5), 0
                ]))
                noise.add(r)
            montage_frames.add(VGroup(frame, noise, frame_lbl))

        # Show frames rapidly one by one
        for i, f in enumerate(montage_frames):
            f.move_to(ORIGIN)
            self.play(FadeIn(f, shift=RIGHT * 0.5), run_time=0.4)
            self.wait(0.3)
            if i < len(montage_frames) - 1:
                self.play(FadeOut(f, shift=LEFT * 0.5), run_time=0.3)

        # ── Part 2: Freeze last frame ──
        frozen = montage_frames[-1]
        freeze_border = Rectangle(
            width=2.9, height=1.7,
            color=HIGHLIGHT_COLOR, stroke_width=3, fill_opacity=0,
        ).move_to(frozen)
        freeze_label = label_text("▶ FREEZE", font_size=14, color=HIGHLIGHT_COLOR)
        freeze_label.next_to(freeze_border, UR, buff=0.1)

        self.play(
            Create(freeze_border),
            FadeIn(freeze_label),
            run_time=0.6,
        )
        self.wait(0.5)

        # Shrink frozen frame and move to left
        self.play(
            VGroup(frozen, freeze_border, freeze_label).animate.scale(0.6).move_to(LEFT * 4),
            run_time=0.8,
        )

        # ── Part 3: Branch into multiple futures ──
        branch_origin = LEFT * 2.5
        n_branches = 5
        branch_angles = np.linspace(-PI / 4, PI / 4, n_branches)
        branch_length = 3.5
        branches = VGroup()
        future_frames = VGroup()

        for i, angle in enumerate(branch_angles):
            end = branch_origin + np.array([
                branch_length * np.cos(angle),
                branch_length * np.sin(angle),
                0,
            ])
            arrow = Arrow(
                branch_origin, end,
                color=interpolate_color(
                    ManimColor(AGENT_COLOR), ManimColor(LATENT_COLOR), i / (n_branches - 1)
                ),
                stroke_width=2,
                buff=0,
                max_tip_length_to_length_ratio=0.08,
            )
            # Small future frame at end
            future = Rectangle(
                width=1.0, height=0.56,
                color=interpolate_color(
                    ManimColor(AGENT_COLOR), ManimColor(LATENT_COLOR), i / (n_branches - 1)
                ),
                fill_opacity=0.15,
                stroke_width=1.5,
            ).move_to(end)
            future_lbl = label_text(f"Future {i + 1}", font_size=10).move_to(future)
            branches.add(arrow)
            future_frames.add(VGroup(future, future_lbl))

        # Animate branches growing like a tree
        self.play(
            LaggedStart(
                *[GrowArrow(a) for a in branches],
                lag_ratio=0.15,
            ),
            run_time=1.5,
        )
        self.play(
            LaggedStart(
                *[FadeIn(f, scale=0.5) for f in future_frames],
                lag_ratio=0.1,
            ),
            run_time=1.0,
        )
        self.wait(0.5)

        # ── Part 4: Zoom into one branch ──
        chosen_idx = 2  # middle branch
        chosen_future = future_frames[chosen_idx]

        # Highlight chosen branch
        highlight_ring = Circle(
            radius=0.6, color=HIGHLIGHT_COLOR, stroke_width=2, fill_opacity=0,
        ).move_to(chosen_future)
        self.play(Create(highlight_ring), run_time=0.5)

        # Fade everything else, zoom into chosen
        others = VGroup(
            *[b for i, b in enumerate(branches) if i != chosen_idx],
            *[f for i, f in enumerate(future_frames) if i != chosen_idx],
            frozen, freeze_border, freeze_label,
        )
        self.play(
            FadeOut(others),
            FadeOut(highlight_ring),
            chosen_future.animate.scale(3).move_to(ORIGIN),
            branches[chosen_idx].animate.set_opacity(0),
            run_time=1.2,
        )
        self.play(FadeOut(chosen_future), FadeOut(branches[chosen_idx]), run_time=0.5)

        # ── Part 5: Title reveal ──
        title_line1 = Text(
            "Scaling Foundation World Models",
            font_size=38, color=TEXT_PRIMARY, weight=BOLD,
        )
        title_line2 = Text(
            "as a Path to Embodied AGI",
            font_size=34, color=HIGHLIGHT_COLOR, weight=BOLD,
        )
        title_group = VGroup(title_line1, title_line2).arrange(DOWN, buff=0.3)

        # Decorative line
        deco_line = Line(LEFT * 4, RIGHT * 4, color=AGENT_COLOR, stroke_width=1)
        deco_line.next_to(title_group, DOWN, buff=0.5)

        credit = label_text(
            "Inspired by Jack Parker-Holder's talk",
            font_size=16, color=TEXT_DIM,
        ).next_to(deco_line, DOWN, buff=0.3)

        self.play(
            FadeIn(title_line1, shift=UP * 0.3),
            run_time=1,
        )
        self.play(
            FadeIn(title_line2, shift=UP * 0.2),
            run_time=0.8,
        )
        self.play(
            Create(deco_line),
            FadeIn(credit),
            run_time=0.8,
        )
        self.wait(2)
        self.play(
            FadeOut(VGroup(title_group, deco_line, credit)),
            run_time=1,
        )
