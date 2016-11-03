# -*- coding: utf-8 -*-
""" Работа с ВСПТД в ООП-стиле """

import re


islt_re = lambda x: '^' + x + '$'  # обособление рег. выражения

_BID = ':'  # заявка (запрос полной информации по заданному объекту, определяемому префиксом)

_RE_PREFIX = '[A-Za-z]+\d*'
_RE_NAME = '[A-Za-z]+'
_RE_VALUE = r'\'?[A-Za-zА-Яа-я0-9 ?:\.]*\'?'
_RE_PREFIX_NAME_WODS = _RE_PREFIX + '\.' + _RE_NAME
_RE_PREFIX_NAME = '\$' + _RE_PREFIX_NAME_WODS
_RE_TRIPLET = '\$(' + _RE_PREFIX + ')\.(' + _RE_NAME + ')=(' + _RE_VALUE + ');'

RE_PREFIX = re.compile(islt_re(_RE_PREFIX))  # префикс: 1 латинский символ
RE_NAME = re.compile(islt_re(_RE_NAME))  # имя: латинские символы и, возможно, число
RE_VALUE = re.compile(islt_re(_RE_VALUE))  # значение
RE_PREFIX_NAME_WODS = re.compile(islt_re(_RE_PREFIX_NAME_WODS))  # префикс.имя
RE_PREFIX_NAME = re.compile(islt_re(_RE_PREFIX_NAME))  # $префикс.имя
RE_TRIPLET = re.compile(_RE_TRIPLET)  # триплет


def parse_triplex_string(trp_str):
    """ПАРСИНГ ТРИПЛЕКСНОЙ СТРОКИ ИЗ str В TriplexString"""
    trp_str = re.findall(RE_TRIPLET, trp_str)
    tmp_trp_str = []
    for trp in trp_str:
        value = _determine_value(trp[2])
        tmp_trp_str += [Trp(trp[0], trp[1], value)]
    return TrpStr(*tmp_trp_str)


def _determine_value(value):
    """ОПРЕДЕЛЕНИЕ ТИПА ЗНАЧЕНИЯ"""
    if value in ('True', 'False'):  # булево значение
        return bool(value)
    elif value.startswith('\'') and value.endswith('\''):  # строка
        return value[1:-1]
    # elif val.startswith('$') and val.endswith(';'):  # TODO триплет
    #     pass
    elif value == _BID:  # заявка
        return _BID
    else:  # число
        try:
            return float(value) if '.' in value else int(value)
        except ValueError:
            raise ValueError('Неверное значение триплета')


class Trp:
    """
    ТРИПЛЕТ
    Принимает:
        prefix (str) - префикс (1 латинский символ)
        name (str) - имя параметра (латинские символы)
        value - значение параметра
    """
    def __init__(self, prefix, name, value=''):
        if not isinstance(prefix, str):
            raise ValueError('Префикс должен быть строкой')
        if not isinstance(name, str):
            raise ValueError('Имя должно быть строкой')
        if not isinstance(value, (str, int, float, Trp, TrpStr)):
            raise ValueError('Значение должно быть строкой, числом, триплетом или триплексной строкой')
        if re.match(RE_PREFIX, prefix) is None:
            raise ValueError('Неверный формат префикса: ' + prefix)
        if re.match(RE_NAME, name) is None:
            raise ValueError('Неверный формат имени: ' + name)
        # TODO может быть и не строкой (следует уточнить)
        # if isinstance(value, str) and value != _BID and re.match(RE_VALUE, value) is None:
        #     raise ValueError

        # префикс и имя приводятся к верхнему регистру
        self.prefix = prefix.upper()
        self.name = name.upper()
        self.value = value

    def __str__(self):
        _ = '${}.{}='.format(self.prefix, self.name)
        if self.value == _BID:
            _ += _BID
        elif isinstance(self.value, str):
            _ += '\'{}\''.format(self.value)
        else:
            _ += str(self.value)
        _ += ';'
        return _

    def __add__(self, other):
        if isinstance(other, Trp):
            return TrpStr(self, other)
        if isinstance(other, TrpStr):
            return TrpStr(self, *other)
        else:
            raise ValueError

    def __eq__(self, other):
        return isinstance(other, Trp) and \
               self.name == other.name and \
               self.prefix == other.prefix and \
               self.value == other.value


