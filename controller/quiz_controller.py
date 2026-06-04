
import time
from model.question import Question, QuestionType
from utils.docx_parser import DocxParser


class QuizController:
    def __init__(self):
        self.all_questions = []
        self.current_questions = []
        self.current_index = 0
        self.start_time = None
        self.is_quizing = False

    def load_questions(self):
        self.single_questions, self.multiple_questions, self.judge_questions = DocxParser.load_all_questions()

    def start_quiz(self, question_types):
        self.current_questions = []
        if QuestionType.SINGLE in question_types:
            self.current_questions.extend(self.single_questions)
        if QuestionType.MULTIPLE in question_types:
            self.current_questions.extend(self.multiple_questions)
        if QuestionType.JUDGE in question_types:
            self.current_questions.extend(self.judge_questions)

        for q in self.current_questions:
            q.user_answer = None
            q.is_correct = None
            q.is_marked = False

        self.current_index = 0
        self.start_time = time.time()
        self.is_quizing = True

    def get_current_question(self):
        if self.current_index < len(self.current_questions):
            return self.current_questions[self.current_index]
        return None

    def get_elapsed_time(self):
        if self.start_time:
            return int(time.time() - self.start_time)
        return 0

    def answer_question(self, answer):
        if self.current_index < len(self.current_questions):
            question = self.current_questions[self.current_index]
            question.set_user_answer(answer)
            question.is_correct = None

    def submit_current_question(self):
        question = self.get_current_question()
        if not question or question.user_answer is None:
            return None
        return question.check_answer()

    def next_question(self):
        if self.current_index < len(self.current_questions) - 1:
            self.current_index += 1
            return True
        return False

    def prev_question(self):
        if self.current_index > 0:
            self.current_index -= 1
            return True
        return False

    def go_to_question(self, index):
        if 0 <= index < len(self.current_questions):
            self.current_index = index

    def mark_current(self):
        if self.current_index < len(self.current_questions):
            self.current_questions[self.current_index].is_marked = not self.current_questions[self.current_index].is_marked

    def submit_quiz(self):
        self.is_quizing = False
        correct_count = 0
        for q in self.current_questions:
            q.check_answer()
            if q.is_correct:
                correct_count += 1
        total_count = len(self.current_questions)
        score = (correct_count / total_count) * 100 if total_count > 0 else 0
        return {
            "total": total_count,
            "correct": correct_count,
            "wrong": total_count - correct_count,
            "score": score,
            "accuracy": correct_count / total_count if total_count > 0 else 0
        }

    def get_wrong_questions(self):
        wrong = []
        for q in self.current_questions:
            q.check_answer()
            if not q.is_correct:
                wrong.append(q)
        return wrong

    def get_submitted_count(self):
        return sum(1 for q in self.current_questions if q.is_correct is not None)
