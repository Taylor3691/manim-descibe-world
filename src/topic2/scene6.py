from pathlib import Path

import numpy as np
from PIL import Image
from manim import *

from video_mobject import VideoMobject, create_video_stage_frame, fit_video_to_frame


IMAGE_DIR = Path("assets/images")


def resolve_image_path(name):
    path = IMAGE_DIR / name
    if path.exists():
        return path

    if name == "campus.png":
        return IMAGE_DIR / "campus-0.png"

    raise FileNotFoundError(f"Missing image asset: {path}")


def fit_image_to_box(image, width, height):
    image.set_width(width)
    if image.height > height:
        image.set_height(height)
    return image


def create_image_panel(
    name,
    label,
    width=2.18,
    max_height=1.54,
    font_size=24,
    with_border=False,
):
    image = ImageMobject(str(resolve_image_path(name)))
    fit_image_to_box(image, width, max_height)
    image.set_z_index(1)

    border = Rectangle(
        width=image.width,
        height=image.height,
        color=WHITE,
        stroke_width=0.9,
    ).move_to(image)
    border.set_z_index(2)

    label_mob = Tex(label, font_size=font_size, color=WHITE)
    label_mob.next_to(image, DOWN, buff=0.13)
    label_mob.set_z_index(3)

    if with_border:
        return Group(image, label_mob, border)

    return Group(image, label_mob)


def create_soft_edge_image(name, width=2.42, edge_size=25):
    path = resolve_image_path(name)
    image = Image.open(path).convert("RGBA")

    w, h = image.size
    edge_size = max(1, int(edge_size))

    x = np.minimum(np.arange(w), np.arange(w)[::-1]) / edge_size
    y = np.minimum(np.arange(h), np.arange(h)[::-1]) / edge_size
    mask = np.clip(np.minimum(y[:, None], x[None, :]), 0, 1)
    mask = mask * mask * (3 - 2 * mask)

    alpha = Image.fromarray(np.uint8(mask * 255), mode="L")
    image.putalpha(alpha)

    image_mobject = ImageMobject(np.asarray(image))
    image_mobject.set_width(width)
    image_mobject.set_z_index(0)
    return image_mobject


def make_arrow(start, end, stroke_width=4.0):
    arrow = Arrow(
        start=start,
        end=end,
        buff=0,
        color=WHITE,
        stroke_width=stroke_width,
        tip_shape=StealthTip,
        tip_length=0.11,
        max_tip_length_to_length_ratio=0.06,
        max_stroke_width_to_length_ratio=10,
    )
    arrow.set_z_index(3)
    return arrow


def create_fontawesome_check_icon(color=GREEN):
    template = TexTemplate()
    template.add_to_preamble(r"\usepackage{fontawesome5}")
    return Tex(
        r"\faCheck",
        tex_template=template,
        font_size=26,
        color=color,
    )


def create_initialization_table():
    row_gap = 0.5
    col_gap = 1.42
    left_labels = ["", "XYZ", "RGB", "Radius", "Orientation", "Opacity"]
    right_cells = [Tex("Initialize?", font_size=28, color=WHITE)]
    right_cells.extend(create_fontawesome_check_icon(color=GREEN) for _ in range(4))
    right_cells.append(VMobject())

    left_column = VGroup()
    right_column = VGroup()
    for row_idx in range(6):
        row_y = -row_idx * row_gap
        if left_labels[row_idx]:
            left_cell = Tex(left_labels[row_idx], font_size=27, color=WHITE)
            left_cell.move_to(LEFT * col_gap / 2 + UP * row_y)
            left_column.add(left_cell)

        right_cell = right_cells[row_idx]
        if len(right_cell.submobjects) > 0:
            right_cell.move_to(RIGHT * col_gap / 2 + UP * row_y)
            right_column.add(right_cell)

    return VGroup(left_column, right_column)


def make_cube_scene_panel(image_name, label):
    cube_width = 2.42
    front_pad = 0.1

    image = create_soft_edge_image(
        image_name,
        width=(cube_width + front_pad) * 1.15,
        edge_size=180,
    )
    image.move_to(ORIGIN + RIGHT * 0.2 + UP * 0.17)

    front = Rectangle(
        width=cube_width + front_pad,
        height=cube_width + front_pad,
        color=WHITE,
        stroke_width=2.2,
    ).move_to(ORIGIN)
    front.set_z_index(4)

    offset = RIGHT * 0.42 + UP * 0.34
    corners = [front.get_corner(UL), front.get_corner(UR), front.get_corner(DR), front.get_corner(DL)]
    side_edges = VGroup()
    for corner in corners:
        edge = DashedLine(
            corner,
            corner + offset,
            color=GRAY_B,
            stroke_width=2,
            dash_length=0.07,
            dashed_ratio=0.55,
        )
        edge.set_z_index(3)
        side_edges.add(edge)

    label_mob = Tex(r"$3$D Scene", font_size=28, color=WHITE)
    label_mob.next_to(front, DOWN, buff=0.16)
    label_mob.set_z_index(5)

    return Group(side_edges, image, front, label_mob)


