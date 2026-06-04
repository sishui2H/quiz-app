
from enum import Enum

class QuestionType(Enum):
    SINGLE = "single"    # 单选题
    MULTIPLE = "multiple"  # 多选题
    JUDGE = "judge"     # 判断题

class Question:
    def __init__(self, question_id, question_type, content, options, answer):
        self.id = question_id
        self.type = question_type
        self.content = content
        self.options = options
        self.answer = answer
        self.user_answer = None
        self.is_correct = None
        self.is_marked = False  # 是否标记为不确定

    def set_user_answer(self, answer):
        self.user_answer = answer

    def check_answer(self):
        if self.user_answer is None:
            self.is_correct = False
            return False
        user_ans = str(self.user_answer).strip().upper()
        correct_ans = str(self.answer).strip().upper()
        self.is_correct = (user_ans == correct_ans)
        return self.is_correct

    def get_type_name(self):
        type_names = {
            QuestionType.SINGLE: "单选题",
            QuestionType.MULTIPLE: "多选题",
            QuestionType.JUDGE: "判断题"
        }
        return type_names.get(self.type, "未知题型")

    def __repr__(self):
        return "Question(id={}, type={}, content={}...)".format(self.id, self.type, self.content[:20])
