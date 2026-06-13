from manim import *

class ContinuousTokensSpeedIssue(Scene):
    def construct(self):
        # Dark background for clean academic slide style
        self.camera.background_color = "#1C1C1C"

        # === Color palette ===
        LAVENDER = "#B39DDB"
        WHITE = "#FFFFFF"
        GRAY = "#BBBBBB"
        BLUE = "#42A5F5"
        GREEN = "#66BB6A"
        ORANGE = "#FFA726"
        DARK_GRAY = "#616161"

        # === Helper functions ===
        def make_token_box(label_text, color, w=0.8, h=0.52):
            box = RoundedRectangle(
                width=w, height=h,
                corner_radius=0.08,
                fill_color=color, fill_opacity=0.85,
                stroke_color=color, stroke_width=2,
            )
            txt = Text(label_text, font_size=24, color=WHITE, font="DejaVu Sans")
            txt.move_to(box.get_center())
            return VGroup(box, txt)

        # ====================================================
        # SCENE 1: Logical sequence (labels under blocks removed)
        # ====================================================
        title1 = Text(
            "Continuous tokens have a speed issue",
            font_size=36, color=LAVENDER, font="DejaVu Sans",
        )
        title1.move_to([0, 3.0, 0])

        subtitle1 = Text(
            "At the sequence level, both token types look compact",
            font_size=20, color=GRAY, font="DejaVu Sans",
        )
        subtitle1.move_to([0, 2.5, 0])

        logical_label = Text("Logical sequence", font_size=22, color=WHITE, font="DejaVu Sans")
        logical_label.move_to([0, 1.7, 0])

        d1 = make_token_box("D1", BLUE)
        c1 = make_token_box("C1", GREEN)
        d2 = make_token_box("D2", BLUE)
        c2 = make_token_box("C2", GREEN)

        logical_tokens = VGroup(d1, c1, d2, c2).arrange(RIGHT, buff=0.25)
        logical_tokens.move_to([0, 0.5, 0])

        bottom1 = Text("So far, they look similarly cheap.", font_size=20, color=WHITE, font="DejaVu Sans")
        bottom1.move_to([0, -2.5, 0])

        self.play(FadeIn(title1, shift=DOWN * 0.2), run_time=1)
        self.play(FadeIn(subtitle1, shift=DOWN * 0.2), run_time=1)
        self.play(FadeIn(logical_label), run_time=1)
        self.play(FadeIn(d1, shift=RIGHT * 0.2), run_time=0.5)
        self.play(FadeIn(c1, shift=RIGHT * 0.2), run_time=0.5)
        self.play(FadeIn(d2, shift=RIGHT * 0.2), run_time=0.5)
        self.play(FadeIn(c2, shift=RIGHT * 0.2), run_time=0.5)
        self.play(FadeIn(bottom1), run_time=1.5)
        self.wait(2)
        self.play(
            *[FadeOut(m) for m in [title1, subtitle1, logical_label, logical_tokens, bottom1]],
            run_time=1.5,
        )

        # ====================================================
        # SCENE 2: Real hardware compute (looping dot replaces arrow)
        # ====================================================
        title2 = Text("But hardware compute is different",
                      font_size=34, color=LAVENDER, font="DejaVu Sans")
        title2.move_to([0, 3.0, 0])

        compute_label = Text("Actual transformer work",
                             font_size=28, color=WHITE, font="DejaVu Sans")
        compute_label.move_to([0, 2.3, 0])

        # --- Token row ---
        compute_d1 = make_token_box("D1", BLUE)
        compute_c1_list = [make_token_box("C1", GREEN) for _ in range(5)]
        c1_group = VGroup(*compute_c1_list).arrange(RIGHT, buff=0.1)

        compute_d1.move_to([-3.0, -0.4, 0])
        c1_group.move_to([0.5, -0.4, 0])

        # --- Labels under token row ---
        one_pass = Text("1 pass", font_size=22, color=WHITE, font="DejaVu Sans")
        one_pass.next_to(compute_d1, DOWN, buff=0.35)
        many_passes = Text("many passes", font_size=22, color=ORANGE, font="DejaVu Sans")
        many_passes.next_to(c1_group, DOWN, buff=0.35)

        # --- Transformer box (only above the C1 group) ---
        trans_w = c1_group.width + 0.4
        transformer_box = RoundedRectangle(
            width=trans_w, height=0.55,
            corner_radius=0.1,
            fill_color=DARK_GRAY, fill_opacity=1.0,
            stroke_color=DARK_GRAY, stroke_width=2,
        )
        transformer_box.move_to([c1_group.get_center()[0], 0.7, 0])
        transformer_text = Text("Transformer", font_size=24, color=WHITE, font="DejaVu Sans")
        transformer_text.move_to(transformer_box.get_center())

        # --- Refinement loop label (above transformer box) ---
        loop_label = Text("refinement loop", font_size=22, color=ORANGE, font="DejaVu Sans")
        loop_label.move_to([c1_group.get_center()[0], 1.5, 0])

        # --- Looping refinement dot (replaces the curved arrow) ---
        # Small orange dot that loops back-and-forth above the C1 group
        # to visually represent repeated refinement passes.
        dot = Dot(color=ORANGE, radius=0.09)

        # Closed racetrack path: stays between transformer box and C1 row.
        left_x = c1_group.get_left()[0] - 0.15
        right_x = c1_group.get_right()[0] + 0.15
        path_y_top = 0.28   # below the transformer (transformer bottom ~ y=0.425)
        path_y_bot = -0.02  # above the C1 tokens (C1 top ~ y=-0.14)

        loop_path = VMobject(stroke_width=0, fill_opacity=0)
        loop_path.set_points_as_corners([
            [left_x, path_y_top, 0],
            [right_x, path_y_top, 0],
            [right_x, path_y_bot, 0],
            [left_x, path_y_bot, 0],
            [left_x, path_y_top, 0],
        ])

        # Place the dot at the start of the path
        dot.move_to([left_x, path_y_top, 0])

        # --- Warning block (right side, shifted further right to avoid the dot path) ---
        warning1 = Text("Speed bottleneck", font_size=30, color=ORANGE, font="DejaVu Sans")
        warning2 = Text("more passes = higher latency",
                        font_size=22, color=WHITE, font="DejaVu Sans")
        warning_group = VGroup(warning1, warning2).arrange(DOWN, buff=0.3)
        warning_group.move_to([5.0, -0.4, 0])

        # --- Animate Scene 2 ---
        self.play(FadeIn(title2), run_time=1)
        self.play(FadeIn(compute_label), run_time=1)
        self.play(FadeIn(compute_d1), run_time=0.5)

        for c in compute_c1_list:
            self.play(FadeIn(c), run_time=0.3)

        self.wait(0.3)
        self.play(FadeIn(one_pass), FadeIn(many_passes), run_time=1)
        self.play(FadeIn(VGroup(transformer_box, transformer_text)), run_time=1.5)
        self.play(FadeIn(loop_label), run_time=1)

        # Create the dot and animate it looping across the C1 group
        self.play(FadeIn(dot), run_time=0.5)
        for _ in range(4):
            self.play(MoveAlongPath(dot, loop_path), run_time=1.2, rate_func=linear)

        self.play(FadeIn(warning_group), run_time=1.5)
        self.play(Indicate(c1_group, color=ORANGE, scale_factor=1.05), run_time=1.5)

        self.wait(2)
        self.play(
            *[FadeOut(m) for m in [title2, compute_label, compute_d1, c1_group,
                                   one_pass, many_passes,
                                   transformer_box, transformer_text,
                                   dot, loop_label, warning_group]],
            run_time=1.5,
        )

        # ====================================================
        # SCENE 3: Side-by-side summary (unchanged)
        # ====================================================
        title3 = Text("Same sequence length, different compute cost",
                       font_size=30, color=LAVENDER, font="DejaVu Sans")
        title3.move_to([0, 3.0, 0])

        left_header = Text("Discrete token", font_size=22, color=WHITE, font="DejaVu Sans")
        left_token = make_token_box("D1", BLUE, w=0.85, h=0.55)
        left_label = Text("1 transformer pass", font_size=18, color=GRAY, font="DejaVu Sans")
        left_col = VGroup(left_header, left_token, left_label).arrange(DOWN, buff=0.5)
        left_col.move_to([-3.5, 0.3, 0])

        right_header = Text("Continuous token", font_size=22, color=WHITE, font="DejaVu Sans")
        right_token_list = [make_token_box("C1", GREEN, w=0.5, h=0.5) for _ in range(5)]
        c1_row = VGroup(*right_token_list).arrange(RIGHT, buff=0.35)
        chain_arrows = []
        for i in range(4):
            arr = Arrow(
                right_token_list[i].get_right(),
                right_token_list[i+1].get_left(),
                color=WHITE, stroke_width=2, buff=0.05,
                max_tip_length_to_length_ratio=0.5,
            )
            chain_arrows.append(arr)
        right_chain = VGroup(c1_row, *chain_arrows)

        right_label = Text("many refinement passes", font_size=18, color=ORANGE, font="DejaVu Sans")
        right_col = VGroup(right_header, right_chain, right_label).arrange(DOWN, buff=0.5)
        right_col.move_to([2.0, 0.3, 0])

        takeaway = Text(
            "Continuous tokens preserve richer signals, but inference becomes slower.",
            font_size=22, color=WHITE, font="DejaVu Sans",
        )
        takeaway.move_to([0, -2.8, 0])

        self.play(FadeIn(title3), run_time=1)
        self.play(FadeIn(left_col), run_time=1.5)
        self.play(FadeIn(right_col), run_time=1.5)
        self.play(Indicate(right_chain, color=ORANGE, scale_factor=1.05), run_time=1.5)
        self.play(FadeIn(takeaway), run_time=1.5)

        self.wait(3)
