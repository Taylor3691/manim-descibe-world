"""
SCENE 7 — The 8 Latent Action Codes
Time: 18:00–23:00

8 glowing action tiles, selecting one changes trajectory.
Same codes reused across different environments.
"""

from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from topic1.shared_styles import *


class Scene07LatentActions(Scene):
    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self):
        scene_title_sequence(self, "The 8 Latent Action Codes")

        # ── Part 1: 8 glowing action tiles ──
        tile_colors = [
            "#ff6b6b", "#ffa94d", "#ffe066", "#69db7c",
            "#38d9a9", "#4dabf7", "#9775fa", "#e056a0",
        ]
        tiles = VGroup()
        for i in range(8):
            tile = RoundedRectangle(
                width=0.9, height=0.9,
                corner_radius=0.12,
                color=tile_colors[i],
                fill_opacity=0.25,
                stroke_width=2,
            )
            # Glow effect
            glow = RoundedRectangle(
                width=1.05, height=1.05,
                corner_radius=0.15,
                color=tile_colors[i],
                fill_opacity=0.08,
                stroke_width=0,
            ).move_to(tile)
            num = Text(
                str(i), font_size=24, color=tile_colors[i], weight=BOLD,
            ).move_to(tile)
            tiles.add(VGroup(glow, tile, num))

        tiles.arrange(RIGHT, buff=0.25)
        tiles.move_to(UP * 2.5)

        tiles_label = body_text(
            "Learned from video data — not manually designed",
            font_size=18, color=TEXT_DIM,
        ).next_to(tiles, DOWN, buff=0.3)

        self.play(
            LaggedStart(
                *[FadeIn(t, scale=0.5) for t in tiles],
                lag_ratio=0.08,
            ),
            run_time=1.2,
        )
        self.play(FadeIn(tiles_label, shift=UP * 0.1), run_time=0.5)
        self.wait(0.5)

        # ── Part 2: Selecting a tile changes trajectory ──
        # Create a "playground" area
        playground = Rectangle(
            width=10, height=3.5,
            color=WORLD_COLOR, fill_opacity=0.05, stroke_width=1,
        ).move_to(DOWN * 1)
        pg_label = label_text("Environment", font_size=14, color=WORLD_COLOR)
        pg_label.move_to(playground.get_corner(UL) + RIGHT * 0.7 + DOWN * 0.2)
        self.play(FadeIn(playground), FadeIn(pg_label), run_time=0.4)

        # Agent starting position
        agent = make_agent(radius=0.12, color=AGENT_COLOR)
        agent.move_to(LEFT * 4 + DOWN * 1)
        self.play(FadeIn(agent, scale=2), run_time=0.4)

        # Demonstrate 3 different action selections → different trajectories
        demo_actions = [
            (2, HIGHLIGHT_COLOR, [LEFT * 2 + DOWN * 0.5, ORIGIN + DOWN * 1.5, RIGHT * 2 + DOWN * 0.3]),
            (5, "#4dabf7", [LEFT * 2 + UP * 0, ORIGIN + UP * 0.2, RIGHT * 2 + UP * 0.5]),
            (7, LATENT_COLOR, [LEFT * 2 + DOWN * 1, RIGHT * 0 + DOWN * 2, RIGHT * 3 + DOWN * 1.5]),
        ]

        trajectories = VGroup()
        for action_idx, color, waypoints in demo_actions:
            # Highlight selected tile
            selected_tile = tiles[action_idx]
            highlight_box = SurroundingRectangle(
                selected_tile, color=HIGHLIGHT_COLOR, buff=0.08, stroke_width=3,
            )
            action_text = label_text(
                f"Action {action_idx}", font_size=16, color=color,
            ).next_to(playground, RIGHT, buff=0.3).shift(UP * (1 - len(trajectories) * 0.8))

            self.play(
                Create(highlight_box),
                FadeIn(action_text),
                run_time=0.3,
            )

            # Draw trajectory
            points = [agent.get_center()] + [
                np.array([wp[0], wp[1], 0]) for wp in waypoints
            ]
            # Create smooth curve through points
            path_dots = VGroup()
            path_lines = VGroup()
            for i_pt in range(len(points) - 1):
                line = Line(
                    points[i_pt], points[i_pt + 1],
                    color=color, stroke_width=2, stroke_opacity=0.7,
                )
                path_lines.add(line)
                if i_pt > 0:
                    dot = Dot(points[i_pt], radius=0.05, color=color, fill_opacity=0.6)
                    path_dots.add(dot)

            # End dot
            end_dot = Dot(points[-1], radius=0.08, color=color, fill_opacity=0.9)
            trajectory = VGroup(path_lines, path_dots, end_dot, action_text)
            trajectories.add(trajectory)

            self.play(
                LaggedStart(
                    *[Create(l) for l in path_lines],
                    lag_ratio=0.2,
                ),
                run_time=0.6,
            )
            self.play(
                FadeIn(path_dots),
                FadeIn(end_dot, scale=2),
                run_time=0.3,
            )
            self.play(FadeOut(highlight_box), run_time=0.2)

        self.wait(0.5)

        # ── Part 3: Same codes across environments ──
        self.play(
            FadeOut(trajectories),
            FadeOut(agent),
            FadeOut(playground), FadeOut(pg_label),
            run_time=0.6,
        )

        # Show two different environments side by side
        env1 = RoundedRectangle(
            width=4, height=2.5,
            corner_radius=0.2,
            color=WORLD_COLOR, fill_opacity=0.08, stroke_width=1.5,
        ).move_to(LEFT * 3 + DOWN * 1)
        env1_label = label_text("Platformer Game", font_size=14, color=WORLD_COLOR)
        env1_label.next_to(env1, UP, buff=0.15)

        env2 = RoundedRectangle(
            width=4, height=2.5,
            corner_radius=0.2,
            color=GENIE_COLOR, fill_opacity=0.08, stroke_width=1.5,
        ).move_to(RIGHT * 3 + DOWN * 1)
        env2_label = label_text("Robot Control", font_size=14, color=GENIE_COLOR)
        env2_label.next_to(env2, UP, buff=0.15)

        # Same action code label
        same_code = VGroup(
            RoundedRectangle(
                width=0.7, height=0.7,
                corner_radius=0.1,
                color=tile_colors[3], fill_opacity=0.25, stroke_width=2,
            ),
            Text("3", font_size=20, color=tile_colors[3], weight=BOLD),
        )
        same_code[1].move_to(same_code[0])
        same_code.move_to(DOWN * 1)

        # Arrows from code to both environments
        arr_to_env1 = Arrow(
            same_code.get_left(), env1.get_right(),
            color=tile_colors[3], stroke_width=2, buff=0.2,
        )
        arr_to_env2 = Arrow(
            same_code.get_right(), env2.get_left(),
            color=tile_colors[3], stroke_width=2, buff=0.2,
        )

        consistency_label = body_text(
            "Same action code → consistent behavior\nacross different environments",
            font_size=18, color=HIGHLIGHT_COLOR,
        ).to_edge(DOWN, buff=0.4)

        self.play(
            FadeIn(env1), FadeIn(env1_label),
            FadeIn(env2), FadeIn(env2_label),
            run_time=0.6,
        )
        self.play(
            FadeIn(same_code, scale=1.5),
            GrowArrow(arr_to_env1),
            GrowArrow(arr_to_env2),
            run_time=0.8,
        )
        self.play(FadeIn(consistency_label, shift=UP * 0.2), run_time=0.5)

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
