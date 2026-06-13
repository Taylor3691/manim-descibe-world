from manim import *

config.frame_width = 16
config.frame_height = 9
config.background_color = "#FAFAF5"

# Color scheme
TEXT_COLOR = "#2E5BBA"
TEXT_FILL = "#DDE6F7"
IMAGE_COLOR = "#2E8B57"
IMAGE_FILL = "#D7F0DD"
PURPLE = "#7B4FBF"
PURPLE_FILL = "#EFE6FA"
NAVY = "#1F2A44"
GREY = "#5A6473"
LIGHT_GREY = "#EEF1F5"
BG_COLOR = "#FAFAF5"
UNIFIED_COLOR = "#1A2540"

FONT = "DejaVu Sans"


def make_token(label, color, fill_color, font_size=20, width=0.9, height=0.5):
    """Create a colored pill-shaped token with text inside."""
    box = RoundedRectangle(
        width=width, height=height, corner_radius=0.12,
        stroke_color=color, stroke_width=2.5,
        fill_color=fill_color, fill_opacity=1.0
    )
    box.set_z_index(1)
    t = Text(label, color=color, font_size=font_size, weight=BOLD, font=FONT)
    t.set_z_index(2)
    t.move_to(box.get_center())
    return VGroup(box, t)


def build_left_box(title_text, inputs, outputs, center_pos, box_width=3.6, box_height=1.2):
    """Build a left-side model box with title and tokens."""
    box = RoundedRectangle(
        width=box_width, height=box_height, corner_radius=0.12,
        stroke_color=NAVY, stroke_width=2.5,
        fill_color=LIGHT_GREY, fill_opacity=0.85
    )
    box.move_to(center_pos)
    box.set_z_index(1)

    title = Text(title_text, font_size=20, weight=BOLD, color=NAVY, font=FONT)
    title.move_to([center_pos[0], center_pos[1] + 0.32, 0])
    title.set_z_index(4)

    input_tokens = VGroup(*[make_token(l, c, f, font_size=16, width=0.7, height=0.4)
                            for l, c, f in inputs]).arrange(RIGHT, buff=0.08)
    output_tokens = VGroup(*[make_token(l, c, f, font_size=16, width=0.7, height=0.4)
                             for l, c, f in outputs]).arrange(RIGHT, buff=0.08)

    arrow = Arrow(
        LEFT * 0.15, RIGHT * 0.45,
        buff=0, stroke_width=3.5, color=NAVY,
        max_tip_length_to_length_ratio=0.35
    )
    arrow.set_z_index(0)

    content = VGroup(input_tokens, arrow, output_tokens).arrange(RIGHT, buff=0.15)
    content.move_to([center_pos[0], center_pos[1] - 0.2, 0])

    return VGroup(box, title, content)


def build_right_box(center_pos, box_width=3.4, box_height=1.5):
    """Build the right-side interleaved model box."""
    box = RoundedRectangle(
        width=box_width, height=box_height, corner_radius=0.12,
        stroke_color=PURPLE, stroke_width=3.5,
        fill_color=PURPLE_FILL, fill_opacity=0.85
    )
    box.move_to(center_pos)
    box.set_z_index(1)

    title = Text("Interleaved Models", font_size=20, weight=BOLD, color=NAVY, font=FONT)
    title.move_to([center_pos[0], center_pos[1] + 0.4, 0])
    title.set_z_index(4)

    input_group = VGroup(
        make_token("Text", TEXT_COLOR, TEXT_FILL, font_size=15, width=0.65, height=0.4),
        make_token("Image", IMAGE_COLOR, IMAGE_FILL, font_size=15, width=0.65, height=0.4)
    ).arrange(RIGHT, buff=0.08)
    input_group.move_to([center_pos[0] - 0.9, center_pos[1] - 0.25, 0])

    output_group = VGroup(
        make_token("Text", TEXT_COLOR, TEXT_FILL, font_size=15, width=0.65, height=0.4),
        make_token("Image", IMAGE_COLOR, IMAGE_FILL, font_size=15, width=0.65, height=0.4)
    ).arrange(RIGHT, buff=0.08)
    output_group.move_to([center_pos[0] + 0.9, center_pos[1] - 0.25, 0])

    arrow = Arrow(
        input_group.get_right() + RIGHT * 0.05,
        output_group.get_left() + LEFT * 0.05,
        buff=0, stroke_width=3, color=PURPLE,
        max_tip_length_to_length_ratio=0.35
    )
    arrow.set_z_index(0)

    return VGroup(box, title, input_group, arrow, output_group)


