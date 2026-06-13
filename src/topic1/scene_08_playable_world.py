"""
SCENE 8 — Turning Video into a Playable World
Time: 23:00–27:00

Generated world becomes controllable: action → synchronized world update.
"""

from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from topic1.shared_styles import *


class Scene08PlayableWorld(Scene):
    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self):
        scene_title_sequence(self, "Turning Video into a Playable World")

        # ── Part 1: Transition concept ──
        # Left side: passive video
        passive_label = Text(
            "Passive Observation", font_size=22, color=DATA_COLOR,
        ).move_to(LEFT * 3.5 + UP * 2.8)
        passive_strip = make_film_strip(n_frames=4, frame_w=0.7, frame_h=0.4)
        passive_strip.move_to(LEFT * 3.5 + UP * 1.5)

        # Right side: interactive
        active_label = Text(
            "Interactive Control", font_size=22, color=ACTION_COLOR,
        ).move_to(RIGHT * 3.5 + UP * 2.8)

        # Game-like world
        game_world = RoundedRectangle(
            width=4.5, height=2.5,
            corner_radius=0.2,
            color=ACTION_COLOR, fill_opacity=0.08, stroke_width=2,
        ).move_to(RIGHT * 3.5 + UP * 1.2)

        # Character inside the game world
        character = VGroup(
            Circle(radius=0.12, color=AGENT_COLOR, fill_opacity=0.8, stroke_width=0),
            Rectangle(
                width=0.15, height=0.2,
                color=AGENT_COLOR, fill_opacity=0.8, stroke_width=0,
            ).shift(DOWN * 0.18),
        ).move_to(game_world.get_center() + LEFT * 1)

        # Transition arrow
        transition_arrow = Arrow(
            LEFT * 1, RIGHT * 1,
            color=HIGHLIGHT_COLOR, stroke_width=3,
        ).move_to(UP * 1.5)
        transition_text = label_text(
            "Controllable", font_size=16, color=HIGHLIGHT_COLOR,
        ).next_to(transition_arrow, UP, buff=0.1)

        self.play(
            FadeIn(passive_label), FadeIn(passive_strip),
            run_time=0.6,
        )
        self.wait(0.5)
        self.play(
            GrowArrow(transition_arrow), FadeIn(transition_text),
            run_time=0.5,
        )
        self.play(
            FadeIn(active_label), FadeIn(game_world), FadeIn(character),
            run_time=0.6,
        )
        self.wait(0.5)

        # ── Part 2: Interactive control demo ──
        self.play(
            FadeOut(passive_label), FadeOut(passive_strip),
            FadeOut(transition_arrow), FadeOut(transition_text),
            FadeOut(active_label),
            game_world.animate.scale(1.6).move_to(UP * 0.5),
            character.animate.scale(1.6).move_to(LEFT * 3 + UP * 0.5),
            run_time=0.8,
        )

        # Platform elements inside game
        platforms = VGroup()
        platform_specs = [
            (LEFT * 4, DOWN * 1, 3),
            (LEFT * 0.5, DOWN * 0.2, 2),
            (RIGHT * 3, UP * 0.5, 2.5),
        ]
        for pos_x, pos_y, width in platform_specs:
            p = Rectangle(
                width=width, height=0.15,
                color=WORLD_COLOR, fill_opacity=0.3, stroke_width=1,
            ).move_to(pos_x + pos_y)
            platforms.add(p)

        self.play(FadeIn(platforms), run_time=0.3)

        # Controller visualization at bottom
        controller = VGroup()
        btn_labels = ["←", "→", "↑", "A"]
        btn_colors = [AGENT_COLOR, AGENT_COLOR, ACTION_COLOR, GENIE_COLOR]
        for i, (lbl, c) in enumerate(zip(btn_labels, btn_colors)):
            btn = RoundedRectangle(
                width=0.8, height=0.6,
                corner_radius=0.1,
                color=c, fill_opacity=0.1, stroke_width=1.5,
            )
            btn_text = Text(lbl, font_size=18, color=c)
            btn_text.move_to(btn)
            controller.add(VGroup(btn, btn_text))
        controller.arrange(RIGHT, buff=0.2)
        controller.move_to(DOWN * 3)

        ctrl_label = label_text(
            "Latent Action Controls", font_size=14, color=TEXT_DIM,
        ).next_to(controller, DOWN, buff=0.15)
        self.play(FadeIn(controller), FadeIn(ctrl_label), run_time=0.5)

        # Demo: press buttons and character moves
        actions = [
            (1, RIGHT * 1.5, "→"),    # Move right
            (1, RIGHT * 1.5, "→"),    # Move right again
            (2, UP * 0.8, "↑"),       # Jump
            (0, LEFT * 1, "←"),       # Move left
        ]

        for btn_idx, movement, symbol in actions:
            btn = controller[btn_idx]
            # Highlight button
            self.play(
                btn[0].animate.set_fill(opacity=0.4).set_stroke(width=3),
                run_time=0.15,
            )
            # Move character
            self.play(
                character.animate.shift(movement),
                btn[0].animate.set_fill(opacity=0.1).set_stroke(width=1.5),
                run_time=0.35,
            )

        self.wait(0.5)

        # ── Part 3: Key message ──
        key_msg = Text(
            "From passive observation → to interaction",
            font_size=24, color=HIGHLIGHT_COLOR, weight=BOLD,
        )
        key_bg = Rectangle(
            width=key_msg.width + 0.8,
            height=key_msg.height + 0.4,
            color=BG_COLOR, fill_opacity=0.9, stroke_width=0,
        ).move_to(key_msg)
        key_group = VGroup(key_bg, key_msg).move_to(ORIGIN)

        self.play(FadeIn(key_group), run_time=0.8)
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
