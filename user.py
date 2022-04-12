import re

import db
from datatypes import Program, College
import filters
from utils import format_declension, parse_request


class User:
    """
    Класс, определяющий диалог с пользователем.
    При создании получает id пользователя и создает новый объект, если экземпляра с
    таким id еще не было создано, в противном случае возвращает созданный ранее объект.

    Атрибуты:
    id: id пользователя
    results: словарь результатов по предметам
    found_programs: список найденных по введенным результатам программ
    filters: список фильтрующих функций
    answer: приготовленный к отправке ответ

    instances: словарь, хранящий все созданные экзмепляры класса в соответствии с id
    """
    id: int
    results: dict[str, int]
    found_programs: list
    filters: list
    answer: str

    instances = {}

    def __init__(self, id):
        if self.new_object:
            self.handlers = {
                r"(?:\w+\s+\d+)(?:\s+\w+\s+\d+){2,}": self.send_program_list,
                "ещ[её]": self.send_more,
            }
            self.id = id
            self.found_programs = []
            self.results = {}
            self.filters = [filters.bound_filter(0.8), filters.count_filter(10)]
            self.answer = ''
            self.new_object = False

    def handle_request(self, message_text: str) -> str:
        """
        Обрабатывает запрос пользователя.
        :param message_text: текст запроса
        :returns: текст ответа
        """
        # перебираем известные обработчики и выбираем подходящий по регулярному выражению
        for regexp, handler in self.handlers.items():
            if re.match(regexp, message_text):
                self.answer = ''
                handler(message_text)
                break
        else:
            # если не нашлось подходящего обработчика, вызываем обработчик по умолчанию
            self.send_default(message_text)
        return self.answer

    def send_program_list(self, message_text):
        self.get_results(message_text)
        if self.answer:
            return

        self.found_programs = Program.get_fitting(self.results)
        if not self.found_programs:
            self.answer = 'Извините, по вашим данным программы не найдены'
        else:
            self.get_filtered_programs()

    def send_more(self, message_text):
        if self.found_programs:
            self.get_filtered_programs()
        elif self.results:
            self.answer = 'Больше нет'
        else:
            self.answer = 'Сначала введи свои результаты ЕГЭ'

    def send_default(self, message_text):
        self.answer = 'Я очень умный, но этой команды не понял'

    def filter_programs(self, programs: list[Program]):
        for filter_function in self.filters:
            programs = filter_function(programs)
        return programs

    def get_results(self, message_text):
        subs = parse_request(message_text)
        with db.get_cursor() as cur:
            cur.execute('select subject_name from subjects')
            db_subs = [x[0] for x in cur.fetchall()]
        incorrect_subs = set(subs) - set(db_subs)
        if incorrect_subs:
            self.answer = 'Неизвестные предметы: ' + ', '.join(incorrect_subs)
        self.results = subs

    def get_filtered_programs(self):
        fit = self.filter_programs(self.found_programs)

        result = ['Вам могут подойти следующие программы:']
        for i, p in enumerate(fit, start=1):
            result.append(f'{i}. {p}')
            if p.additional and (add := p.check_additional(self.results)) > 0:
                result.append('Вам нужно сдать дополнительные вступительные испытания на '
                        + format_declension(add, 'балл', 'балла', 'баллов'))

        self.found_programs = self.found_programs[len(fit):]
        self.answer = '\n'.join(result)

    def __new__(cls, id, *args, **kwargs):
        if id in cls.instances:
            return cls.instances[id]
        obj = super().__new__(cls)
        obj.new_object = True
        cls.instances[id] = obj
        return obj
