from unittest import TestCase

from assertpy import assert_that

from grapple.bom.graph import Graph
from grapple.tentative_engine.condition import Payload, IsNode, HasLabel, IsRelation, HasType, HasProperty, HasKey, AreEqual

Node = 0
Relation = -1
Other = -2


class TestCondition(TestCase):
    payload = None

    @staticmethod
    def _payload(pos: int = 0) -> Payload:
        if not TestCondition.payload:
            g = Graph()
            n1 = g.create_node()
            n1.add_labels('main', 'person')
            n1.set_property('first name', 'Wiley')
            n1.set_property('middle names', 'E.')
            n1.set_property('last name', 'Coyote')
            n2 = g.create_node()
            n2.add_labels('company')
            n2.set_property('name', 'ACME')
            r = n1.create_relation_to(n2)
            r.add_types('works_at')
            r.set_property('current', True)
            TestCondition.payload = [n1, r, n2]

        return TestCondition.payload[:pos] if pos else TestCondition.payload

    def test__when__validating_is_node__given__empty_payload__then__false(self):
        condition = IsNode()
        assert_that(condition.is_valid([])).is_false()

    def test__when__validating_is_node__given__payload_with_last_node__then__true(self):
        condition = IsNode()
        assert_that(condition.is_valid(self._payload(Node))).is_true()

    def test__when__validating_is_node__given__payload_with_last_relation__then__false(self):
        condition = IsNode()
        assert_that(condition.is_valid(self._payload(Relation))).is_false()

    def test__when__validating_has_label__given__empty_payload__then__false(self):
        condition = HasLabel('label')
        assert_that(condition.is_valid([])).is_false()

    def test__when__validating_has_label__given__payload_with_last_node_with_label__then__true(self):
        condition = HasLabel('company')
        assert_that(condition.is_valid(self._payload(Node))).is_true()

    def test__when__validating_has_label__given__payload_with_last_node_without_label__then__false(self):
        condition = HasLabel('person')
        assert_that(condition.is_valid(self._payload(Node))).is_false()

    def test__when__validating_has_label__given__payload_with_last_relation__then__false(self):
        condition = HasLabel('company')
        assert_that(condition.is_valid(self._payload(Relation))).is_false()

    def test__when__validating_is_relation__given__empty_payload__then__false(self):
        condition = IsRelation()
        assert_that(condition.is_valid([])).is_false()

    def test__when__validating_is_relation__given__payload_with_last_node__then__false(self):
        condition = IsRelation()
        assert_that(condition.is_valid(self._payload(Node))).is_false()

    def test__when__validating_is_relation__given__payload_with_last_relation__then__true(self):
        condition = IsRelation()
        assert_that(condition.is_valid(self._payload(Relation))).is_true()

    def test__when__validating_has_type__given__empty_payload__then__false(self):
        condition = HasType('type')
        assert_that(condition.is_valid([])).is_false()

    def test__when__validating_has_type__given__payload_with_last_relation_with_type__then__true(self):
        condition = HasType('works_at')
        assert_that(condition.is_valid(self._payload(Relation))).is_true()

    def test__when__validating_has_type__given__payload_with_last_relation_without_type__then__false(self):
        condition = HasType('is_located_in')
        assert_that(condition.is_valid(self._payload(Relation))).is_false()

    def test__when__validating_has_type__given__payload_with_last_node__then__false(self):
        condition = HasType('works_at')
        assert_that(condition.is_valid(self._payload(Node))).is_false()

    def test__when__validating_has_key__given__empty_payload__then__false(self):
        condition = HasKey('key')
        assert_that(condition.is_valid([])).is_false()

    def test__when__validating_has_key__given__payload_with_last_node_with_key__then_true(self):
        condition = HasKey('name')
        assert_that(condition.is_valid(self._payload(Node))).is_true()

    def test__when__validating_has_key__given__payload_with_last_node_with_key__then_false(self):
        condition = HasKey('last name')
        assert_that(condition.is_valid(self._payload(Node))).is_false()

    def test__when__validating_has_key__given__payload_with_last_relation_with_key__then_true(self):
        condition = HasKey('current')
        assert_that(condition.is_valid(self._payload(Relation))).is_true()

    def test__when__validating_has_key__given__payload_with_last_relation_without_key__then_false(self):
        condition = HasKey('modified')
        assert_that(condition.is_valid(self._payload(Relation))).is_false()

    def test__when__validating_has_property__given__empty_payload__then__false(self):
        condition = HasProperty('key', 'value')
        assert_that(condition.is_valid([])).is_false()

    def test__when__validating_has_property__given__payload_with_last_node_with_key_with_value__then_true(self):
        condition = HasProperty('name', 'ACME')
        assert_that(condition.is_valid(self._payload(Node))).is_true()

    def test__when__validating_has_property__given__payload_with_last_node_with_key_without_value__then_false(self):
        condition = HasProperty('name', 'Wrong-Name')
        assert_that(condition.is_valid(self._payload(Node))).is_false()

    def test__when__validating_has_property__given__payload_with_last_node_without_key__then_false(self):
        condition = HasProperty('last name', 'Coyote')
        assert_that(condition.is_valid(self._payload(Node))).is_false()

    def test__when__validating_has_property__given__payload_with_last_relation_with_key_with_value__then_true(self):
        condition = HasProperty('current', True)
        assert_that(condition.is_valid(self._payload(Relation))).is_true()

    def test__when__validating_has_property__given__payload_with_last_relation_with_key_without_value__then_false(self):
        condition = HasProperty('current', 123)
        assert_that(condition.is_valid(self._payload(Relation))).is_false()

    def test__when__validating_has_property__given__payload_with_last_relation_without_key__then_false(self):
        condition = HasProperty('last name', 'Coyote')
        assert_that(condition.is_valid(self._payload(Relation))).is_false()

    def test__when__validating_are_equal__given__empty_payload__then__false(self):
        condition = AreEqual()
        assert_that(condition.is_valid([])).is_false()

    def test__when__validating_are_equal__given__empty_other__then__false(self):
        condition = AreEqual()
        assert_that(condition.is_valid(self._payload(Node), [])).is_false()

    def test__when__validating_are_equal__given__payload_other_same_last_node__then__true(self):
        condition = AreEqual()
        assert_that(condition.is_valid(self._payload(Node), self._payload(Node))).is_true()

    def test__when__validating_are_equal__given__payload_other_same_last_relation__then__true(self):
        condition = AreEqual()
        assert_that(condition.is_valid(self._payload(Relation), self._payload(Relation))).is_true()

    def test__when__validating_are_equal__given__payload_other_last_node_vs_relation__then__false(self):
        condition = AreEqual()
        assert_that(condition.is_valid(self._payload(Node), self._payload(Relation))).is_false()

    def test__when__validating_are_equal__given__payload_other_last_relation_vs_node__then__false(self):
        condition = AreEqual()
        assert_that(condition.is_valid(self._payload(Relation), self._payload(Node))).is_false()

    def test__when__validating_are_equal__given__payload_other_mismatch__then__true(self):
        condition = AreEqual()
        assert_that(condition.is_valid(self._payload(Other), self._payload(Relation))).is_false()
