# -*- coding: utf-8 -*-
""" Реализация функции вычисления условия в правиле вывода """

import re
from vsptd import parse_triplex_string

# импортирование функций для реализации функции check_condition
from math import sin, cos, tan, acos, atan, sinh, cosh, tanh, sqrt, exp
from math import log as ln
from math import log10 as log


# WARN аналогичные регулярки есть и в vsptd
RE_PREFIX_NAME_WODS = re.compile('[A-Za-z]\d*\.[A-Za-z]+')  # префикс.имя
RE_PREFIX_NAME = re.compile('\$[A-Za-z]\d*\.[A-Za-z]+')  # $префикс.имя


RE_TRIPLET_WODS = re.compile('([A-Za-z])\.([A-Za-z]+)=([A-Za-zА-Яа-я0-9 \':\.]*);')  # триплет без $
RE_FUNC_PRESENT = re.compile('(?:есть|ЕСТЬ)\(\$[A-Za-z]\.[A-Za-z]+\)')  # функция ЕСТЬ
RE_FUNC_PRESENT_WODS = re.compile('(?:есть|ЕСТЬ)\([A-Za-z]\.[A-Za-z]+\)')  # функция ЕСТЬ без $
RE_FUNC_ABSENCE = re.compile('(?:нет|НЕТ)\(\$[A-Za-z]\.[A-Za-z]+\)')  # функция НЕТ
RE_FUNC_ABSENCE_WODS = re.compile('(?:нет|НЕТ)\([A-Za-z]\.[A-Za-z]+\)')  # функция НЕТ без $
RE_SLICE = re.compile('(\[(\d+),(\d+)\])')  # срез [n,n]


def strcat(a, b):
    return a + b


def check_condition(trp_str, condition, trp_str_from_db=''):
    # WARN используется небезопасный алгоритм, который также может не всегда верно работать
    """
    ПРОВЕРКА ТРИПЛЕКСНОЙ СТРОКИ НА УСЛОВИЕ
    Алгоритм заменяет триплеты, указанные в условии соответствующими значениями, затем
    проверяет истинность условия. Триплеты, указанные без префикса "$", заменяются
    соответствующими значениями, указанными в параметре trpStringFromDB
    Принимает:
        trpString (str) - триплексная строка
        condition (str) - условие
        trpStringFromDB (str) необязательный - триплексная строка по данным из базы данных
    Возвращает:
        (bool) - результат проверки условия
    Вызывает исключение ValueError, если:
        триплескная строка или условие не является строкой
        получена пустая строка вместо триплексной строки или условия
        триплет из условия не найден в триплексной строке
        в условии не соблюден баланс скобок
    """
    if not isinstance(trp_str, str) or not isinstance(trp_str_from_db, str):
        raise ValueError('Триплексная строка должна быть строкой')
    if not isinstance(condition, str):
        raise ValueError('Условие должно быть строкой')
    if len(trp_str) == 0:
        raise ValueError('Пустая строка')
    if len(condition) == 0:
        raise ValueError('Пустое условие')

    trp_str = parse_triplex_string(trp_str)
    trp_str_from_db = parse_triplex_string(trp_str_from_db)

    # замена операторов
    # WARN возможна неверная замена
    # например, замена слов произойдёт, даже если в условии происходит
    # сравнение со строкой, содержащей слово на замену
    # $W.B = ' или '
    replacements = [[' или ', ' or '],
                    [' и ', ' and '],
                    [' ИЛИ ', ' or '],
                    [' И ', ' and '],
                    ['=', '=='],
                    ['<>', '!='],
                    ['^', '**']]
    for rplc in replacements:
        condition = condition.replace(rplc[0], rplc[1])

    # переводим названия функций в нижний регистр
    func_replacements = ('sin', 'cos', 'tan', 'acos', 'atan', 'sinh', 'cosh', 'tanh',
                         'sqrt', 'exp', 'ln', 'log', 'strcat', 'min', 'max', 'abs')
    for rplc in func_replacements:
        condition = condition.replace(rplc.upper(), rplc)

    # замены для функций ЕСТЬ и НЕТ
    # TODO
    # поиск триплетов в строке
    for trp in re.findall(RE_FUNC_PRESENT, condition):  # функция ЕСТЬ
        item = trp[6:-1].upper().split('.')  # извлекаем префикс и имя в кортеж
        value = False
        for triplet in trp_str.triplets:
            if [triplet.prefix, triplet.name] == item:
                value = True
                break
        condition = condition.replace(trp, str(value))
    for trp in re.findall(RE_FUNC_ABSENCE, condition):  # функция НЕТ
        item = trp[5:-1].upper().split('.')  # извлекаем префикс и имя в кортеж
        value = False
        for triplet in trp_str.triplets:
            if [triplet.prefix, triplet.name] == item:
                value = True
                break
        condition = condition.replace(trp, str(not value))
    # поиск триплетов в строке по данным из базы
    if len(trp_str_from_db) > 0:
        for trp in re.findall(RE_FUNC_PRESENT_WODS, condition):  # функция ЕСТЬ
            item = trp[5:-1].upper().split('.')  # извлекаем префикс и имя в кортеж
            value = False
            for triplet in trp_str_from_db.triplets:
                if [triplet.prefix, triplet.name] == item:
                    value = True
                    break
            condition = condition.replace(trp, str(value))
        for trp in re.findall(RE_FUNC_ABSENCE_WODS, condition):  # функция НЕТ
            item = trp[4:-1].upper().split('.')  # извлекаем префикс и имя в кортеж
            value = False
            for triplet in trp_str_from_db.triplets:
                if [triplet.prefix, triplet.name] == item:
                    value = True
                    break
            condition = condition.replace(trp, str(not value))

    # поиск триплетов
    for trp in re.findall(RE_PREFIX_NAME, condition):  # замена триплетов на их значения
        value = trp_str.__getitem__(trp[1:])  # получаем значение триплета
        if value is None:
            raise ValueError('Триплет {} не найден в триплексной строке'.format(trp))
        value = '\'{}\''.format(value) if isinstance(value, str) else str(value)  # приводим к формату значений триплета
        condition = condition.replace(trp, value)

    # поиск триплетов в строке по данным из базы
    if len(trp_str_from_db) > 0:
        for trp in re.findall(RE_PREFIX_NAME_WODS, condition):  # замена триплетов на их значения
            value = trp_str_from_db.__getitem__(trp)  # получаем значение триплета
            if value is None:
                raise ValueError('Триплет {} не найден в триплескной строке из базы'.format(trp))
            value = '\'{}\''.format(value) if isinstance(value, str) else str(value)  # приводим к формату значений триплета
            condition = condition.replace(trp, value)
    # поиск срезов
    # CHECK
    for rplc in re.findall(RE_SLICE, condition):
        _ = str(int(rplc[1]) - 1)
        __ = str(int(rplc[1]) + int(rplc[2]))
        condition.replace(rplc[0], '[{}:{}]'.format(_, __))

    # проверка баланса скобок
    if condition.count('(') != condition.count(')'):
        raise ValueError('Не соблюден баланс скобок')

    # print('Конечное выражение: ', condition, sep='')
    return eval(condition)