def build_center_pipeline():
    """Build the center pipeline: [Text][Image] -> Unified -> [Text][Image]"""
    input_tokens = VGroup(
        make_token("Text", TEXT_COLOR, TEXT_FILL, font_size=20, width=0.9, height=0.5),
        make_token("Image", IMAGE_COLOR, IMAGE_FILL, font_size=20, width=0.9, height=0.5)
    ).arrange(RIGHT, buff=0.12)

    unified_box = RoundedRectangle(
        width=2.0, height=1.1, corner_radius=0.13,
        stroke_color=UNIFIED_COLOR, stroke_width=3,
        fill_color=UNIFIED_COLOR, fill_opacity=1.0
    )
    unified_box.set_z_index(1)
    unified_text = Text(
        "Unified\nMulti-Modal\nModel",
        font_size=15, weight=BOLD, color=WHITE, font=FONT
    )
    unified_text.set_z_index(2)
    unified_text.move_to(unified_box.get_center())
    unified = VGroup(unified_box, unified_text)

    output_tokens = VGroup(
        make_token("Text", TEXT_COLOR, TEXT_FILL, font_size=20, width=0.9, height=0.5),
        make_token("Image", IMAGE_COLOR, IMAGE_FILL, font_size=20, width=0.9, height=0.5)
    ).arrange(RIGHT, buff=0.12)

    # Position elements with explicit spacing
    input_tokens.move_to([-2.7, -0.25, 0])
    unified.move_to([0, -0.25, 0])
    output_tokens.move_to([2.7, -0.25, 0])

    arrow1 = Arrow(
        input_tokens.get_right() + RIGHT * 0.15,
        unified.get_left() + LEFT * 0.2,
        buff=0, stroke_width=4.5, color=NAVY,
        max_tip_length_to_length_ratio=0.25
    )
    arrow1.set_z_index(0)

    arrow2 = Arrow(
        unified.get_right() + RIGHT * 0.2,
        output_tokens.get_left() + LEFT * 0.2,
        buff=0, stroke_width=4.5, color=NAVY,
        max_tip_length_to_length_ratio=0.25
    )
    arrow2.set_z_index(0)

    return {
        'input_tokens': input_tokens,
        'arrow1': arrow1,
        'unified': unified,
        'arrow2': arrow2,
        'output_tokens': output_tokens,
    }


