from manim import *

# Color palette - clean academic style
DISCRETE_FILL = "#3B82F6"
DISCRETE_BORDER = "#1E40AF"
CONTINUOUS_FILL = "#22C55E"
CONTINUOUS_BORDER = "#15803D"
ORANGE = "#FF6B35"
WARN_RED = "#EF4444"
DARK_GRAY = "#4B5563"
LIGHT_BORDER = "#9CA3AF"
LAVENDER = "#C4B5FD"
WHITE = "#FFFFFF"
LIGHT_GRAY = "#A1A1AA"
PANEL_BG = "#1E1E2E"
PANEL_BORDER = "#4A4A6A"


def make_token(label, fill_color, border_color, w=0.9, h=0.55):
    box = RoundedRectangle(
        width=w, height=h, corner_radius=0.08,
        fill_color=fill_color, fill_opacity=0.5,
        stroke_color=border_color, stroke_width=2.5
    )
    text = Text(label, font="Arial", color=WHITE, font_size=26, weight=BOLD)
    text.move_to(box.get_center())
    return VGroup(box, text)


class ContinuousTokensSpeedBottleneck(Scene):
    def construct(self):
        # Dark academic background
        self.camera.background_color = "#0F0F1A"

        # === 1. TITLE ===
        title = Text(
            "Continuous tokens have a speed issue",
            font="Arial", color=LAVENDER, font_size=40, weight=BOLD
        )
        title.to_edge(UP, buff=0.4).to_edge(LEFT, buff=0.6)

        self.play(FadeIn(title), run_time=1)
        self.wait(0.2)

        # === 2. TOP PANEL: Logical Sequence ===
        top_panel = RoundedRectangle(
            width=12.5, height=2.0, corner_radius=0.15,
            fill_color=PANEL_BG, fill_opacity=0.7,
            stroke_color=PANEL_BORDER, stroke_width=2
        )
        top_panel.move_to([0, 1.9, 0])

        top_panel_title = Text(
            "Logical sequence",
            font="Arial", color=LAVENDER, font_size=28, weight=BOLD
        )
        top_panel_title.move_to(top_panel.get_corner(UL) + RIGHT * 0.4 + DOWN * 0.35)

        # Token row [D1][C1][D2][C2]
        d1 = make_token("D1", DISCRETE_FILL, DISCRETE_BORDER)
        c1 = make_token("C1", CONTINUOUS_FILL, CONTINUOUS_BORDER)
        d2 = make_token("D2", DISCRETE_FILL, DISCRETE_BORDER)
        c2 = make_token("C2", CONTINUOUS_FILL, CONTINUOUS_BORDER)
        top_tokens = VGroup(d1, c1, d2, c2).arrange(RIGHT, buff=0.3)
        top_tokens.move_to([0, 1.95, 0])

        # Labels
        discrete_label = Text("Discrete token", font="Arial", color=LIGHT_GRAY, font_size=20)
        discrete_label.next_to(VGroup(d1, d2), DOWN, buff=0.2)

        continuous_label = Text("Continuous signal", font="Arial", color=LIGHT_GRAY, font_size=20)
        continuous_label.next_to(VGroup(c1, c2), DOWN, buff=0.2)
        continuous_sublabel = Text("image / video / audio / actions", font="Arial", color=LIGHT_GRAY, font_size=16)
        continuous_sublabel.next_to(continuous_label, DOWN, buff=0.08)

        # Bottom caption
        top_caption = Text(
            "Both token types look compact in the sequence.",
            font="Arial", color=WHITE, font_size=22
        )
        top_caption.next_to(top_panel.get_bottom(), UP, buff=0.3)

        self.play(FadeIn(top_panel), FadeIn(top_panel_title), run_time=1)
        self.play(
            LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in top_tokens], lag_ratio=0.2),
            run_time=1.2
        )
        self.play(
            FadeIn(discrete_label),
            FadeIn(continuous_label),
            FadeIn(continuous_sublabel),
            run_time=0.8
        )
        self.play(FadeIn(top_caption), run_time=0.8)
        self.wait(0.3)

        # === 3. TRANSITION ===
        arrow = Arrow(
            start=[0, 0.7, 0], end=[0, 0.1, 0],
            color=ORANGE, stroke_width=5, buff=0.05
        )
        transition_text = Text(
            "But hardware compute is different",
            font="Arial", color=ORANGE, font_size=24, weight=BOLD
        )
        transition_text.next_to(arrow, RIGHT, buff=0.4)

        self.play(GrowFromPoint(arrow, arrow.get_start()), run_time=0.8)
        self.play(FadeIn(transition_text), run_time=0.6)
        self.wait(0.3)

        # === 4. BOTTOM PANEL: Actual Hardware Compute ===
        bottom_panel = RoundedRectangle(
            width=13, height=2.8, corner_radius=0.15,
            fill_color=PANEL_BG, fill_opacity=0.7,
            stroke_color=PANEL_BORDER, stroke_width=2
        )
        bottom_panel.move_to([0, -1.5, 0])

        bottom_panel_title = Text(
            "Actual hardware compute",
            font="Arial", color=LAVENDER, font_size=28, weight=BOLD
        )
        bottom_panel_title.move_to(bottom_panel.get_corner(UL) + RIGHT * 0.4 + DOWN * 0.35)

        # Token row: D1 + 5 C1s
        hw_d1 = make_token("D1", DISCRETE_FILL, DISCRETE_BORDER, w=0.7, h=0.5)
        hw_c1s = VGroup(*[make_token("C1", CONTINUOUS_FILL, CONTINUOUS_BORDER, w=0.7, h=0.5) for _ in range(5)])
        hw_tokens = VGroup(hw_d1, *hw_c1s).arrange(RIGHT, buff=0.1)
        hw_tokens.move_to([-2.0, -1.7, 0])

        # Labels under tokens
        d1_label_bottom = Text("1 pass", font="Arial", color=LIGHT_GRAY, font_size=20)
        d1_label_bottom.next_to(hw_d1, DOWN, buff=0.25)

        c1_label_bottom = Text("many refinement passes", font="Arial", color=LIGHT_GRAY, font_size=20)
        c1_label_bottom.next_to(hw_c1s, DOWN, buff=0.25)

        self.play(FadeIn(bottom_panel), FadeIn(bottom_panel_title), run_time=1)
        self.play(FadeIn(hw_d1), run_time=0.4)
        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in hw_c1s], lag_ratio=0.15),
            run_time=1.2
        )
        self.play(
            FadeIn(d1_label_bottom),
            FadeIn(c1_label_bottom),
            run_time=0.6
        )
        self.wait(0.2)

        # === 5. TRANSFORMER BOX ===
        c1_left_x = hw_c1s.get_left()[0]
        c1_right_x = hw_c1s.get_right()[0]
        trans_width = c1_right_x - c1_left_x + 0.4

        transformer_box = RoundedRectangle(
            width=trans_width, height=0.55, corner_radius=0.08,
            fill_color=DARK_GRAY, fill_opacity=0.7,
            stroke_color=LIGHT_BORDER, stroke_width=2
        )
        transformer_label = Text("Transformer", font="Arial", color=WHITE, font_size=24, weight=BOLD)
        transformer_label.move_to(transformer_box.get_center())
        transformer_group = VGroup(transformer_box, transformer_label)
        transformer_group.next_to(hw_c1s, UP, buff=0.6)

        self.play(
            FadeIn(transformer_box),
            FadeIn(transformer_label),
            run_time=0.8
        )
        self.wait(0.2)

        # === 6. ANIMATE PASSES ===
        # 1 pass for D1: small arrow
        d1_arrow = Arrow(
            start=hw_d1.get_top() + UP * 0.5,
            end=hw_d1.get_top() + UP * 0.05,
            color=ORANGE, stroke_width=4, buff=0
        )
        self.play(GrowFromPoint(d1_arrow, d1_arrow.get_start()), run_time=0.4)
        self.play(d1_arrow.animate.shift(DOWN * 0.4), run_time=0.3, rate_func=smooth)
        self.play(FadeOut(d1_arrow), run_time=0.3)
        self.wait(0.2)

        # 5 passes for C1: dot moves across transformer
        dot = Dot(radius=0.1, color=ORANGE, fill_opacity=1)
        start_pos = transformer_box.get_left() + RIGHT * 0.2
        end_pos = transformer_box.get_right() + LEFT * 0.2
        dot.move_to(start_pos)

        self.play(FadeIn(dot, scale=0.5), run_time=0.2)

        for i in range(5):
            self.play(
                dot.animate.move_to(end_pos),
                run_time=0.35, rate_func=smooth
            )
            self.play(
                dot.animate.move_to(start_pos),
                run_time=0.25, rate_func=smooth
            )

        self.play(FadeOut(dot), run_time=0.2)
        self.wait(0.3)

        # === 7. REFINEMENT LOOP BRACE ===
        brace = Brace(hw_c1s, direction=UP, color=ORANGE, buff=0.12)
        brace_label = Text("Refinement loop", font="Arial", color=ORANGE, font_size=22, weight=BOLD)
        brace_label.next_to(brace, UP, buff=0.15)

        self.play(
            GrowFromCenter(brace),
            FadeIn(brace_label, shift=DOWN * 0.1),
            run_time=1
        )
        self.wait(0.3)

        # === 8. WARNING BADGE ===
        badge_box = RoundedRectangle(
            width=2.2, height=1.1, corner_radius=0.1,
            fill_color=WARN_RED, fill_opacity=0.15,
            stroke_color=WARN_RED, stroke_width=2.5
        )
        badge_text1 = Text("Speed bottleneck", font="Arial", color=WARN_RED, font_size=22, weight=BOLD)
        badge_text2 = Text("More passes = higher latency", font="Arial", color=WHITE, font_size=16)
        badge_text1.move_to(badge_box.get_center() + UP * 0.25)
        badge_text2.move_to(badge_box.get_center() + DOWN * 0.25)

        badge = VGroup(badge_box, badge_text1, badge_text2)
        badge.move_to([5.0, -1.7, 0])

        self.play(
            FadeIn(badge_box, scale=0.8),
            FadeIn(badge_text1),
            FadeIn(badge_text2),
            run_time=1
        )
        self.wait(0.5)

        # === 9. FINAL TAKEAWAY ===
        final_message = Text(
            "Continuous tokens preserve rich signals, but cost more inference steps.",
            font="Arial", color=WHITE, font_size=24, weight=BOLD
        )
        final_message.to_edge(DOWN, buff=0.4)

        self.play(FadeIn(final_message, shift=UP * 0.2), run_time=1.2)
        self.wait(2)
