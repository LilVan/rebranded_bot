from . import terms_work
from random import choices


class Quiz:
    def __init__(self, name):
        random_terms = choices(terms_work.get_terms_for_table(), k=5)   # TODO: вынести количество вопросов в .env

        self.qna = []
        cnt = 0
        for rt in random_terms:
            qna_item = []
            cnt += 1
            qna_item.append(cnt)
            qna_item = qna_item + rt[1:]
            self.qna.append(qna_item)

            self.user_answers = []
            self.qna_iter = iter(self.qna)  # Объект-итератор для вопросов-ответов
            self.name = name
            self.is_start = True

    def next_qna(self):
        """Возвращает очередной вопрос"""
        return next(self.qna_iter)

    def record_user_answer(self, a):
        """Добавляет ответ пользователя в переменную экземпляра (список ответов)"""
        self.user_answers.append(a)

    def get_user_answers(self):
        """Возвращает список ответов пользователя"""
        return self.user_answers

    def check_quiz(self):
        """Проверяет ответы и возвращает список эмодзи"""
        correct_answers = [qna_item[2] for qna_item in self.qna]
        answers_true_false = [i == j for i, j in zip(self.user_answers, correct_answers)]
        answers_emoji = [str(atf).replace('False', '❌').replace('True', '✅') for atf in answers_true_false]
        return answers_emoji


def country_check(text):
    with open("./data/brands.csv", "r", encoding="utf-8") as f:
        for line in f.read().splitlines()[1:]:
            name, action, industry, country, rus_name = line.split(";")
            if country == text:
                return True
    return False


def name_check(text):
    with open("./data/brands.csv", "r", encoding="utf-8") as f:
        for line in f.read().splitlines()[1:]:
            name, action, industry, country, rus_name = line.split(";")
            if name == text:
                return True
    return False


def get_info(name_info='', country_info=''):
    with open("./data/brands.csv", "r", encoding="utf-8") as f:
        if name_info != '':
            for line in f.read().splitlines()[1:]:
                name, action, industry, country, rus_name = line.split(";")
                if name_info == name:
                    if rus_name == ' ':
                        return [name, action, industry, country]
                    else:
                        return [name, action, industry, country, rus_name]

        elif country_info != '':
            res = []
            for line in f.read().splitlines()[1:]:
                name, action, industry, country, rus_name = line.split(";")
                if country_info == country:
                    res.append(name)
            return res


def write_rus_name(name_info, rus_name_info):
    with open("./data/brands.csv", "r", encoding="utf-8") as f:
        lines = []
        for line in f.read().splitlines():
            name, action, industry, country, rus_name = line.split(";")
            if name_info == name:
                new_line = f'{name};{action};{industry};{country};{rus_name_info} (not checked yet)'
                lines += [new_line]
            else:
                lines += [line]
    with open("./data/brands.csv", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
