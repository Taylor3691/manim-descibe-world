"""
SCENE 4 — Open-Ended Learning and Darwin-Complete Spaces
Time: 8:00–11:00

Tiny task tree → enormous galaxy-like network → agent explores branches.
"""

from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from topic1.shared_styles import *


class Scene04OpenEnded(Scene):
    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self):
        scene_title_sequence(self, "Open-Ended Learning", "Darwin-Complete Search Spaces")

        # ── Part 1: Start with a tiny task tree ──
        # Build a small binary tree
        root_pos = UP * 2
        small_tree_nodes = VGroup()
        small_tree_edges = VGroup()

        levels = 3
        all_positions = []

        for level in range(levels):
            n_nodes_at_level = 2 ** level
            y = 2 - level * 1.3
            spacing = 5.0 / (n_nodes_at_level + 1)
            level_positions = []
            for i in range(n_nodes_at_level):
                x = -2.5 + (i + 1) * spacing
                pos = np.array([x, y, 0])
                level_positions.append(pos)

                c = interpolate_color(
                    ManimColor(DATA_COLOR),
                    ManimColor(WORLD_COLOR),
                    level / (levels - 1),
                )
                dot = Dot(pos, radius=0.1, color=c, fill_opacity=0.8)
                small_tree_nodes.add(dot)

                # Edge to parent
                if level > 0:
                    parent_idx = len(all_positions) - n_nodes_at_level + i // 2
                    if parent_idx < len(all_positions):
                        parent_pos = all_positions[parent_idx]
                        edge = Line(
                            parent_pos, pos,
                            color=c, stroke_width=1.5, stroke_opacity=0.6,
                        )
                        small_tree_edges.add(edge)

            all_positions.extend(level_positions)

        small_tree = VGroup(small_tree_edges, small_tree_nodes)
        tree_label = label_text("Task Space", font_size=18, color=TEXT_DIM)
        tree_label.next_to(small_tree, DOWN, buff=0.3)

        self.play(
            LaggedStart(
                *[FadeIn(e) for e in small_tree_edges],
                lag_ratio=0.05,
            ),
            LaggedStart(
                *[FadeIn(n, scale=0.5) for n in small_tree_nodes],
                lag_ratio=0.08,
            ),
            FadeIn(tree_label),
            run_time=1.5,
        )
        self.wait(0.5)

        # ── Part 2: Expand into enormous galaxy-like network ──
        self.play(
            FadeOut(small_tree),
            FadeOut(tree_label),
            run_time=0.5,
        )

        # Create galaxy network
        rng = np.random.RandomState(42)
        n_galaxy_nodes = 120
        galaxy_nodes = VGroup()
        galaxy_edges = VGroup()

        # Generate positions using polar coordinates for galaxy-like feel
        positions = []
        for i in range(n_galaxy_nodes):
            if i < 10:
                # Core nodes — center cluster
                r = rng.uniform(0, 1.0)
                theta = rng.uniform(0, TAU)
            elif i < 40:
                # Inner ring
                r = rng.uniform(1.0, 2.5)
                theta = rng.uniform(0, TAU)
            else:
                # Outer spiral arms
                arm = rng.randint(3)
                base_theta = arm * TAU / 3 + rng.uniform(-0.4, 0.4)
                r = rng.uniform(2.0, 4.5)
                theta = base_theta + r * 0.3  # spiral
                r += rng.uniform(-0.5, 0.5)

            x = r * np.cos(theta)
            y = r * np.sin(theta)
            positions.append(np.array([x, y, 0]))

            # Node size decreases with distance
            node_size = max(0.03, 0.12 - r * 0.02)
            node_opacity = max(0.2, 0.9 - r * 0.15)
            c = interpolate_color(
                ManimColor(AGENT_COLOR),
                ManimColor(DATA_COLOR),
                min(1.0, r / 4.0),
            )
            dot = Dot(
                np.array([x, y, 0]),
                radius=node_size,
                color=c,
                fill_opacity=node_opacity,
            )
            galaxy_nodes.add(dot)

        # Connect nearby nodes
        for i in range(n_galaxy_nodes):
            for j in range(i + 1, n_galaxy_nodes):
                dist = np.linalg.norm(positions[i] - positions[j])
                if dist < 0.8 and rng.random() < 0.4:
                    edge = Line(
                        positions[i], positions[j],
                        color=AGENT_COLOR,
                        stroke_width=0.5,
                        stroke_opacity=max(0.05, 0.3 - dist * 0.3),
                    )
                    galaxy_edges.add(edge)

        galaxy = VGroup(galaxy_edges, galaxy_nodes)

        # Animate galaxy appearing in waves from center outward
        self.play(
            LaggedStart(
                *[FadeIn(n, scale=0.3) for n in galaxy_nodes],
                lag_ratio=0.01,
            ),
            run_time=2.0,
        )
        self.play(
            LaggedStart(
                *[Create(e) for e in galaxy_edges],
                lag_ratio=0.005,
            ),
            run_time=1.5,
        )

        # ── Part 3: Agent explores branches ──
        agent = make_agent(radius=0.12, color=HIGHLIGHT_COLOR)
        agent.move_to(ORIGIN)
        self.play(FadeIn(agent, scale=2), run_time=0.5)

        # Agent moves through some nodes
        explore_path = [0, 3, 12, 25, 45, 70]
        for idx in explore_path:
            if idx < len(positions):
                trail = Line(
                    agent.get_center(), positions[idx],
                    color=HIGHLIGHT_COLOR, stroke_width=1, stroke_opacity=0.4,
                )
                self.play(
                    Create(trail),
                    agent.animate.move_to(positions[idx]),
                    run_time=0.35,
                )

        # ── Part 4: Label appears ──
        darwin_label = Text(
            "Darwin-Complete Search Space",
            font_size=28,
            color=HIGHLIGHT_COLOR,
            weight=BOLD,
        )
        darwin_bg = Rectangle(
            width=darwin_label.width + 0.6,
            height=darwin_label.height + 0.4,
            color=BG_COLOR, fill_opacity=0.8, stroke_width=0,
        ).move_to(darwin_label)
        darwin_group = VGroup(darwin_bg, darwin_label).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(darwin_group), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(darwin_group), run_time=0.6)

        # Slow zoom out to show more structure
        self.play(
            VGroup(galaxy, agent).animate.scale(0.7),
            run_time=1.5,
        )
        self.wait(1)

        self.play(FadeOut(VGroup(galaxy, agent)), run_time=1)
