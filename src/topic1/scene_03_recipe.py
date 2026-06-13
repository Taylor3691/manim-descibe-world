"""
SCENE 3 — The Recipe for Embodied AGI
Time: 5:00–8:00

Circular ecosystem loop: Worlds → Agents → Experience → Better Worlds → Better Agents.
Loop grows larger each cycle with new branches and subworlds.
"""

from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from topic1.shared_styles import *


class Scene03Recipe(Scene):
    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self):
        scene_title_sequence(self, "The Recipe for Embodied AGI")

        # ── Build the circular loop ──
        loop_radius = 2.0
        node_labels = ["Worlds", "Agents", "Experience", "Better\nWorlds", "Better\nAgents"]
        node_colors = [WORLD_COLOR, AGENT_COLOR, DATA_COLOR, WORLD_COLOR, AGENT_COLOR]
        n_nodes = len(node_labels)
        angles = [PI / 2 - i * TAU / n_nodes for i in range(n_nodes)]

        # Create nodes
        nodes = VGroup()
        node_texts = VGroup()
        for i, (lbl, c, angle) in enumerate(zip(node_labels, node_colors, angles)):
            pos = np.array([
                loop_radius * np.cos(angle),
                loop_radius * np.sin(angle),
                0,
            ])
            circle = Circle(
                radius=0.45, color=c, fill_opacity=0.15, stroke_width=2,
            ).move_to(pos)
            txt = Text(
                lbl, font_size=14, color=c, weight=BOLD,
            ).move_to(pos)
            nodes.add(circle)
            node_texts.add(txt)

        # Create curved arrows between consecutive nodes
        arrows = VGroup()
        for i in range(n_nodes):
            j = (i + 1) % n_nodes
            start_angle = angles[i]
            end_angle = angles[j]

            # Calculate start and end points on the circle edges
            start_pos = nodes[i].get_center()
            end_pos = nodes[j].get_center()

            direction = end_pos - start_pos
            direction_norm = direction / np.linalg.norm(direction)
            start_pt = start_pos + direction_norm * 0.5
            end_pt = end_pos - direction_norm * 0.5

            arrow = Arrow(
                start_pt, end_pt,
                color=interpolate_color(
                    ManimColor(node_colors[i]),
                    ManimColor(node_colors[j]),
                    0.5,
                ),
                stroke_width=2.5,
                buff=0,
                max_tip_length_to_length_ratio=0.15,
            )
            arrows.add(arrow)

        loop_group = VGroup(nodes, node_texts, arrows)

        # ── Animate loop appearing ──
        self.play(
            LaggedStart(
                *[FadeIn(n, scale=0.5) for n in nodes],
                lag_ratio=0.15,
            ),
            run_time=1.2,
        )
        self.play(
            LaggedStart(
                *[FadeIn(t) for t in node_texts],
                lag_ratio=0.1,
            ),
            run_time=0.8,
        )
        self.play(
            LaggedStart(
                *[GrowArrow(a) for a in arrows],
                lag_ratio=0.15,
            ),
            run_time=1.5,
        )
        self.wait(0.5)

        # ── Pulsing arrows to show the cycle ──
        cycle_label = body_text(
            "The cycle continuously grows\nlarger and more complex",
            font_size=20, color=TEXT_DIM,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(cycle_label, shift=UP * 0.2), run_time=0.5)

        # Pulse each arrow in sequence to show flow
        for cycle in range(2):
            for i, arrow in enumerate(arrows):
                self.play(
                    arrow.animate.set_stroke(width=5),
                    nodes[(i + 1) % n_nodes].animate.set_fill(opacity=0.35),
                    run_time=0.25,
                )
                self.play(
                    arrow.animate.set_stroke(width=2.5),
                    nodes[(i + 1) % n_nodes].animate.set_fill(opacity=0.15),
                    run_time=0.15,
                )

        # ── Loop grows — scale up and add sub-branches ──
        self.play(
            loop_group.animate.scale(0.7).move_to(ORIGIN),
            run_time=0.8,
        )

        # Add sub-branches emerging from nodes
        sub_branches = VGroup()
        rng = np.random.RandomState(42)
        for i, node in enumerate(nodes):
            n_sub = rng.randint(2, 4)
            for j in range(n_sub):
                angle = rng.uniform(0, TAU)
                length = rng.uniform(0.8, 1.5)
                end = node.get_center() + np.array([
                    length * np.cos(angle),
                    length * np.sin(angle),
                    0,
                ])
                sub_line = Line(
                    node.get_center(), end,
                    color=node_colors[i],
                    stroke_width=1,
                    stroke_opacity=0.4,
                )
                sub_dot = Dot(
                    end, radius=0.06,
                    color=node_colors[i],
                    fill_opacity=0.5,
                )
                sub_branches.add(sub_line, sub_dot)

        self.play(
            LaggedStart(
                *[Create(sb) for sb in sub_branches],
                lag_ratio=0.03,
            ),
            run_time=1.5,
        )
        self.wait(0.5)

        # Scale everything up to show growth
        all_content = VGroup(loop_group, sub_branches)
        self.play(
            all_content.animate.scale(1.3),
            run_time=1,
        )
        self.wait(1)

        self.play(
            FadeOut(all_content),
            FadeOut(cycle_label),
            run_time=1,
        )
