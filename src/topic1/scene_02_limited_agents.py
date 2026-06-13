"""
SCENE 2 — Why Current AI Agents Are Limited
Time: 2:30–5:00

Tiny simulators → dissolve into massive open world → agent ↔ environment relationship.
"""

from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from topic1.shared_styles import *


class Scene02LimitedAgents(Scene):
    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self):
        scene_title_sequence(self, "Why Current AI Agents Are Limited")

        # ── Part 1: Single tiny simulator with agent repeating a task ──
        sim = make_box_simulator(side=2.0, agent_radius=0.12)
        sim_box, sim_agent = sim[0], sim[1]
        sim.move_to(ORIGIN)

        task_label = label_text("Simple Task", font_size=16, color=WORLD_COLOR)
        task_label.next_to(sim, DOWN, buff=0.3)

        self.play(FadeIn(sim), FadeIn(task_label), run_time=0.8)

        # Agent bouncing back and forth (repetitive task)
        for _ in range(3):
            self.play(
                sim_agent.animate.move_to(sim_box.get_right() * 0.7),
                run_time=0.4,
            )
            self.play(
                sim_agent.animate.move_to(sim_box.get_left() * 0.7),
                run_time=0.4,
            )
        sim_agent.move_to(sim_box.get_center())
        self.wait(0.3)

        # ── Part 2: Duplicate many tiny simulators ──
        self.play(FadeOut(task_label), run_time=0.3)

        # Shrink and move the original
        self.play(sim.animate.scale(0.5).move_to(UP * 1.5 + LEFT * 3), run_time=0.6)

        # Create grid of tiny simulators
        tiny_sims = VGroup()
        positions = [
            UP * 1.5 + LEFT * 1, UP * 1.5 + RIGHT * 1, UP * 1.5 + RIGHT * 3,
            DOWN * 0.5 + LEFT * 3, DOWN * 0.5 + LEFT * 1,
            DOWN * 0.5 + RIGHT * 1, DOWN * 0.5 + RIGHT * 3,
        ]
        for pos in positions:
            ts = make_box_simulator(side=1.0, agent_radius=0.06)
            ts.move_to(pos)
            tiny_sims.add(ts)

        label_small = label_text(
            "Small worlds. Small rules. Small possibilities.",
            font_size=18, color=TEXT_DIM,
        ).to_edge(DOWN, buff=0.6)

        self.play(
            LaggedStart(
                *[FadeIn(ts, scale=0.5) for ts in tiny_sims],
                lag_ratio=0.1,
            ),
            FadeIn(label_small, shift=UP * 0.2),
            run_time=1.2,
        )
        self.wait(1)

        # ── Part 3: Zoom out — dissolve boundaries into massive landscape ──
        all_sims = VGroup(sim, *tiny_sims)

        # Create the "real world" — large complex environment
        real_world = RoundedRectangle(
            width=12, height=7,
            corner_radius=0.5,
            color=WORLD_COLOR,
            fill_opacity=0.08,
            stroke_width=2,
        )

        # Add complexity: scattered dots, lines, shapes
        complexity = VGroup()
        rng = np.random.RandomState(123)
        for _ in range(40):
            x, y = rng.uniform(-5, 5), rng.uniform(-2.5, 2.5)
            size = rng.uniform(0.05, 0.2)
            opacity = rng.uniform(0.1, 0.4)
            color = [AGENT_COLOR, WORLD_COLOR, ACTION_COLOR, DATA_COLOR][rng.randint(4)]
            dot = Dot(
                point=np.array([x, y, 0]),
                radius=size,
                color=color,
                fill_opacity=opacity,
            )
            complexity.add(dot)

        # Connection lines between some dots
        for _ in range(15):
            i1, i2 = rng.randint(0, 40, size=2)
            if i1 != i2:
                line = Line(
                    complexity[i1].get_center(),
                    complexity[i2].get_center(),
                    color=WORLD_COLOR,
                    stroke_width=0.5,
                    stroke_opacity=0.2,
                )
                complexity.add(line)

        real_world_group = VGroup(real_world, complexity)

        world_label = subtitle_text("The Real World", font_size=28)
        world_label.to_edge(UP, buff=0.5)

        self.play(
            FadeOut(all_sims),
            FadeOut(label_small),
            run_time=0.8,
        )
        self.play(
            FadeIn(real_world_group),
            FadeIn(world_label),
            run_time=1.2,
        )
        self.wait(0.5)

        # ── Part 4: Agent ↔ Environment ──
        agent = make_agent(radius=0.2, color=AGENT_COLOR)
        agent.move_to(LEFT * 2.5)
        agent_label = body_text("Agent", font_size=22, color=AGENT_COLOR)
        agent_label.next_to(agent, DOWN, buff=0.3)

        env_icon = make_world_cube(side=1.5, color=WORLD_COLOR)
        env_icon.move_to(RIGHT * 2.5)
        env_label = body_text("Environment", font_size=22, color=WORLD_COLOR)
        env_label.next_to(env_icon, DOWN, buff=0.3)

        # Two-way arrows
        arrow_right = Arrow(
            LEFT * 1.2, RIGHT * 1.2,
            color=ACTION_COLOR, stroke_width=3,
        ).shift(UP * 0.2)
        arrow_left = Arrow(
            RIGHT * 1.2, LEFT * 1.2,
            color=WORLD_COLOR, stroke_width=3,
        ).shift(DOWN * 0.2)

        interaction_label_top = label_text(
            "agent shapes environment", font_size=14, color=ACTION_COLOR
        ).next_to(arrow_right, UP, buff=0.1)
        interaction_label_bot = label_text(
            "environment shapes agent", font_size=14, color=WORLD_COLOR
        ).next_to(arrow_left, DOWN, buff=0.1)

        self.play(
            FadeOut(real_world_group),
            FadeOut(world_label),
            run_time=0.5,
        )

        self.play(
            FadeIn(agent), FadeIn(agent_label),
            FadeIn(env_icon), FadeIn(env_label),
            run_time=0.8,
        )
        self.play(
            GrowArrow(arrow_right),
            FadeIn(interaction_label_top, shift=UP * 0.1),
            run_time=0.6,
        )
        self.play(
            GrowArrow(arrow_left),
            FadeIn(interaction_label_bot, shift=DOWN * 0.1),
            run_time=0.6,
        )
        self.wait(1.5)

        # Quote
        quote = Text(
            '"The relationship between environment\nand organism is transactional."',
            font_size=18,
            color=TEXT_DIM,
            slant=ITALIC,
        ).to_edge(DOWN, buff=0.5)
        attribution = label_text("— Alan Watts", font_size=14, color=TEXT_DIM)
        attribution.next_to(quote, DOWN, buff=0.15)

        self.play(FadeIn(quote), FadeIn(attribution), run_time=0.8)
        self.wait(2)

        self.play(
            FadeOut(VGroup(
                agent, agent_label, env_icon, env_label,
                arrow_right, arrow_left,
                interaction_label_top, interaction_label_bot,
                quote, attribution,
            )),
            run_time=1,
        )
