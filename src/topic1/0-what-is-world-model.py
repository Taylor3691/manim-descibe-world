from manim import *
from pathlib import Path
import shutil
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService


class WhatIsWorldModelScene(VoiceoverScene):
    FONT = "Arial"
    ASSETS_FOLDER = (Path(__file__).resolve().parent.parent / "assets").as_posix()
    VOICE_SPEED = 2
    ANIMATION_SPEED = 1.0

    def asset_path(self, filename: str) -> str:
        return f"{self.ASSETS_FOLDER}/{filename}"

    def say(self, text: str, hold: float = 0.15):
        with self.voiceover(text=text) as tracker:
            self.wait(tracker.duration + hold)

    def play(self, *args, **kwargs):
        if "run_time" in kwargs:
            kwargs["run_time"] /= self.ANIMATION_SPEED
        super().play(*args, **kwargs)

    def clear_scene(self, wait_time: float = 0.5, fade_time: float = 0.35):
        self.wait(wait_time)
        if self.mobjects:
            self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=fade_time)

    def construct(self):
        # Keep TTS setup in one place so switching provider is straightforward.
        has_sox = shutil.which("sox") is not None
        voice_speed = self.VOICE_SPEED if has_sox else 1.0
        self.set_speech_service(
            GTTSService(lang="vi", tld="com.vn", global_speed=voice_speed),
            create_subcaption=False,
        )

        self.show_intro_image()
        self.say(
            "Trong đoạn này, chúng ta sẽ nhìn World Model theo một góc rất đơn giản: "
            "nó là cách để AI học về thế giới, thay vì chỉ học thuộc dữ liệu.",
            0.2,
        )
        self.say(
            "Nói cách khác, AI không chỉ trả lời câu hỏi hay tạo nội dung. "
            "Nó còn có thể tưởng tượng ra một không gian giả lập, nơi ta thử ý tưởng "
            "trước khi đem ra thế giới thật.",
            0.2,
        )
        self.clear_scene()

        self.show_paper_context()
        self.say(
            "Nếu nhìn vào những tín hiệu gần đây, ta thấy World Model đang được quan tâm "
            "mạnh trở lại. Không chỉ vì nghiên cứu, mà còn vì nhiều công ty lớn đang để ý "
            "tới hướng này.",
            0.2,
        )
        self.say(
            "Điều đó cho thấy câu chuyện về World Model không còn là lý thuyết xa vời nữa. "
            "Nó đang dần trở thành một hướng rất thực tế cho AI hiện đại.",
            0.2,
        )
        self.clear_scene()

        self.show_world_model_definition()
        self.say(
            "Vậy World Model là gì? Hiểu ngắn gọn, đây là mô hình học cách dự đoán trạng thái "
            "tiếp theo của môi trường khi ta đưa vào một hành động.",
            0.2,
        )
        self.say(
            "Thay vì chỉ nhìn vào dữ liệu tĩnh, nó học được quy luật chuyển động của thế giới: "
            "điều gì có thể xảy ra tiếp theo, và kết quả có thể trông như thế nào.",
            0.2,
        )
        self.clear_scene()

        self.show_agent_definition()
        self.say(
            "Còn agent là gì? Agent là thực thể ra quyết định. Nó quan sát môi trường, "
            "chọn hành động, rồi nhận phản hồi để học cách làm tốt hơn ở lần sau.",
            0.2,
        )
        self.say(
            "Nếu World Model là thứ mô phỏng thế giới, thì agent là thứ đang sống trong mô phỏng đó "
            "để thử, sai, và cải thiện chiến lược của mình.",
            0.2,
        )
        self.clear_scene()

        self.show_interaction_loop()
        self.say(
            "Khi ghép agent với World Model, ta có thể sinh ra rất nhiều kịch bản mô phỏng. "
            "Đây là điểm rất quan trọng, vì agent có thể luyện tập trong vô số tình huống "
            "mà ngoài đời thật có thể khó hoặc tốn kém để tạo ra.",
            0.2,
        )
        self.say(
            "Tóm lại, World Model giúp tạo ra một phòng thí nghiệm cho agent. "
            "Còn agent là người học trong phòng thí nghiệm đó để tiến bộ nhanh hơn và tổng quát tốt hơn.",
            0.2,
        )
        self.wait(1.2)

    def show_intro_image(self):
        title = Text("AI có thể tưởng tượng?", font=self.FONT)
        title.to_edge(UP)
        img = ImageMobject(self.asset_path("1-people-imagination.png"))
        self.play(FadeIn(img), Write(title))

    def show_paper_context(self):
        caption = Text(
            "Một bài báo nghiên cứu về các tạo thế giới giả lập cho AI tương tác",
            font=self.FONT,
        ).scale(0.4)
        caption.to_edge(DOWN)

        paper = ImageMobject(self.asset_path("1-world-model-paper.png"))
        website = ImageMobject(self.asset_path("1-world-model-website.png"))
        paper.scale(0.8).to_edge(RIGHT)
        website.scale(0.5).to_edge(LEFT)

        self.play(Write(caption), FadeIn(paper), FadeIn(website))

    def show_world_model_definition(self):
        title = Text("World model là gì?", font=self.FONT, weight=BOLD).scale(0.8)
        title.to_edge(UP)

        real_world = RoundedRectangle(corner_radius=0.15, width=4.6, height=2.4, color=BLUE_C)
        real_world.set_fill(BLUE_E, opacity=0.35)
        real_world.shift(LEFT * 3.1)
        real_label = Text("Thế giới thật", font="Segoe UI", weight=MEDIUM).scale(0.5)
        real_label.move_to(real_world.get_top() + DOWN * 0.35)
        real_desc = Text(
            "Dữ liệu cảm biến, hình ảnh,\nhành động, phần thưởng",
            font="Segoe UI",
        ).scale(0.36)
        real_desc.move_to(real_world.get_center() + DOWN * 0.35)

        model_box = RoundedRectangle(corner_radius=0.15, width=4.8, height=2.4, color=GREEN_C)
        model_box.set_fill(GREEN_E, opacity=0.35)
        model_box.shift(RIGHT * 3.1)
        model_label = Text("World model", font="Segoe UI", weight=BOLD).scale(0.56)
        model_label.move_to(model_box.get_top() + DOWN * 0.35)
        model_desc = Text(
            "Mô hình học cách dự đoán\ntrạng thái tiếp theo của môi trường",
            font="Segoe UI",
        ).scale(0.35)
        model_desc.move_to(model_box.get_center() + DOWN * 0.35)

        arrow = Arrow(real_world.get_right(), model_box.get_left(), buff=0.2, stroke_width=4)
        arrow.set_color(YELLOW_C)
        arrow_text = Text("Học từ dữ liệu", font="Segoe UI").scale(0.35)
        arrow_text.next_to(arrow, UP, buff=0.15)

        takeaway = Text(
            "World model là bản mô phỏng nén của thế giới để dự đoán tương lai.",
            font="Segoe UI",
        ).scale(0.42)
        takeaway.set_color(YELLOW_B)
        takeaway.to_edge(DOWN)

        self.play(FadeIn(title, shift=UP * 0.2))
        self.play(FadeIn(real_world), Write(real_label), Write(real_desc))
        self.play(GrowArrow(arrow), FadeIn(arrow_text, shift=UP * 0.1))
        self.play(FadeIn(model_box), Write(model_label), Write(model_desc))
        self.play(Write(takeaway))

    def show_agent_definition(self):
        title = Text("Agent là gì?", font="Segoe UI", weight=BOLD).scale(0.8)
        title.to_edge(UP)

        env = RoundedRectangle(corner_radius=0.15, width=5.0, height=2.8, color=TEAL_C)
        env.set_fill(TEAL_E, opacity=0.35)
        env.shift(RIGHT * 2.8)
        env_label = Text("Môi trường", font="Segoe UI", weight=MEDIUM).scale(0.5)
        env_label.move_to(env.get_top() + DOWN * 0.35)

        agent_body = Circle(radius=0.62, color=BLUE_C)
        agent_body.set_fill(BLUE_E, opacity=0.7)
        agent_body.shift(LEFT * 3.4)
        agent_label = Text("Agent", font="Consolas", weight=BOLD).scale(0.46)
        agent_label.move_to(agent_body)

        action_arrow = Arrow(agent_body.get_right(), env.get_left(), buff=0.16, stroke_width=4)
        action_arrow.set_color(ORANGE)
        action_text = Text("Hành động", font="Segoe UI").scale(0.34)
        action_text.next_to(action_arrow, UP, buff=0.1)

        obs_arrow = Arrow(
            env.get_left() + DOWN * 0.55,
            agent_body.get_right() + DOWN * 0.55,
            buff=0.16,
            stroke_width=4,
        )
        obs_arrow.set_color(PURPLE_C)
        obs_text = Text("Quan sát + phần thưởng", font="Segoe UI").scale(0.32)
        obs_text.next_to(obs_arrow, DOWN, buff=0.1)

        goal = Text(
            "Agent là hệ ra quyết định để tối đa mục tiêu qua tương tác lặp.",
            font="Segoe UI",
        ).scale(0.42)
        goal.set_color(YELLOW_B)
        goal.to_edge(DOWN)

        self.play(FadeIn(title, shift=UP * 0.2))
        self.play(FadeIn(agent_body), Write(agent_label))
        self.play(FadeIn(env), Write(env_label))
        self.play(GrowArrow(action_arrow), FadeIn(action_text, shift=UP * 0.1))
        self.play(GrowArrow(obs_arrow), FadeIn(obs_text, shift=DOWN * 0.1))
        self.play(Write(goal))

    def show_interaction_loop(self):
        title = Text("Khi ghép Agent với World model", font="Segoe UI", weight=BOLD).scale(0.74)
        title.to_edge(UP)

        wm_box = RoundedRectangle(corner_radius=0.12, width=3.6, height=1.6, color=GREEN_C)
        wm_box.set_fill(GREEN_E, opacity=0.4)
        wm_box.shift(LEFT * 3 + UP * 0.7)
        wm_label = Text("World model", font="Segoe UI", weight=BOLD).scale(0.42).move_to(wm_box)

        env_box = RoundedRectangle(corner_radius=0.12, width=3.6, height=1.6, color=TEAL_C)
        env_box.set_fill(TEAL_E, opacity=0.4)
        env_box.shift(RIGHT * 3 + UP * 0.7)
        env_label = Text("Môi trường mô phỏng", font="Segoe UI", weight=MEDIUM).scale(0.38).move_to(env_box)

        agent = Dot(color=YELLOW, radius=0.1)
        agent.move_to(DOWN * 1.0)
        agent_label = Text("Agent", font="Consolas").scale(0.34).next_to(agent, DOWN, buff=0.12)

        wm_to_env = Arrow(wm_box.get_right(), env_box.get_left(), buff=0.14, stroke_width=4).set_color(GREEN_B)
        env_to_agent = Arrow(env_box.get_bottom(), agent.get_right() + UP * 0.05, buff=0.2, stroke_width=4).set_color(PURPLE_C)
        agent_to_wm = Arrow(agent.get_left() + UP * 0.05, wm_box.get_bottom(), buff=0.2, stroke_width=4).set_color(ORANGE)

        loop_text = VGroup(
            Text("1) World model sinh kịch bản", font="Segoe UI").scale(0.33),
            Text("2) Agent thử nhiều chiến lược", font="Segoe UI").scale(0.33),
            Text("3) Học nhanh hơn, tổng quát tốt hơn", font="Segoe UI").scale(0.33),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        loop_text.to_edge(DOWN)

        self.play(FadeIn(title))
        self.play(FadeIn(wm_box), Write(wm_label), FadeIn(env_box), Write(env_label))
        self.play(FadeIn(agent), FadeIn(agent_label))
        self.play(GrowArrow(wm_to_env), GrowArrow(env_to_agent), GrowArrow(agent_to_wm))

        waypoints = [
            wm_box.get_bottom() + DOWN * 0.15,
            env_box.get_bottom() + DOWN * 0.15,
            agent.get_center(),
        ]
        for _ in range(2):
            for point in waypoints:
                self.play(agent.animate.move_to(point), run_time=0.32)

        self.play(Write(loop_text), run_time=5)
