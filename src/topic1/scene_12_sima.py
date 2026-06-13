"""
SCENE 12 — SIMA and the Closed Loop
Time: 36:00–38:00

Closed-loop: Frame → SIMA → Action → Genie → Next Frame → repeat.
Circular handshake motion with alternating highlights.
"""

from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from topic1.shared_styles import *


class Scene12SIMA(Scene):
    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self):
        scene_title_sequence(self, "SIMA and the Closed Loop")

        # ── Build the closed-loop diagram ──
        loop_radius = 2.2
        modules = [
            ("Frame", DATA_COLOR),
            ("SIMA", SIMA_COLOR),
            ("Action", ACTION_COLOR),
            ("Genie", GENIE_COLOR),
            ("Next Frame", DATA_COLOR),
        ]
        n_modules = len(modules)
        angles = [PI / 2 - i * TAU / n_modules for i in range(n_modules)]

        module_nodes = VGroup()
        module_labels = VGroup()

        for i, (name, color) in enumerate(modules):
            pos = np.array([
                loop_radius * np.cos(angles[i]),
                loop_radius * np.sin(angles[i]),
                0,
            ])
            # Module box
            box = RoundedRectangle(
                width=1.6, height=0.8,
                corner_radius=0.12,
                color=color, fill_opacity=0.15, stroke_width=2,
            ).move_to(pos)

            label = Text(
                name, font_size=16, color=color, weight=BOLD,
            ).move_to(pos)

            module_nodes.add(box)
            module_labels.add(label)

        # Arrows between consecutive modules
        module_arrows = VGroup()
        for i in range(n_modules):
            j = (i + 1) % n_modules
            start = module_nodes[i].get_center()
            end = module_nodes[j].get_center()
            direction = end - start
            direction_norm = direction / np.linalg.norm(direction)

            arrow = Arrow(
                start + direction_norm * 0.85,
                end - direction_norm * 0.85,
                color=interpolate_color(
                    ManimColor(modules[i][1]),
                    ManimColor(modules[j][1]),
                    0.5,
                ),
                stroke_width=2.5,
                buff=0,
                max_tip_length_to_length_ratio=0.12,
            )
            module_arrows.add(arrow)

        loop_group = VGroup(module_nodes, module_labels, module_arrows)

        # Animate the loop appearing
        self.play(
            LaggedStart(
                *[FadeIn(n, scale=0.5) for n in module_nodes],
                lag_ratio=0.12,
            ),
            LaggedStart(
                *[FadeIn(l) for l in module_labels],
                lag_ratio=0.12,
            ),
            run_time=1.2,
        )
        self.play(
            LaggedStart(
                *[GrowArrow(a) for a in module_arrows],
                lag_ratio=0.1,
            ),
            run_time=1.0,
        )

        # ── "A conversation between agent and world" ──
        conv_text = body_text(
            "A conversation between agent and world",
            font_size=20, color=HIGHLIGHT_COLOR,
        ).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(conv_text, shift=UP * 0.2), run_time=0.5)
        self.wait(0.5)

        # ── Animate the loop cycling — highlight each module in sequence ──
        for cycle in range(3):
            for i in range(n_modules):
                # Highlight current module
                self.play(
                    module_nodes[i].animate.set_fill(opacity=0.4).set_stroke(width=4),
                    module_labels[i].animate.scale(1.15),
                    module_arrows[i].animate.set_stroke(width=5),
                    run_time=0.2,
                )
                self.play(
                    module_nodes[i].animate.set_fill(opacity=0.15).set_stroke(width=2),
                    module_labels[i].animate.scale(1 / 1.15),
                    module_arrows[i].animate.set_stroke(width=2.5),
                    run_time=0.15,
                )

        self.wait(0.5)

        # ── SIMA description ──
        desc_bg = RoundedRectangle(
            width=8, height=2,
            corner_radius=0.15,
            color=SIMA_COLOR, fill_opacity=0.08, stroke_width=1,
        ).to_edge(DOWN, buff=0.3)

        self.play(
            FadeOut(conv_text),
            FadeIn(desc_bg),
            run_time=0.4,
        )

        desc_lines = VGroup(
            Text("SIMA observes a frame", font_size=16, color=TEXT_PRIMARY),
            Text("→ Chooses a latent action", font_size=16, color=SIMA_COLOR),
            Text("→ Genie generates next frame", font_size=16, color=GENIE_COLOR),
            Text("→ Repeat", font_size=16, color=HIGHLIGHT_COLOR),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to(desc_bg)

        for line in desc_lines:
            self.play(FadeIn(line, shift=RIGHT * 0.2), run_time=0.3)

        self.wait(1.5)

        # ── "Not a static stack — it's interaction" ──
        final_msg = Text(
            "Not a static stack of modules — it's continuous interaction",
            font_size=18, color=TEXT_DIM,
        ).to_edge(DOWN, buff=0.15)

        self.play(FadeIn(final_msg), run_time=0.5)
        self.wait(1.5)

        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
