from manim import *
from pathlib import Path
import random

from video_mobject import VideoMobject, create_video_stage_frame, freeze_video_frame


def fit_video_preserving_aspect(video, frame, padding=0.15):
    video.move_to(frame.get_center())
    scale_factor = min(
        (frame.width - padding) / video.width,
        (frame.height - padding) / video.height,
    )
    video.scale(scale_factor)
    video.pause()


def fit_mobject_to_frame(mobject, frame, padding=0.12):
    scale_factor = min(
        (frame.width - padding) / mobject.width,
        (frame.height - padding) / mobject.height,
    )
    mobject.scale(scale_factor)
    mobject.move_to(frame.get_center())


def create_camera_icon(color=WHITE):
    lens_color = BLACK if color == WHITE else WHITE
    body = RoundedRectangle(
        corner_radius=0.05,
        width=0.42,
        height=0.27,
        color=color,
        stroke_width=0,
        fill_color=color,
        fill_opacity=0.88,
    )
    lens = Circle(
        radius=0.065,
        color=lens_color,
        stroke_width=2.6,
        fill_opacity=0,
    ).move_to(body.get_center())
    flash = Dot(
        radius=0.022,
        color=lens_color,
    ).move_to(body.get_center() + RIGHT * 0.14 + UP * 0.075)
    top = Rectangle(
        width=0.16,
        height=0.06,
        color=color,
        stroke_width=0,
        fill_color=color,
        fill_opacity=0.88,
    ).next_to(body, UP, buff=0)
    return VGroup(body, lens, flash, top)


def create_camera_view_group(
    camera_pos,
    view_end_1,
    view_end_2,
    camera_color=BLACK,
    camera_scale=1,
    yaw_angle=0 * DEGREES,
    pitch_angle=0 * DEGREES,
    roll_angle=0 * DEGREES,
    line_color=BLACK,
    line_opacity=0.62,
    line_stroke_width=2,
    cone_opacity=0.08,
):
    camera_icon = create_camera_icon(color=camera_color)
    camera_icon.scale(camera_scale)
    camera_icon.move_to(camera_pos)
    camera_icon.rotate(
        pitch_angle,
        axis=RIGHT,
        about_point=camera_icon.get_center(),
    )
    camera_icon.rotate(
        yaw_angle,
        axis=UP,
        about_point=camera_icon.get_center(),
    )
    camera_icon.rotate(
        roll_angle,
        axis=OUT,
        about_point=camera_icon.get_center(),
    )
    camera_icon.set_z_index(4)

    view_line_1 = DashedLine(
        camera_icon.get_center(),
        view_end_1,
        color=line_color,
        stroke_width=line_stroke_width,
    )
    view_line_2 = DashedLine(
        camera_icon.get_center(),
        view_end_2,
        color=line_color,
        stroke_width=line_stroke_width,
    )
    view_line_1.set_opacity(line_opacity)
    view_line_2.set_opacity(line_opacity)

    view_cone = Polygon(
        camera_icon.get_center(),
        view_end_1,
        view_end_2,
        color=line_color,
        fill_color=line_color,
        fill_opacity=cone_opacity,
        stroke_opacity=0,
    )

    view_cone.set_z_index(2)
    view_line_1.set_z_index(3)
    view_line_2.set_z_index(3)

    return VGroup(camera_icon, view_cone, view_line_1, view_line_2)


def create_numbered_bullet(number, text, color=YELLOW):
    circle = Circle(radius=0.17, color=color, stroke_width=3)
    number_text = Text(str(number), font_size=20, color=WHITE).move_to(circle)
    label = Text(text, font_size=25, color=WHITE).next_to(circle, RIGHT, buff=0.22)
    return VGroup(circle, number_text, label)


def create_fontawesome_hourglass_icon(color=RED):
    template = TexTemplate()
    template.add_to_preamble(r"\usepackage{fontawesome5}")
    return Tex(
        r"\faHourglassHalf",
        tex_template=template,
        font_size=34,
        color=color,
    )


