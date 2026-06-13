from manim import *

class MultimodalTokenGeneration(Scene):
    def construct(self):
        # ===== Color & typography constants =====
        TEXT_COLOR = BLUE
        IMG_COLOR = ORANGE
        MASK_COLOR = GRAY
        MODEL_COLOR = "#FFD700"
        FONT = "DejaVu Sans"

        # ===== Text styling helpers (typography consistency) =====
        def make_title(text, color, size=42, weight=BOLD):
            return Text(text, font=FONT, font_size=size, color=color, weight=weight)

        def make_bullet(text, color=WHITE, size=22):
            return Text(f"\u2022  {text}", font=FONT, font_size=size, color=color)

        def make_caption(text, color=WHITE, size=20):
            return Text(text, font=FONT, font_size=size, color=color)

        def make_token(text, color, width=0.85, height=0.5, font_size=14):
            rect = RoundedRectangle(
                corner_radius=0.08, width=width, height=height,
                fill_color=color, fill_opacity=0.25,
                stroke_color=color, stroke_width=2,
            )
            label = Text(text, font=FONT, font_size=font_size, color=color)
            label.move_to(rect.get_center())
            return VGroup(rect, label)

        # ==================== Phase 1: Tokenization ====================
        text_input = Text('"A red bird flying"', font=FONT, font_size=24, color=TEXT_COLOR)
        text_input.move_to([-5.5, 1.8, 0])

        icon_bg = Rectangle(width=1.4, height=1.0,
                            fill_color=IMG_COLOR, fill_opacity=0.15,
                            stroke_color=IMG_COLOR, stroke_width=2)
        m1 = Polygon([-0.5, -0.35, 0], [-0.1, 0.2, 0], [0.3, -0.35, 0],
                     fill_color=IMG_COLOR, fill_opacity=0.7, stroke_width=0)
        m2 = Polygon([-0.2, -0.35, 0], [0.2, 0.05, 0], [0.5, -0.35, 0],
                     fill_color=IMG_COLOR, fill_opacity=0.5, stroke_width=0)
        sun = Circle(radius=0.12, fill_color=YELLOW, fill_opacity=1,
                     stroke_width=0).move_to([0.35, 0.25, 0])
        image_icon = VGroup(icon_bg, m1, m2, sun).move_to([-5.5, -1.5, 0])

        self.play(FadeIn(text_input), FadeIn(image_icon), run_time=0.8)

        text_tok_box = RoundedRectangle(corner_radius=0.1, width=1.7, height=0.9,
                                        stroke_width=2, color=TEXT_COLOR)
        text_tok_box.move_to([-2.2, 1.8, 0])
        text_tok_label = Text("Text Tokenizer", font=FONT, font_size=14, color=TEXT_COLOR)
        text_tok_label.move_to(text_tok_box.get_center())

        image_tok_box = RoundedRectangle(corner_radius=0.1, width=1.7, height=0.9,
                                         stroke_width=2, color=IMG_COLOR)
        image_tok_box.move_to([-2.2, -1.5, 0])
        image_tok_label = Text("Image Tokenizer", font=FONT, font_size=14, color=IMG_COLOR)
        image_tok_label.move_to(image_tok_box.get_center())

        self.play(
            Create(text_tok_box), Write(text_tok_label),
            Create(image_tok_box), Write(image_tok_label),
            run_time=0.8
        )

        arrow1 = Arrow(text_input.get_right(), text_tok_box.get_left(),
                       buff=0.1, color=TEXT_COLOR, stroke_width=3)
        arrow2 = Arrow(image_icon.get_right(), image_tok_box.get_left(),
                       buff=0.1, color=IMG_COLOR, stroke_width=3)
        self.play(Create(arrow1), Create(arrow2), run_time=0.5)

        text_token_data = ["A", "red", "bird", "flying"]
        image_token_data = ["IMG_12", "IMG_45", "IMG_08", "IMG_91"]

        text_tokens = VGroup(*[make_token(f"[{t}]", TEXT_COLOR) for t in text_token_data])
        text_tokens.arrange(RIGHT, buff=0.1)
        text_tokens.move_to([2.5, 1.8, 0])

        image_tokens = VGroup(*[make_token(f"[{t}]", IMG_COLOR) for t in image_token_data])
        image_tokens.arrange(RIGHT, buff=0.1)
        image_tokens.move_to([2.5, -1.5, 0])

        arrow3 = Arrow(text_tok_box.get_right(), text_tokens.get_left(),
                       buff=0.1, color=TEXT_COLOR, stroke_width=3)
        arrow4 = Arrow(image_tok_box.get_right(), image_tokens.get_left(),
                       buff=0.1, color=IMG_COLOR, stroke_width=3)
        self.play(Create(arrow3), Create(arrow4), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(t, scale=0.5) for t in text_tokens], lag_ratio=0.15),
            LaggedStart(*[FadeIn(t, scale=0.5) for t in image_tokens], lag_ratio=0.15),
            run_time=1.0
        )
        self.wait(0.3)

        self.play(
            FadeOut(text_input), FadeOut(image_icon),
            FadeOut(text_tok_box), FadeOut(text_tok_label),
            FadeOut(image_tok_box), FadeOut(image_tok_label),
            FadeOut(arrow1), FadeOut(arrow2), FadeOut(arrow3), FadeOut(arrow4),
            run_time=0.6
        )

        merged_text = VGroup(*[make_token(f"[{t}]", TEXT_COLOR) for t in text_token_data])
        merged_text.arrange(RIGHT, buff=0.1)
        merged_text.move_to([-2.2, 0.3, 0])

        merged_image = VGroup(*[make_token(f"[{t}]", IMG_COLOR) for t in image_token_data])
        merged_image.arrange(RIGHT, buff=0.1)
        merged_image.move_to([2.2, 0.3, 0])

        self.play(
            Transform(text_tokens, merged_text),
            Transform(image_tokens, merged_image),
            run_time=0.9
        )

        merge_label = Text("Multimodal Token Sequence", font=FONT, font_size=20, color=WHITE)
        merge_label.move_to([0, 1.5, 0])
        self.play(Write(merge_label), run_time=0.7)
        self.wait(0.3)

        # ==================== Phase 2: Autoregressive Generation ====================
        self.play(
            FadeOut(text_tokens), FadeOut(image_tokens), FadeOut(merge_label),
            run_time=0.5
        )

        model_box = RoundedRectangle(corner_radius=0.1, width=4.8, height=0.8,
                                     stroke_width=3, color=MODEL_COLOR)
        model_box.move_to([0, 2.5, 0])
        model_label = Text("Autoregressive Transformer", font=FONT, font_size=22, color=MODEL_COLOR)
        model_label.move_to(model_box.get_center())
        model = VGroup(model_box, model_label)
        self.play(Create(model), run_time=0.8)

        formula = MathTex(r"p(x_t \mid x_1, \ldots, x_{t-1})", font_size=34)
        formula.move_to([0, 1.4, 0])
        self.play(Write(formula), run_time=0.8)

        all_token_data = text_token_data + image_token_data
        all_token_colors = [TEXT_COLOR]*4 + [IMG_COLOR]*4
        placeholders = [make_token("[?]", MASK_COLOR) for _ in all_token_data]
        placeholder_grp = VGroup(*placeholders).arrange(RIGHT, buff=0.1)
        placeholder_grp.move_to([0, -0.2, 0])
        self.play(LaggedStart(*[FadeIn(t) for t in placeholders], lag_ratio=0.05),
                  run_time=0.7)

        def make_predict_group(target_token):
            arrow = Arrow(model.get_bottom(), target_token.get_top() + DOWN*0.05,
                          buff=0.05, color=MODEL_COLOR, stroke_width=4)
            label = Text("Predict", font=FONT, font_size=14, color=MODEL_COLOR)
            label.next_to(arrow, RIGHT, buff=0.1)
            return VGroup(arrow, label)

        predict_grp = make_predict_group(placeholders[0])
        self.play(Create(predict_grp), run_time=0.5)

        current_tokens = list(placeholders)
        for i, (data, color) in enumerate(zip(all_token_data, all_token_colors)):
            new_tok = make_token(f"[{data}]", color)
            new_tok.move_to(current_tokens[i].get_center())
            self.play(ReplacementTransform(current_tokens[i], new_tok), run_time=0.3)
            current_tokens[i] = new_tok
            if i < len(all_token_data) - 1:
                new_predict = make_predict_group(placeholders[i+1])
                self.play(Transform(predict_grp, new_predict), run_time=0.15)

        self.wait(0.2)

        explanation = Text(
            "Discrete AR treats text and image as one sequence of tokens.\n"
            "The model generates one token at a time.",
            font=FONT, font_size=18, color=WHITE
        ).move_to([0, -2.6, 0])
        self.play(Write(explanation), run_time=0.9)
        self.wait(0.4)

        final_label1 = Text("Text: Discrete AR  |  Image: Discrete AR",
                            font=FONT, font_size=20, color=MODEL_COLOR)
        final_label1.move_to([0, -3.5, 0])
        self.play(Write(final_label1), run_time=0.6)
        self.wait(0.4)

        # ==================== Phase 3: Transition to Discrete Diffusion ====================
        scene1_mobjects = VGroup(
            model, formula, predict_grp, explanation, final_label1
        )
        for t in current_tokens:
            scene1_mobjects.add(t)
        self.play(FadeOut(scene1_mobjects), run_time=0.7)
        self.wait(0.2)

        # ==================== Phase 4: Forward Corruption ====================
        diff_tokens_data = ["IMG_12", "IMG_45", "IMG_08", "IMG_91", "IMG_33", "IMG_70"]

        clean_tokens = VGroup(*[make_token(f"[{t}]", IMG_COLOR) for t in diff_tokens_data])
        clean_tokens.arrange(RIGHT, buff=0.12)
        clean_tokens.move_to([0, 0.8, 0])
        self.play(LaggedStart(*[FadeIn(t) for t in clean_tokens], lag_ratio=0.08),
                  run_time=1.0)
        self.wait(0.3)

        fwd_label = Text("Forward process: add discrete noise / masking",
                         font=FONT, font_size=20, color=IMG_COLOR)
        fwd_label.move_to([0, 2.5, 0])
        self.play(Write(fwd_label), run_time=0.7)

        step_label = Text("Step 0: 0 masked", font=FONT, font_size=18, color=IMG_COLOR)
        step_label.move_to([0, -0.5, 0])
        self.play(Write(step_label), run_time=0.5)
        self.wait(0.3)

        m_a = make_token("[MASK]", MASK_COLOR).move_to(clean_tokens[3].get_center())
        m_b = make_token("[MASK]", MASK_COLOR).move_to(clean_tokens[4].get_center())
        self.play(Transform(clean_tokens[3], m_a), Transform(clean_tokens[4], m_b),
                  run_time=0.7)
        new_step = Text("Step 1: 2 masked", font=FONT, font_size=18, color=IMG_COLOR)
        new_step.move_to([0, -0.5, 0])
        self.play(ReplacementTransform(step_label, new_step), run_time=0.4)
        step_label = new_step
        self.wait(0.25)

        m_c = make_token("[MASK]", MASK_COLOR).move_to(clean_tokens[1].get_center())
        m_d = make_token("[MASK]", MASK_COLOR).move_to(clean_tokens[2].get_center())
        self.play(Transform(clean_tokens[1], m_c), Transform(clean_tokens[2], m_d),
                  run_time=0.7)
        new_step = Text("Step 2: 4 masked", font=FONT, font_size=18, color=IMG_COLOR)
        new_step.move_to([0, -0.5, 0])
        self.play(ReplacementTransform(step_label, new_step), run_time=0.4)
        step_label = new_step
        self.wait(0.25)

        m_e = make_token("[MASK]", MASK_COLOR).move_to(clean_tokens[0].get_center())
        m_f = make_token("[MASK]", MASK_COLOR).move_to(clean_tokens[5].get_center())
        self.play(Transform(clean_tokens[0], m_e), Transform(clean_tokens[5], m_f),
                  run_time=0.7)
        new_step = Text("Step 3: 6 masked", font=FONT, font_size=18, color=IMG_COLOR)
        new_step.move_to([0, -0.5, 0])
        self.play(ReplacementTransform(step_label, new_step), run_time=0.4)
        step_label = new_step
        self.wait(0.5)

        # ==================== Phase 5: Reverse Denoising ====================
        self.play(
            FadeOut(fwd_label), FadeOut(step_label), FadeOut(clean_tokens),
            run_time=0.6
        )

        diff_model_box = RoundedRectangle(corner_radius=0.1, width=4.5, height=0.8,
                                         stroke_width=3, color=IMG_COLOR)
        diff_model_box.move_to([0, 2.5, 0])
        diff_model_label = Text("Discrete Diffusion Model", font=FONT, font_size=22, color=IMG_COLOR)
        diff_model_label.move_to(diff_model_box.get_center())
        diff_model = VGroup(diff_model_box, diff_model_label)
        self.play(Create(diff_model), run_time=0.8)

        masked_tokens = VGroup(*[make_token("[MASK]", MASK_COLOR) for _ in diff_tokens_data])
        masked_tokens.arrange(RIGHT, buff=0.12)
        masked_tokens.move_to([0, 0.8, 0])
        self.play(LaggedStart(*[FadeIn(t) for t in masked_tokens], lag_ratio=0.08),
                  run_time=0.9)
        self.wait(0.3)

        rev_step = Text("Step 0: 0 recovered", font=FONT, font_size=18, color=IMG_COLOR)
        rev_step.move_to([0, -0.5, 0])
        self.play(Write(rev_step), run_time=0.5)
        self.wait(0.3)

        r_a = make_token(f"[{diff_tokens_data[3]}]", IMG_COLOR).move_to(masked_tokens[3].get_center())
        r_b = make_token(f"[{diff_tokens_data[4]}]", IMG_COLOR).move_to(masked_tokens[4].get_center())
        self.play(Transform(masked_tokens[3], r_a), Transform(masked_tokens[4], r_b),
                  run_time=0.7)
        new_rev = Text("Step 1: 2 recovered", font=FONT, font_size=18, color=IMG_COLOR)
        new_rev.move_to([0, -0.5, 0])
        self.play(ReplacementTransform(rev_step, new_rev), run_time=0.4)
        rev_step = new_rev
        self.wait(0.25)

        r_c = make_token(f"[{diff_tokens_data[1]}]", IMG_COLOR).move_to(masked_tokens[1].get_center())
        r_d = make_token(f"[{diff_tokens_data[2]}]", IMG_COLOR).move_to(masked_tokens[2].get_center())
        self.play(Transform(masked_tokens[1], r_c), Transform(masked_tokens[2], r_d),
                  run_time=0.7)
        new_rev = Text("Step 2: 4 recovered", font=FONT, font_size=18, color=IMG_COLOR)
        new_rev.move_to([0, -0.5, 0])
        self.play(ReplacementTransform(rev_step, new_rev), run_time=0.4)
        rev_step = new_rev
        self.wait(0.25)

        r_e = make_token(f"[{diff_tokens_data[0]}]", IMG_COLOR).move_to(masked_tokens[0].get_center())
        r_f = make_token(f"[{diff_tokens_data[5]}]", IMG_COLOR).move_to(masked_tokens[5].get_center())
        self.play(Transform(masked_tokens[0], r_e), Transform(masked_tokens[5], r_f),
                  run_time=0.7)
        new_rev = Text("Step 3: 6 recovered", font=FONT, font_size=18, color=IMG_COLOR)
        new_rev.move_to([0, -0.5, 0])
        self.play(ReplacementTransform(rev_step, new_rev), run_time=0.4)
        rev_step = new_rev
        self.wait(0.4)

        diff_explanation = Text(
            "Discrete Diffusion generates by iteratively refining corrupted discrete tokens.",
            font=FONT, font_size=18, color=WHITE
        ).move_to([0, -2.5, 0])
        self.play(Write(diff_explanation), run_time=0.9)
        self.wait(0.5)

        # ==================== Phase 6: Comparison (clean two-column) ====================
        self.play(
            FadeOut(diff_model), FadeOut(masked_tokens), FadeOut(rev_step),
            FadeOut(diff_explanation),
            run_time=0.6
        )

        # --- Titles (left blue, right orange) ---
        ar_title = make_title("Discrete AR", TEXT_COLOR, size=42)
        diff_title = make_title("Discrete Diffusion", IMG_COLOR, size=42)

        # --- Bullet lists (regular weight, clean dot, consistent indent) ---
        ar_bullets = VGroup(
            make_bullet("Tokenize text and image"),
            make_bullet("Predict next token"),
            make_bullet("Sequential generation"),
            make_bullet("LLM-like mechanism"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)

        diff_bullets = VGroup(
            make_bullet("Tokenize text and image"),
            make_bullet("Add masks or noise"),
            make_bullet("Recover tokens step by step"),
            make_bullet("Refinement-based mechanism"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)

        # Position titles near the top of their columns
        ar_title.move_to([-3.4, 2.3, 0])
        diff_title.move_to([3.4, 2.3, 0])

        # Bullets sit comfortably below the titles, left-aligned with them
        ar_bullets.next_to(ar_title, DOWN, buff=0.85, aligned_edge=LEFT)
        diff_bullets.next_to(diff_title, DOWN, buff=0.85, aligned_edge=LEFT)

        # Center vertical divider
        divider = Line(UP*2.7, DOWN*2.7, color=WHITE, stroke_width=1.5)
        divider.move_to([0, 0.3, 0])

        self.play(
            Write(ar_title), Write(diff_title), Create(divider),
            run_time=0.8
        )
        self.play(
            LaggedStart(*[Write(b) for b in ar_bullets], lag_ratio=0.25),
            LaggedStart(*[Write(b) for b in diff_bullets], lag_ratio=0.25),
            run_time=2.0
        )
        self.wait(0.4)

        # --- Bottom caption: split into 2 balanced lines, safely inside frame ---
        bottom_msg = VGroup(
            make_caption("Many recent multimodal models are built from combinations of",
                         MODEL_COLOR, size=20),
            make_caption("Discrete AR and Discrete Diffusion.",
                         MODEL_COLOR, size=20),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        bottom_msg.move_to([0, -3.25, 0])

        self.play(Write(bottom_msg), run_time=1.2)
        self.wait(0.5)

        self.wait()