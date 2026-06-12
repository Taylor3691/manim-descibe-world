from pathlib import Path

import numpy as np
from manim import *

from video_mobject import (
    VideoMobject,
    create_video_stage_frame,
    fit_video_to_frame,
    freeze_video_frame,
)


class Scene1(Scene):
    def construct(self):
        title = Tex(r"\textbf{Video Generation}").scale(1.2).to_edge(UP)
        self.play(Write(title))

        intro_video_path = Path("assets/videos/intro.mp4")
        intro_video = VideoMobject(intro_video_path)
        intro_video.set_time_source(lambda: self.time)
        video_frame = create_video_stage_frame()

        fit_video_to_frame(intro_video, video_frame)

        self.play(FadeIn(video_frame), FadeIn(intro_video))
        intro_video.play()
        self.wait(5)
        intro_video.pause()

        self.wait(2)

        final_frame = freeze_video_frame(intro_video)

        self.play(FadeOut(intro_video, run_time=0.2), FadeIn(final_frame, run_time=0.2))

        img_data = np.copy(final_frame.pixel_array)
        img_h, img_w = img_data.shape[:2]

        cols = 32
        rows = max(1, int(round(cols * final_frame.height / final_frame.width)))
        pixel_side = min(final_frame.width / cols, final_frame.height / rows)
        grid_width = cols * pixel_side
        grid_height = rows * pixel_side
        center = final_frame.get_center()

        pixels = Group()
        patch_borders = VGroup()
        for i in range(rows):
            for j in range(cols):
                x0 = int(j * img_w / cols)
                x1 = int((j + 1) * img_w / cols)
                y0 = int(i * img_h / rows)
                y1 = int((i + 1) * img_h / rows)
                if x1 <= x0 or y1 <= y0:
                    continue

                patch_array = np.ascontiguousarray(img_data[y0:y1, x0:x1])
                px = ImageMobject(patch_array)

                patch_width = (x1 - x0) / img_w * final_frame.width
                patch_height = (y1 - y0) / img_h * final_frame.height
                px.set_width(patch_width)
                px.set_height(patch_height)
                px.move_to(
                    [
                        center[0] - grid_width / 2 + (j + 0.5) * pixel_side,
                        center[1] + grid_height / 2 - (i + 0.5) * pixel_side,
                        0,
                    ]
                )

                border = Square(side_length=pixel_side)
                border.set_fill(opacity=0)
                border.set_stroke(color=GRAY_B, width=0.35, opacity=0.45)
                border.move_to(px.get_center())

                pixels.add(px)
                patch_borders.add(border)

        self.remove(final_frame)
        self.add(pixels, patch_borders)

        target_pixels = pixels.copy()
        for px in target_pixels:
            px.scale(0.82, about_point=px.get_center())

        target_borders = patch_borders.copy()
        for border in target_borders:
            border.scale(0.82, about_point=border.get_center())

        self.play(
            Transform(pixels, target_pixels, lag_ratio=0.0),
            Transform(patch_borders, target_borders, lag_ratio=0.0),
            run_time=1,
            rate_func=linear,
        )

        blue_pixels = VGroup()
        for px in pixels:
            blue_square = Square(side_length=pixel_side * 0.82)
            blue_square.set_fill(BLUE_D, opacity=1.0)
            blue_square.set_stroke(BLUE_E, width=0.25, opacity=0.9)
            blue_square.move_to(px.get_center())
            blue_pixels.add(blue_square)

        self.play(
            FadeOut(pixels),
            FadeIn(blue_pixels),
            FadeOut(patch_borders),
            run_time=0.75,
            rate_func=linear,
        )

        pixels = blue_pixels

        self.wait(0.75)

        self.play(FadeOut(pixels), FadeOut(title), run_time=0.7)

        left_box = RoundedRectangle(corner_radius=0.1, width=3.2, height=1.3)
        left_box.set_fill(BLUE_E, opacity=0.35)
        left_box.set_stroke(BLUE_D, width=2)
        left_text = Tex(r"\textbf{Video Model}", font_size=38)
        left_group = VGroup(left_box, left_text)
        left_text.move_to(left_box.get_center())

        right_box = RoundedRectangle(corner_radius=0.1, width=3.2, height=1.3)
        right_box.set_fill(GREEN_E, opacity=0.35)
        right_box.set_stroke(GREEN_D, width=2)
        right_text = Tex(r"\textbf{World Model}", font_size=38)
        right_group = VGroup(right_box, right_text)
        right_text.move_to(right_box.get_center())

        arrow_text = Tex(
            r"Understanding how the world\\evolves under actions",
            font_size=28,
        )
        arrow_len = arrow_text.width + 1.2
        flow_arrow = Arrow(
            LEFT * (arrow_len / 2),
            RIGHT * (arrow_len / 2),
            buff=0,
            stroke_width=4,
            color=YELLOW,
            tip_shape=StealthTip,
            max_tip_length_to_length_ratio=0.09,
        )
        flow_group = VGroup(flow_arrow, arrow_text)
        arrow_text.move_to(flow_arrow.get_center() + UP * 0.42)

        left_group.next_to(flow_arrow, LEFT, buff=0.4)
        right_group.next_to(flow_arrow, RIGHT, buff=0.4)

        model_pipeline = VGroup(left_group, flow_group, right_group)
        model_pipeline.move_to(ORIGIN)

        self.play(FadeOut(video_frame), run_time=0.6)
        self.play(FadeIn(left_group, shift=RIGHT * 0.2), run_time=1.2)
        self.play(GrowArrow(flow_arrow), Write(arrow_text), run_time=1.7)
        self.play(FadeIn(right_group, shift=LEFT * 0.2), run_time=1.2)
        self.wait(5)
        intro_video.stop()
        intro_video.close()