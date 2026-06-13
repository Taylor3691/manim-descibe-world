from manim import *
import numpy as np
import random

class InferenceTimeScaling(Scene):
    def construct(self):
        # Dark background
        self.camera.background_color = "#0f0f1e"
        
        np.random.seed(42)
        random.seed(42)
        
        # ========== Phase 1: Title & Subtitle ==========
        title = Text("Inference-time Scaling in Refinement Steps", 
                     font_size=32, color=WHITE)
        title.to_edge(UP, buff=0.4)
        
        subtitle = Text("Does not increase the number of tokens",
                        font_size=20, color="#9090a8")
        subtitle.next_to(title, DOWN, buff=0.15)
        
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=1)
        self.play(FadeIn(subtitle, shift=DOWN * 0.2), run_time=1)
        
        # ========== Panel positions ==========
        panel_size = 1.4
        panel_y = 0.4
        x_positions = [-3.0, -1.0, 1.0, 3.0]
        
        # ========== Phase 2: Panel 1 - Noise ==========
        frame1 = Square(side_length=panel_size, color=BLUE_C, 
                       fill_opacity=0.05, stroke_width=2)
        frame1.move_to([x_positions[0], panel_y, 0])
        
        noise_dots = VGroup()
        for _ in range(110):
            dx = np.random.uniform(-panel_size/2 + 0.1, panel_size/2 - 0.1)
            dy = np.random.uniform(-panel_size/2 + 0.1, panel_size/2 - 0.1)
            color = random.choice([WHITE, "#c0c0d0", "#8080a0", "#5a5a8a"])
            dot = Dot(point=[x_positions[0] + dx, panel_y + dy, 0], 
                     radius=0.022, color=color, fill_opacity=0.85)
            noise_dots.add(dot)
        
        panel1 = VGroup(frame1, noise_dots)
        label1 = Text("Noise", font_size=18, color="#a0a0b5")
        label1.next_to(frame1, DOWN, buff=0.2)
        
        self.play(FadeIn(panel1, scale=0.95), FadeIn(label1), run_time=1.5)
        
        # ========== Phase 3: Panel 2 - Rough Image ==========
        frame2 = Square(side_length=panel_size, color=BLUE_C, 
                       fill_opacity=0.05, stroke_width=2)
        frame2.move_to([x_positions[1], panel_y, 0])
        
        rough_circle = Circle(radius=0.45, color=BLUE_B, fill_opacity=0.25, 
                             stroke_opacity=0.6, stroke_width=2)
        rough_circle.move_to([x_positions[1], panel_y, 0])
        
        rough_dots = VGroup()
        for _ in range(45):
            angle = np.random.uniform(0, 2 * np.pi)
            r = np.random.uniform(0.15, 0.6)
            dx = r * np.cos(angle)
            dy = r * np.sin(angle)
            color = random.choice(["#c0c0d0", "#9090a8", "#7a7a90"])
            dot = Dot(point=[x_positions[1] + dx, panel_y + dy, 0], 
                     radius=0.018, color=color, fill_opacity=0.5)
            rough_dots.add(dot)
        
        panel2 = VGroup(frame2, rough_dots, rough_circle)
        label2 = Text("Rough Image", font_size=18, color="#a0a0b5")
        label2.next_to(frame2, DOWN, buff=0.2)
        
        arrow1 = Arrow(frame1.get_right(), frame2.get_left(),
                      buff=0.08, color=WHITE, stroke_width=3,
                      max_tip_length_to_length_ratio=0.25)
        
        self.play(Create(arrow1), FadeIn(panel2, scale=0.95), FadeIn(label2), run_time=2)
        
        # ========== Phase 4: Panel 3 - Clearer Image ==========
        frame3 = Square(side_length=panel_size, color=BLUE_C, 
                       fill_opacity=0.05, stroke_width=2)
        frame3.move_to([x_positions[2], panel_y, 0])
        
        clear_circle = Circle(radius=0.5, color=BLUE_A, fill_opacity=0.75, 
                             stroke_width=2, stroke_color=WHITE)
        clear_circle.move_to([x_positions[2], panel_y, 0])
        
        clear_dots = VGroup()
        for _ in range(15):
            angle = np.random.uniform(0, 2 * np.pi)
            r = np.random.uniform(0.2, 0.6)
            dx = r * np.cos(angle)
            dy = r * np.sin(angle)
            dot = Dot(point=[x_positions[2] + dx, panel_y + dy, 0], 
                     radius=0.014, color="#8080a0", fill_opacity=0.3)
            clear_dots.add(dot)
        
        panel3 = VGroup(frame3, clear_dots, clear_circle)
        label3 = Text("Clearer Image", font_size=18, color="#a0a0b5")
        label3.next_to(frame3, DOWN, buff=0.2)
        
        arrow2 = Arrow(frame2.get_right(), frame3.get_left(),
                      buff=0.08, color=WHITE, stroke_width=3,
                      max_tip_length_to_length_ratio=0.25)
        
        self.play(Create(arrow2), FadeIn(panel3, scale=0.95), FadeIn(label3), run_time=2)
        
        # ========== Phase 5: Panel 4 - Final Image ==========
        frame4 = Square(side_length=panel_size, color=BLUE_C, 
                       fill_opacity=0.05, stroke_width=2)
        frame4.move_to([x_positions[3], panel_y, 0])
        
        final_circle = Circle(radius=0.55, color=BLUE_A, fill_opacity=1.0, 
                             stroke_width=2.5, stroke_color=WHITE)
        final_circle.move_to([x_positions[3], panel_y, 0])
        
        panel4 = VGroup(frame4, final_circle)
        label4 = Text("Final Image", font_size=18, color="#a0a0b5")
        label4.next_to(frame4, DOWN, buff=0.2)
        
        arrow3 = Arrow(frame3.get_right(), frame4.get_left(),
                      buff=0.08, color=WHITE, stroke_width=3,
                      max_tip_length_to_length_ratio=0.25)
        
        self.play(Create(arrow3), FadeIn(panel4, scale=0.95), FadeIn(label4), run_time=2)
        
        # ========== Phase 6: Pipeline label ==========
        pipeline_label = Text("Same signal, refined over multiple steps",
                              font_size=22, color=WHITE)
        pipeline_label.move_to([0, -1.6, 0])
        self.play(FadeIn(pipeline_label), run_time=1)
        
        # ========== Phase 7: Step markers ==========
        step_texts = ["Step 1", "Step 2", "Step 3", "Step 4", "...", "Step N"]
        step_markers = VGroup()
        for t in step_texts:
            marker = Text(t, font_size=18, color="#7a7a90")
            step_markers.add(marker)
        step_markers.arrange(RIGHT, buff=0.45)
        step_markers.move_to([0, -2.5, 0])
        
        for marker in step_markers:
            self.play(FadeIn(marker, shift=UP * 0.2), run_time=0.3)
        
        # ========== Phase 8: Examples ==========
        ex_title = Text("Examples:", font_size=20, color=WHITE)
        ex1 = Text("- Diffusion Models", font_size=18, color="#a0a0b5")
        ex2 = Text("- Flow Matching", font_size=18, color="#a0a0b5")
        
        examples = VGroup(ex_title, ex1, ex2)
        examples.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        examples.move_to([5.3, 0.4, 0])
        
        self.play(FadeIn(examples, shift=LEFT * 0.3), run_time=1.5)
        
        # ========== Phase 9: Final takeaway ==========
        takeaway = Text(
            "Refinement scaling improves quality by spending more steps on denoising and correction.",
            font_size=20, color=YELLOW
        )
        takeaway.to_edge(DOWN, buff=0.4)
        
        self.play(FadeIn(takeaway, shift=UP * 0.2), run_time=2)
        
        self.wait()
