from abc import ABC, abstractmethod

from datatypes import Program


def non_filter(fit):
    return fit


def count_filter(count):
    def filter_func(fit):
        return fit[:count]

    return filter_func


def bound_filter(percent_bound):
    def filter_func(fit):
        bound = fit[0].score * percent_bound
        result = []
        for p in fit:
            if p.score < bound:
                break
            result.append(p)
        return result

    return filter_func


def many_colleges_filter(n_col):
    def filter_func(fit):
        result = []
        col_set = set()
        for p in fit:
            result.append(p)
            col_set.add(p.college.id)
            if len(col_set) == n_col:
                break
        return result

    return filter_func


# class ProgramsFilter(ABC):

#     @abstractmethod
#     def filter(self, programs: list[Program]) -> list[Program]:
#         pass


# class NonFilter(ProgramsFilter):
#     def filter(self, programs: list[Program]) -> list[Program]:
#         return programs


# class CountFilter(ProgramsFilter):
#     def __init__(self, count):
#         self.count = count

#     def filter(self, programs: list[Program]) -> list[Program]:
#         return programs[:self.count]
