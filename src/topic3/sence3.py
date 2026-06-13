from manim import *

# Color scheme
TEXT_COLOR = "#3B82F6"     # Blue
IMAGE_COLOR = "#F97316"    # Orange
AUDIO_COLOR = "#10B981"    # Green
VIDEO_COLOR = "#8B5CF6"    # Purple
NEUTRAL = "#1F2937"        # Dark navy
NEUTRAL_FILL = "#F1F5F9"   # Light gray
WARNING = "#DC2626"        # Red
GOLD = "#F59E0B"           # Gold for highlight
BG_COLOR = "#F8FAFC"       # Off-white

FONT = "Arial"


# --------------------------------------------------------------------------
# Typography helpers
# Single source of truth for all text. Uses a consistent font (Arial) and
# sensible default sizes so the look stays clean and readable.
# --------------------------------------------------------------------------
def clean_text(content, size=28, color=NEUTRAL, weight=NORMAL, slant=NORMAL):
    return Text(
        content,
        font=FONT,
        font_size=size,
        color=color,
        weight=weight,
        slant=slant,
        disable_ligatures=False,
    )


def title_text(text, font_size=36):
    """Top-of-screen title. Bold."""
    return clean_text(text, size=font_size, color=NEUTRAL, weight=BOLD)


def section_title(text, font_size=32):
    """Slightly smaller title used when we change between headings."""
    return clean_text(text, size=font_size, color=NEUTRAL, weight=BOLD)


def box_label(text, font_size=20):
    """Label inside a model/component box. Bold, compact."""
    return clean_text(text, size=font_size, color=NEUTRAL, weight=BOLD)


def caption_text(text, font_size=22):
    """Explanatory caption under the diagram. Normal weight."""
    return clean_text(text, size=font_size, color=NEUTRAL, weight=NORMAL)


def subtitle_text(text, font_size=24):
    """General-purpose normal-weight text."""
    return clean_text(text, size=font_size, color=NEUTRAL, weight=NORMAL)


def small_italic(text, font_size=20):
    """Italic for things like 'e.g. VideoPoet' or
    'predicted next token' -- kept readable."""
    return clean_text(text, size=font_size, color=NEUTRAL, weight=NORMAL, slant=ITALIC)


def small_bold_label(text, font_size=20):
    """Small bold label for output groups (e.g. 'Output video tokens')."""
    return clean_text(text, size=font_size, color=NEUTRAL, weight=BOLD)


def warning_markup(text, highlight, font_size=26):
    """Create warning text with a specific phrase highlighted in red.
    Uses MarkupText so the highlight renders cleanly without glyph issues."""
    idx = text.find(highlight)
    if idx == -1:
        return MarkupText(
            text,
            font=FONT,
            font_size=font_size,
            color=NEUTRAL,
            disable_ligatures=False,
        )
    before = text[:idx]
    after = text[idx + len(highlight):]
    safe_text = f'{before}<span foreground="{WARNING}">{highlight}</span>{after}'
    return MarkupText(
        safe_text,
        font=FONT,
        font_size=font_size,
        color=NEUTRAL,
        disable_ligatures=False,
    )


def make_token(label, color, size=0.5, stroke_color=None, stroke_width=2, font_size=18):
    """Colored square token with a label inside."""
    if stroke_color is None:
        stroke_color = color
    square = Square(
        side_length=size,
        fill_color=color,
        fill_opacity=1,
        stroke_color=stroke_color,
        stroke_width=stroke_width,
    )
    token_text = clean_text(label, size=font_size, color=WHITE, weight=BOLD)
    token_text.move_to(square.get_center())
    return VGroup(square, token_text)


def make_tokenizer(width=1.5, height=0.6):
    """Tokenizer box with a label inside."""
    box = Rectangle(
        width=width, height=height,
        fill_color=NEUTRAL_FILL, fill_opacity=1,
        stroke_color=NEUTRAL, stroke_width=2,
    )
    label_text = box_label("Tokenizer", font_size=18)
    label_text.move_to(box.get_center())
    return VGroup(box, label_text)


def make_arrow(start, end, color=None, buff=0.18, stroke_width=2.5):
    """Clean arrow with safe spacing from start/end mobjects."""
    if color is None:
        color = NEUTRAL
    return Arrow(start, end, color=color, buff=buff, stroke_width=stroke_width)


def grow_arrow(arrow, **kwargs):
    """Animate an arrow by growing it from its start point."""
    return GrowFromPoint(arrow, arrow.get_start(), **kwargs)