def create_mixed_math_label(prefix, math_text, suffix, font_size=25, color=WHITE):
    prefix_mob = Text(prefix.rstrip(), font_size=font_size, color=color)
    math_mob = MathTex(math_text, font_size=font_size + 8, color=color)
    suffix_mob = Text(suffix, font_size=font_size, color=color)

    math_mob.next_to(prefix_mob, RIGHT, buff=0.075)
    suffix_mob.next_to(math_mob, RIGHT, buff=0.01)

    prefix_mob.align_to(suffix_mob, UP)
    math_mob.set_y(suffix_mob.get_center()[1])
    label = VGroup(prefix_mob, math_mob, suffix_mob)
    return label


def create_image_panel(path, label, width):
    image = ImageMobject(str(path))
    image.set_width(width)
    image.set_z_index(0)
    label_mob = Text(label, font_size=22, color=WHITE).next_to(image, DOWN, buff=0.22)
    return Group(image, label_mob)


def create_image_grid(
    paths,
    rows=3,
    cols=3,
    target_width=None,
    target_height=None,
    gap=0.08,
):
    x_gap = gap
    y_gap = gap
    cell_width = (
        (target_width - (cols - 1) * x_gap) / cols
        if target_width is not None
        else 1.08
    )
    cell_height = (
        (target_height - (rows - 1) * y_gap) / rows
        if target_height is not None
        else 0.72
    )
    grid = Group()

    for index, path in enumerate(paths):
        row = index // cols
        col = index % cols
        image = ImageMobject(str(path))
        image.set_width(cell_width)
        if image.height > cell_height:
            image.set_height(cell_height)
        image.move_to(
            RIGHT * ((col - (cols - 1) / 2) * (cell_width + x_gap))
            + DOWN * ((row - (rows - 1) / 2) * (cell_height + y_gap))
        )
        grid.add(image)

    return grid