class Scene6(Scene):
    def construct(self):
        # SCENE 6A: FIND OCCLUDED REGIONS AND COMPLETE

        title = Tex(
            r"\textbf{Fast Layered Gaussian Surfels (FLAGS)}",
            font_size=40,
        ).to_edge(UP, buff=0.28)

        subtitle = Tex(
            r"Core idea $1$: Find occluded regions and complete",
            font_size=32,
            color=YELLOW,
        )
        subtitle.next_to(title, DOWN, buff=0.2)

        self.play(Write(title), run_time=1.0)
        self.wait(0.5)
        self.play(Write(subtitle), run_time=1.0)
        self.wait(3.0)

        col1_x = -5.55
        col2_x = -2.05
        col3_x = 1.05
        col4_x = 5.25
        row_ys = [1.5, -0.52, -2.54]
        input_arrow_pad = 0.28
        middle_arrow_pad = 0.26
        scene_arrow_pad = 0.48

        input_panel = create_image_panel(
            "campus.png",
            "Input Image",
            width=3.35,
            max_height=2.47,
            font_size=28,
        )
        input_panel.move_to([col1_x, row_ys[1], 0])
        input_image = input_panel[0]

        source_panels = Group(
            create_image_panel("foreground.png", "Foreground", with_border=True),
            create_image_panel("background.png", "Background", with_border=True),
            create_image_panel("sky.png", "Sky", with_border=True),
        )
        completed_panels = Group(
            create_image_panel("foreground-c.png", "Completed", with_border=True),
            create_image_panel("background-c.png", "Completed", with_border=True),
            create_image_panel("sky-c.png", "Completed", with_border=True),
        )

        for idx, panel in enumerate(source_panels):
            panel.move_to([col2_x, row_ys[idx], 0])
        for idx, panel in enumerate(completed_panels):
            panel.move_to([col3_x, row_ys[idx], 0])

        scene_panel = make_cube_scene_panel("campus.png", "3D Scene")
        scene_panel.move_to([col4_x, row_ys[1], 0])
        scene_image = scene_panel[1]

        input_to_layers = VGroup()
        input_start_anchor = input_image.get_right() + RIGHT * input_arrow_pad
        input_starts = [
            input_start_anchor + UP * 0.38,
            input_start_anchor,
            input_start_anchor + DOWN * 0.38,
        ]
        for start_point, panel in zip(input_starts, source_panels):
            target_image = panel[0]
            input_to_layers.add(
                make_arrow(
                    start_point,
                    target_image.get_left() + LEFT * input_arrow_pad,
                    stroke_width=3.4,
                )
            )

        layers_to_completed = VGroup()
        for src_panel, dst_panel in zip(source_panels, completed_panels):
            src_image = src_panel[0]
            dst_image = dst_panel[0]
            layers_to_completed.add(
                make_arrow(
                    src_image.get_right() + RIGHT * middle_arrow_pad,
                    dst_image.get_left() + LEFT * middle_arrow_pad,
                    stroke_width=3.4,
                )
            )

        completed_to_scene = VGroup()
        scene_end_anchor = scene_image.get_left() + LEFT * scene_arrow_pad
        scene_targets = [
            scene_end_anchor + UP * 0.42,
            [scene_end_anchor[0], completed_panels[1][0].get_center()[1], 0],
            scene_end_anchor + DOWN * 0.42,
        ]
        for panel, end_point in zip(completed_panels, scene_targets):
            src_image = panel[0]
            completed_to_scene.add(
                make_arrow(
                    src_image.get_right() + RIGHT * scene_arrow_pad,
                    end_point,
                    stroke_width=3.4,
                )
            )

        self.play(FadeIn(input_panel, shift=UP * 0.12), run_time=1.0)
        self.wait(1.0)
        self.play(
            *[GrowArrow(arrow) for arrow in input_to_layers],
            *[FadeIn(panel, shift=RIGHT * 0.12) for panel in source_panels],
            run_time=1.5,
        )
        self.wait(8.0)

        self.play(
            *[GrowArrow(arrow) for arrow in layers_to_completed],
            *[FadeIn(panel, shift=RIGHT * 0.12) for panel in completed_panels],
            run_time=1.5,
        )
        self.wait(15.0)

        self.play(
            *[GrowArrow(arrow) for arrow in completed_to_scene],
            FadeIn(scene_panel, shift=RIGHT * 0.12),
            run_time=1.5,
        )

        self.wait(6.0)

        # SCENE 6B: SURFELS LEVERAGE PIXEL GEOMETRY FOR INITIALIZATION

        self.play(
            FadeOut(subtitle),
            FadeOut(input_panel),
            FadeOut(source_panels),
            FadeOut(completed_panels),
            FadeOut(input_to_layers),
            FadeOut(layers_to_completed),
            FadeOut(completed_to_scene),
            run_time=1.0,
        )
        self.play(scene_panel.animate.move_to(LEFT * 4.05 + DOWN * 0.46), run_time=1.0)

        subtitle_6b = Tex(
            r"Core idea $2$: Design surfels to leverage pixel geometry for initialization",
            font_size=32,
            color=YELLOW,
        )
        subtitle_6b.next_to(title, DOWN, buff=0.4)

        self.play(Write(subtitle_6b), run_time=1.5)
        self.wait(2.0)

        scene_image = scene_panel[1]
        sample_box = Square(
            side_length=0.14,
            color=PURE_RED,
            stroke_width=4.2,
            fill_opacity=0,
        )
        sample_box.move_to(scene_image.get_center() + RIGHT * 0.8 + DOWN * 0.65)
        sample_box.set_z_index(7)
        surfel_center = DOWN * 0.18
        top_line_end = surfel_center + UP * 1.5
        bottom_line_end = surfel_center + DOWN * 1.5

        zoom_lines = VGroup(
            DashedLine(
                sample_box.get_corner(UR),
                top_line_end,
                color=PURE_YELLOW,
                stroke_width=2,
                dash_length=0.08,
                dashed_ratio=0.55,
            ),
            DashedLine(
                sample_box.get_corner(DR),
                bottom_line_end,
                color=PURE_YELLOW,
                stroke_width=2,
                dash_length=0.08,
                dashed_ratio=0.55,
            ),
        )
        zoom_lines.set_z_index(6)

        surfel_glow = VGroup(
            Ellipse(
                width=1.5,
                height=3.0,
                color=GREEN,
                stroke_width=10,
                stroke_opacity=0.16,
                fill_opacity=0,
            )
        ).move_to(surfel_center)
        surfel_glow.set_z_index(3)

        surfel_ellipse = Ellipse(
            width=1.3,
            height=2.8,
            color=GREEN,
            stroke_width=5,
            fill_color=GREEN,
            fill_opacity=0.18,
        ).move_to(surfel_center)
        surfel_ellipse.set_z_index(4)
        surfel_label = Tex(
            "Gaussian Surfel",
            font_size=30,
            color=WHITE,
        ).next_to(surfel_ellipse, DOWN, buff=0.3)
        surfel_label.set_z_index(5)
        surfel_group = VGroup(surfel_glow, surfel_ellipse, surfel_label)

        init_table = create_initialization_table()
        init_table.move_to(RIGHT * 3.35 + DOWN * 0.35)
        left_table_column = init_table[0]
        right_table_column = init_table[1]

        self.play(Create(sample_box), run_time=0.5)
        self.wait(2.0)
        self.play(*[Create(line) for line in zoom_lines], run_time=1.0)
        self.play(
            FadeIn(surfel_glow, scale=0.85),
            FadeIn(surfel_ellipse, scale=0.9),
            Write(surfel_label),
            run_time=1.0,
        )
        self.wait(6.5)
        for cell in left_table_column:
            self.play(FadeIn(cell, shift=UP * 0.08), run_time=0.75)
        self.wait(1.5)
        for cell in right_table_column:
            self.play(FadeIn(cell, shift=UP * 0.08), run_time=0.75)

        self.wait(12.0)

        # SCENE 6C: INTERACTIVE GENERATION PROCESS

        self.play(
            FadeOut(*[mobject for mobject in self.mobjects if mobject is not title]),
            run_time=0.8,
        )

        title_6c = Tex(
            r"\textbf{Interactive Generation Process}",
            font_size=42,
        ).to_edge(UP, buff=0.28)

        self.play(FadeOut(title), run_time=0.45)
        self.play(Write(title_6c), run_time=0.9)
        title = title_6c

        hcmc_video_path = Path("assets/videos/hcmc.mp4")
        hcmc_frame = create_video_stage_frame(width=10.4, height=5.5, center=DOWN * 0.35)
        hcmc_video = VideoMobject(hcmc_video_path)
        hcmc_video.set_time_source(lambda: self.time * 2)
        fit_video_to_frame(hcmc_video, hcmc_frame, padding=0.16)
        citation = Tex(
            r"[\textbf{WonderWorld}, Yu \textit{et al.}, $2025$]",
            font_size=22,
            color=WHITE,
        )
        citation.next_to(hcmc_frame, DOWN, buff=0.12, aligned_edge=RIGHT)
        citation.to_edge(RIGHT, buff=0.32)

        self.play(FadeIn(hcmc_frame), FadeIn(hcmc_video), Write(citation), run_time=0.7)
        hcmc_video.play()
        self.wait(hcmc_video.duration / 2)
        hcmc_video.pause()

        self.wait(8.0)
        hcmc_video.close()
