"""
SCENE 11 — Internalizing Physics
Time: 32:30–36:00

Three mini-scenes demonstrating emergent physics understanding:
A) Parallax  B) Object Persistence  C) Deformable Physics
"""

from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from topic1.shared_styles import *


class Scene11Physics(Scene):
    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self):
        scene_title_sequence(
            self,
            "Internalizing Physics",
            "Signs of Deeper Understanding",
        )

        # ══════════════════════════════════════════════
        # MINI-SCENE A: Parallax
        # ══════════════════════════════════════════════
        section_a = subtitle_text("A. Parallax", font_size=26)
        section_a.to_edge(UP, buff=0.4)
        self.play(FadeIn(section_a, shift=DOWN * 0.2), run_time=0.5)

        # Create layered scene — background (far), midground, foreground (near)
        bg_layer = VGroup()
        for i in range(5):
            mountain = Triangle(
                color="#334466", fill_opacity=0.3, stroke_width=0,
            ).scale(0.8).shift(RIGHT * (i * 2 - 4) + DOWN * 0.5)
            bg_layer.add(mountain)
        bg_label = label_text("Background", font_size=12, color="#334466")
        bg_label.next_to(bg_layer, UP, buff=0.1)

        mid_layer = VGroup()
        for i in range(4):
            tree = VGroup(
                Circle(radius=0.2, color=ACTION_COLOR, fill_opacity=0.4, stroke_width=0),
                Rectangle(width=0.06, height=0.25, color="#8B6914", fill_opacity=0.5, stroke_width=0).shift(DOWN * 0.25),
            ).shift(RIGHT * (i * 2.5 - 3.5) + DOWN * 0.3)
            mid_layer.add(tree)

        fg_layer = VGroup()
        for i in range(3):
            rock = Circle(
                radius=0.25, color=WORLD_COLOR, fill_opacity=0.5, stroke_width=1,
            ).shift(RIGHT * (i * 3 - 3) + DOWN * 1.5)
            fg_layer.add(rock)
        fg_label = label_text("Foreground", font_size=12, color=WORLD_COLOR)
        fg_label.next_to(fg_layer, DOWN, buff=0.1)

        scene_layers = VGroup(bg_layer, mid_layer, fg_layer)
        self.play(
            FadeIn(bg_layer), FadeIn(mid_layer), FadeIn(fg_layer),
            FadeIn(bg_label), FadeIn(fg_label),
            run_time=0.8,
        )

        # Camera pans right — foreground moves faster than background
        narr = body_text(
            "Foreground moves faster than background",
            font_size=18, color=TEXT_DIM,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(narr), run_time=0.3)

        # Simulate parallax: fg moves more, bg moves less
        self.play(
            fg_layer.animate.shift(LEFT * 2.5),
            fg_label.animate.shift(LEFT * 2.5),
            mid_layer.animate.shift(LEFT * 1.5),
            bg_layer.animate.shift(LEFT * 0.7),
            bg_label.animate.shift(LEFT * 0.7),
            run_time=1.5,
            rate_func=linear,
        )
        self.wait(0.5)

        # Move back
        self.play(
            fg_layer.animate.shift(RIGHT * 2.5),
            fg_label.animate.shift(RIGHT * 2.5),
            mid_layer.animate.shift(RIGHT * 1.5),
            bg_layer.animate.shift(RIGHT * 0.7),
            bg_label.animate.shift(RIGHT * 0.7),
            run_time=1.0,
            rate_func=linear,
        )
        self.wait(0.3)

        self.play(
            FadeOut(VGroup(bg_layer, mid_layer, fg_layer, bg_label, fg_label, narr, section_a)),
            run_time=0.5,
        )

        # ══════════════════════════════════════════════
        # MINI-SCENE B: Object Persistence
        # ══════════════════════════════════════════════
        section_b = subtitle_text("B. Object Persistence", font_size=26)
        section_b.to_edge(UP, buff=0.4)
        self.play(FadeIn(section_b, shift=DOWN * 0.2), run_time=0.5)

        # Setup: a room with an object
        room = RoundedRectangle(
            width=8, height=4,
            corner_radius=0.3,
            color=WORLD_COLOR, fill_opacity=0.05, stroke_width=1.5,
        )

        # Object (a treasure chest)
        obj = VGroup(
            RoundedRectangle(
                width=0.8, height=0.5,
                corner_radius=0.08,
                color=HIGHLIGHT_COLOR, fill_opacity=0.4, stroke_width=2,
            ),
            Text("★", font_size=20, color=HIGHLIGHT_COLOR),
        )
        obj[1].move_to(obj[0])
        obj.move_to(RIGHT * 2 + UP * 0.5)

        obj_label = label_text("Object", font_size=14, color=HIGHLIGHT_COLOR)
        obj_label.next_to(obj, UP, buff=0.15)

        # Camera view indicator
        cam_view = DashedVMobject(
            Arc(radius=3, start_angle=-PI / 6, angle=PI / 3, arc_center=LEFT * 3),
            num_dashes=15,
        )
        cam_view.set_color(AGENT_COLOR)
        cam_icon = Text("📷", font_size=24).move_to(LEFT * 3)

        self.play(
            FadeIn(room), FadeIn(obj), FadeIn(obj_label),
            FadeIn(cam_view), FadeIn(cam_icon),
            run_time=0.8,
        )

        narr_b = body_text(
            "Camera turns away... object persists",
            font_size=18, color=TEXT_DIM,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(narr_b), run_time=0.3)

        # Camera rotates away — object fades (leaving view)
        self.play(
            Rotate(cam_view, angle=PI, about_point=LEFT * 3),
            obj.animate.set_opacity(0.15),
            obj_label.animate.set_opacity(0.15),
            run_time=1.2,
        )

        hidden_label = label_text(
            "Out of view", font_size=14, color=TEXT_DIM,
        ).next_to(obj, DOWN, buff=0.15)
        self.play(FadeIn(hidden_label), run_time=0.3)
        self.wait(0.5)

        # Camera rotates back — object is still there!
        self.play(
            Rotate(cam_view, angle=-PI, about_point=LEFT * 3),
            obj.animate.set_opacity(1.0),
            obj_label.animate.set_opacity(1.0),
            FadeOut(hidden_label),
            run_time=1.2,
        )

        # Checkmark
        check = Text("✓", font_size=36, color=ACTION_COLOR, weight=BOLD)
        check.next_to(obj, RIGHT, buff=0.3)
        still_there = label_text("Still there!", font_size=14, color=ACTION_COLOR)
        still_there.next_to(check, RIGHT, buff=0.1)

        self.play(FadeIn(check, scale=2), FadeIn(still_there), run_time=0.5)
        self.wait(0.8)

        self.play(
            FadeOut(VGroup(room, obj, obj_label, cam_view, cam_icon,
                           check, still_there, narr_b, section_b)),
            run_time=0.5,
        )

        # ══════════════════════════════════════════════
        # MINI-SCENE C: Deformable Physics
        # ══════════════════════════════════════════════
        section_c = subtitle_text("C. Deformable Physics", font_size=26)
        section_c.to_edge(UP, buff=0.4)
        self.play(FadeIn(section_c, shift=DOWN * 0.2), run_time=0.5)

        # Robot arm (simple representation)
        arm_base = Rectangle(
            width=0.3, height=1.5,
            color=AGENT_COLOR, fill_opacity=0.4, stroke_width=2,
        ).move_to(LEFT * 2 + UP * 0.5)

        arm_joint = Dot(
            arm_base.get_bottom(), radius=0.1,
            color=AGENT_COLOR, fill_opacity=0.8,
        )

        arm_segment = Rectangle(
            width=0.2, height=1.2,
            color=AGENT_COLOR, fill_opacity=0.3, stroke_width=1.5,
        )
        arm_segment.next_to(arm_joint, RIGHT, buff=0)
        arm_segment.rotate(-PI / 6, about_point=arm_joint.get_center())

        arm_tip = Dot(
            arm_segment.get_bottom(), radius=0.08,
            color=HIGHLIGHT_COLOR, fill_opacity=0.9,
        )

        robot_arm = VGroup(arm_base, arm_joint, arm_segment, arm_tip)
        arm_label = label_text("Robot Hand", font_size=14, color=AGENT_COLOR)
        arm_label.next_to(arm_base, UP, buff=0.15)

        # Chip bag (deformable object)
        bag_points = [
            RIGHT * 1 + UP * 0.5,
            RIGHT * 1.8 + UP * 0.6,
            RIGHT * 2.2 + UP * 0.3,
            RIGHT * 2 + DOWN * 0.3,
            RIGHT * 1.2 + DOWN * 0.4,
            RIGHT * 0.8 + DOWN * 0.1,
        ]
        bag = Polygon(
            *bag_points,
            color=WORLD_COLOR, fill_opacity=0.3, stroke_width=2,
        )
        bag_label = label_text("Chip Bag", font_size=14, color=WORLD_COLOR)
        bag_label.next_to(bag, DOWN, buff=0.3)

        self.play(
            FadeIn(robot_arm), FadeIn(arm_label),
            FadeIn(bag), FadeIn(bag_label),
            run_time=0.8,
        )

        narr_c = body_text(
            "Soft objects deform under pressure",
            font_size=18, color=TEXT_DIM,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(narr_c), run_time=0.3)

        # Robot arm presses down — bag deforms
        # Deformed bag shape
        deformed_points = [
            RIGHT * 1 + UP * 0.3,       # compressed top-left
            RIGHT * 1.8 + UP * 0.25,    # compressed top
            RIGHT * 2.4 + UP * 0.2,     # pushed right
            RIGHT * 2.3 + DOWN * 0.4,   # stretched bottom-right
            RIGHT * 1.2 + DOWN * 0.5,   # stretched bottom
            RIGHT * 0.7 + DOWN * 0.15,  # pushed left-bottom
        ]
        deformed_bag = Polygon(
            *deformed_points,
            color=WORLD_COLOR, fill_opacity=0.3, stroke_width=2,
        )

        # Move arm toward bag and deform
        self.play(
            robot_arm.animate.shift(RIGHT * 0.8 + DOWN * 0.3),
            arm_label.animate.shift(RIGHT * 0.8 + DOWN * 0.3),
            Transform(bag, deformed_bag),
            run_time=1.2,
        )

        pressure_indicator = Text(
            "↓ pressure", font_size=16, color=GENIE_COLOR,
        ).next_to(robot_arm, RIGHT, buff=0.2)
        self.play(FadeIn(pressure_indicator), run_time=0.3)
        self.wait(1)

        # Key takeaway
        takeaway = Text(
            "Motion produces consequences",
            font_size=24, color=HIGHLIGHT_COLOR, weight=BOLD,
        )
        takeaway_bg = Rectangle(
            width=takeaway.width + 0.6,
            height=takeaway.height + 0.4,
            color=BG_COLOR, fill_opacity=0.9, stroke_width=0,
        ).move_to(takeaway)
        takeaway_group = VGroup(takeaway_bg, takeaway).move_to(ORIGIN)

        self.play(
            FadeOut(VGroup(
                robot_arm, arm_label, bag, bag_label,
                pressure_indicator, narr_c, section_c,
            )),
            run_time=0.4,
        )
        self.play(FadeIn(takeaway_group), run_time=0.8)
        self.wait(1.5)

        self.play(FadeOut(takeaway_group), run_time=0.8)
