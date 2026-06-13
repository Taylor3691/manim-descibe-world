"""
Shared visual language and helpers for Topic 1:
"Scaling Foundation World Models as a Path to Embodied AGI"

All scenes import from here to maintain consistent styling.
"""

from manim import *
import numpy as np

# ─── Color Palette (Dark Theme, 3B1B-inspired) ──────────────────────────────

BG_COLOR = "#0f0f23"
TEXT_PRIMARY = "#e2e2e2"
TEXT_DIM = "#8888aa"

AGENT_COLOR = "#00d2ff"       # Cyan glow — agents
WORLD_COLOR = "#ffb347"       # Warm amber — worlds / environments
ACTION_COLOR = "#2ecc71"      # Emerald — actions
LATENT_COLOR = "#e056a0"      # Magenta — latent actions / hidden variables
DATA_COLOR = "#a68eff"        # Soft purple — video data
HIGHLIGHT_COLOR = "#ffe066"   # Bright yellow — emphasis
GENIE_COLOR = "#ff6b6b"       # Coral — Genie brand
SIMA_COLOR = "#4ecdc4"        # Teal — SIMA brand

# Gradient pairs for richer visuals
GRADIENT_CYBER = [AGENT_COLOR, LATENT_COLOR]
GRADIENT_WARM = [WORLD_COLOR, GENIE_COLOR]
GRADIENT_COOL = [AGENT_COLOR, DATA_COLOR]

# ─── Typography Helpers ─────────────────────────────────────────────────────

def title_text(text, font_size=48, color=TEXT_PRIMARY):
    """Scene title — large, bold."""
    return Text(
        text,
        font_size=font_size,
        color=color,
        weight=BOLD,
    )


def subtitle_text(text, font_size=32, color=HIGHLIGHT_COLOR):
    """Subtitle or section header."""
    return Text(
        text,
        font_size=font_size,
        color=color,
    )


def body_text(text, font_size=24, color=TEXT_PRIMARY):
    """Body / narration text."""
    return Text(
        text,
        font_size=font_size,
        color=color,
        line_spacing=1.4,
    )


def label_text(text, font_size=20, color=TEXT_DIM):
    """Small labels, annotations."""
    return Text(
        text,
        font_size=font_size,
        color=color,
    )


def math_label(tex_string, font_size=36, color=LATENT_COLOR):
    """MathTex label for latent variables, equations."""
    return MathTex(tex_string, font_size=font_size, color=color)


# ─── Visual Primitives ──────────────────────────────────────────────────────

def make_agent(radius=0.15, color=AGENT_COLOR, glow=True):
    """Glowing agent dot."""
    dot = Dot(radius=radius, color=color)
    if glow:
        glow_circle = Circle(radius=radius * 3, color=color, fill_opacity=0.15, stroke_width=0)
        return VGroup(glow_circle, dot)
    return dot


def make_world_cube(side=2.0, color=WORLD_COLOR, opacity=0.2):
    """Translucent world cube (represented as a rounded rectangle in 2D)."""
    cube = RoundedRectangle(
        width=side,
        height=side,
        corner_radius=0.2,
        color=color,
        fill_opacity=opacity,
        stroke_width=2,
    )
    # Add subtle grid lines inside
    grid = VGroup()
    for i in range(1, 3):
        frac = i / 3
        h_line = Line(
            cube.get_left() + UP * (side / 2 - frac * side),
            cube.get_right() + UP * (side / 2 - frac * side),
            color=color,
            stroke_width=0.5,
            stroke_opacity=0.3,
        )
        v_line = Line(
            cube.get_top() + RIGHT * (-side / 2 + frac * side),
            cube.get_bottom() + RIGHT * (-side / 2 + frac * side),
            color=color,
            stroke_width=0.5,
            stroke_opacity=0.3,
        )
        grid.add(h_line, v_line)
    return VGroup(cube, grid)


def make_action_arrow(start=LEFT, end=RIGHT, color=ACTION_COLOR):
    """Solid action arrow."""
    return Arrow(
        start, end,
        color=color,
        stroke_width=3,
        buff=0.1,
        max_tip_length_to_length_ratio=0.15,
    )


