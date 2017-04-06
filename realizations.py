#!/usr/bin/env python3
"""Модуль для порождения реализаций графических разбиений."""
from argparse import ArgumentParser
from time import time
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
    sequence, directory, debug = argument_parse()
    realizations, measure = generate_realizations(sequence)
    if debug:
        assert isomorphic_pair(realizations) is None
        print("Реализации построены за {} сек".format(measure))
    print_realizations(realizations, directory)


def argument_parse():
    """Аргументы командной строки."""
    parser = ArgumentParser(prog='python3 realizations.py', \
        description='Программа порождает все реализации данного графического разбиения', \
        epilog='(c) Семён Махаев, 2017.')
    parser.add_argument('-dir', '--directory', type=str, default=PICTURES_DIRECTORY, \
        help='Директория для вывода картинок')
    parser.add_argument('degree', type=int, nargs='+', \
        help='Степень очередной вершины графического разбиения')
    parser.add_argument('-d', '--debug', action='store_true', \
        help='Запуск дополнительных проверок')
    args = parser.parse_args()
    return args.degree, args.directory, args.debug


def read_sequence(filename):
    """Читает графическое разбиение из файла."""
    with open(filename, mode='r', encoding='utf-8') as file:
        return [int(degree) for degree in file.read().split(' ')]


def generate_realizations(sequence):
    """Запускает основной алгоритм. Измеряет время работы."""
    start = time()
    sequence.sort(reverse=True)
    if not is_correct(sequence):
        error('Неверно задано разбиение')
        sys.exit(0)
    realization = get_realization(sequence)
    realizations = get_all_realizations_on_set(realization)
    return realizations, time() - start


def is_correct(sequence):
    """Проверяет заданное графическое разбиение на корректность."""
    for item in sequence:
        if item < 0:
            return False
    return True


def get_realization(sequence):
    """Порождает одну реализацию данного разбиения."""
    numbered_sequence = list(sequence)
    graph = networkx.Graph()
    for i in range(len(sequence)):
        numbered_sequence[i] = [sequence[i], i]
        if sequence[i] == 0:
            graph.add_node(i)
    for _ in range(len(numbered_sequence)):
        for idx in range(1, len(numbered_sequence)):
            if numbered_sequence[0][0] <= 0:
                break
            if numbered_sequence[idx][0] > 0 and not graph.has_edge( \
                        numbered_sequence[idx][1], numbered_sequence[0][1]):
                numbered_sequence[0][0] -= 1
                numbered_sequence[idx][0] -= 1
                graph.add_edge(numbered_sequence[0][1], numbered_sequence[idx][1])
        numbered_sequence.sort(key=lambda items: items[0], reverse=True)
    for items in numbered_sequence:
        if items[0] != 0:
            error('Разбиние не графично')
            sys.exit(0)
    return graph


def get_all_realizations(realization):
    """Получает все реализации по одной из них."""
    stack = [realization]
    realizations = [realization]
    while len(stack) > 0:
        current = stack.pop()
        for this_edge in current.edges():
            for that_edge in current.edges():
                if not intersect_edges(this_edge, that_edge):
                    swapped = swap(current, this_edge, that_edge)
                    if not some(realizations, lambda item: \
                                    networkx.is_isomorphic(swapped, item)):
                        stack.append(swapped)
                        realizations.append(swapped)
    return realizations


def get_all_realizations_on_set(realization):
    """
    Оптимизация основного алгиритма, основанная на
    предварительной генерации всех необходимых пар рёбер.
    """
    stack = [realization]
    realizations = [realization]
    while len(stack) > 0:
        current = stack.pop()
        for pair in get_not_intersected_edges_pairs(current):
            swapped = swap(current, *pair)
            if not some(realizations, lambda item: \
                                networkx.is_isomorphic(swapped, item)):
                stack.append(swapped)
                realizations.append(swapped)
    return realizations


def get_not_intersected_edges_pairs(graph):
    """
    Находит в переданном графе все пары
    непересекающихся неориентированных рёбер.
    """
    seen = set()
    return [(this_edge, that_edge) for this_edge in graph.edges() \
            for that_edge in graph.edges() \
            if not intersect_edges(this_edge, that_edge) and \
            not (this_edge, that_edge) in seen and \
            not (that_edge, this_edge) in seen and \
            not seen.add((this_edge, that_edge))]


def intersect_edges(this_edge, that_edge):
    """Проверяет совпадение инцидентных рёбрам вершин"""
    for this_vertex in this_edge:
        for that_vertex in that_edge:
            if this_vertex == that_vertex:
                return True
    return False


def swap(graph, this_edge, that_edge):
    """Переключение рёбер."""
    swapped = graph.copy()
    had_edge = swapped.has_edge(this_edge[0], that_edge[0]) or \
            swapped.has_edge(this_edge[1], that_edge[1])
    swapped.remove_edge(*this_edge)
    swapped.remove_edge(*that_edge)
    if had_edge:
        swapped.add_edge(this_edge[0], that_edge[1])
        swapped.add_edge(this_edge[1], that_edge[0])
    else:
        swapped.add_edge(this_edge[0], that_edge[0])
        swapped.add_edge(this_edge[1], that_edge[1])
    return swapped


def some(iterable, func):
    """
    Возвращает True, если хотя бы для одного элемента
    переданная функция возвращает True.
    """
    for item in iterable:
        if func(item):
            return True
    return False


def print_realizations(realizations, directory):
    """Сохраняет картинки с порждёнными реализациями."""
    make_directory(directory)
    for idx in range(len(realizations)):
        print_graph(realizations[idx], idx+1, directory)


def print_graph(graph, number, directory):
    """Сохраняет текущую реализацию в виде изображения."""
    layout = networkx.shell_layout(graph)
    networkx.draw_networkx_nodes(graph, layout, node_size=NODE_SIZE)
    networkx.draw_networkx_edges(graph, layout, width=EDGE_WIDTH)
    networkx.draw_networkx_labels(graph, layout, font_size=FONT_SIZE, font_family='serif')
    pyplot.axis('off')
    pyplot.savefig(path.join(directory, '{}.png'.format(number)))
    pyplot.clf()


def make_directory(directory):
    """Создаёт папку для сохранения изображений."""
    try:
        if path.exists(directory):
            rmtree(directory)
        makedirs(directory)
    except Exception:
        error('Ошибка при создании директории')
        sys.exit(0)


def isomorphic_pair(realizations):
    """Возвращает пару изоморфных реализаций, если они есть."""
    for this_realization in realizations:
        for that_realization in realizations:
            if this_realization != that_realization and \
                    networkx.is_isomorphic(this_realization, \
                            that_realization):
                return this_realization, that_realization
    return None


if __name__ == '__main__':
    main()
