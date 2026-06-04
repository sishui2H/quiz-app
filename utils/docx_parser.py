
import os
import re
import sys
from docx import Document
from model.question import Question, QuestionType


class DocxParser:
    def __init__(self):
        pass

    @staticmethod
    def get_resource_path(file_name):
        # Kivy/Android 资源路径
        try:
            from kivy.utils import platform
            if platform == 'android':
                from kivy.resources import resource_find
                path = resource_find(file_name)
                if path:
                    return path
                from android.storage import app_storage_path
                return os.path.join(app_storage_path(), file_name)
        except ImportError:
            pass
        
        # PyInstaller 打包路径
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, file_name)

        # 本地开发路径
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        local_path = os.path.join(project_root, file_name)
        if os.path.exists(local_path):
            return local_path

        parent_dir = os.path.dirname(project_root)
        return os.path.join(parent_dir, file_name)

    @staticmethod
    def extract_questions_from_docx(file_path, question_type):
        doc = Document(file_path)
        questions = []

        text_lines = []
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                text_lines.append(text)

        if question_type == QuestionType.JUDGE:
            questions = DocxParser._parse_judge_questions(text_lines)
        elif question_type == QuestionType.SINGLE:
            questions = DocxParser._parse_single_questions(text_lines)
        elif question_type == QuestionType.MULTIPLE:
            questions = DocxParser._parse_multiple_questions(text_lines)

        for i, q in enumerate(questions):
            q.id = i + 1

        return questions

    @staticmethod
    def _parse_judge_questions(text_lines):
        questions = []
        for line in text_lines:
            # 跳过只有"答案"的行
            if line.strip() == "答案：" or line.strip() == "答案:":
                continue

            # 看看是否有答案标记
            answer = None
            content = line

            # 尝试匹配各种格式
            # 格式1: （√）或（×）
            match1 = re.search(r'[（\(]([√×])[）\)]', content)
            # 格式2: （√ ）或（× ）有空格的
            match1_sp = re.search(r'[（\(]([√×])\s*[）\)]', content)
            # 格式3: 答案：√ 或答案：×
            match2 = re.search(r'答案[:：]\s*([√×])', content)
            # 格式4: （ ）答案：√ 这种
            match3 = re.search(r'（\s*）答案[:：]\s*([√×])', content)

            if match1_sp:
                answer = "正确" if match1_sp.group(1) == "√" else "错误"
                content = re.sub(r'[（\(]([√×])\s*[）\)]', '', content).strip()
            elif match1:
                answer = "正确" if match1.group(1) == "√" else "错误"
                content = re.sub(r'[（\(]([√×])[）\)]', '', content).strip()
            elif match2:
                answer = "正确" if match2.group(1) == "√" else "错误"
                content = re.sub(r'答案[:：]\s*([√×])', '', content).strip()
            elif match3:
                answer = "正确" if match3.group(1) == "√" else "错误"
                content = re.sub(r'（\s*）答案[:：]\s*([√×])', '', content).strip()

            # 如果找到了答案，并且内容里有文字
            if answer and len(content) > 5:
                q = Question(
                    question_id=len(questions) + 1,
                    question_type=QuestionType.JUDGE,
                    content=content,
                    options=["正确", "错误"],
                    answer=answer
                )
                questions.append(q)

        return questions

    @staticmethod
    def _parse_single_questions(text_lines):
        questions = []
        full_text = "\n".join(text_lines)
        ans_pattern = r'正确答案[:：]\s*([A-D])'
        answer_matches = list(re.finditer(ans_pattern, full_text))
        start_index = 0

        for ans_match in answer_matches:
            block = full_text[start_index:ans_match.start()].strip()
            answer = ans_match.group(1)
            start_index = ans_match.end()

            if not block:
                continue

            lines = [line.strip() for line in block.splitlines() if line.strip()]
            content_lines = []
            option_map = {}
            current_label = None

            for line in lines:
                option_match = re.match(r'^([A-D])[\.、]\s*(.*)$', line)
                if option_match:
                    current_label = option_match.group(1)
                    option_map[current_label] = option_match.group(2).strip()
                elif current_label:
                    option_map[current_label] = (option_map[current_label] + " " + line).strip()
                else:
                    content_lines.append(line)

            content = " ".join(content_lines).strip()
            content = re.sub(r'^\d+\s*[\.、]\s*', '', content)
            content = re.sub(r'^\d+\s+', '', content)

            options = []
            for label in ["A", "B", "C", "D"]:
                if label in option_map and option_map[label]:
                    options.append(label + ". " + option_map[label])

            if answer and content and options:
                q = Question(
                    question_id=len(questions) + 1,
                    question_type=QuestionType.SINGLE,
                    content=content,
                    options=options,
                    answer=answer
                )
                questions.append(q)
        return questions

    @staticmethod
    def _parse_multiple_questions(text_lines):
        questions = []
        full_text = "\n".join(text_lines)
        ans_pattern = r'答案[:：]\s*([A-Z]+)'
        answer_matches = list(re.finditer(ans_pattern, full_text))
        start_index = 0

        for ans_match in answer_matches:
            block = full_text[start_index:ans_match.start()].strip()
            answer = ans_match.group(1)
            start_index = ans_match.end()

            if not block:
                continue

            lines = [line.strip() for line in block.splitlines() if line.strip()]
            content_lines = []
            option_map = {}
            current_label = None

            for line in lines:
                if re.match(r'^[一二三四五六七八九十]+、', line):
                    continue

                option_match = re.match(r'^([A-Z])[\.、]\s*(.*)$', line)
                if option_match:
                    current_label = option_match.group(1)
                    option_map[current_label] = option_match.group(2).strip()
                elif current_label:
                    option_map[current_label] = (option_map[current_label] + " " + line).strip()
                else:
                    content_lines.append(line)

            content = " ".join(content_lines).strip()
            content = re.sub(r'^\d+\s*[\.、]\s*', '', content)
            content = re.sub(r'^\d+\s+', '', content)

            options = []
            for label in ["A", "B", "C", "D", "E", "F"]:
                if label in option_map and option_map[label]:
                    options.append(label + ". " + option_map[label])

            if answer and content and options:
                q = Question(
                    question_id=len(questions) + 1,
                    question_type=QuestionType.MULTIPLE,
                    content=content,
                    options=options,
                    answer=answer
                )
                questions.append(q)
        return questions

    @staticmethod
    def load_all_questions():
        single_path = DocxParser.get_resource_path("给学生的练习题（单选300）.docx")
        multiple_path = DocxParser.get_resource_path("给学生的练习题（多选200）.docx")
        judge_path = DocxParser.get_resource_path("给学生的练习题（判断100）.docx")

        single_questions = DocxParser.extract_questions_from_docx(single_path, QuestionType.SINGLE)
        multiple_questions = DocxParser.extract_questions_from_docx(multiple_path, QuestionType.MULTIPLE)
        judge_questions = DocxParser.extract_questions_from_docx(judge_path, QuestionType.JUDGE)

        return single_questions, multiple_questions, judge_questions
