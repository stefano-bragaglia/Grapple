from unittest import TestCase

from assertpy import assert_that

from grapple.bom.graph import Graph
from grapple.rete.builders import Builder


class TestService(TestCase):

    def test_load_from_str_0(self):
        builder = Builder().load_from_str('')
        assert_that(builder.build) \
            .raises(ValueError) \
            .when_called_with() \
            .is_equal_to('No clause given')

    def test_session_insert_0(self):
        graph = Graph()
        kb = Builder().load_from_str('RULE RETURN True').build()
        session = kb.get_session(graph)
        assert_that(session.insert) \
            .raises(ValueError) \
            .when_called_with(None) \
            .is_equal_to('This something is invalid')

    def test_return_value_0(self):
        graph = Graph()
        kb = Builder().load_from_str('RULE RETURN "Coot-coot!" AS msg').build()
        session = kb.get_session(graph)
        session.fire_all()
        session.close()
        assert_that(session).is_not_none()
