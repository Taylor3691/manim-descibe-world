"""
SCENE 5 — Prediction vs Interaction
Time: 11:00–14:00

Split screen: LEFT = passive linear video, RIGHT = interactive branching futures.
"""

from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from topic1.shared_styles import *


class Scene05PredictionVsInteraction(Scene):
    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self):
        scene_title_sequence(self, "Prediction vs Interaction")

        # ── Divider ──
        divider = DashedLine(
            UP * 3.5, DOWN * 3.5,
            color=TEXT_DIM, stroke_width=1, dash_length=0.15,
        )
        self.play(Create(divider), run_time=0.5)

        # ── Headers ──
        header_left = Text(
            "Passive Video Model",
            font_size=22, color=DATA_COLOR, weight=BOLD,
        ).move_to(UP * 3 + LEFT * 3.5)
        header_right = Text(
            "Interactive World Model",
            font_size=22, color=ACTION_COLOR, weight=BOLD,
        ).move_to(UP * 3 + RIGHT * 3.5)

        question_left = Text(
            '"What frame comes next?"',
            font_size=16, color=TEXT_DIM, slant=ITALIC,
        ).next_to(header_left, DOWN, buff=0.25)
        question_right = Text(
            '"What happens if I act?"',
            font_size=16, color=TEXT_DIM, slant=ITALIC,
        ).next_to(header_right, DOWN, buff=0.25)

        self.play(
            FadeIn(header_left), FadeIn(header_right),
            FadeIn(question_left), FadeIn(question_right),
            run_time=0.8,
        )

        # ── Same starting frame on both sides ──
        start_frame_left = Rectangle(
            width=2.0, height=1.13,
            color=DATA_COLOR, fill_opacity=0.15, stroke_width=2,
        ).move_to(LEFT * 3.5 + UP * 0.8)
        start_lbl_left = label_text("Frame₀", font_size=14, color=DATA_COLOR)
        start_lbl_left.move_to(start_frame_left)

        start_frame_right = Rectangle(
            width=2.0, height=1.13,
            color=ACTION_COLOR, fill_opacity=0.15, stroke_width=2,
        ).move_to(RIGHT * 3.5 + UP * 0.8)
        start_lbl_right = label_text("Frame₀", font_size=14, color=ACTION_COLOR)
        start_lbl_right.move_to(start_frame_right)

        self.play(
            FadeIn(start_frame_left), FadeIn(start_lbl_left),
            FadeIn(start_frame_right), FadeIn(start_lbl_right),
            run_time=0.6,
        )

        # ── LEFT: Linear continuation ──
        left_frames = VGroup()
        left_arrows = VGroup()
        for i in range(3):
            y = 0.8 - (i + 1) * 1.1
            frame = Rectangle(
                width=2.0, height=0.7,
                color=DATA_COLOR, fill_opacity=0.08, stroke_width=1.5,
            ).move_to(LEFT * 3.5 + UP * y)
            lbl = label_text(f"Frame_{i + 1}", font_size=12, color=DATA_COLOR)
            lbl.move_to(frame)
            left_frames.add(VGroup(frame, lbl))

            arrow_start = LEFT * 3.5 + UP * (y + 0.55)
            arrow_end = LEFT * 3.5 + UP * (y + 0.15)
            arrow = Arrow(
                arrow_start, arrow_end,
                color=DATA_COLOR, stroke_width=2,
                max_tip_length_to_length_ratio=0.3,
                buff=0,
            )
            left_arrows.add(arrow)

        for arrow, frame in zip(left_arrows, left_frames):
            self.play(
                GrowArrow(arrow),
                FadeIn(frame, shift=DOWN * 0.2),
                run_time=0.4,
            )

        # ── RIGHT: Branching futures based on actions ──
        # First branch from starting frame
        branch_y = 0.0
        n_branches = 3
        action_labels = ["Action A", "Action B", "Action C"]
        branch_colors = [ACTION_COLOR, HIGHLIGHT_COLOR, LATENT_COLOR]
        branch_x_positions = [RIGHT * 2, RIGHT * 3.5, RIGHT * 5]

        right_elements = VGroup()

        for i in range(n_branches):
            # Arrow from start frame to branch
            end_pos = branch_x_positions[i] + UP * branch_y
            arrow = Arrow(
                start_frame_right.get_bottom(),
                end_pos + UP * 0.35,
                color=branch_colors[i],
                stroke_width=2,
                buff=0,
                max_tip_length_to_length_ratio=0.12,
            )

            frame = Rectangle(
                width=1.3, height=0.7,
                color=branch_colors[i], fill_opacity=0.12, stroke_width=1.5,
            ).move_to(end_pos)

            action_lbl = label_text(
                action_labels[i], font_size=11, color=branch_colors[i]
            )
            action_lbl.next_to(arrow, RIGHT if i > 0 else LEFT, buff=0.05)
            action_lbl.scale(0.8)

            future_lbl = label_text(
                f"Future {i + 1}", font_size=11, color=branch_colors[i]
            ).move_to(frame)

            right_elements.add(VGroup(arrow, frame, action_lbl, future_lbl))

        # Second level branching from middle branch
        second_branches = VGroup()
        for i, dx in enumerate([-0.7, 0.7]):
            end_pos = RIGHT * 3.5 + DOWN * 1.3 + RIGHT * dx
            arrow = Arrow(
                RIGHT * 3.5 + UP * branch_y + DOWN * 0.35,
                end_pos + UP * 0.25,
                color=interpolate_color(ManimColor(HIGHLIGHT_COLOR), ManimColor(DATA_COLOR), 0.5),
                stroke_width=1.5,
                buff=0,
                max_tip_length_to_length_ratio=0.15,
            )
            frame = Rectangle(
                width=1.0, height=0.5,
                color=HIGHLIGHT_COLOR, fill_opacity=0.08, stroke_width=1,
            ).move_to(end_pos)
            second_branches.add(VGroup(arrow, frame))

        # Animate right side
        for elem in right_elements:
            self.play(
                GrowArrow(elem[0]),
                FadeIn(elem[1], scale=0.5),
                FadeIn(elem[2]),
                FadeIn(elem[3]),
                run_time=0.5,
            )

        self.play(
            LaggedStart(
                *[AnimationGroup(GrowArrow(sb[0]), FadeIn(sb[1], scale=0.5))
                  for sb in second_branches],
                lag_ratio=0.3,
            ),
            run_time=0.8,
        )

        # ── Emphasis text ──
        emphasis = Text(
            "That single difference changes everything.",
            font_size=22,
            color=HIGHLIGHT_COLOR,
            weight=BOLD,
        ).to_edge(DOWN, buff=0.5)

        self.play(FadeIn(emphasis, shift=UP * 0.2), run_time=0.8)
        self.wait(2)

        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1,
        )
