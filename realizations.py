#!/usr/bin/env python3
"""Модуль для порождения реализаций графических разбиений."""
from argparse import ArgumentParser
from logging import error
from shutil import rmtree
from os import path, makedirs
from matplotlib import pyplot

import sys
import networkx


PICTURES_DIRECTORY = 'pictures'
NODE_SIZE = 400
EDGE_WIDTH = 1
FONT_SIZE = 14


def main():
    """Порождает все реализации данного разбиения."""
    sequence = argument_parse()
    if not is_correct(sequence):
        error('Неверно задано разбиение')
    realization = get_realization(sequence)
    # realizations = get_realizations([realization])
    make_directory()
    # print_realizations(realizations)
    print_graph(realization, 1)# TODO: удалить


def argument_parse():
    """Аргументы командной строки."""
    parser = ArgumentParser(prog='python3 realizations.py', \
        description='Программа порождает все реализации данного графического разбиения', \
        epilog='(c) Семён Махаев, 2017.')
    parser.add_argument('degree', type=int, nargs='+', \
        help='Степень очередной вершины графического разбиения')
    args = parser.parse_args()
    return args.degree


def read_sequence(filename):
    """Читает графическое разбиение из файла."""
    with open(filename, mode='r', encoding='utf-8') as file:
        sequence = [int(degree) for degree in file.read().split(' ')]
        sequence.sort(reverse=True)
        return sequence


def is_correct(sequence):
    """Проверяет заданное графическое разбиение на корректность."""
    for item in sequence:
        if item < 0:
            return False
    return True


def get_realization(sequence):
    """Порождает одну реализацию данного разбиения."""
    numbered_sequence = list(sequence)
    for i in range(len(sequence)):
        numbered_sequence[i] = [sequence[i], i]
    graph = networkx.Graph()
    for _ in range(len(numbered_sequence)):
        for idx in range(1, len(numbered_sequence)):
            if numbered_sequence[0][0] <= 0:
                break
            if numbered_sequence[idx][0] > 0:
                numbered_sequence[0][0] -= 1
                numbered_sequence[idx][0] -= 1
                graph.add_edge(numbered_sequence[0][1], numbered_sequence[idx][1])
        numbered_sequence.sort(key=lambda items: items[0], reverse=True)
    for items in numbered_sequence:
        if items[0] != 0:
            error('Разбиние не графично')
            sys.exit(0)
    return graph


def get_realizations(stack):
    """Получает все реализации по одной из них."""
    realizations = []
    while len(stack) > 0:
        current = stack.pop()
        realizations.append(current)
        for this_edge in current.edges():
            for that_edge in current.edges():
                switched = swap(current, this_edge, that_edge)
                need_to_append = True
                for realization in realizations:
                    if networkx.is_isomorphic(switched, realization):
                        need_to_append = False
                        break
                if need_to_append:
                    stack.append(switched)
    return realizations


def swap(graph, this_edge, that_edge):
    """Переключение рёбер."""
    switched = graph.copy()
    # TODO: осуществить переключение
    return switched


def print_realizations(realizations):
    """Сохраняет картинки с порждёнными реализациями."""
    for idx in range(len(realizations)):
        print_graph(realizations[idx], idx)


def print_graph(graph, number):
    """Сохраняет текущую реализацию в виде изображения."""
    layout = networkx.shell_layout(graph)
    networkx.draw_networkx_nodes(graph, layout, node_size=NODE_SIZE)
    networkx.draw_networkx_edges(graph, layout, width=EDGE_WIDTH)
    networkx.draw_networkx_labels(graph, layout, font_size=FONT_SIZE, font_family='serif')
    pyplot.axis('off')
    pyplot.savefig(path.join(PICTURES_DIRECTORY, '{}.png'.format(number)))
    pyplot.clf()


def make_directory():
    """Создаёт папку для сохранения изображений."""
    try:
        if path.exists(PICTURES_DIRECTORY):
            rmtree(PICTURES_DIRECTORY)
        makedirs(PICTURES_DIRECTORY)
    except Exception:
        error('Ошибка при создании директории')
        sys.exit(0)


if __name__ == '__main__':
    main()
