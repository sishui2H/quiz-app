
import os
import sys
import platform
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.text import LabelBase

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 配置中文字体
def configure_chinese_font():
    system = platform.system()
    font_paths = []
    
    if system == 'Windows':
        # Windows 常见中文字体路径
        font_paths = [
            'C:\\Windows\\Fonts\\msyh.ttc',      # 微软雅黑
            'C:\\Windows\\Fonts\\simhei.ttf',    # 黑体
            'C:\\Windows\\Fonts\\simsun.ttc',    # 宋体
        ]
    elif system == 'Darwin':
        # macOS 常见中文字体
        font_paths = [
            '/System/Library/Fonts/PingFang.ttc',
            '/System/Library/Fonts/STHeiti Light.ttc',
        ]
    else:
        # Linux
        font_paths = [
            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                LabelBase.register(name='ChineseFont', fn_regular=font_path)
                print(f"使用字体: {font_path}")
                return 'ChineseFont'
            except Exception as e:
                print(f"加载字体失败 {font_path}: {e}")
    
    print("未找到中文字体，使用默认字体")
    return None

# 设置中文字体
CHINESE_FONT = configure_chinese_font()

from controller.quiz_controller import QuizController
from model.question import QuestionType

# 配置窗口大小（移动设备适配）
Window.size = (400, 600)


class HomeScreen(Screen):
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.instant_feedback = False
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 标题
        title = Label(
            text='毛概答题练习系统',
            font_size=28,
            size_hint_y=0.15,
            font_name=CHINESE_FONT
        )
        layout.add_widget(title)
        
        # 模式选择
        mode_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.1)
        self.instant_check = CheckBox(active=False, size_hint_x=0.2)
        mode_layout.add_widget(self.instant_check)
        mode_layout.add_widget(Label(text='即时反馈模式', font_size=18, size_hint_x=0.8, font_name=CHINESE_FONT))
        layout.add_widget(mode_layout)
        
        # 题型选择
        self.single_check = CheckBox(active=True, size_hint_x=0.2)
        self.multiple_check = CheckBox(active=True, size_hint_x=0.2)
        self.judge_check = CheckBox(active=True, size_hint_x=0.2)
        
        options_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=0.35)
        
        for text, check in [
            ('单选题', self.single_check),
            ('多选题', self.multiple_check),
            ('判断题', self.judge_check)
        ]:
            row = BoxLayout(orientation='horizontal', spacing=10)
            row.add_widget(check)
            row.add_widget(Label(text=text, font_size=20, size_hint_x=0.8, font_name=CHINESE_FONT))
            options_layout.add_widget(row)
        
        layout.add_widget(options_layout)
        
        # 开始按钮
        start_btn = Button(
            text='开始答题',
            font_size=24,
            size_hint_y=0.25,
            background_color=(0.2, 0.7, 0.3, 1),
            font_name=CHINESE_FONT
        )
        start_btn.bind(on_press=self.start_quiz)
        layout.add_widget(start_btn)
        
        self.add_widget(layout)
    
    def start_quiz(self, instance):
        selected_types = []
        if self.single_check.active:
            selected_types.append(QuestionType.SINGLE)
        if self.multiple_check.active:
            selected_types.append(QuestionType.MULTIPLE)
        if self.judge_check.active:
            selected_types.append(QuestionType.JUDGE)
        
        if not selected_types:
            return
        
        self.controller.start_quiz(selected_types)
        quiz_screen = self.manager.get_screen('quiz')
        quiz_screen.instant_feedback = self.instant_check.active
        self.manager.current = 'quiz'


