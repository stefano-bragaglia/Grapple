from unittest import TestCase

from assertpy import assert_that

from grapple.bom.graph import Graph


class TestRelation(TestCase):

    def test__when__init__given__node_from_other_graph__then__exception(self):
        graph_1 = Graph()
        node_1 = graph_1.create_node()
        graph_2 = Graph()
        node_2 = graph_2.create_node()

        assert_that(node_1.create_relation_to) \
            .raises(ValueError) \
            .when_called_with(node_2) \
            .is_equal_to("'node' is invalid: <%s>" % node_2)

    def test__when__init__given__node__then__properties_are_set(self):
        graph = Graph()
        tail = graph.create_node()
        head = graph.create_node()
        ident = graph.next_ident()
        relation = tail.create_relation_to(head)

        assert_that(relation.graph).is_equal_to(graph)
        assert_that(relation.ident).is_equal_to(ident)
        assert_that(relation.tail).is_equal_to(tail)
        assert_that(relation.head).is_equal_to(head)

    def test__when__other__given__tail__then__head(self):
        graph = Graph()
        tail = graph.create_node()
        head = graph.create_node()
        relation = tail.create_relation_to(head)
        other = relation.other(tail)

        assert_that(other).is_equal_to(head)

    def test__when__other__given__head__then__tail(self):
        graph = Graph()
        tail = graph.create_node()
        head = graph.create_node()
        relation = tail.create_relation_to(head)
        other = relation.other(head)

        assert_that(other).is_equal_to(tail)

    def test__when__other__given__other_node__then__exception(self):
        graph = Graph()
        tail = graph.create_node()
        head = graph.create_node()
        other = graph.create_node()
        r = tail.create_relation_to(head)

        assert_that(r.other) \
            .raises(ValueError) \
            .when_called_with(other) \
            .is_equal_to("'node' is invalid: <%s>" % other)

    def test__when__other__given__node_from_other_graph__then__exception(self):
        graph_1 = Graph()
        tail_1 = graph_1.create_node()
        head_1 = graph_1.create_node()
        graph_2 = Graph()
        node_2 = graph_2.create_node()
        relation = tail_1.create_relation_to(head_1)

        assert_that(relation.other) \
            .raises(ValueError) \
            .when_called_with(node_2) \
            .is_equal_to("'node' is invalid: <%s>" % node_2)

    def test__when__delete__given____then__graph_none_ident_released(self):
        graph = Graph()
        tail = graph.create_node()
        head = graph.create_node()
        ident = graph.next_ident()
        relation = tail.create_relation_to(head)
        relation.delete()

        assert_that(relation.graph).is_none()
        assert_that(graph.next_ident()).is_equal_to(ident)
