from unittest import TestCase

from assertpy import assert_that

from grapple.bom.container import Container


class TestContainer(TestCase):

    def test__when__using__given__properties__then__only_used_keys(self):
        container = Container()

        assert_that(container.keys).is_empty()

        container.set_property('key1', True)
        container.set_property('key2', 1)
        container.set_property('key3', 2.0)
        container.set_property('key4', 'value')
        container.set_property('key1', [True, False])
        container.set_property('key2', [1, 2])
        container.set_property('key3', [2.0, 3.0])
        container.set_property('key4', ['value', 'value'])
        assert_that(container.keys).contains_only('key1', 'key2', 'key3', 'key4')

    def test__when__get_properties__given__none__then__all_properties(self):
        container = Container()
        container.set_property('key1', True)
        container.set_property('key2', 1)
        container.set_property('key3', 2.0)
        container.set_property('key4', 'value')

        assert_that(container.get_properties(keys=None)) \
            .contains_only('key1', 'key2', 'key3', 'key4') \
            .contains_entry({'key1': True}, {'key2': 1}, {'key3': 2.0}, {'key4': 'value'})

    def test__when__get_properties__given__some__then__all_properties(self):
        container = Container()
        container.set_property('key1', True)
        container.set_property('key2', 1)
        container.set_property('key3', 2.0)
        container.set_property('key4', 'value')

        assert_that(container.get_properties(keys=['key1', 'key2'])) \
            .contains_only('key1', 'key2') \
            .contains_entry({'key1': True}, {'key2': 1})

    def test__when__get_properties__given__some_with_outlier__then__all_properties(self):
        container = Container()
        container.set_property('key1', True)
        container.set_property('key2', 1)
        container.set_property('key3', 2.0)
        container.set_property('key4', 'value')

        assert_that(container.get_properties(keys=['key1', 'key5'])) \
            .contains_only('key1') \
            .contains_entry({'key1': True})

    def test__when__has_property__given__non_existing_key__then__false(self):
        container = Container()

        assert_that(container.has_property('key')).is_false()

    def test__when__has_property__given__existing_key__then__true(self):
        container = Container()
        container.set_property('key', 'value')

        assert_that(container.has_property('key')).is_true()

    def test__when__get_property__given__existing_key__then__value(self):
        container = Container()
        container.set_property('key', 'value')

        assert_that(container.get_property('key')).is_equal_to('value')

    def test__when__get_property__given__non_existing_key__then__none(self):
        container = Container()

        assert_that(container.get_property('key')).is_none()

    def test__when__get_property__given__existing_key_and_default__then__value(self):
        container = Container()
        container.set_property('key', 'value')

        assert_that(container.get_property('key', 'default')).is_equal_to('value')

    def test__when__get_property__given__non_existing_key_and_default__then__default(self):
        container = Container()

        assert_that(container.get_property('key', 'default')).is_equal_to('default')

    def test__set_property__given__key_and_value__then__value_set_to_key(self):
        container = Container()
        container.set_property('key', 'value')

        assert_that(container.has_property('key')).is_true()
        assert_that(container.get_property('key')).is_equal_to('value')

    def test__set_property__given__key_and_none__then__key_deleted(self):
        container = Container()
        container.set_property('key', 'value')
        container.set_property('key', None)

        assert_that(container.has_property('key')).is_false()

    def test__set_property__given__non_existing_key_and_none__then__key_deleted(self):
        container = Container()
        container.set_property('key', None)

        assert_that(container.has_property('key')).is_false()

    def test__remove_property__given__existing_key__then__key_deleted(self):
        container = Container()
        container.set_property('key', 'value')
        container.remove_property('key')

        assert_that(container.has_property('key')).is_false()

    def test__remove_property__given__non_existing_key__then__nothing(self):
        container = Container()
        container.remove_property('key')

        assert_that(container.has_property('key')).is_false()
