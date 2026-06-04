import os
import sys
import platform
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.core.window import Window
from kivy.core.text import LabelBase

# 配置中文字体
def configure_chinese_font():
    system = platform.system()
    font_paths = []
    
    if system == 'Windows':
        font_paths = [
            'C:\\Windows\\Fonts\\msyh.ttc',
            'C:\\Windows\\Fonts\\simhei.ttf',
        ]
    elif system == 'Darwin':
        font_paths = [
            '/System/Library/Fonts/PingFang.ttc',
        ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                LabelBase.register(name='ChineseFont', fn_regular=font_path)
                print(f"Using font: {font_path}")
                return 'ChineseFont'
            except Exception as e:
                print(f"Failed to load font {font_path}: {e}")
    
    print("Using default font")
    return None

CHINESE_FONT = configure_chinese_font()
Window.size = (400, 600)

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=20, **kwargs)
        
        title = Label(
            text='毛概答题练习系统',
            font_size=28,
            font_name=CHINESE_FONT
        )
        self.add_widget(title)
        
        info = Label(
            text='APK 打包成功！',
            font_size=20,
            font_name=CHINESE_FONT
        )
        self.add_widget(info)

class QuizApp(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    QuizApp().run()