class NextTokenPrediction(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        self.scene1_modality_tokenization()
        self.scene2_text_prediction()
        self.scene3_multimodal_llm()
        self.scene4_final_question()

        self.wait(2)

    # ----- Scene 1: Modality tokenization -----
    def scene1_modality_tokenization(self):
        title = title_text("Tokenize each modality separately")
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title), run_time=0.5)

        modalities = [
            ("Text",  TEXT_COLOR,  ["T1", "T2", "T3"]),
            ("Image", IMAGE_COLOR, ["I1", "I2", "I3"]),
            ("Audio", AUDIO_COLOR, ["A1", "A2", "A3"]),
            ("Video", VIDEO_COLOR, ["V1", "V2", "V3"]),
        ]

        y_positions = [1.7, 0.3, -1.1, -2.5]
        row_groups = []

        for (name, color, toks), y in zip(modalities, y_positions):
            # Modality label
            label = box_label(name, font_size=20)
            label.move_to(LEFT * 5.3 + UP * y)

            # Tokenizer box
            tokenizer = make_tokenizer()
            tokenizer.move_to(LEFT * 3.0 + UP * y)

            # Arrow from label to tokenizer
            arrow1 = make_arrow(label.get_right(), tokenizer.get_left())

            # Output tokens
            row_tokens = VGroup(*[make_token(t, color, size=0.5) for t in toks])
            row_tokens.arrange(RIGHT, buff=0.12)
            row_tokens.move_to(RIGHT * 1.5 + UP * y)

            # Arrow from tokenizer to tokens
            arrow2 = make_arrow(tokenizer.get_right(), row_tokens.get_left())

            row = VGroup(label, tokenizer, arrow1, row_tokens, arrow2)
            row_groups.append(row)

        # Animate row by row
        for row in row_groups:
            label_mob, tok_mob, arr1_mob, tokens_mob, arr2_mob = row
            self.play(FadeIn(label_mob, shift=RIGHT * 0.2), run_time=0.35)
            self.play(
                grow_arrow(arr1_mob),
                FadeIn(tok_mob, scale=0.9),
                run_time=0.5,
            )
            self.play(
                grow_arrow(arr2_mob),
                LaggedStart(*[FadeIn(t, scale=0.85) for t in tokens_mob], lag_ratio=0.2),
                run_time=0.8,
            )

        self.wait(1.5)

        new_title = section_title("Merge into one multimodal token sequence")
        new_title.to_edge(UP, buff=0.4)
        self.play(
            FadeOut(title),
            FadeIn(new_title),
            run_time=0.6,
        )

        merged_data = [
            ("T1", TEXT_COLOR), ("T2", TEXT_COLOR),
            ("I1", IMAGE_COLOR), ("I2", IMAGE_COLOR),
            ("A1", AUDIO_COLOR),
            ("V1", VIDEO_COLOR), ("V2", VIDEO_COLOR),
        ]
        merged_tokens = VGroup(*[make_token(l, c, size=0.5) for l, c in merged_data])
        merged_tokens.arrange(RIGHT, buff=0.12)
        merged_tokens.move_to(DOWN * 3.1)

        rows_vgroup = VGroup(*row_groups)
        self.play(
            FadeOut(rows_vgroup),
            LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in merged_tokens], lag_ratio=0.08),
            run_time=1.5,
        )
        self.wait(2)

        self.scene1_group = VGroup(new_title, merged_tokens)

    # ----- Scene 2: Text next-token prediction -----
    def scene2_text_prediction(self):
        title = self.scene1_group[0]
        merged_tokens = self.scene1_group[1]

        self.play(FadeOut(merged_tokens), run_time=0.5)

        new_title = section_title("Next-token prediction works very well for text")
        new_title.to_edge(UP, buff=0.4)
        self.play(
            FadeOut(title),
            FadeIn(new_title),
            run_time=0.5,
        )

        y_level = 0.5

        words = ["The", "cat", "sits", "on", "the"]
        tokens = VGroup(*[make_token(w, TEXT_COLOR, size=0.6, font_size=18) for w in words])
        tokens.arrange(RIGHT, buff=0.15)
        tokens.move_to(LEFT * 3.5 + UP * y_level)

        # Transformer block
        tf_box = Rectangle(
            width=2.2, height=1.3,
            fill_color=NEUTRAL_FILL, fill_opacity=1,
            stroke_color=NEUTRAL, stroke_width=2.5,
        )
        tf_label = box_label("Transformer", font_size=20)
        tf_label.move_to(tf_box.get_center())
        transformer = VGroup(tf_box, tf_label)
        transformer.move_to(UP * y_level)

        # Predicted next token (highlighted with thin gold border)
        predicted = make_token(
            "mat", TEXT_COLOR, size=0.6,
            stroke_color=GOLD, stroke_width=4, font_size=18,
        )
        predicted.move_to(RIGHT * 3.5 + UP * y_level)

        # Italic label above the predicted token
        pred_label = small_italic("predicted next token", font_size=20)
        pred_label.next_to(predicted, UP, buff=0.22)

        arrow_in = make_arrow(tokens.get_right(), transformer.get_left())
        arrow_out = make_arrow(transformer.get_right(), predicted.get_left())

        caption = caption_text(
            "The model predicts the most likely next token from context.",
            font_size=22,
        )
        caption.to_edge(DOWN, buff=0.5)

        self.play(
            LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in tokens], lag_ratio=0.2),
            run_time=1.5,
        )
        self.play(
            grow_arrow(arrow_in),
            FadeIn(transformer, scale=0.9),
            run_time=1.0,
        )
        self.play(grow_arrow(arrow_out), run_time=0.4)
        self.play(FadeIn(predicted, scale=0.8), run_time=0.6)
        self.play(FadeIn(pred_label, shift=UP * 0.1), run_time=0.5)
        self.wait(0.4)
        self.play(FadeIn(caption, shift=UP * 0.1), run_time=1.0)
        self.wait(2)

        self.scene2_group = VGroup(
            new_title, tokens, transformer, predicted, pred_label,
            arrow_in, arrow_out, caption,
        )

    # ----- Scene 3: Multimodal LLM -----
    def scene3_multimodal_llm(self):
        self.play(FadeOut(self.scene2_group), run_time=0.5)

        title = title_text("Feed all tokens into one LLM")
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title), run_time=0.5)

        merged_data = [
            ("T1", TEXT_COLOR), ("T2", TEXT_COLOR),
            ("I1", IMAGE_COLOR), ("I2", IMAGE_COLOR),
            ("A1", AUDIO_COLOR),
            ("V1", VIDEO_COLOR), ("V2", VIDEO_COLOR),
        ]
        merged_tokens = VGroup(*[make_token(l, c, size=0.5) for l, c in merged_data])
        merged_tokens.arrange(RIGHT, buff=0.12)
        merged_tokens.move_to(LEFT * 4.5 + UP * 0.3)

        # LLM block
        llm_box = Rectangle(
            width=2.6, height=1.8,
            fill_color=NEUTRAL_FILL, fill_opacity=1,
            stroke_color=NEUTRAL, stroke_width=2.5,
        )
        llm_label1 = box_label("Multimodal LLM", font_size=20)
        llm_label2 = small_italic("e.g. VideoPoet", font_size=20)
        llm_labels = VGroup(llm_label1, llm_label2).arrange(DOWN, buff=0.18)
        llm_labels.move_to(llm_box.get_center())
        llm_block = VGroup(llm_box, llm_labels)
        llm_block.move_to(LEFT * 0.3 + UP * 0.3)

        self.play(
            LaggedStart(*[FadeIn(t, shift=RIGHT * 0.2) for t in merged_tokens], lag_ratio=0.1),
            run_time=1.0,
        )
        self.play(FadeIn(llm_block, scale=0.9), run_time=0.8)

        arrow_in = make_arrow(merged_tokens.get_right(), llm_block.get_left())
        self.play(grow_arrow(arrow_in), run_time=0.5)

        # Video output group
        vid_label = small_bold_label("Output video tokens", font_size=20)
        vid_tokens = VGroup(*[make_token(f"V{i}", VIDEO_COLOR, size=0.4) for i in range(1, 4)])
        vid_tokens.arrange(RIGHT, buff=0.08)
        vid_group = VGroup(vid_label, vid_tokens).arrange(DOWN, buff=0.18)
        vid_group.move_to(RIGHT * 3.8 + UP * 0.95)

        # Audio output group
        aud_label = small_bold_label("Output audio tokens", font_size=20)
        aud_tokens = VGroup(*[make_token(f"A{i}", AUDIO_COLOR, size=0.4) for i in range(1, 3)])
        aud_tokens.arrange(RIGHT, buff=0.08)
        aud_group = VGroup(aud_label, aud_tokens).arrange(DOWN, buff=0.18)
        aud_group.move_to(RIGHT * 3.8 + DOWN * 0.7)

        arrow_vid = make_arrow(llm_block.get_right(), vid_group.get_left())
        arrow_aud = make_arrow(llm_block.get_right(), aud_group.get_left())

        self.play(
            grow_arrow(arrow_vid),
            grow_arrow(arrow_aud),
            run_time=0.6,
        )
        self.play(
            LaggedStart(*[FadeIn(t, shift=LEFT * 0.2) for t in vid_tokens], lag_ratio=0.2),
            LaggedStart(*[FadeIn(t, shift=LEFT * 0.2) for t in aud_tokens], lag_ratio=0.2),
            FadeIn(vid_label, shift=LEFT * 0.2),
            FadeIn(aud_label, shift=LEFT * 0.2),
            run_time=1.2,
        )
        self.wait(2)

        self.scene3_group = VGroup(
            title, merged_tokens, llm_block, arrow_in,
            arrow_vid, arrow_aud, vid_group, aud_group,
        )

    # ----- Scene 4: Final question -----
    def scene4_final_question(self):
        self.play(FadeOut(self.scene3_group), run_time=0.6)

        question = title_text(
            "So why not use next-token prediction for everything?",
            font_size=36,
        )
        question.move_to(UP * 1.5)
        self.play(FadeIn(question, shift=UP * 0.3), run_time=1.5)
        self.wait(0.8)

        warning1 = warning_markup(
            "But visual tokens may lose important details.",
            "important details",
            font_size=26,
        )
        warning1.next_to(question, DOWN, buff=0.7)

        warning2 = warning_markup(
            "This leads to the quality issue of discrete tokens.",
            "discrete tokens",
            font_size=26,
        )
        warning2.next_to(warning1, DOWN, buff=0.35)

        self.play(FadeIn(warning1, shift=UP * 0.3), run_time=1)
        self.wait(0.4)
        self.play(FadeIn(warning2, shift=UP * 0.3), run_time=1)
        self.wait(2)