class QuizScreen(Screen):
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.instant_feedback = False
        self.feedback_shown = False
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 顶部信息栏
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        self.question_num_label = Label(text='题目 1/100', font_size=16, font_name=CHINESE_FONT)
        self.time_label = Label(text='用时: 00:00', font_size=16, font_name=CHINESE_FONT)
        top_bar.add_widget(self.question_num_label)
        top_bar.add_widget(self.time_label)
        layout.add_widget(top_bar)
        
        # 题目区域（可滚动）
        scroll = ScrollView()
        self.question_layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        self.question_layout.bind(minimum_height=self.question_layout.setter('height'))
        scroll.add_widget(self.question_layout)
        layout.add_widget(scroll)
        
        # 底部按钮栏
        bottom_bar = BoxLayout(orientation='horizontal', size_hint_y=0.15, spacing=10)
        
        prev_btn = Button(text='上一题', font_size=18, font_name=CHINESE_FONT)
        prev_btn.bind(on_press=self.prev_question)
        
        mark_btn = Button(text='标记', font_size=18, font_name=CHINESE_FONT)
        mark_btn.bind(on_press=self.toggle_mark)
        
        submit_btn = Button(text='交卷', font_size=18, background_color=(0.9, 0.3, 0.3, 1), font_name=CHINESE_FONT)
        submit_btn.bind(on_press=self.submit_quiz)
        
        next_btn = Button(text='下一题', font_size=18, font_name=CHINESE_FONT)
        next_btn.bind(on_press=self.next_question)
        
        bottom_bar.add_widget(prev_btn)
        bottom_bar.add_widget(mark_btn)
        bottom_bar.add_widget(submit_btn)
        bottom_bar.add_widget(next_btn)
        layout.add_widget(bottom_bar)
        
        self.add_widget(layout)
    
    def on_pre_enter(self):
        self.feedback_shown = False
        self.update_question()
        self.start_timer()
    
    def on_leave(self):
        self.stop_timer()
    
    def start_timer(self):
        self.timer_event = Clock.schedule_interval(self.update_time, 1)
    
    def stop_timer(self):
        if hasattr(self, 'timer_event'):
            Clock.unschedule(self.timer_event)
    
    def update_time(self, dt):
        elapsed = self.controller.get_elapsed_time()
        minutes = elapsed // 60
        seconds = elapsed % 60
        self.time_label.text = f'用时: {minutes:02d}:{seconds:02d}'
    
    def update_question(self):
        question = self.controller.get_current_question()
        if not question:
            return
        
        total = len(self.controller.current_questions)
        idx = self.controller.current_index + 1
        self.question_num_label.text = f'题目 {idx}/{total}'
        self.feedback_shown = False
        
        # 清空当前内容
        self.question_layout.clear_widgets()
        
        # 题目内容
        content_label = Label(
            text=f'{idx}. {question.content}',
            font_size=18,
            text_size=(380, None),
            size_hint_y=None,
            valign='top',
            font_name=CHINESE_FONT
        )
        content_label.bind(texture_size=content_label.setter('size'))
        self.question_layout.add_widget(content_label)
        
        # 选项
        self.answer_buttons = []
        for i, option in enumerate(question.options):
            btn = Button(
                text=option,
                font_size=16,
                size_hint_y=None,
                height=50,
                background_normal='',
                background_color=(0.8, 0.8, 0.8, 1),
                font_name=CHINESE_FONT
            )
            btn.answer_idx = i
            btn.bind(on_press=self.select_answer)
            self.answer_buttons.append(btn)
            self.question_layout.add_widget(btn)
        
        # 恢复已选答案
        if question.user_answer is not None:
            self.highlight_answer(question.user_answer)
            if self.instant_feedback and question.is_correct is not None:
                self.show_feedback()
    
    def select_answer(self, instance):
        question = self.controller.get_current_question()
        if not question:
            return
        
        if question.type == QuestionType.SINGLE or question.type == QuestionType.JUDGE:
            # 单选题和判断题
            answer_text = instance.text.split('.')[0].strip()
            self.controller.answer_question(answer_text)
            self.highlight_answer(answer_text)
            
            if self.instant_feedback and not self.feedback_shown:
                question.check_answer()
                self.show_feedback()
    
    def highlight_answer(self, answer):
        for btn in self.answer_buttons:
            if answer in btn.text:
                btn.background_color = (0.3, 0.6, 0.9, 1)
            else:
                btn.background_color = (0.8, 0.8, 0.8, 1)
    
    def show_feedback(self):
        question = self.controller.get_current_question()
        if not question:
            return
        
        self.feedback_shown = True
        
        # 更新选项颜色：正确绿色，错误红色
        for btn in self.answer_buttons:
            option_label = btn.text.split('.')[0].strip()
            if option_label == question.answer:
                btn.background_color = (0.2, 0.8, 0.3, 1)
            elif question.user_answer and option_label == question.user_answer and not question.is_correct:
                btn.background_color = (0.9, 0.3, 0.3, 1)
        
        # 添加反馈文本
        feedback_text = '回答正确！' if question.is_correct else f'回答错误！正确答案是 {question.answer}'
        feedback_label = Label(
            text=feedback_text,
            font_size=18,
            size_hint_y=None,
            height=40,
            color=(0.2, 0.6, 0.9, 1) if question.is_correct else (0.9, 0.3, 0.3, 1),
            font_name=CHINESE_FONT
        )
        self.question_layout.add_widget(feedback_label)
    
    def next_question(self, instance):
        if self.controller.next_question():
            self.update_question()
    
    def prev_question(self, instance):
        if self.controller.prev_question():
            self.update_question()
    
    def toggle_mark(self, instance):
        self.controller.mark_current()
        question = self.controller.get_current_question()
        instance.text = '已标记' if question.is_marked else '标记'
        instance.font_name = CHINESE_FONT
    
    def submit_quiz(self, instance):
        self.stop_timer()
        self.manager.current = 'result'


