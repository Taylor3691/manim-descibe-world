"""
SCENE 10 — The Real-Time Caveat
Time: 31:00–32:30

Speed gauge, "Not Real-Time Yet", brief factual note.
"""

from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from topic1.shared_styles import *


class Scene10RealtimeCaveat(Scene):
    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self):
        # No scene title sequence — keep this scene brief

        # ── Speed Gauge ──
        gauge_center = UP * 0.5
        gauge_radius = 2.0

        # Arc background (semi-circle)
        gauge_bg = Arc(
            radius=gauge_radius,
            start_angle=PI,
            angle=PI,
            color=TEXT_DIM,
            stroke_width=8,
            stroke_opacity=0.2,
            arc_center=gauge_center,
        )

        # Color gradient segments on the gauge
        n_segments = 20
        gauge_segments = VGroup()
        for i in range(n_segments):
            frac = i / n_segments
            start = PI + frac * PI
            seg = Arc(
                radius=gauge_radius,
                start_angle=start,
                angle=PI / n_segments * 0.9,
                color=interpolate_color(
                    ManimColor(GENIE_COLOR),
                    ManimColor(ACTION_COLOR),
                    frac,
                ),
                stroke_width=12,
                stroke_opacity=0.5,
                arc_center=gauge_center,
            )
            gauge_segments.add(seg)

        # Speed labels
        slow_label = label_text("Slow", font_size=16, color=GENIE_COLOR)
        slow_label.move_to(gauge_center + LEFT * (gauge_radius + 0.5) + DOWN * 0.1)
        fast_label = label_text("Fast", font_size=16, color=ACTION_COLOR)
        fast_label.move_to(gauge_center + RIGHT * (gauge_radius + 0.5) + DOWN * 0.1)

        # Needle — pointing to "slow" area (about 30% of the way)
        needle_angle = PI + PI * 0.25  # 25% → slow side
        needle_end = gauge_center + np.array([
            (gauge_radius - 0.3) * np.cos(needle_angle),
            (gauge_radius - 0.3) * np.sin(needle_angle),
            0,
        ])
        needle = Arrow(
            gauge_center, needle_end,
            color=HIGHLIGHT_COLOR, stroke_width=4, buff=0,
            max_tip_length_to_length_ratio=0.1,
        )
        needle_dot = Dot(gauge_center, radius=0.12, color=HIGHLIGHT_COLOR)

        # Tick marks
        ticks = VGroup()
        for i in range(11):
            angle = PI + i * PI / 10
            inner = gauge_center + np.array([
                (gauge_radius - 0.15) * np.cos(angle),
                (gauge_radius - 0.15) * np.sin(angle), 0,
            ])
            outer = gauge_center + np.array([
                (gauge_radius + 0.15) * np.cos(angle),
                (gauge_radius + 0.15) * np.sin(angle), 0,
            ])
            tick = Line(inner, outer, color=TEXT_DIM, stroke_width=1.5)
            ticks.add(tick)

        gauge = VGroup(gauge_bg, gauge_segments, ticks, slow_label, fast_label)

        self.play(
            FadeIn(gauge),
            run_time=0.8,
        )
        self.play(
            FadeIn(needle_dot),
            GrowArrow(needle),
            run_time=0.6,
        )
        self.wait(0.5)

        # ── "Not Real-Time Yet" label ──
        caveat_text = Text(
            "Not Real-Time Yet",
            font_size=36, color=GENIE_COLOR, weight=BOLD,
        ).move_to(DOWN * 1.2)

        caveat_underline = Line(
            caveat_text.get_left() + DOWN * 0.15,
            caveat_text.get_right() + DOWN * 0.15,
            color=GENIE_COLOR, stroke_width=2,
        )

        self.play(
            FadeIn(caveat_text, shift=UP * 0.2),
            Create(caveat_underline),
            run_time=0.8,
        )
        self.wait(0.5)

        # ── Note about internal version ──
        note_bg = RoundedRectangle(
            width=6, height=0.8,
            corner_radius=0.1,
            color=TEXT_DIM, fill_opacity=0.08, stroke_width=1,
        ).move_to(DOWN * 2.5)

        note_text = Text(
            "⚡ A faster distilled version exists internally at DeepMind",
            font_size=16, color=TEXT_DIM,
        ).move_to(note_bg)

        self.play(
            FadeIn(note_bg),
            FadeIn(note_text),
            run_time=0.6,
        )

        # Brief explanation
        explain = label_text(
            "The public version trades speed for quality",
            font_size=14, color=TEXT_DIM,
        ).next_to(note_bg, DOWN, buff=0.2)

        self.play(FadeIn(explain), run_time=0.4)
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)
