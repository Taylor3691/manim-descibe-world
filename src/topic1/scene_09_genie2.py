"""
SCENE 9 — Genie 2: More Than Scaling
Time: 27:00–31:00

Architecture change: MaskGIT → Latent Diffusion.
World cube expands in detail and complexity.
"""

from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from topic1.shared_styles import *


class Scene09Genie2(Scene):
    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self):
        scene_title_sequence(self, "Genie 2", "More Than Scaling")

        # ── Part 1: Architecture comparison — MaskGIT vs Latent Diffusion ──
        # Genie 1 block
        g1_block = RoundedRectangle(
            width=3.5, height=2.5,
            corner_radius=0.2,
            color=DATA_COLOR, fill_opacity=0.1, stroke_width=2,
        ).move_to(LEFT * 3.5)

        g1_title = Text(
            "Genie 1", font_size=24, color=DATA_COLOR, weight=BOLD,
        ).move_to(g1_block.get_top() + DOWN * 0.4)

        g1_arch = Text(
            "MaskGIT\nDynamics", font_size=18, color=DATA_COLOR,
        ).move_to(g1_block.get_center() + DOWN * 0.2)

        # Internal diagram for MaskGIT — grid with masked cells
        mask_grid = VGroup()
        for r in range(3):
            for c in range(4):
                cell = Square(
                    side_length=0.3,
                    color=DATA_COLOR,
                    fill_opacity=0.15 if (r + c) % 2 == 0 else 0.05,
                    stroke_width=0.5,
                )
                cell.move_to(g1_block.get_center() + DOWN * 0.8 +
                             RIGHT * (c - 1.5) * 0.35 + UP * (1 - r) * 0.35)
                mask_grid.add(cell)
        # Mark some as "masked"
        for idx in [1, 4, 7, 10]:
            if idx < len(mask_grid):
                x_mark = Text("×", font_size=12, color=GENIE_COLOR)
                x_mark.move_to(mask_grid[idx])
                mask_grid.add(x_mark)

        # Genie 2 block
        g2_block = RoundedRectangle(
            width=3.5, height=2.5,
            corner_radius=0.2,
            color=GENIE_COLOR, fill_opacity=0.1, stroke_width=2,
        ).move_to(RIGHT * 3.5)

        g2_title = Text(
            "Genie 2", font_size=24, color=GENIE_COLOR, weight=BOLD,
        ).move_to(g2_block.get_top() + DOWN * 0.4)

        g2_arch = Text(
            "Latent\nDiffusion", font_size=18, color=GENIE_COLOR,
        ).move_to(g2_block.get_center() + DOWN * 0.2)

        # Internal diagram for Latent Diffusion — noise → clean
        diff_stages = VGroup()
        for i in range(4):
            rect = RoundedRectangle(
                width=0.5, height=0.5,
                corner_radius=0.05,
                color=GENIE_COLOR,
                fill_opacity=0.1 + i * 0.1,
                stroke_width=0.8,
            )
            # Add "noise" dots that decrease
            noise = VGroup()
            rng = np.random.RandomState(i * 10)
            n_noise = max(0, 8 - i * 3)
            for _ in range(n_noise):
                nd = Dot(
                    radius=0.02,
                    color=TEXT_DIM,
                    fill_opacity=0.5,
                ).move_to(rect.get_center() + np.array([
                    rng.uniform(-0.15, 0.15),
                    rng.uniform(-0.15, 0.15), 0
                ]))
                noise.add(nd)
            diff_stages.add(VGroup(rect, noise))

        diff_stages.arrange(RIGHT, buff=0.15)
        diff_stages.move_to(g2_block.get_center() + DOWN * 0.8)

        # Small arrows between stages
        diff_arrows = VGroup()
        for i in range(len(diff_stages) - 1):
            a = Arrow(
                diff_stages[i].get_right(),
                diff_stages[i + 1].get_left(),
                color=GENIE_COLOR, stroke_width=1.5, buff=0.02,
                max_tip_length_to_length_ratio=0.3,
            )
            diff_arrows.add(a)

        # Transition arrow
        big_arrow = Arrow(
            g1_block.get_right(), g2_block.get_left(),
            color=HIGHLIGHT_COLOR, stroke_width=3, buff=0.3,
        )
        arrow_label = label_text("Evolution", font_size=16, color=HIGHLIGHT_COLOR)
        arrow_label.next_to(big_arrow, UP, buff=0.1)

        # Animate
        self.play(
            FadeIn(g1_block), FadeIn(g1_title), FadeIn(g1_arch),
            FadeIn(mask_grid),
            run_time=0.8,
        )
        self.wait(0.3)
        self.play(
            GrowArrow(big_arrow), FadeIn(arrow_label),
            run_time=0.6,
        )
        self.play(
            FadeIn(g2_block), FadeIn(g2_title), FadeIn(g2_arch),
            FadeIn(diff_stages), FadeIn(diff_arrows),
            run_time=0.8,
        )
        self.wait(1)

        # ── Part 2: Scaling — world cube expands ──
        self.play(
            FadeOut(VGroup(
                g1_block, g1_title, g1_arch, mask_grid,
                g2_block, g2_title, g2_arch, diff_stages, diff_arrows,
                big_arrow, arrow_label,
            )),
            run_time=0.6,
        )

        scale_title = subtitle_text("Scaling Up", font_size=28)
        scale_title.to_edge(UP, buff=0.5)
        self.play(FadeIn(scale_title), run_time=0.4)

        # Small world cube → grows larger with more detail
        world = make_world_cube(side=1.5, color=WORLD_COLOR, opacity=0.15)
        world.move_to(ORIGIN)
        world_label = label_text(
            "Generated Environment", font_size=16, color=WORLD_COLOR,
        ).next_to(world, DOWN, buff=0.3)

        self.play(FadeIn(world, scale=0.5), FadeIn(world_label), run_time=0.6)

        # Scaling steps
        scale_stages = [
            ("More Games", 1.5, 0.2),
            ("More Worlds", 2.0, 0.25),
            ("More Visual Diversity", 2.5, 0.3),
        ]

        for stage_label, scale, opacity in scale_stages:
            stage_text = label_text(stage_label, font_size=18, color=HIGHLIGHT_COLOR)
            stage_text.next_to(world, RIGHT, buff=1.0)

            # Add more detail dots inside
            new_details = VGroup()
            rng = np.random.RandomState(hash(stage_label) % 1000)
            current_side = world[0].width
            for _ in range(8):
                d = Dot(
                    radius=rng.uniform(0.02, 0.06),
                    color=interpolate_color(
                        ManimColor(WORLD_COLOR), ManimColor(ACTION_COLOR), rng.random()
                    ),
                    fill_opacity=rng.uniform(0.2, 0.5),
                ).move_to(world.get_center() + np.array([
                    rng.uniform(-current_side / 3, current_side / 3),
                    rng.uniform(-current_side / 3, current_side / 3), 0
                ]))
                new_details.add(d)

            self.play(
                FadeIn(stage_text, shift=LEFT * 0.3),
                world.animate.scale(scale / world[0].width * 1.5),
                FadeIn(new_details),
                run_time=0.8,
            )
            self.wait(0.3)
            self.play(FadeOut(stage_text), run_time=0.3)

        # Final label
        rich_label = body_text(
            "Richer and more coherent environments",
            font_size=20, color=HIGHLIGHT_COLOR,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(rich_label, shift=UP * 0.2), run_time=0.5)
        self.wait(1.5)

        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1)