class ResultScreen(Screen):
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.add_widget(self.layout)
    
    def on_pre_enter(self):
        self.show_result()
    
    def show_result(self):
        self.layout.clear_widgets()
        result = self.controller.submit_quiz()
        
        # 成绩展示
        score_label = Label(
            text=f'得分: {result["score"]:.1f}',
            font_size=36,
            color=(0.2, 0.8, 0.3, 1),
            font_name=CHINESE_FONT
        )
        self.layout.add_widget(score_label)
        
        # 统计信息
        stats = BoxLayout(orientation='vertical', spacing=10)
        stats.add_widget(Label(text=f'总题数: {result["total"]}', font_size=20, font_name=CHINESE_FONT))
        stats.add_widget(Label(text=f'正确: {result["correct"]}', font_size=20, color=(0.2, 0.8, 0.3, 1), font_name=CHINESE_FONT))
        stats.add_widget(Label(text=f'错误: {result["wrong"]}', font_size=20, color=(0.9, 0.3, 0.3, 1), font_name=CHINESE_FONT))
        stats.add_widget(Label(text=f'正确率: {result["accuracy"]*100:.1f}%', font_size=20, font_name=CHINESE_FONT))
        self.layout.add_widget(stats)
        
        # 返回首页按钮
        back_btn = Button(
            text='返回首页',
            font_size=22,
            size_hint_y=0.3,
            background_color=(0.3, 0.5, 0.8, 1),
            font_name=CHINESE_FONT
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        self.layout.add_widget(back_btn)


class QuizApp(App):
    def build(self):
        self.copy_resources()
        self.controller = QuizController()
        self.controller.load_questions()
        
        sm = ScreenManager()
        sm.add_widget(HomeScreen(self.controller, name='home'))
        sm.add_widget(QuizScreen(self.controller, name='quiz'))
        sm.add_widget(ResultScreen(self.controller, name='result'))
        
        return sm
    
    def copy_resources(self):
        # 在 Android 上把资源文件复制到可访问的位置
        try:
            from kivy.utils import platform
            if platform == 'android':
                from android.storage import app_storage_path
                from kivy.resources import resource_find
                import shutil
                
                app_dir = app_storage_path()
                docx_files = [
                    '给学生的练习题（单选300）.docx',
                    '给学生的练习题（多选200）.docx',
                    '给学生的练习题（判断100）.docx'
                ]
                
                for filename in docx_files:
                    src = resource_find(filename)
                    if src:
                        dst = os.path.join(app_dir, filename)
                        if not os.path.exists(dst):
                            shutil.copy(src, dst)
                            print(f"Copied {filename} to {dst}")
        except Exception as e:
            print(f"Error copying resources: {e}")


if __name__ == '__main__':
    QuizApp().run()
