from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

class WhatIsWorldModelScene(VoiceoverScene):
    FONT = "Arial"
    ASSETS_FOLDER = "src/assets/"

    def construct(self):
        self.ai_dream_up_solution()
        self.wait(4)
        self.clear()

        self.introduce_world_model_paper()
        self.wait(2)
        self.clear()

        self.phase_world_model_definition()
        self.wait(0.6)
        self.clear()

        self.phase_agent_definition()
        self.wait(0.6)
        self.clear()

        #self.phase_agent_environment_sketch()
        #self.wait(0.8)
        #self.clear()

        self.phase_interaction_loop()
        self.wait(1.5)

    def phase_agent_environment_sketch(self):
        title = Text("Vòng lặp Agent - Environment", font="Segoe UI", weight=BOLD).scale(0.72)
        title.to_edge(UP)

        agent_head = RoundedRectangle(corner_radius=0.08, width=1.1, height=0.8, color=GRAY_B)
        agent_head.set_fill(GRAY_D, opacity=0.9)
        agent_head.shift(LEFT * 4.5 + UP * 0.7)
        agent_body = RoundedRectangle(corner_radius=0.08, width=1.4, height=1.2, color=GRAY_B)
        agent_body.set_fill(GRAY_D, opacity=0.9)
        agent_body.next_to(agent_head, DOWN, buff=0.06)
        eye_l = Dot(color=RED, radius=0.08).move_to(agent_head.get_left() + RIGHT * 0.32 + UP * 0.06)
        eye_r = Dot(color=RED, radius=0.08).move_to(agent_head.get_right() + LEFT * 0.32 + UP * 0.06)
        antenna = Line(agent_head.get_top(), agent_head.get_top() + UP * 0.35, color=GRAY_B)
        antenna_dot = Dot(color=GRAY_B, radius=0.05).move_to(antenna.get_end())
        arm_l = Line(agent_body.get_left() + UP * 0.2, agent_body.get_left() + LEFT * 0.45 + DOWN * 0.25, color=GRAY_B)
        arm_r = Line(agent_body.get_right() + UP * 0.2, agent_body.get_right() + RIGHT * 0.45 + DOWN * 0.25, color=GRAY_B)
        leg_l = Line(agent_body.get_bottom() + LEFT * 0.25, agent_body.get_bottom() + LEFT * 0.45 + DOWN * 0.5, color=GRAY_B)
        leg_r = Line(agent_body.get_bottom() + RIGHT * 0.25, agent_body.get_bottom() + RIGHT * 0.45 + DOWN * 0.5, color=GRAY_B)
        agent_group = VGroup(
            agent_head,
            agent_body,
            eye_l,
            eye_r,
            antenna,
            antenna_dot,
            arm_l,
            arm_r,
            leg_l,
            leg_r,
        )
        agent_label = Text("agent", font="Consolas", weight=BOLD).scale(0.44)
        agent_label.next_to(agent_group, UP, buff=0.18)

        earth = Circle(radius=1.15, color=BLUE_D)
        earth.set_fill(BLUE_E, opacity=0.95)
        earth.shift(RIGHT * 3.6 + DOWN * 0.2)
        land_1 = VMobject(color=GREEN_C, fill_opacity=0.95, stroke_width=0)
        land_1.set_points_as_corners(
            [
                earth.get_center() + LEFT * 0.45 + UP * 0.55,
                earth.get_center() + LEFT * 0.1 + UP * 0.85,
                earth.get_center() + RIGHT * 0.18 + UP * 0.45,
                earth.get_center() + RIGHT * 0.05 + UP * 0.05,
                earth.get_center() + LEFT * 0.2 + DOWN * 0.15,
                earth.get_center() + LEFT * 0.42 + UP * 0.1,
            ]
        )
        land_1.close_path()
        land_2 = VMobject(color=GREEN_C, fill_opacity=0.95, stroke_width=0)
        land_2.set_points_as_corners(
            [
                earth.get_center() + RIGHT * 0.35 + UP * 0.62,
                earth.get_center() + RIGHT * 0.68 + UP * 0.55,
                earth.get_center() + RIGHT * 0.6 + UP * 0.25,
                earth.get_center() + RIGHT * 0.35 + UP * 0.3,
            ]
        )
        land_2.close_path()
        env_group = VGroup(earth, land_1, land_2)
        env_label = Text("environment", font="Consolas", weight=BOLD).scale(0.44)
        env_label.next_to(env_group, UP, buff=0.18)

        arrow_action = CurvedArrow(
            start_point=agent_group.get_top() + RIGHT * 0.9,
            end_point=env_group.get_top() + LEFT * 0.9,
            angle=-PI / 2.6,
            stroke_width=5,
            color=BLACK,
        )
        action_text = Text("từ trạng thái s, chọn hành động a", font="Segoe UI").scale(0.35)
        action_text.next_to(arrow_action, UP, buff=0.1)

        arrow_reward = CurvedArrow(
            start_point=env_group.get_bottom() + LEFT * 0.9,
            end_point=agent_group.get_bottom() + RIGHT * 0.9,
            angle=-PI / 2.8,
            stroke_width=5,
            color=BLACK,
        )
        reward_text = Text("nhận phần thưởng R, trạng thái mới s'", font="Segoe UI").scale(0.34)
        reward_text.next_to(arrow_reward, DOWN * 0.7, buff=0.1)

        self.play(FadeIn(title, shift=UP * 0.15))
        self.play(FadeIn(agent_group), FadeIn(agent_label), run_time=0.8)
        self.play(FadeIn(env_group), FadeIn(env_label), run_time=0.8)
        self.play(Create(arrow_action), FadeIn(action_text, shift=UP * 0.1), run_time=3)
        self.play(Create(arrow_reward), FadeIn(reward_text, shift=DOWN * 0.1), run_time=3)
        self.play(
            agent_group.animate.shift(UP * 0.08),
            rate_func=there_and_back,
            run_time=0.5,
        )

    def phase_world_model_definition(self):
        title = Text("World model là gì?", font=self.FONT, weight=BOLD).scale(0.8)
        title.to_edge(UP)

        real_world = RoundedRectangle(corner_radius=0.15, width=4.6, height=2.4, color=BLUE_C)
        real_world.set_fill(BLUE_E, opacity=0.35)
        real_world.shift(LEFT * 3.1)
        real_label = Text("Thế giới thật", font="Segoe UI", weight=MEDIUM).scale(0.5)
        real_label.move_to(real_world.get_top() + DOWN * 0.35)
        real_desc = Text(
            "Dữ liệu cảm biến, hình ảnh,\n"
            "hành động, phần thưởng",
            font="Segoe UI",
        ).scale(0.36)
        real_desc.move_to(real_world.get_center() + DOWN * 0.35)

        model_box = RoundedRectangle(corner_radius=0.15, width=4.8, height=2.4, color=GREEN_C)
        model_box.set_fill(GREEN_E, opacity=0.35)
        model_box.shift(RIGHT * 3.1)
        model_label = Text("World model", font="Segoe UI", weight=BOLD).scale(0.56)
        model_label.move_to(model_box.get_top() + DOWN * 0.35)
        model_desc = Text(
            "Mô hình học cách dự đoán\n"
            "trạng thái tiếp theo của môi trường",
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

    def phase_agent_definition(self):
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

        obs_arrow = Arrow(env.get_left() + DOWN * 0.55, agent_body.get_right() + DOWN * 0.55, buff=0.16, stroke_width=4)
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

    def phase_interaction_loop(self):
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

        loop_text_1 = Text("1) World model sinh kịch bản", font="Segoe UI").scale(0.33)
        loop_text_2 = Text("2) Agent thử nhiều chiến lược", font="Segoe UI").scale(0.33)
        loop_text_3 = Text("3) Học nhanh hơn, tổng quát tốt hơn", font="Segoe UI").scale(0.33)
        loop_text = VGroup(loop_text_1, loop_text_2, loop_text_3).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
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

    def ai_dream_up_solution(self):
        title = Text("AI có thể tưởng tượng?", font=self.FONT)
        img = ImageMobject(self.ASSETS_FOLDER + "1-people-imagination.png")
        title.to_edge(UP)
        self.play(FadeIn(img),Write(title))

    def introduce_world_model_paper(self):
        text = Text(
            "Một bài báo nghiên cứu về các tạo thế giới giả lập cho AI tương tác",
            font=self.FONT
        )
        text.to_edge(DOWN)
        text.scale(0.4)

        paper = ImageMobject(self.ASSETS_FOLDER + "1-world-model-paper.png")
        website = ImageMobject(self.ASSETS_FOLDER + "1-world-model-website.png")

        paper.scale(0.8).to_edge(RIGHT)
        website.scale(0.5).to_edge(LEFT)

        self.play(
            Write(text),
            FadeIn(paper),
            FadeIn(website)
        )


class WhatIsWorldModelNarratedScene(WhatIsWorldModelScene):
    def say(self, text, hold=0.15):
        with self.voiceover(text=text) as tracker:
            self.wait(tracker.duration + hold)

    def construct(self):
        self.set_speech_service(GTTSService(lang="vi", tld="com.vn"), create_subcaption=False)

        self.say("Trong đoạn này, chúng ta sẽ nhìn World Model theo một góc rất đơn giản: nó là cách để AI học về thế giới, thay vì chỉ học thuộc dữ liệu.", 0.2)
        self.ai_dream_up_solution()
        self.say("Nói cách khác, AI không chỉ trả lời câu hỏi hay tạo nội dung. Nó còn có thể tưởng tượng ra một không gian giả lập, nơi ta thử ý tưởng trước khi đem ra thế giới thật.", 0.2)
        self.wait(0.8)
        self.clear()

        self.say("Nếu nhìn vào những tín hiệu gần đây, ta thấy World Model đang được quan tâm mạnh trở lại. Không chỉ vì nghiên cứu, mà còn vì nhiều công ty lớn đang để ý tới hướng này.", 0.2)
        self.introduce_world_model_paper()
        self.say("Điều đó cho thấy câu chuyện về World Model không còn là lý thuyết xa vời nữa. Nó đang dần trở thành một hướng rất thực tế cho AI hiện đại.", 0.2)
        self.wait(0.8)
        self.clear()

        self.say("Vậy World Model là gì? Hiểu ngắn gọn, đây là mô hình học cách dự đoán trạng thái tiếp theo của môi trường khi ta đưa vào một hành động.", 0.2)
        self.phase_world_model_definition()
        self.say("Thay vì chỉ nhìn vào dữ liệu tĩnh, nó học được quy luật chuyển động của thế giới: điều gì có thể xảy ra tiếp theo, và kết quả có thể trông như thế nào.", 0.2)
        self.wait(0.8)
        self.clear()

        self.say("Còn agent là gì? Agent là thực thể ra quyết định. Nó quan sát môi trường, chọn hành động, rồi nhận phản hồi để học cách làm tốt hơn ở lần sau.", 0.2)
        self.phase_agent_definition()
        self.say("Nếu World Model là thứ mô phỏng thế giới, thì agent là thứ đang sống trong mô phỏng đó để thử, sai, và cải thiện chiến lược của mình.", 0.2)
        self.wait(0.8)
        self.clear()

        self.say("Khi ghép agent với World Model, ta có thể sinh ra rất nhiều kịch bản mô phỏng. Đây là điểm rất quan trọng, vì agent có thể luyện tập trong vô số tình huống mà ngoài đời thật có thể khó hoặc tốn kém để tạo ra.", 0.2)
        self.phase_interaction_loop()
        self.say("Tóm lại, World Model giúp tạo ra một 'phòng thí nghiệm' cho agent. Còn agent là người học trong phòng thí nghiệm đó để tiến bộ nhanh hơn và tổng quát tốt hơn.", 0.2)
        self.wait(1.2)