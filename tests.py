#!/usr/bin/env python3
"""Тесты для реализаций графических последовательностей."""
from unittest import TestCase, main
from networkx import Graph
from realizations import get_realization, generate_realizations, \
    is_correct, intersect_edges, swap, some, isomorphic_pair


class RealizationsTests(TestCase):
    """Тестирующий класс."""
    def test_get_realization(self):
        """
        Тесты для генерации одной произвольной
        реализации заданного разбиения.
        """
        edges = {(1, 1): 1, \
            (1, 1, 1, 1): 2, \
            (2, 1, 1): 2, \
            (2, 2, 2, 2): 4, \
            (3, 2, 1, 1, 1): 4}
        for sequence in edges:
            self.assertEqual(edges[sequence], \
                        len(get_realization(sequence).edges()))


    def test_generate_realizations(self):
        """
        Тесты для получения всех реализаций
        по одной данной реализации.
        """
        count = {(1, 1): 1, \
            (1, 1, 1, 1): 1, \
            (2, 1, 1): 1, \
            (2, 2, 2, 2): 1,\
            (3, 2, 1, 1, 1): 1, \
            (2, 2, 2, 2, 1, 1, 1, 1): 5}
        for sequence in count:
            self.assertEqual(count[sequence], len(generate_realizations(list(sequence))[0]))


    def test_is_correct(self):
        """Проверка на корректность разбиения."""
        self.assertTrue(is_correct([1, 2, 3, 4, 5]))
        self.assertTrue(is_correct([0, 1, 2, 3]))
        self.assertFalse(is_correct([-1]))


    def test_intersect_edges(self):
        """Проверка на пересечение двух рёбер."""
        self.assertTrue(intersect_edges((0, 1), (1, 2)))
        self.assertTrue(intersect_edges((0, 2), (1, 2)))
        self.assertTrue(intersect_edges((0, 1), (0, 2)))
        self.assertTrue(intersect_edges((0, 1), (1, 0)))
        self.assertTrue(intersect_edges((0, 1), (1, 1)))
        self.assertTrue(intersect_edges((0, 1), (0, 1)))
        self.assertFalse(intersect_edges((0, 1), (2, 3)))


    def test_swap(self):
        """Тест на операцию своп."""
        graph = Graph()
        graph.add_edge(0, 1)
        graph.add_edge(0, 2)
        graph.add_edge(0, 3)
        graph.add_edge(1, 2)
        swapped = swap(graph, (1, 2), (0, 3))
        self.assertNotEqual(graph, swapped)
        self.assertTrue(swapped.has_edge(0, 1))
        self.assertTrue(swapped.has_edge(0, 2))
        self.assertFalse(swapped.has_edge(0, 3))
        self.assertFalse(swapped.has_edge(1, 2))
        self.assertTrue(swapped.has_edge(1, 3))
        self.assertTrue(swapped.has_edge(0, 2))


    def test_some(self):
        """Проверка метода some."""
        self.assertTrue(some([1, 2, 3], lambda x: isinstance(x, int)))
        self.assertTrue(some([1, 2, 3], lambda x: x == 1))
        self.assertFalse(some([1, 2, 3], lambda x: x == 4))
        self.assertFalse(some([], lambda x: x == x))


    def test_isomorphic_pair(self):
        """Тест на поиск изоморфной пары графов."""
        graph_a = Graph()
        graph_a.add_edge(0, 1)
        graph_a.add_edge(1, 2)
        graph_a.add_edge(2, 3)
        graph_b = Graph()
        graph_b.add_edge(0, 2)
        graph_b.add_edge(2, 1)
        graph_b.add_edge(0, 3)
        graph_c = Graph()
        graph_c.add_edge(0, 1)
        graph_c.add_edge(0, 2)
        graph_c.add_edge(0, 3)
        self.assertIsNotNone(isomorphic_pair([graph_a, graph_b]))
        self.assertIsNone(isomorphic_pair([graph_a, graph_c]))
        self.assertIsNone(isomorphic_pair([graph_b, graph_c]))


if __name__ == '__main__':
    main()
