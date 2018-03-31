from unittest import TestCase

from assertpy import assert_that

from grapple.bom.graph import Graph


class TestGraph(TestCase):

    def test__when__creating__given____then__properties_are_set(self):
        graph = Graph()
        node_a = graph.create_node()
        node_b = graph.create_node()
        node_c = graph.create_node()
        relation_a = node_a.create_relation_to(node_b)
        relation_b = node_b.create_relation_to(node_c)
        relation_c = node_c.create_relation_to(node_a)

        assert_that(graph.nodes).contains_only(node_a, node_b, node_c)
        assert_that(graph.relations).contains_only(relation_a, relation_b, relation_c)

    def test__when__getting_ident__given____then__values(self):
        graph = Graph()
        assert_that(graph.next_ident()).is_equal_to(0)
        node_a = graph.create_node()
        assert_that(graph.next_ident()).is_equal_to(1)
        node_b = graph.create_node()
        assert_that(graph.next_ident()).is_equal_to(2)
        node_c = graph.create_node()
        assert_that(graph.next_ident()).is_equal_to(3)
        node_a
