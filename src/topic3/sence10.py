from manim import *
from manim_dsa import *


class WhatDoWeWantInstead(Scene):
    def construct(self):
        # ---------- Phase 1: Title ----------
        title = Text("What do we want instead?", font_size=36)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=2)
        self.wait(0.3)

        # ---------- Phase 2: Faded long DDIM chain (left) ----------
        long_chain, long_arrows, long_ddim = self.build_long_chain()
        long_ddim.set_opacity(0.4)
        self.play(FadeIn(long_ddim), run_time=1.5)
        self.wait(0.5)

        # ---------- Phase 3: Checklist items (right) ----------
        right_x = 1.8
        labels = [
            "Scales with refinement",
            "Uses as few steps as possible",
            "Still produces high-quality samples",
        ]
        items = []
        for i, label in enumerate(labels):
            check = self.make_check()
            text = Text(label, font_size=22)
            item = VGroup(check, text).arrange(RIGHT, buff=0.2)
            item.move_to(np.array([right_x, 1.5 - i * 1.0, 0]))
            items.append(item)

        for item in items:
            check, text = item
            self.play(
                FadeIn(text, shift=RIGHT * 0.2),
                GrowFromCenter(check),
                run_time=1.5,
            )
            self.wait(0.3)

        # ---------- Phase 4: Emphasize item 2 ----------
        self.play(Circumscribe(items[1], color=GREEN, run_time=1.5))
        self.wait(0.3)

        # ---------- Phase 5: Long chain -> short chain ----------
        short_chain, short_arrows, short_ddim = self.build_short_chain()
        self.play(
            FadeOut(long_ddim, shift=UP * 0.25),
            FadeIn(short_ddim, shift=UP * 0.25),
            run_time=2.5,
        )
        self.wait(0.5)

        # ---------- Phase 6: Summary at bottom ----------
        summary = Text(
            "Efficient inference should do more with fewer steps.",
            font_size=28,
            color=GREEN,
            weight=BOLD,
        )
        summary.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(summary), run_time=1.5)
        self.wait(1)

    # ------------------------------------------------------------------
    def build_long_chain(self):
        num_circles = 10
        circle_radius = 0.08
        spacing = 0.32
        chain = VGroup()
        for i in range(num_circles):
            c = Circle(radius=circle_radius, color=BLUE, fill_opacity=0.8)
            c.move_to(np.array([i * spacing, 0, 0]))
            chain.add(c)

        arrows = VGroup()
        for i in range(num_circles - 1):
            a = Arrow(
                chain[i].get_right(),
                chain[i + 1].get_left(),
                buff=0.03,
                color=BLUE,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.4,
            )
            arrows.add(a)

        group = VGroup(chain, arrows)
        group.move_to(np.array([-3.0, 1.0, 0]))
        return chain, arrows, group

    def build_short_chain(self):
        num_circles = 4
        circle_radius = 0.2
        spacing = 0.85
        chain = VGroup()
        for i in range(num_circles):
            c = Circle(radius=circle_radius, color=BLUE, fill_opacity=0.8)
            c.move_to(np.array([i * spacing, 0, 0]))
            chain.add(c)

        arrows = VGroup()
        for i in range(num_circles - 1):
            a = Arrow(
                chain[i].get_right(),
                chain[i + 1].get_left(),
                buff=0.05,
                color=BLUE,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.3,
            )
            arrows.add(a)

        group = VGroup(chain, arrows)
        group.move_to(np.array([-3.0, 1.0, 0]))
        return chain, arrows, group

    def make_check(self):
        return VGroup(
            Line(
                np.array([-0.12, 0.0, 0]),
                np.array([-0.02, -0.12, 0]),
                color=GREEN,
                stroke_width=5,
            ),
            Line(
                np.array([-0.02, -0.12, 0]),
                np.array([0.18, 0.15, 0]),
                color=GREEN,
                stroke_width=5,
            ),
        )