class NativeMultiModalGeneration(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # ========== Title & Subtitle ==========
        title = Text(
            "Native Multi-Modal Generation",
            font_size=36, weight=BOLD, color=NAVY, font=FONT
        )
        title.move_to([0, 4.0, 0])

        subtitle = Text(
            "The current hype",
            font_size=20, color=GREY, slant=ITALIC, font=FONT
        )
        subtitle.next_to(title, DOWN, buff=0.18)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=1.0)
        self.wait(0.3)
        self.play(FadeIn(subtitle, shift=UP * 0.1), run_time=0.6)
        self.wait(0.3)

        # ========== FROM and TO headers ==========
        from_label = Text("FROM", font_size=22, weight=BOLD, color=GREY, font=FONT)
        from_label.move_to([-5.5, 2.5, 0])

        to_label = Text("TO", font_size=22, weight=BOLD, color=GREY, font=FONT)
        to_label.move_to([5.7, 2.5, 0])

        self.play(
            FadeIn(from_label, shift=RIGHT * 0.2),
            FadeIn(to_label, shift=LEFT * 0.2),
            run_time=0.7
        )
        self.wait(0.3)

        # ========== Left boxes (VLM and Diffusion) ==========
        vlm_box = build_left_box(
            "Vision Language Models",
            [("Text", TEXT_COLOR, TEXT_FILL), ("Image", IMAGE_COLOR, IMAGE_FILL)],
            [("Text", TEXT_COLOR, TEXT_FILL)],
            center_pos=[-5.5, 1.6, 0],
            box_width=3.6, box_height=1.2
        )

        diff_box = build_left_box(
            "Diffusion Models",
            [("Text", TEXT_COLOR, TEXT_FILL), ("Image", IMAGE_COLOR, IMAGE_FILL)],
            [("Image", IMAGE_COLOR, IMAGE_FILL)],
            center_pos=[-5.5, -1.6, 0],
            box_width=3.6, box_height=1.2
        )

        # Draw box outlines
        self.play(
            Create(vlm_box[0]),
            Create(diff_box[0]),
            run_time=0.7
        )
        self.wait(0.2)
        # Add titles
        self.play(
            FadeIn(vlm_box[1], shift=UP * 0.1),
            FadeIn(diff_box[1], shift=UP * 0.1),
            run_time=0.5
        )
        self.wait(0.2)
        # Add content
        self.play(
            LaggedStart(
                FadeIn(vlm_box[2], shift=UP * 0.1),
                FadeIn(diff_box[2], shift=UP * 0.1),
                lag_ratio=0.3
            ),
            run_time=0.8
        )
        self.wait(0.3)

        # ========== Right box (Interleaved) ==========
        right_box = build_right_box(
            center_pos=[5.7, -0.25, 0],
            box_width=3.4, box_height=1.5
        )

        self.play(Create(right_box[0]), run_time=0.6)
        self.wait(0.2)
        self.play(FadeIn(right_box[1], shift=UP * 0.1), run_time=0.4)
        self.wait(0.2)
        self.play(
            LaggedStart(
                FadeIn(right_box[2], shift=UP * 0.1),
                GrowFromPoint(right_box[3], right_box[3].get_start()),
                FadeIn(right_box[4], shift=UP * 0.1),
                lag_ratio=0.3
            ),
            run_time=1.0
        )
        self.wait(0.3)

        # ========== Transition label ==========
        transition_label = Text(
            "Evolving toward unified generation",
            font_size=20, color=PURPLE, slant=ITALIC, weight=BOLD, font=FONT
        )
        transition_label.move_to([0, 0.7, 0])
        transition_label.set_z_index(4)

        # ========== Center pipeline ==========
        center = build_center_pipeline()

        # Animate input tokens and transition label
        self.play(
            LaggedStart(*[FadeIn(tok, shift=UP * 0.1) for tok in center['input_tokens']], lag_ratio=0.3),
            FadeIn(transition_label, shift=DOWN * 0.1),
            run_time=0.8
        )
        self.wait(0.2)

        # Animate first arrow and unified block
        self.play(
            GrowFromPoint(center['arrow1'], center['arrow1'].get_start()),
            run_time=0.4
        )
        self.play(FadeIn(center['unified'], shift=UP * 0.1), run_time=0.5)
        self.wait(0.2)

        # Animate second arrow and output tokens
        self.play(
            GrowFromPoint(center['arrow2'], center['arrow2'].get_start()),
            run_time=0.4
        )
        self.play(
            LaggedStart(*[FadeIn(tok, shift=UP * 0.1) for tok in center['output_tokens']], lag_ratio=0.3),
            run_time=0.7
        )
        self.wait(0.4)

        # ========== Final emphasis on TO box ==========
        highlight = SurroundingRectangle(
            right_box[0], color=PURPLE, stroke_width=4, buff=0.15
        )
        highlight.set_z_index(5)
        self.play(Create(highlight), run_time=0.7)
        self.play(
            Circumscribe(right_box[1], color=PURPLE, buff=0.1, run_time=1.0)
        )
        self.wait(0.5)
