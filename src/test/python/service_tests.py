from unittest import TestCase

from assertpy import assert_that

from grapple.graph import Graph
from grapple.builders import Builder


class TestService(TestCase):

    def test_build_0(self):
        builder = Builder().load_from_str('')
        assert_that(builder.build) \
            .raises(ValueError) \
            .when_called_with() \
            .is_equal_to('No clause given')

    def test_get_session_0(self):
        kb = Builder().load_from_str('RULE RETURN True').build()
        assert_that(kb.get_session) \
            .raises(ValueError) \
            .when_called_with(None) \
            .is_equal_to('This graph is invalid')

    def test_insert_0(self):
        graph = Graph()
        kb = Builder().load_from_str('RULE RETURN True').build()
        session = kb.get_session(graph)
        assert_that(session.insert) \
            .raises(ValueError) \
            .when_called_with(None) \
            .is_equal_to('This entity is invalid')

    def test_return_value_0(self):
        graph = Graph()
        kb = Builder().load_from_str('RULE RETURN "Coot-coot!" AS msg').build()
        session = kb.get_session(graph)
        session.fire_all()
        session.close()
        assert_that(session).is_not_none()
        assert_that(session._graph).is_none()

    def test_create_labels_0(self):
        graph = Graph()
        kb = Builder().load_from_str("RULE CREATE ($n:main:person{name: 'Stefano'}) RETURN labels($n) AS classes").build()
        session = kb.get_session(graph)
        session.fire_all()
        session.close()
        assert_that(session).is_not_none()

