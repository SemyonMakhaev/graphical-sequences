"""Засекает время работы программы и чертит график."""
from time import time
from argparse import ArgumentParser
from logging import warning
from matplotlib import pyplot
from realizations import get_realization, get_realizations


DEFAULT_LENGTH = 10
DEFAULT_SEQUENCES = {1: [0], 2: [1, 1], 3: [1, 1, 2]}


def main():
    """Измерение времени работы программы и построение графика."""
    length = argument_parsing()
    if length < 1:
        warning('Неверное значение длины. Установлено значение по умолчанию')
        length = DEFAULT_LENGTH
    values = get_values(length)
    draw_diagram(values)


def argument_parsing():
    """Аргументы командной строки."""
    parser = ArgumentParser(prog='python3 measures.py', \
        description='Утилита для построения графика зависимости времени \
                работы программы от длины разбиения', \
        epilog='(c) Семён Махаев, 2017.')
    parser.add_argument('length', type=int, nargs='?', default=DEFAULT_LENGTH, \
        help='Максимальная длина разбиения')
    return parser.parse_args().length


def get_values(length):
    """Получает время работы на входе длины, не превосходящей заданную."""
    values = {}
    for current in range(1, length+1):
        sequence = get_sequence(current)
        value = measure(sequence)
        values[len(sequence)] = value
        print('{}: {} мс'.format(len(sequence), value))
    return values


def get_sequence(length):
    """Порождает графическое разбиение заданной длины."""
    if length in DEFAULT_SEQUENCES:
        return DEFAULT_SEQUENCES[length]
    else:
        return [2] * length


def measure(sequence):
    """Измеряет время работы для заданного разбиения."""
    start = time()
    sequence.sort(reverse=True)
    realization = get_realization(sequence)
    get_realizations(realization)
    return time() - start


def draw_diagram(values):
    """Рисует график по переданным данным."""
    pyplot.plot(list(values.keys()), list(values.values()), marker='o', color='r')
    pyplot.title('Зависимость врмени работы программы от длины разбиения')
    pyplot.xlabel('длина разбиения')
    pyplot.ylabel('время работы, сек')
    pyplot.grid(True)
    pyplot.show()


if __name__ == '__main__':
    main()
