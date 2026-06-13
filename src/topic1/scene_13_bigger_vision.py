"""
SCENE 13 — The Bigger Vision
Time: 38:00–39:15

Merge all concepts into one expanding ecosystem.
Reuse visual motifs for narrative closure.
"""

from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from topic1.shared_styles import *


class Scene13BiggerVision(Scene):
    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self):
        scene_title_sequence(self, "The Bigger Vision")

        # ── Central hub: "Embodied Intelligence" ──
        center_circle = Circle(
            radius=0.8,
            color=HIGHLIGHT_COLOR,
            fill_opacity=0.15,
            stroke_width=2,
        )
        center_label = Text(
            "Embodied\nIntelligence",
            font_size=18, color=HIGHLIGHT_COLOR, weight=BOLD,
        ).move_to(center_circle)

        self.play(
            FadeIn(center_circle, scale=0.5),
            FadeIn(center_label),
            run_time=0.8,
        )

        # ── Five satellite concepts — reusing motifs from earlier scenes ──
        satellites = [
            ("Worlds", WORLD_COLOR, UP * 2.5),
            ("Agents", AGENT_COLOR, UP * 1.0 + RIGHT * 2.5),
            ("Actions", ACTION_COLOR, DOWN * 1.5 + RIGHT * 2.0),
            ("Generated\nEnvironments", GENIE_COLOR, DOWN * 1.5 + LEFT * 2.0),
            ("Language\nGoals", DATA_COLOR, UP * 1.0 + LEFT * 2.5),
        ]

        sat_nodes = VGroup()
        sat_labels = VGroup()
        sat_connections = VGroup()

        for name, color, pos in satellites:
            # Satellite node with glow
            node = Circle(
                radius=0.5, color=color,
                fill_opacity=0.1, stroke_width=2,
            ).move_to(pos)
            glow = Circle(
                radius=0.65, color=color,
                fill_opacity=0.05, stroke_width=0,
            ).move_to(pos)

            label = Text(
                name, font_size=14, color=color,
            ).move_to(pos)

            # Connection to center
            conn = Line(
                center_circle.get_center(),
                pos,
                color=color, stroke_width=1.5, stroke_opacity=0.5,
            )

            sat_nodes.add(VGroup(glow, node))
            sat_labels.add(label)
            sat_connections.add(conn)

        # Animate satellites appearing one by one
        for i in range(len(satellites)):
            self.play(
                Create(sat_connections[i]),
                FadeIn(sat_nodes[i], scale=0.3),
                FadeIn(sat_labels[i]),
                run_time=0.4,
            )

        self.wait(0.5)

        # ── Cross-connections between satellites ──
        cross_connections = VGroup()
        cross_pairs = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2), (1, 3)]
        for i, j in cross_pairs:
            cc = Line(
                sat_nodes[i].get_center(),
                sat_nodes[j].get_center(),
                color=TEXT_DIM, stroke_width=0.8, stroke_opacity=0.25,
            )
            cross_connections.add(cc)

        self.play(
            LaggedStart(
                *[Create(cc) for cc in cross_connections],
                lag_ratio=0.05,
            ),
            run_time=0.8,
        )

        # ── Expanding ecosystem — everything scales up ──
        all_ecosystem = VGroup(
            center_circle, center_label,
            sat_nodes, sat_labels,
            sat_connections, cross_connections,
        )

        # Add outer particles for "expanding" effect
        outer_particles = VGroup()
        rng = np.random.RandomState(77)
        for _ in range(30):
            angle = rng.uniform(0, TAU)
            r = rng.uniform(3.0, 5.5)
            pos = np.array([r * np.cos(angle), r * np.sin(angle), 0])
            p = Dot(
                pos, radius=rng.uniform(0.02, 0.05),
                color=interpolate_color(
                    ManimColor(AGENT_COLOR), ManimColor(WORLD_COLOR), rng.random()
                ),
                fill_opacity=rng.uniform(0.15, 0.4),
            )
            outer_particles.add(p)

        # Faint connections from particles to nearest satellite
        particle_connections = VGroup()
        for p in outer_particles:
            nearest_idx = min(
                range(len(satellites)),
                key=lambda k: np.linalg.norm(
                    p.get_center() - sat_nodes[k].get_center()
                ),
            )
            pc = Line(
                sat_nodes[nearest_idx].get_center(),
                p.get_center(),
                color=satellites[nearest_idx][1],
                stroke_width=0.3,
                stroke_opacity=0.15,
            )
            particle_connections.add(pc)

        self.play(
            LaggedStart(
                *[FadeIn(p, scale=0.3) for p in outer_particles],
                lag_ratio=0.02,
            ),
            LaggedStart(
                *[Create(pc) for pc in particle_connections],
                lag_ratio=0.02,
            ),
            run_time=1.5,
        )

        # Pulse the center
        self.play(
            center_circle.animate.scale(1.2).set_fill(opacity=0.25),
            run_time=0.5,
        )
        self.play(
            center_circle.animate.scale(1 / 1.2).set_fill(opacity=0.15),
            run_time=0.5,
        )

        # ── Vision statement ──
        vision = body_text(
            "Systems capable of imagining futures,\nexploring possibilities, and learning\ninside open-ended worlds",
            font_size=20, color=HIGHLIGHT_COLOR,
        )
        vision_bg = Rectangle(
            width=vision.width + 0.6,
            height=vision.height + 0.4,
            color=BG_COLOR, fill_opacity=0.85, stroke_width=0,
        ).move_to(vision)
        vision_group = VGroup(vision_bg, vision).to_edge(DOWN, buff=0.4)

        self.play(FadeIn(vision_group), run_time=0.8)
        self.wait(2)

        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.2)
