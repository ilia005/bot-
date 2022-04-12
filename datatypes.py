from db import get_cursor
from dataclasses import dataclass


subjects = {
 'английский',
 'биология',
 'география',
 'иностранный',
 'информатика',
 'история',
 'литература',
 'математика',
 'обществознание',
 'русский',
 'физика',
 'химия'
}


@dataclass
class College:
    id: int
    name: str
    link: str

    def __str__(self):
        return self.name

    @classmethod
    def load_all(cls):
        with get_cursor() as cur:
            cur.execute('SELECT college_id, college_name, college_link FROM colleges')
            result = cur.fetchall()
        return [cls(*args) for args in result]


@dataclass
class Program:
    id: int
    college: College
    name: str
    link: str
    subjects: set
    score: int
    additional: bool = False

    def __post_init__(self):
        if 'вступительные' in self.subjects:
            self.additional = True
            self.subjects.remove('вступительные')
        if 'иностранный язык' in self.subjects:
            self.subjects.remove('иностранный язык')
            self.subjects.add('иностранный')

    def __str__(self):
        return f'{self.name}. ВУЗ: {self.college}. Проходной балл: {self.score}'

    def check_fit(self, subject_scores: dict):
        if not self.subjects.issubset(set(subject_scores.keys())):
            return False
        not_enough = self.check_additional(subject_scores)
        return not_enough <= 0 or self.additional and not_enough <= 100

    def check_additional(self, subject_scores: dict):
        user_scores = sum(subject_scores[x] for x in self.subjects)
        return self.score - user_scores

    @classmethod
    def find_by_subjects(cls, subjects: list[str]):
        placeholder = ', '.join('?' * len(subjects))

        with get_cursor() as cur:
            cur.execute(f'''
                select * from programs inner join colleges using(college_id)
                where program_id not in
                (select program_id from subjects_for_program where subject_id in
                (select subject_id from subjects where subject_name not in ({placeholder})))
            ''', tuple(subjects))
            programs_data = cur.fetchall()
            programs = []
            for p_id, p_name, p_link, score, additional, c_id, c_name, c_link in programs_data:
                cur.execute(f'''
                    select subject_name from subjects where subject_id in
                    (select subject_id from subjects_for_program where program_id = {p_id})''')
                s = {x[0] for x in cur.fetchall()}
                p = cls(p_id, College(c_id, c_name, c_link), p_name, p_link, s, score, additional)
                programs.append(p)
        return programs

    @classmethod
    def get_fitting(cls, subs: dict[str, int]):
        programs = cls.find_by_subjects(subs.keys())
        score = sum(subs.values())
        fit = sorted(
            (p for p in programs if p.check_fit(subs)),
            key=lambda p: p.score / (len(p.subjects) + p.additional),
            reverse=True
        )

        return fit


if __name__ == '__main__':
    colleges = College.load_all()
    for c in colleges:
        print(c)