def make_latent_arrow(start=LEFT, end=RIGHT, color=LATENT_COLOR):
    """Dashed latent / hidden action arrow (DashedLine + Triangle tip)."""
    line = DashedLine(
        start, end,
        color=color,
        stroke_width=3,
        dash_length=0.15,
    )
    # Add arrowhead
    direction = (np.array(end) - np.array(start)).astype(float)
    direction /= np.linalg.norm(direction)
    tip = Triangle(color=color, fill_opacity=1, stroke_width=0)
    tip.scale(0.12)
    tip.rotate(np.arctan2(direction[1], direction[0]) - PI / 2)
    tip.move_to(end)
    return VGroup(line, tip)


def make_frame_rect(width=1.6, height=0.9, color=DATA_COLOR, label=None):
    """Video frame rectangle (16:9 aspect ratio by default)."""
    rect = Rectangle(
        width=width,
        height=height,
        color=color,
        fill_opacity=0.1,
        stroke_width=2,
    )
    if label:
        lbl = label_text(label, font_size=16, color=color).move_to(rect)
        return VGroup(rect, lbl)
    return rect


def make_film_strip(n_frames=5, frame_w=0.8, frame_h=0.45, spacing=0.15, color=DATA_COLOR):
    """A horizontal strip of video frames."""
    frames = VGroup()
    for i in range(n_frames):
        f = Rectangle(
            width=frame_w, height=frame_h,
            color=color, fill_opacity=0.08, stroke_width=1.5,
        )
        frames.add(f)
    frames.arrange(RIGHT, buff=spacing)
    # Top and bottom perforations
    perf_top = VGroup()
    perf_bot = VGroup()
    total_w = frames.width + 0.4
    for x in np.linspace(-total_w / 2, total_w / 2, n_frames * 3):
        perf_top.add(
            Square(side_length=0.06, color=color, fill_opacity=0.3, stroke_width=0)
            .move_to(frames.get_top() + UP * 0.12 + RIGHT * x)
        )
        perf_bot.add(
            Square(side_length=0.06, color=color, fill_opacity=0.3, stroke_width=0)
            .move_to(frames.get_bottom() + DOWN * 0.12 + RIGHT * x)
        )
    border = Rectangle(
        width=total_w, height=frames.height + 0.5,
        color=color, fill_opacity=0.03, stroke_width=1,
        stroke_opacity=0.4,
    ).move_to(frames)
    return VGroup(border, perf_top, perf_bot, frames)


def make_box_simulator(side=1.2, agent_radius=0.08, color=WORLD_COLOR):
    """Tiny boxed simulator with an agent inside."""
    box = Square(side_length=side, color=color, stroke_width=1.5, fill_opacity=0.05)
    agent = make_agent(radius=agent_radius, color=AGENT_COLOR, glow=False)
    return VGroup(box, agent)


# ─── Transition / Animation Helpers ─────────────────────────────────────────

def scene_title_sequence(scene, title_str, subtitle_str=None, hold=1.5):
    """Standard scene opening: fade-in title, optional subtitle, then fade out."""
    t = title_text(title_str, font_size=40)
    group = VGroup(t)
    if subtitle_str:
        s = subtitle_text(subtitle_str, font_size=26)
        group.add(s)
        group.arrange(DOWN, buff=0.4)
    group.move_to(ORIGIN)
    scene.play(FadeIn(group, shift=UP * 0.3), run_time=1)
    scene.wait(hold)
    scene.play(FadeOut(group, shift=UP * 0.5), run_time=0.8)
    scene.wait(0.3)


def pulse_glow(mobject, scale_factor=1.15, n_pulses=2, color=None):
    """Return a pulsing animation sequence."""
    anims = []
    for _ in range(n_pulses):
        anims.append(mobject.animate.scale(scale_factor))
        anims.append(mobject.animate.scale(1 / scale_factor))
    return Succession(*[a.build() if hasattr(a, 'build') else a for a in anims])


def circular_arrow_path(center=ORIGIN, radius=1.5, start_angle=0, angle=TAU):
    """Create a circular arc path."""
    return Arc(
        radius=radius,
        start_angle=start_angle,
        angle=angle * 0.9,
        arc_center=center,
    )
