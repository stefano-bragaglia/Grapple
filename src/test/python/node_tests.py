from unittest import TestCase

from assertpy import assert_that

from grapple.bom.graph import Graph


class TestNode(TestCase):

    def test__when__init__given__nothing__then__properties_are_set(self):
        graph = Graph()
        ident = graph.next_ident()
        node = graph.create_node()

        assert_that(node.graph).is_equal_to(graph)
        assert_that(node.ident).is_equal_to(ident)

    def test__when__relations__given__nothing__then__relations(self):
        graph = Graph()
        node = graph.create_node()
        relation_a = graph.create_node().create_relation_to(node)
        relation_b = node.create_relation_to(graph.create_node())

        assert_that(node.relations).contains_only(relation_a, relation_b)

    def test__when__delete__given____then__graph_none_ident_released(self):
        graph = Graph()
        ident = graph.next_ident()
        node = graph.create_node()
        node.delete()

        assert_that(node.graph).is_none()
        assert_that(graph.next_ident()).is_equal_to(ident)

    def test__when__delete__given__relations__then__exception(self):
        graph = Graph()
        node = graph.create_node()
        node.create_relation_to(graph.create_node())

        assert_that(node.delete) \
            .raises(Exception) \
            .when_called_with() \
            .is_equal_to('Node not empty')
