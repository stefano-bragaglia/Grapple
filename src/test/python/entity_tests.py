from unittest import TestCase

from assertpy import assert_that

from grapple.bom.entity import Entity
from grapple.bom.graph import Graph


class TestEntity(TestCase):

    def test__when__init__given__graph_and_ident__then__properties_are_set(self):
        graph = Graph()
        entity = Entity(graph, 5)

        assert_that(entity.graph).is_equal_to(graph)
        assert_that(entity.ident).is_equal_to(5)
