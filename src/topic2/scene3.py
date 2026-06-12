from manim import *


class Scene3(Scene):
    def construct(self):
        # SCENE 3A: SIMPLY SCALING UP?

        title_prefix = Tex(r"\textbf{Solution:}", font_size=42)
        title_rest = Tex(r"\textbf{Simply scaling up?}", font_size=42)
        title = VGroup(title_prefix, title_rest).arrange(RIGHT, buff=0.18).to_edge(UP)

        self.wait(1.0)
        self.play(Write(title_prefix), Write(title_rest), run_time=1.1)
        self.wait(4.0)

        # Divider
        divider = Line(UP * 2.6, DOWN * 2.6, color=GRAY_B, stroke_width=2)
        divider.move_to(ORIGIN + DOWN * 0.25)

        self.play(Create(divider), run_time=0.8)

        # LEFT HALF: TRADEOFF
        left_center = LEFT * 3.4 + DOWN * 0.15

        accuracy_rect = RoundedRectangle(
            corner_radius=0,
            width=2.0,
            height=0.9,
            color=GREEN_D,
            stroke_width=1.5,
            fill_opacity=0.22,
        )
        accuracy_text = Text("Accuracy", font_size=22, weight=BOLD)
        accuracy_arrow = MathTex(r"\uparrow", color=GREEN, font_size=40)
        accuracy_content = VGroup(accuracy_text, accuracy_arrow).arrange(RIGHT, buff=0.14)
        accuracy_box = VGroup(accuracy_rect, accuracy_content)
        accuracy_content.move_to(accuracy_rect.get_center())

        efficiency_rect = RoundedRectangle(
            corner_radius=0,
            width=2.0,
            height=0.9,
            color=RED_D,
            stroke_width=1.5,
            fill_opacity=0.22,
        )
        efficiency_text = Text("Efficiency", font_size=22, weight=BOLD)
        efficiency_arrow = MathTex(r"\downarrow", color=RED, font_size=40)
        efficiency_content = VGroup(efficiency_text, efficiency_arrow).arrange(RIGHT, buff=0.14)
        efficiency_box = VGroup(efficiency_rect, efficiency_content)
        efficiency_content.move_to(efficiency_rect.get_center())

        trade_arrow = DoubleArrow(
            LEFT * 0.75,
            RIGHT * 0.75,
            buff=0,
            color=YELLOW,
            stroke_width=4,
            tip_shape=StealthTip,
            tip_shape_start=StealthTip,
            max_tip_length_to_length_ratio=0.16,
        )
        trade_label = Text("Trade off", font_size=22, color=YELLOW)
        trade_group = VGroup(trade_label, trade_arrow).arrange(DOWN, buff=0.12)

        tradeoff_group = VGroup(accuracy_box, trade_group, efficiency_box).arrange(
            RIGHT,
            buff=0.45,
        )
        tradeoff_group.move_to(left_center)

        self.play(
            FadeIn(trade_arrow),
            FadeIn(trade_label),
            run_time=0.95,
        )
        self.play(
            LaggedStart(
                FadeIn(accuracy_box, shift=UP * 0.3),
                FadeIn(efficiency_box, shift=DOWN * 0.3),
                lag_ratio=0,
            ),
            run_time=0.9,
        )

        self.play(
            accuracy_arrow.animate.scale(1.15),
            efficiency_arrow.animate.scale(1.15),
            rate_func=there_and_back,
            run_time=0.8,
        )

        self.wait(4.0)

        # RIGHT HALF: PRECISE ACTION-VIDEO DATA IS HARD TO SCALE
        right_center = RIGHT * 3.35 + DOWN * 0.15

        data_box = RoundedRectangle(
            corner_radius=0,
            width=3.05,
            height=1.45,
            color=GREEN_D,
            fill_opacity=0.18,
            stroke_width=1.8,
        )

        data_text = Paragraph(
            "Precise",
            "Action-Video",
            "Data",
            alignment="center",
            font_size=24,
            color=WHITE,
            # no bold: natural weight
            line_spacing=0.8,
        )
        data_text.move_to(data_box.get_center())

        data_group = VGroup(data_box, data_text).move_to(right_center)

        self.play(FadeIn(data_group, shift=UP * 0.25), run_time=0.9)
        self.wait(0.3)

        # Arrows pointing outward from 4 corners
        arrow_style = {
            "color": RED,
            "stroke_width": 3.2,
            "tip_shape": StealthTip,
            "max_tip_length_to_length_ratio": 0.18,
        }

        corner_dirs = [
            UL,
            UR,
            DL,
            DR,
        ]

        outward_arrows = VGroup()
        for direction in corner_dirs:
            start = data_box.get_corner(direction) + direction * 0.08
            end = start + direction * 0.72
            arrow = Arrow(start=start, end=end, buff=0, **arrow_style)
            outward_arrows.add(arrow)

        self.play(
            LaggedStart(
                *[GrowArrow(arrow) for arrow in outward_arrows],
                lag_ratio=0,
            ),
            run_time=0.9,
        )

        # Larger dashed red box: hard to scale
        scale_box = DashedVMobject(
            RoundedRectangle(
                corner_radius=0.06,
                width=5.0,
                height=3.4,
                color=RED_D,
                stroke_width=3.6,
            ),
            num_dashes=42,
            dashed_ratio=0.55,
        )
        scale_box.move_to(data_box.get_center())
        scale_box.set_z_index(-1000)

        scale_label = Text(
            "Hard to scale!",
            font_size=24,
            color=WHITE,
        ).next_to(scale_box, DOWN, buff=0.2)

        # Entrance: start at the same visual size as `data_box`, then expand to final
        initial_scale = data_box.width / scale_box.width
        scale_box.scale(initial_scale)
        self.play(
            scale_box.animate.scale(1 / initial_scale).set_stroke(color=RED, width=3.6),
            Write(scale_label),
            run_time=1.0,
            rate_func=smooth,
        )

        self.play(
            scale_box.animate.set_stroke(color=RED, width=4),
            scale_label.animate.scale(1.08),
            rate_func=there_and_back,
            run_time=0.9,
        )

        self.wait(2)

        # Final: strike-through the title and show "Other idea?"
        strike_line = Line(
            title_rest.get_left() + DOWN * 0.02,
            title_rest.get_right() + DOWN * 0.02,
            color=RED,
            stroke_width=10,
        )
        strike_line.move_to(strike_line.get_center())

        other_text = Text("Other idea?", font_size=28, color=RED)
        other_text.next_to(strike_line, DOWN, buff=0.38)

        self.wait(1.0)
        self.play(Create(strike_line), run_time=0.6)
        self.play(FadeIn(other_text), run_time=0.6)
        self.wait(0.5)

        # Clean up Scene 3A
        self.play(
            FadeOut(title_prefix),
            FadeOut(title_rest),
            FadeOut(divider),
            FadeOut(accuracy_box),
            FadeOut(efficiency_box),
            FadeOut(trade_group),
            FadeOut(data_box),
            FadeOut(data_text),
            FadeOut(outward_arrows),
            FadeOut(scale_box),
            FadeOut(scale_label),
            FadeOut(strike_line),
            FadeOut(other_text),
            run_time=0.5,
        )

        # SCENE 3B: PHYSICS-GROUNDED WORLD MODELS

        title = Tex(
            r"\textbf{Beyond Scaling: Physics Grounding}",
            font_size=42,
        ).to_edge(UP)

        self.play(Write(title), run_time=1.1)
        self.wait(0.5)

        # Main boxes
        left_box = Rectangle(
            width=3.9,
            height=1.5,
            color=BLUE_D,
            fill_opacity=0.24,
            stroke_width=2.4,
        )
        left_text = Paragraph(
            "Pixel",
            "Generation",
            alignment="center",
            font_size=24,
            weight=BOLD,
            line_spacing=0.7,
        )
        left_group = VGroup(left_box, left_text)
        left_text.move_to(left_box.get_center())
        left_group.move_to(LEFT * 3.25 + UP * 0.45)

        right_box = Rectangle(
            width=3.9,
            height=1.5,
            color=GREEN_D,
            fill_opacity=0.24,
            stroke_width=2.4,
        )
        right_text = Paragraph(
            "Physical",
            "Representation",
            alignment="center",
            font_size=22,
            weight=BOLD,
            line_spacing=0.7,
        )
        right_group = VGroup(right_box, right_text)
        right_text.move_to(right_box.get_center())
        right_group.move_to(RIGHT * 3.25 + UP * 0.45)

        # Text-only labels below each box.
        left_label_1 = Text("Realism", font_size=20, color=WHITE)
        left_label_2 = Text("Diversity", font_size=20, color=WHITE)
        left_labels = VGroup(left_label_1, left_label_2).arrange(DOWN, buff=0.18)
        left_labels.next_to(left_group, DOWN, buff=0.35)

        right_label_1 = Text("Precise Action", font_size=20, color=WHITE)
        right_label_2 = Text("Efficient Rendering", font_size=20, color=WHITE)
        right_labels = VGroup(right_label_1, right_label_2).arrange(DOWN, buff=0.18)
        right_labels.next_to(right_group, DOWN, buff=0.35)

        self.play(
            FadeIn(left_group, shift=RIGHT * 0.25),
            FadeIn(right_group, shift=LEFT * 0.25),
            run_time=1.0,
        )

        self.wait(4.0)
        self.play(
            Write(left_labels[0]),
            Write(left_labels[1]),
            run_time=1.2,
        )
        self.wait(3.0)
        self.play(
            Write(right_labels[0]),
            Write(right_labels[1]),
            run_time=1.2,
        )

        self.wait(1.5)

        # Move two boxes toward center while the labels escape together.
        left_target = left_group.copy()
        left_target.move_to(ORIGIN + UP * left_group.get_center()[1])
        right_target = right_group.copy()
        right_target.move_to(ORIGIN + UP * right_group.get_center()[1])

        self.play(
            Transform(left_group, left_target),
            Transform(right_group, right_target),
            FadeOut(left_label_1, shift=DOWN * 0.12),
            FadeOut(left_label_2, shift=DOWN * 0.12),
            FadeOut(right_label_1, shift=DOWN * 0.12),
            FadeOut(right_label_2, shift=DOWN * 0.12),
            run_time=1.15,
            rate_func=smooth,
        )

        final_box = Rectangle(
            width=5.6,
            height=1.55,
            color=YELLOW,
            fill_opacity=0.18,
            stroke_width=2.8,
        )
        final_text = Paragraph(
            "Physics-Grounded",
            "World Models",
            alignment="center",
            font_size=30,
            color=WHITE,
            weight=BOLD,
            line_spacing=0.85,
        )
        final_text.move_to(final_box.get_center())
        final_group = VGroup(final_box, final_text).move_to(ORIGIN + UP * 0.45)

        glow_core = Rectangle(
            width=5.3,
            height=1.45,
            color=YELLOW,
            fill_opacity=0.06,
            stroke_width=0,
        ).move_to(final_group)
        glow_ring = Rectangle(
            width=5.65,
            height=1.75,
            color=YELLOW,
            fill_opacity=0,
            stroke_width=8,
        ).set_stroke(YELLOW, width=8, opacity=0.35).move_to(final_group)
        glow_group = VGroup(glow_core, glow_ring)

        self.play(
            FadeOut(left_group),
            FadeOut(right_group),
            FadeIn(glow_group, scale=0.92),
            FadeIn(final_group, scale=1.02),
            run_time=0.65,
            rate_func=smooth,
        )
        self.play(
            glow_ring.animate.scale(1.08).set_stroke(opacity=0.05),
            glow_core.animate.set_fill(opacity=0.12),
            FadeOut(glow_group, scale=1.05),
            run_time=0.35,
            rate_func=smooth,
        )

        self.wait(6.0)

        # SCENE 3C: TABLE OF CONTENTS
        # Transform final_text (2 lines) to title (1 line) and move up
        title_target = Tex(
            r"\textbf{Physics-Grounded World Models}",
            font_size=42,
        ).to_edge(UP)

        self.play(
            ReplacementTransform(final_text, title_target),
            FadeOut(final_box),
            FadeOut(title),
            run_time=1.0,
            rate_func=smooth,
        )
        self.wait(0.3)

        # Table of Contents with numbered circles
        circle_1 = Circle(radius=0.35, color=BLUE_D, stroke_width=3)
        text_1 = Tex("1", font_size=36, color=WHITE)
        text_1.move_to(circle_1.get_center())
        group_1 = VGroup(circle_1, text_1)

        circle_2 = Circle(radius=0.35, color=GREEN_D, stroke_width=3)
        text_2 = Tex("2", font_size=36, color=WHITE)
        text_2.move_to(circle_2.get_center())
        group_2 = VGroup(circle_2, text_2)

        circle_3 = Circle(radius=0.35, color=RED_D, stroke_width=3)
        text_3 = Tex("3", font_size=36, color=WHITE)
        text_3.move_to(circle_3.get_center())
        group_3 = VGroup(circle_3, text_3)

        # Arrange circles horizontally (wider spacing)
        circles_group = VGroup(group_1, group_2, group_3).arrange(RIGHT, buff=3.0)
        circles_group.move_to(ORIGIN + UP * 0.8)

        # Connecting lines between circles (white)
        line_1_2 = Line(
            group_1.get_center() + RIGHT * 0.4,
            group_2.get_center() + LEFT * 0.4,
            color=WHITE,
            stroke_width=2.5,
        )

        line_2_3 = Line(
            group_2.get_center() + RIGHT * 0.4,
            group_3.get_center() + LEFT * 0.4,
            color=WHITE,
            stroke_width=2.5,
        )

        # Labels below each circle
        label_1 = Text("Generation", font_size=26, color=WHITE)
        label_1.next_to(group_1, DOWN, buff=0.35)

        label_2 = Text("Interaction", font_size=26, color=WHITE)
        label_2.next_to(group_2, DOWN, buff=0.35)

        label_3 = Text("Evaluation", font_size=26, color=WHITE)
        label_3.next_to(group_3, DOWN, buff=0.35)

        # Animate appearance: step-by-step
        # Step 1: Circle 1 and label
        self.play(
            FadeIn(group_1),
            FadeIn(label_1),
            run_time=0.6,
        )

        # Step 2: Line from circle 1 to circle 2
        self.play(
            Create(line_1_2),
            run_time=0.5,
        )

        # Step 3: Circle 2 and label
        self.play(
            FadeIn(group_2),
            FadeIn(label_2),
            run_time=0.6,
        )

        # Step 4: Line from circle 2 to circle 3
        self.play(
            Create(line_2_3),
            run_time=0.5,
        )

        # Step 5: Circle 3 and label
        self.play(
            FadeIn(group_3),
            FadeIn(label_3),
            run_time=0.6,
        )

        self.wait(7)

        # TRANSITION: "Generation" zooms and becomes bold, "1" becomes bold and black, circle 1 fills with blue (all at same time)
        self.play(
            label_1.animate.scale(1.4).set_weight(BOLD),
            text_1.animate.scale(1.2).set_weight(BOLD).set_color(BLACK),
            circle_1.animate.set_fill(BLUE_D, opacity=1),
            circle_2.animate.set_stroke(opacity=0.3),
            text_2.animate.set_opacity(0.3),
            circle_3.animate.set_stroke(opacity=0.3),
            text_3.animate.set_opacity(0.3),
            label_2.animate.set_opacity(0.3),
            label_3.animate.set_opacity(0.3),
            line_1_2.animate.set_opacity(0.3),
            line_2_3.animate.set_opacity(0.3),
            run_time=1.2,
        )

        self.wait(0.5)