class TrpStr:
    """
    ТРИПЛЕКСНАЯ СТРОКА
    Принимает:
        *triplets (Triplet) - триплеты
    """
    def __init__(self, *triplets):
        # TODO добавить возможность создания строки по списку/кортежу
        for _ in triplets:  # CHECK проверить скорость работы через filter
            if not isinstance(_, Trp):
                raise ValueError('Аргументы должны быть триплетами')
        self.triplets = list(triplets)

        # удаление повторов триплетов (по префиксам и именам)
        for trp in self.triplets.copy():
            # триплеты с данными префиксами и именами
            triplets_to_remove = [_trp for _trp in self.triplets if trp.prefix == _trp.prefix and trp.name == _trp.name]
            triplets_to_remove = triplets_to_remove[:-1]  # исключение последнего найденного триплета
            for rem_trp in triplets_to_remove:
                self.triplets.remove(rem_trp)

    def __len__(self):
        return len(self.triplets)

    def __add__(self, other):
        if isinstance(other, Trp):
            return TrpStr(*(self.triplets + [other]))
        elif isinstance(other, TrpStr):
            return TrpStr(*(self.triplets + other.triplets))
        else:
            raise ValueError('Должен быть триплет или триплексная строка')

    def __str__(self):
        return ''.join(tuple(str(trp) for trp in self.triplets))

    def __contains__(self, item):
        # TODO возможно, стоит включить возможность проверки включения по префиксу и имени
        if not isinstance(item, Trp):
            raise ValueError('Должен быть триплет')

        for trp in self.triplets:
            if trp.prefix == item.prefix and \
               trp.name == item.name and \
               trp.value == item.value:
                return True
        return False

    def __getitem__(self, key):
        """
        (str) - ключ
            ключ формата префикса -> TripletString из триплетов с данным префиксом
            ключ формата 'префикс.имя' или '$префикс.имя' -> значение триплета
        иначе - индекс/срез
        """
        # TODO CHECK
        if isinstance(key, str):  # элемент по ключу
            if re.match(RE_PREFIX, key) is not None:  # получить триплеты по префиксу в виде триплесной строки
                return TrpStr(*[trp for trp in self.triplets if trp.prefix == key])
            elif (re.match(RE_PREFIX_NAME_WODS, key) is not None) or (re.match(RE_PREFIX_NAME, key) is not None):
                if key.startswith('$'):
                    key = key[1:]
                key = key.upper().split('.')
                for trp in self.triplets:
                    if trp.prefix == key[0] and trp.name == key[1]:
                        return trp.value
                return None
        else:  # элемент по индексу
            return self.triplets[key]

    def __eq__(self, other):
        # CHECK возможно, стоит замерить скорость работы
        if not isinstance(other, TrpStr):
            raise ValueError

        if len(self.triplets) != len(other):
            return False
        for triplet in other:
            if triplet not in self.triplets:
                return False
        return True

    def __iter__(self):
        return iter(self.triplets)

    def add(self, other):
        """
        СЛОЖЕНИЕ ТРИПЛЕКСНОЙ СТРОКИ С ТРИПЛЕКСНОЙ СТРОКОЙ ИЛИ ТРИПЛЕТОМ
        Эквивалентно сложению через оператор "+"
        Принимает:
            other (TriplexString или Triplet) - триплексная строка или триплет
        Возвращает:
            (TriplexString)
        """
        return self.__add__(other)

    def del_trp(self, prefix, name):
        # CHECK
        """
        УДАЛИТЬ ТРИПЛЕТ ИЗ ТРИПЛЕКСНОЙ СТРОКИ
        Принимает:
            prefix (str) - префикс (1 латинский символ)
            name (str) - имя параметра (латинские символы)
        Вызывает исключение ValueError, если триплет не найден
        """
        if not isinstance(prefix, str):
            raise ValueError('Префикс должен быть строкой')
        if not isinstance(name, str):
            raise ValueError('Имя должно быть строкой')
        if re.match(RE_PREFIX, prefix) is None:
            raise ValueError('Неверный формат префикса')
        if re.match(RE_NAME, name) is None:
            raise ValueError('Неверный формат имени')

        for trp in self.triplets:
            if trp.prefix == prefix and trp.name == name:
                self.triplets.remove(trp)
                return
        raise ValueError('Триплет не найден')

    def del_trp_pref(self, prefix):
        # CHECK
        """
        УДАЛИТЬ ВСЕ ТРИПЛЕТЫ С ЗАДАННЫМ ПРЕФИКСОМ ИЗ ТРИПЛЕКСНОЙ СТРОКИ
        Принимает:
            prefix (str) - префикс
        """
        if not isinstance(prefix, str):
            raise ValueError('Должен быть триплет')

        for trp in self.triplets:
            if trp.prefix == prefix:
                self.triplets.remove(trp)