class Scene5(Scene):
    def construct(self):
        title = Tex(
            r"\textbf{3D World Generation via Grounding}",
            font_size=42,
        ).to_edge(UP)

        self.play(Write(title), run_time=1.0)
        self.wait(1.0)

        frame_scale = 0.9
        video_y = -0.28

        wonder_frame = create_video_stage_frame().scale(frame_scale)
        wonder_frame.move_to(LEFT * 3.57 + UP * video_y)

        realm_frame = create_video_stage_frame().scale(frame_scale)
        realm_frame.move_to(RIGHT * 3.57 + UP * video_y)

        wonder_video_path = Path("assets/videos/wonderjourney.mp4")
        realm_video_path = Path("assets/videos/realmdreamer.mp4")

        wonder_video = VideoMobject(wonder_video_path, loop=True)
        realm_video = VideoMobject(realm_video_path, loop=True)
        wonder_video.set_time_source(lambda: self.time * 0.5)
        realm_video.set_time_source(lambda: self.time * 0.5)

        fit_video_preserving_aspect(wonder_video, wonder_frame, padding=0.15)
        fit_video_preserving_aspect(realm_video, realm_frame, padding=0.15)

        wonder_label = Tex(
            r"\textbf{WonderJourney} (Yu \textit{et al.}, $2024$)",
            font_size=28,
        ).next_to(wonder_frame, DOWN, buff=0.28)
        realm_label = Tex(
            r"\textbf{RealmDreamer} (Shriram \textit{et al.}, $2025$)",
            font_size=28,
        ).next_to(realm_frame, DOWN, buff=0.28)

        self.play(
            FadeIn(wonder_frame, shift=LEFT * 0.2),
            FadeIn(realm_frame, shift=RIGHT * 0.2),
            run_time=0.7,
        )
        self.play(
            FadeIn(wonder_video),
            FadeIn(realm_video),
            Write(wonder_label),
            Write(realm_label),
            run_time=0.9,
        )

        wonder_video.play()
        realm_video.play()
        self.wait(6)

        wonder_video.pause()
        realm_video.pause()
        self.wait(5)

        wonder_still = freeze_video_frame(wonder_video)
        realm_still = freeze_video_frame(realm_video)
        self.add(wonder_still, realm_still)
        self.remove(wonder_video, realm_video)
        wonder_video.close()
        realm_video.close()

        self.play(
            FadeOut(title),
            FadeOut(wonder_frame),
            FadeOut(realm_frame),
            FadeOut(wonder_still),
            FadeOut(realm_still),
            FadeOut(wonder_label),
            FadeOut(realm_label),
            run_time=0.8,
        )
        self.wait(1.0)

        # SCENE 5B: SIMPLE GROUNDING BY UNPROJECTION

        title_5b = Tex(
            r"\textbf{Simple Grounding by }",
            r"\textbf{Unprojection}",
            font_size=42,
        ).to_edge(UP)
        title_5b[1].set_color(YELLOW)

        self.play(Write(title_5b), run_time=1.0)

        panel_width = 4.9
        panel_height = 3.25
        panel_y = 0.25
        panel_x = 4.7
        rgb_center = LEFT * panel_x + UP * panel_y
        depth_center = UP * panel_y
        cloud_center = RIGHT * panel_x + UP * panel_y

        rgb_frame = Rectangle(width=panel_width, height=panel_height).move_to(rgb_center)
        depth_frame = Rectangle(width=panel_width, height=panel_height).move_to(depth_center)
        cloud_frame = Rectangle(width=panel_width, height=panel_height).move_to(cloud_center)

        village_path = Path("assets/images/village.png")
        depth_path = Path("assets/images/village-depth.png")
        cloud_path = Path("assets/images/village-cloud.png")

        rgb_image = ImageMobject(str(village_path))
        depth_image_target = ImageMobject(str(depth_path))
        fit_mobject_to_frame(rgb_image, rgb_frame)
        fit_mobject_to_frame(depth_image_target, depth_frame)
        rgb_image.set_z_index(0)
        depth_image_target.set_z_index(-1)

        rgb_label = Text("Current Scene Image", font_size=22).next_to(
            rgb_frame,
            DOWN,
            buff=0.24,
        )
        rgb_label.set_z_index(3)
        depth_label = Text("Estimated Depth", font_size=22).next_to(
            depth_frame,
            DOWN,
            buff=0.24,
        )
        depth_label.set_z_index(3)
        cloud_label = Text("Point Cloud", font_size=22).next_to(
            cloud_frame,
            DOWN,
            buff=0.24,
        )
        cloud_label.set_z_index(3)

        self.play(FadeIn(rgb_image, shift=UP * 0.15), run_time=1.2)
        self.play(Write(rgb_label), run_time=1.0)
        self.wait(2.0)

        arrow_style = {
            "color": YELLOW,
            "stroke_width": 10,
            "tip_shape": StealthTip,
            "max_tip_length_to_length_ratio": 0.15,
        }
        rgb_to_depth_arrow = Arrow(
            rgb_center + RIGHT * 1.75,
            depth_center + LEFT * 1.75,
            buff=0,
            **arrow_style,
        )
        rgb_to_depth_arrow.set_width(0.9)
        rgb_to_depth_arrow.set_z_index(2)
        depth_image = depth_image_target.copy()
        depth_image.match_width(rgb_image)
        depth_image.match_height(rgb_image)
        depth_image.move_to(rgb_image.get_center())
        depth_image.set_opacity(0)
        depth_image.set_z_index(-1)
        self.play(
            GrowArrow(rgb_to_depth_arrow),
            Transform(depth_image, depth_image_target),
            run_time=1.0,
        )
        self.play(Write(depth_label), run_time=1.0)
        self.wait(1.0)

        depth_to_cloud_arrow = Arrow(
            depth_center + RIGHT * 1.75,
            cloud_center + LEFT * 1.75,
            buff=0,
            **arrow_style,
        )
        depth_to_cloud_arrow.set_width(0.9)
        depth_to_cloud_arrow.set_z_index(2)

        random.seed(7)
        cloud_bg_target = ImageMobject(str(cloud_path))
        fit_mobject_to_frame(cloud_bg_target, cloud_frame, padding=0.18)
        cloud_bg_target.set_z_index(-2)
        cloud_bg = cloud_bg_target.copy()
        cloud_bg.match_width(depth_image)
        cloud_bg.match_height(depth_image)
        cloud_bg.move_to(depth_image.get_center())
        cloud_bg.set_opacity(0)
        cloud_bg.set_z_index(-2)

        parallax_layers = []
        dot_colors = [WHITE, BLUE_B, TEAL_A, GRAY_A]
        for layer_idx, layer_shift in enumerate([-0.18, 0.0, 0.2]):
            dots = VGroup()
            for _ in range(85):
                x = random.uniform(-panel_width * 0.34, panel_width * 0.34)
                y = random.uniform(-panel_height / 2 + 0.25, panel_height / 2 - 0.25)
                dot = Dot(
                    radius=random.uniform(0.008, 0.04),
                    color=random.choice(dot_colors),
                )
                dot.set_opacity(random.uniform(0.55, 0.95))
                dot.set_z_index(1)
                dot.move_to(cloud_frame.get_center() + RIGHT * (x + layer_shift) + UP * y)
                dots.add(dot)
            parallax_layers.append(dots)

        camera_icon = create_camera_icon()
        camera_icon.scale(0.8)
        camera_icon.move_to(cloud_frame.get_corner(DL) + RIGHT * 0.38 + UP * 0.33)
        camera_icon.set_z_index(4)
        point_cloud_group = Group(*parallax_layers)
        camera_start = camera_icon.get_center()
        point_cloud_right_edge = point_cloud_group.get_right()[0] - 0.18
        camera_target = camera_start + RIGHT * (point_cloud_right_edge - camera_start[0])

        self.play(
            GrowArrow(depth_to_cloud_arrow),
            Transform(cloud_bg, cloud_bg_target),
            run_time=1.0,
        )

        self.play(Write(cloud_label), run_time=1.0)

        self.wait(6.5)

        self.play(
            cloud_bg.animate.set_opacity(0.2),
            FadeIn(point_cloud_group, shift=RIGHT * 0.1),
            FadeIn(camera_icon),
            run_time=1.0,
        )

        layer_anims = []
        for idx, layer in enumerate(parallax_layers):
            layer_anims.append(layer.animate.shift(LEFT * (0.3 + idx * 0.22)))

        self.play(
            camera_icon.animate.move_to(camera_target),
            *layer_anims,
            run_time=1.6,
            rate_func=smooth,
        )
        self.play(
            camera_icon.animate.move_to(camera_start),
            *[layer.animate.shift(RIGHT * (0.14 + idx * 0.1)) for idx, layer in enumerate(parallax_layers)],
            run_time=1.2,
            rate_func=smooth,
        )

        self.wait(2.5)

        # SCENE 5C: CHALLENGE - TOO SLOW TO BE INTERACTIVE

        self.play(FadeOut(*self.mobjects), run_time=0.8)
        self.clear()

        title_5c = Tex(
            r"\textbf{Challenge: Too }",
            r"\textbf{Slow}",
            r"\textbf{ To Be Interactive}",
            font_size=40,
        ).to_edge(UP)
        title_5c[1].set_color(YELLOW)

        self.play(Write(title_5c), run_time=1.0)

        bullet_1 = create_numbered_bullet(
            1,
            "Needs to generate many views",
            color=YELLOW,
        )
        bullet_1.to_edge(LEFT, buff=0.65).shift(UP * 2.15)

        self.play(
            FadeIn(VGroup(bullet_1[0], bullet_1[1]), scale=0.7),
            Write(bullet_1[2]),
            run_time=0.8,
        )

        campus_panel = create_image_panel(
            Path("assets/images/campus-0.png"),
            "Input Image",
            width=3.9,
        )
        campus_panel.move_to(LEFT * 4.2 + DOWN * 1.45)
        campus_img = campus_panel[0]
        campus_label = campus_panel[1]
        campus_label.next_to(campus_img, DOWN, buff=0.22)

        dim_overlay = Rectangle(
            width=campus_img.width,
            height=campus_img.height,
            stroke_opacity=0,
            fill_color=WHITE,
            fill_opacity=0.5,
        ).move_to(campus_img)
        dim_overlay.set_z_index(1)

        self.play(FadeIn(campus_panel, shift=UP * 0.12), run_time=0.8)
        self.play(FadeIn(dim_overlay), run_time=0.45)

        # Adjust camera_pos, yaw, and pitch manually
        camera_pos = campus_img.get_center() + LEFT * 1.25 + UP * 0.6
        yaw_angle = 45 * DEGREES
        pitch_angle = -22 * DEGREES
        roll_angle = -15 * DEGREES

        # Adjust view_end_1 and view_end_2 manually
        view_end_1 = campus_img.get_corner(UR) + LEFT * 2.8 + DOWN * 0.08
        view_end_2 = campus_img.get_corner(UR) + LEFT * 1.9 + DOWN * 0.35

        # Camera view group 1 and 2
        camera_view_group_1 = create_camera_view_group(
            camera_pos=camera_pos,
            view_end_1=view_end_1,
            view_end_2=view_end_2,
            camera_color=BLACK,
            yaw_angle=yaw_angle,
            pitch_angle=pitch_angle,
            roll_angle=roll_angle,
        )
        camera_pos_mirror = camera_pos + RIGHT * 1.25
        view_end_1_mirror = camera_pos_mirror + LEFT * (
            view_end_1[0] - camera_pos[0]
        ) + UP * (
            view_end_1[1] - camera_pos[1]
        )
        view_end_2_mirror = camera_pos_mirror + LEFT * (
            view_end_2[0] - camera_pos[0]
        ) + UP * (
            view_end_2[1] - camera_pos[1]
        )
        camera_view_group_2 = create_camera_view_group(
            camera_pos=camera_pos_mirror,
            view_end_1=view_end_1_mirror,
            view_end_2=view_end_2_mirror,
            camera_color=BLACK,
            yaw_angle=-yaw_angle,
            pitch_angle=pitch_angle,
            roll_angle=-roll_angle,
        )

        self.play(
            FadeIn(camera_view_group_1[0], scale=0.6),
            FadeIn(camera_view_group_2[0], scale=0.6),
            run_time=0.6,
        )

        self.play(
            FadeIn(camera_view_group_1[1]),
            FadeIn(camera_view_group_2[1]),
            Create(camera_view_group_1[2]),
            Create(camera_view_group_1[3]),
            Create(camera_view_group_2[2]),
            Create(camera_view_group_2[3]),
            run_time=0.9,
        )

        behind_arrow_1 = CurvedArrow(
            start_point=campus_img.get_center() + UP * 1.4 + LEFT * 0.6,
            end_point=campus_img.get_top() + RIGHT * 0.35 + UP * 0.7,
            angle=-TAU / 3,
            color=PURE_YELLOW,
            stroke_width=3,
            tip_shape=StealthTip,
        )
        behind_arrow_1.pop_tips()
        behind_arrow_1.add_tip(
            tip_shape=StealthTip,
            tip_length=0.14,
            tip_width=0.14,
        )
        behind_arrow_1.set_z_index(5)
        behind_text_1 = Text(
            "What's behind?",
            font_size=22,
            color=YELLOW,
        ).next_to(behind_arrow_1.get_end(), RIGHT, buff=0.18)
        behind_text_1.set_z_index(5)

        self.play(Create(behind_arrow_1), run_time=0.8)
        self.play(Write(behind_text_1), run_time=0.6)

        # Camera view group 3
        camera_view_group_3 = create_camera_view_group(
            camera_pos=campus_img.get_center() + RIGHT * 0 + DOWN * 0,
            view_end_1=campus_img.get_center() + RIGHT * 1.8 + UP * 0.9,
            view_end_2=campus_img.get_center() + RIGHT * 1.8 + UP * 0.1,
            camera_color=BLACK,
            yaw_angle=45 * DEGREES,
            pitch_angle=-22 * DEGREES,
            roll_angle=-15 * DEGREES
        )

        self.play(
            FadeIn(camera_view_group_3[0], scale=0.6),
            run_time=0.6,
        )

        self.play(
            FadeIn(camera_view_group_3[1]),
            Create(camera_view_group_3[2]),
            Create(camera_view_group_3[3]),
            run_time=0.9,
        )

        behind_arrow_2 = CurvedArrow(
            start_point=campus_img.get_center() + RIGHT * 1.3 + UP * 0.3,
            end_point=campus_img.get_right() + RIGHT * 1.25 + UP * 0.6,
            angle=TAU / 3,
            color=PURE_YELLOW,
            stroke_width=3,
            tip_shape=StealthTip,
        )
        behind_arrow_2.pop_tips()
        behind_arrow_2.add_tip(
            tip_shape=StealthTip,
            tip_length=0.14,
            tip_width=0.14,
        )
        behind_arrow_2.set_z_index(5)
        behind_text_2 = Text(
            "What's behind?",
            font_size=22,
            color=YELLOW,
        ).next_to(behind_arrow_2.get_end(), UP, buff=0.18)
        behind_text_2.set_z_index(5)

        self.play(Create(behind_arrow_2), run_time=0.8)
        self.play(Write(behind_text_2), run_time=0.6)

        # Camera view group 4 and 5
        camera_view_group_4 = create_camera_view_group(
            camera_pos=campus_img.get_center() + LEFT * 0.3 + DOWN * 1.2,
            view_end_1=campus_img.get_center() + RIGHT * 0.8 + DOWN * 0.4,
            view_end_2=campus_img.get_center() + RIGHT * 1.1 + DOWN * 0.9,
            camera_color=BLACK,
            yaw_angle=45 * DEGREES,
            pitch_angle=-22 * DEGREES,
            roll_angle=-15 * DEGREES
        )

        camera_view_group_5 = create_camera_view_group(
            camera_pos=campus_img.get_center() + RIGHT * 1.6 + DOWN * 1.3,
            view_end_1=campus_img.get_center() + RIGHT * 0.5 + DOWN * 0.5,
            view_end_2=campus_img.get_center() + RIGHT * 0.3 + DOWN * 0.9,
            camera_color=BLACK,
            yaw_angle=-45 * DEGREES,
            pitch_angle=-22 * DEGREES,
            roll_angle=15 * DEGREES
        )

        self.play(
            FadeIn(camera_view_group_4[0], scale=0.6),
            FadeIn(camera_view_group_5[0], scale=0.6),
            run_time=0.6,
        )

        self.play(
            FadeIn(camera_view_group_4[1]),
            FadeIn(camera_view_group_5[1]),
            Create(camera_view_group_4[2]),
            Create(camera_view_group_4[3]),
            Create(camera_view_group_5[2]),
            Create(camera_view_group_5[3]),
            run_time=0.9,
        )

        behind_arrow_3 = CurvedArrow(
            start_point=campus_img.get_center() + RIGHT * 0.5 + DOWN * 0.85,
            end_point=campus_img.get_right() + RIGHT * 1.25 + DOWN * 1.5,
            angle=-TAU / 4,
            color=PURE_YELLOW,
            stroke_width=3,
            tip_shape=StealthTip,
        )
        behind_arrow_3.pop_tips()
        behind_arrow_3.add_tip(
            tip_shape=StealthTip,
            tip_length=0.14,
            tip_width=0.14,
        )
        behind_arrow_3.set_z_index(5)
        behind_text_3 = Text(
            "What's behind?",
            font_size=22,
            color=YELLOW,
        ).next_to(behind_arrow_3.get_end(), DOWN, buff=0.16)
        behind_text_3.set_z_index(5)

        self.play(Create(behind_arrow_3), run_time=0.8)
        self.play(Write(behind_text_3), run_time=0.6)

        # RIGHT PANEL
        generated_paths = [
            Path(f"assets/images/campus-{index}.png")
            for index in range(1, 10)
        ]
        generated_grid = create_image_grid(
            generated_paths,
            rows=3,
            cols=3,
            target_width=campus_img.width,
            target_height=campus_img.height,
        )
        generated_grid.move_to(RIGHT * 3.15 + UP * (campus_img.get_center()[1] + 0.22))
        generated_ellipsis = Text("...", font_size=40, color=WHITE).next_to(
            generated_grid,
            DOWN,
            buff=0.24,
        )
        generated_label = Text("Generated Views", font_size=22, color=WHITE).next_to(
            generated_ellipsis,
            DOWN,
            buff=0.2,
        )

        self.play(
            LaggedStart(
                *[FadeIn(cell, shift=RIGHT * 0.1) for cell in generated_grid],
                lag_ratio=0.12,
            ),
            run_time=1.2,
        )
        self.play(
            Write(generated_ellipsis),
            Write(generated_label),
            run_time=0.75,
        )
        self.wait(1.0)

        self.play(
            FadeOut(campus_panel),
            FadeOut(dim_overlay),
            FadeOut(camera_view_group_1),
            FadeOut(camera_view_group_2),
            FadeOut(camera_view_group_3),
            FadeOut(camera_view_group_4),
            FadeOut(camera_view_group_5),
            FadeOut(behind_arrow_1),
            FadeOut(behind_arrow_2),
            FadeOut(behind_arrow_3),
            FadeOut(behind_text_1),
            FadeOut(behind_text_2),
            FadeOut(behind_text_3),
            FadeOut(generated_grid),
            FadeOut(generated_ellipsis),
            FadeOut(generated_label),
            run_time=0.8,
        )

        self.wait(2.5)

        bullet_2 = create_numbered_bullet(
            2,
            "Slow optimization",
            color=BLUE_D,
        )
        bullet_2.remove(bullet_2[2])
        bullet_2_label = create_mixed_math_label(
            "Slow ",
            "3",
            "D optimization",
            font_size=25,
            color=WHITE,
        ).next_to(bullet_2[0], RIGHT, buff=0.22)
        bullet_2.add(bullet_2_label)
        bullet_2.next_to(bullet_1, DOWN, buff=0.38, aligned_edge=LEFT)

        self.play(
            FadeIn(VGroup(bullet_2[0], bullet_2[1]), scale=0.7),
            Write(bullet_2[2]),
            run_time=0.8,
        )
        self.wait(3.0)

        bottleneck_text = Text(
            "Minutes ~ Hours!",
            font_size=28,
            color=RED,
        )
        hourglass_icon = create_fontawesome_hourglass_icon(color=RED).next_to(
            bottleneck_text,
            LEFT,
            buff=0.16,
        )
        bottleneck_label = VGroup(hourglass_icon, bottleneck_text)
        bottleneck_label.next_to(bullet_2, DOWN, buff=2.46)
        bottleneck_label.align_to(bullet_1[2], LEFT)

        bottleneck_x = bottleneck_label.get_center()[0]
        bottleneck_arrow = Arrow(
            [bottleneck_x, bullet_2.get_bottom()[1] - 0.58, 0],
            [bottleneck_x, bottleneck_label.get_top()[1] + 0.58, 0],
            buff=0,
            color=RED,
            stroke_width=14,
            tip_shape=StealthTip,
            max_tip_length_to_length_ratio=0.16,
        )

        self.play(GrowArrow(bottleneck_arrow), run_time=0.65)
        self.play(FadeIn(hourglass_icon, scale=0.7), run_time=0.2)
        self.play(
            Rotate(hourglass_icon, angle=TAU, about_point=hourglass_icon.get_center()),
            Write(bottleneck_text),
            run_time=0.9,
        )
        self.play(
            bottleneck_label.animate.scale(1.12),
            rate_func=there_and_back,
            run_time=1.2,
        )

        self.wait(7.0)
        self.play(FadeOut(bottleneck_label), FadeOut(bottleneck_arrow), run_time=0.5)

        bullet_1_solution_text = Text(
            "One view",
            font_size=25,
            color=YELLOW,
            weight=BOLD,
        )
        solution_arrow_start_x = bullet_1[2].get_right()[0] + 0.28
        solution_arrow_end_x = solution_arrow_start_x + 1.75
        bullet_1_solution_arrow = Arrow(
            [solution_arrow_start_x, bullet_1[2].get_center()[1], 0],
            [solution_arrow_end_x, bullet_1[2].get_center()[1], 0],
            buff=0,
            color=WHITE,
            stroke_width=2.5,
            tip_shape=StealthTip,
            tip_length=0.2,
            max_tip_length_to_length_ratio=0.08,
        )
        bullet_1_solution_text.next_to(
            bullet_1_solution_arrow,
            RIGHT,
            buff=0.32,
        )

        bullet_2_solution_text = Tex(
            r"\textbf{Fast optimization ($\mathbf{<1}$ second)}",
            font_size=32,
            color=BLUE_D,
        )
        bullet_2_solution_arrow = Arrow(
            [solution_arrow_start_x, bullet_2[2].get_center()[1], 0],
            [solution_arrow_end_x, bullet_2[2].get_center()[1], 0],
            buff=0,
            color=WHITE,
            stroke_width=2.5,
            tip_shape=StealthTip,
            tip_length=0.2,
            max_tip_length_to_length_ratio=0.08,
        )
        bullet_2_solution_text.next_to(
            bullet_2_solution_arrow,
            RIGHT,
            buff=0.32,
        )

        flags_text = Tex(
            r"\textbf{FLAGS}: Fast Layered Gaussian Surfels",
            font_size=33,
            color=WHITE,
        )
        if flags_text.width > 5.7:
            flags_text.scale_to_fit_width(5.7)
        flags_text.align_to(bullet_1_solution_text, LEFT)
        flags_text.set_y(bottleneck_text.get_center()[1])
        flags_text.shift(LEFT * 0.95)

        flags_x = flags_text.get_center()[0]
        flags_arrow = Arrow(
            [flags_x, bullet_2.get_bottom()[1] - 0.58, 0],
            [flags_x, flags_text.get_top()[1] + 0.58, 0],
            buff=0,
            color=WHITE,
            stroke_width=14,
            tip_shape=StealthTip,
            max_tip_length_to_length_ratio=0.16,
        )

        self.play(GrowArrow(bullet_1_solution_arrow),run_time=0.8)
        self.play(Write(bullet_1_solution_text), run_time=0.45)
        self.wait(2.0)

        self.play(GrowArrow(bullet_2_solution_arrow),run_time=0.8)
        self.play(Write(bullet_2_solution_text), run_time=0.45)
        self.wait(3.0)

        self.play(GrowArrow(flags_arrow), run_time=0.65)
        self.play(Write(flags_text), run_time=0.9)
        self.play(
            flags_text.animate.scale(1.08),
            rate_func=there_and_back,
            run_time=0.8,
        )

        self.wait(5.0)
