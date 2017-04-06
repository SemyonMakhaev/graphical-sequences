"""Засекает время работы программы и чертит график."""
from datetime import datetime
from os import sep, path, makedirs
from argparse import ArgumentParser
from logging import warning
from pylab import gcf
from matplotlib import pyplot
from realizations import generate_realizations


MEASURES_DIRECTORY = 'measures'
DEFAULT_LENGTH = 10
DEFAULT_SEQUENCES = {1: [0], 2: [1, 1], 3: [1, 1, 2]}


def main():
    """Измерение времени работы программы и построение графика."""
    length, save = argument_parsing()
    if length < 1:
        warning('Неверное значение длины. Установлено значение по умолчанию')
        length = DEFAULT_LENGTH
    values = get_values(length)
    draw_diagram(values, save)


def argument_parsing():
    """Аргументы командной строки."""
    parser = ArgumentParser(prog='python3 measures.py', \
        description='Утилита для построения графика зависимости времени \
                работы программы от длины разбиения', \
        epilog='(c) Семён Махаев, 2017.')
    parser.add_argument('length', type=int, nargs='?', default=DEFAULT_LENGTH, \
        help='Максимальная длина разбиения')
    parser.add_argument('-s', '--save', action='store_true', \
        help='Сохранить график в файл')
    args = parser.parse_args()
    return args.length, args.save


def get_values(length):
    """Получает время работы на входе длины, не превосходящей заданную."""
    values = {}
    for current in range(1, length+1):
        sequence = get_sequence(current)
        value = generate_realizations(sequence)[1]
        values[len(sequence)] = value
        print('{}: {} сек'.format(len(sequence), value))
    return values


def get_sequence(length):
    """Порождает графическое разбиение заданной длины."""
    if length in DEFAULT_SEQUENCES:
        return DEFAULT_SEQUENCES[length]
    else:
        return [2] * length


def draw_diagram(values, save):
    """Рисует график по переданным данным."""
    pyplot.plot(list(values.keys()), list(values.values()), marker='o', color='r')
    pyplot.title('Зависимость врмени работы программы от длины разбиения')
    pyplot.xlabel('длина разбиения')
    pyplot.ylabel('время работы, сек')
    pyplot.grid(True)
    if save:
        if not path.exists(MEASURES_DIRECTORY):
            makedirs(MEASURES_DIRECTORY)
        pyplot.savefig('{}{}{:%Y-%m-%d_%H-%M-%S}.png'.format(\
                                MEASURES_DIRECTORY, sep, datetime.now()))
        print('Изображение сохранено в папку {}'.format(MEASURES_DIRECTORY))
    else:
        gcf().canvas.set_window_title('Измерения')
        pyplot.show()


if __name__ == '__main__':
    main()
