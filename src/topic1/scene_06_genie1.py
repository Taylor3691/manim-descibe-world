"""
SCENE 6 — Genie 1: Inferring Hidden Actions
Time: 14:00–18:00

frame_t → ? → frame_t+1 → backward inference → reveal latent action.
Includes Video Tokenizer and Latent Action Model diagrams.
"""

from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from topic1.shared_styles import *


class Scene06Genie1(Scene):
    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self):
        scene_title_sequence(
            self,
            "Genie 1",
            "Inferring Hidden Actions from Video",
        )

        # ── Part 1: The problem — frame_t  ?  frame_t+1 ──
        frame_t = make_frame_rect(width=2.4, height=1.35, color=DATA_COLOR, label="frame_t")
        frame_t.move_to(LEFT * 4)

        question = Text("?", font_size=60, color=GENIE_COLOR, weight=BOLD)
        question.move_to(ORIGIN)

        frame_t1 = make_frame_rect(width=2.4, height=1.35, color=DATA_COLOR, label="frame_t+1")
        frame_t1.move_to(RIGHT * 4)

        # Arrows
        arrow_left = Arrow(
            LEFT * 2.5, LEFT * 0.7,
            color=TEXT_DIM, stroke_width=2, buff=0,
        )
        arrow_right = Arrow(
            RIGHT * 0.7, RIGHT * 2.5,
            color=TEXT_DIM, stroke_width=2, buff=0,
        )

        problem_label = body_text(
            "Videos don't contain action labels",
            font_size=20, color=TEXT_DIM,
        ).to_edge(UP, buff=0.5)

        self.play(
            FadeIn(frame_t, shift=RIGHT * 0.3),
            FadeIn(frame_t1, shift=LEFT * 0.3),
            run_time=0.8,
        )
        self.play(
            GrowArrow(arrow_left),
            GrowArrow(arrow_right),
            FadeIn(question, scale=2),
            FadeIn(problem_label),
            run_time=0.8,
        )
        self.wait(1)

        # ── Part 2: Backward inference — scan line from future ──
        self.play(FadeOut(problem_label), run_time=0.3)

        inference_label = body_text(
            "Look at the future → infer the hidden action",
            font_size=20, color=GENIE_COLOR,
        ).to_edge(UP, buff=0.5)
        self.play(FadeIn(inference_label, shift=DOWN * 0.2), run_time=0.5)

        # Bright scan line moving from future frame backward
        scan_line = Line(
            frame_t1.get_left() + UP * 0.7,
            frame_t1.get_left() + DOWN * 0.7,
            color=HIGHLIGHT_COLOR, stroke_width=3,
        )
        scan_glow = scan_line.copy().set_stroke(width=10, opacity=0.3)

        self.play(
            FadeIn(scan_line), FadeIn(scan_glow),
            frame_t1[0].animate.set_stroke(color=HIGHLIGHT_COLOR, width=3),
            run_time=0.5,
        )

        # Move scan line from right to left (backward through time)
        self.play(
            scan_line.animate.move_to(question.get_center()),
            scan_glow.animate.move_to(question.get_center()),
            run_time=1.2,
            rate_func=linear,
        )

        # ── Part 3: Reveal the hidden latent action ──
        # Replace ? with latent action
        latent_action = VGroup(
            make_latent_arrow(
                start=LEFT * 1.5, end=RIGHT * 1.5, color=LATENT_COLOR,
            ),
            math_label(r"\alpha_t", font_size=32, color=LATENT_COLOR).shift(UP * 0.4),
        ).move_to(ORIGIN)

        self.play(
            FadeOut(question),
            FadeOut(scan_line), FadeOut(scan_glow),
            FadeOut(arrow_left), FadeOut(arrow_right),
            FadeIn(latent_action, scale=0.5),
            run_time=0.8,
        )
        self.wait(0.5)

        revealed_label = label_text(
            "Hidden action revealed", font_size=16, color=LATENT_COLOR,
        ).next_to(latent_action, DOWN, buff=0.3)
        self.play(FadeIn(revealed_label), run_time=0.4)
        self.wait(1)

        # ── Part 4: Architecture diagram ──
        self.play(
            FadeOut(VGroup(
                frame_t, frame_t1, latent_action,
                inference_label, revealed_label,
            )),
            run_time=0.6,
        )

        arch_title = subtitle_text("Genie Architecture", font_size=28)
        arch_title.to_edge(UP, buff=0.4)
        self.play(FadeIn(arch_title), run_time=0.5)

        # Input frames
        input_frames = VGroup()
        for i in range(4):
            f = Rectangle(
                width=0.8, height=0.6,
                color=DATA_COLOR, fill_opacity=0.1, stroke_width=1.5,
            )
            lbl = label_text(f"f_{i + 1}", font_size=12, color=DATA_COLOR).move_to(f)
            input_frames.add(VGroup(f, lbl))
        input_frames.arrange(RIGHT, buff=0.15)
        input_frames.move_to(LEFT * 3 + UP * 0.5)

        input_label = label_text("Input Frames", font_size=14, color=TEXT_DIM)
        input_label.next_to(input_frames, DOWN, buff=0.2)

        self.play(FadeIn(input_frames), FadeIn(input_label), run_time=0.6)

        # Video Tokenizer block
        vt_block = RoundedRectangle(
            width=2.5, height=1.2,
            corner_radius=0.15,
            color=AGENT_COLOR, fill_opacity=0.12, stroke_width=2,
        ).move_to(UP * 0.5)
        vt_label = Text(
            "Video\nTokenizer", font_size=16, color=AGENT_COLOR, weight=BOLD,
        ).move_to(vt_block)

        # Latent Action Model block
        lam_block = RoundedRectangle(
            width=2.5, height=1.2,
            corner_radius=0.15,
            color=LATENT_COLOR, fill_opacity=0.12, stroke_width=2,
        ).move_to(DOWN * 1.5)
        lam_label = Text(
            "Latent Action\nModel", font_size=16, color=LATENT_COLOR, weight=BOLD,
        ).move_to(lam_block)

        # Arrows from input to blocks
        arr_to_vt = Arrow(
            input_frames.get_right(), vt_block.get_left(),
            color=DATA_COLOR, stroke_width=2, buff=0.1,
        )
        arr_to_lam = Arrow(
            input_frames.get_right() + DOWN * 0.5,
            lam_block.get_left(),
            color=DATA_COLOR, stroke_width=2, buff=0.1,
        )

        self.play(
            FadeIn(vt_block), FadeIn(vt_label),
            FadeIn(lam_block), FadeIn(lam_label),
            GrowArrow(arr_to_vt),
            GrowArrow(arr_to_lam),
            run_time=0.8,
        )

        # Outputs
        tokens_output = VGroup()
        for i in range(4):
            t = RoundedRectangle(
                width=0.6, height=0.4,
                corner_radius=0.08,
                color=AGENT_COLOR, fill_opacity=0.2, stroke_width=1,
            )
            lbl = math_label(f"z_{i + 1}", font_size=18, color=AGENT_COLOR).move_to(t)
            tokens_output.add(VGroup(t, lbl))
        tokens_output.arrange(RIGHT, buff=0.1)
        tokens_output.move_to(RIGHT * 4 + UP * 0.5)

        actions_output = VGroup()
        for i in range(3):
            a = RoundedRectangle(
                width=0.6, height=0.4,
                corner_radius=0.08,
                color=LATENT_COLOR, fill_opacity=0.2, stroke_width=1,
            )
            lbl = math_label(rf"\alpha_{i + 1}", font_size=18, color=LATENT_COLOR).move_to(a)
            actions_output.add(VGroup(a, lbl))
        actions_output.arrange(RIGHT, buff=0.1)
        actions_output.move_to(RIGHT * 4 + DOWN * 1.5)

        arr_vt_out = Arrow(
            vt_block.get_right(), tokens_output.get_left(),
            color=AGENT_COLOR, stroke_width=2, buff=0.1,
        )
        arr_lam_out = Arrow(
            lam_block.get_right(), actions_output.get_left(),
            color=LATENT_COLOR, stroke_width=2, buff=0.1,
        )

        token_label = label_text("Tokens (T)", font_size=14, color=AGENT_COLOR)
        token_label.next_to(tokens_output, UP, buff=0.15)
        action_label = label_text("Latent Actions (T-1)", font_size=14, color=LATENT_COLOR)
        action_label.next_to(actions_output, DOWN, buff=0.15)

        self.play(
            GrowArrow(arr_vt_out), FadeIn(tokens_output),
            FadeIn(token_label),
            run_time=0.6,
        )
        self.play(
            GrowArrow(arr_lam_out), FadeIn(actions_output),
            FadeIn(action_label),
            run_time=0.6,
        )

        # Highlight the "future frame" trick in LAM
        future_note = body_text(
            "LAM looks at future frame f_{t+1}\nto infer action α_t",
            font_size=16, color=LATENT_COLOR,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(future_note, shift=UP * 0.2), run_time=0.5)

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
