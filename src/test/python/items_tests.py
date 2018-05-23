from unittest import TestCase

from arpeggio import NoMatch, ParserPython, visit_parse_tree
from assertpy import assert_that

from grapple.parsing.grammar import order_by, sortable
from grapple.parsing.visitor import KnowledgeVisitor


class TestParsing(TestCase):
    def test_order_by_00(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(order_by, '~other~') \
            .starts_with('Expected key_order at position')

    def test_order_by_01(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(order_by, 'ORDER') \
            .starts_with('Expected key_by at position')

    def test_order_by_02(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(order_by, 'ORDER BY') \
            .starts_with("Expected entity or entity or ''' or '\"' or identifier at position")

    def test_order_by_03(self):
        assert_that(self.process(order_by, 'ORDER BY $ent')) \
            .contains_only('data') \
            .contains_entry({'data': 'SKIP'})

    def test_sortable_00(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(sortable, '~other~') \
            .starts_with("Expected entity or entity or ''' or '\"' or identifier at position")

    def test_sortable_01(self):
        assert_that(self.process(sortable, '$ent')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent'}}})

    def test_sortable_02(self):
        assert_that(self.process(sortable, '$ent ASC')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent'}}})

    def test_sortable_03(self):
        assert_that(self.process(sortable, '$ent Asc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent'}}})

    def test_sortable_04(self):
        assert_that(self.process(sortable, '$ent asc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent'}}})

    def test_sortable_05(self):
        assert_that(self.process(sortable, '$ent ASCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent'}}})

    def test_sortable_06(self):
        assert_that(self.process(sortable, '$ent Ascending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent'}}})

    def test_sortable_07(self):
        assert_that(self.process(sortable, '$ent ascending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent'}}})

    def test_sortable_08(self):
        assert_that(self.process(sortable, '$ent DESC')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent'}}})

    def test_sortable_09(self):
        assert_that(self.process(sortable, '$ent Desc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent'}}})

    def test_sortable_10(self):
        assert_that(self.process(sortable, '$ent desc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent'}}})

    def test_sortable_11(self):
        assert_that(self.process(sortable, '$ent DESCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent'}}})

    def test_sortable_12(self):
        assert_that(self.process(sortable, '$ent Descending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent'}}})

    def test_sortable_13(self):
        assert_that(self.process(sortable, '$ent descending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent'}}})

    def test_sortable_14(self):
        assert_that(self.process(sortable, '$ent.')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent'}}})

    def test_sortable_15(self):
        assert_that(self.process(sortable, '$ent. ASC')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'ASC'}}})

    def test_sortable_16(self):
        assert_that(self.process(sortable, '$ent. Asc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'Asc'}}})

    def test_sortable_17(self):
        assert_that(self.process(sortable, '$ent. asc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'asc'}}})

    def test_sortable_18(self):
        assert_that(self.process(sortable, '$ent. ASCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'ASCENDING'}}})

    def test_sortable_19(self):
        assert_that(self.process(sortable, '$ent. Ascending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'Ascending'}}})

    def test_sortable_20(self):
        assert_that(self.process(sortable, '$ent. ascending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'ascending'}}})

    def test_sortable_21(self):
        assert_that(self.process(sortable, '$ent. DESC')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'DESC'}}})

    def test_sortable_22(self):
        assert_that(self.process(sortable, '$ent. Desc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'Desc'}}})

    def test_sortable_23(self):
        assert_that(self.process(sortable, '$ent. desc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'desc'}}})

    def test_sortable_24(self):
        assert_that(self.process(sortable, '$ent. DESCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'DESCENDING'}}})

    def test_sortable_25(self):
        assert_that(self.process(sortable, '$ent. Descending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'Descending'}}})

    def test_sortable_26(self):
        assert_that(self.process(sortable, '$ent. descending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'descending'}}})

    def test_sortable_27(self):
        assert_that(self.process(sortable, '$ent .')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent'}}})

    def test_sortable_28(self):
        assert_that(self.process(sortable, '$ent . ASC')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'ASC'}}})

    def test_sortable_29(self):
        assert_that(self.process(sortable, '$ent . Asc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'Asc'}}})

    def test_sortable_30(self):
        assert_that(self.process(sortable, '$ent . asc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'asc'}}})

    def test_sortable_31(self):
        assert_that(self.process(sortable, '$ent . ASCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'ASCENDING'}}})

    def test_sortable_32(self):
        assert_that(self.process(sortable, '$ent . Ascending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'Ascending'}}})

    def test_sortable_33(self):
        assert_that(self.process(sortable, '$ent . ascending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'ascending'}}})

    def test_sortable_34(self):
        assert_that(self.process(sortable, '$ent . DESC')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'DESC'}}})

    def test_sortable_35(self):
        assert_that(self.process(sortable, '$ent . Desc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'Desc'}}})

    def test_sortable_36(self):
        assert_that(self.process(sortable, '$ent . desc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'desc'}}})

    def test_sortable_37(self):
        assert_that(self.process(sortable, '$ent . DESCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'DESCENDING'}}})

    def test_sortable_38(self):
        assert_that(self.process(sortable, '$ent . Descending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'Descending'}}})

    def test_sortable_39(self):
        assert_that(self.process(sortable, '$ent . descending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'descending'}}})

    def test_sortable_40(self):
        assert_that(self.process(sortable, '$ent.key')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_41(self):
        assert_that(self.process(sortable, '$ent.key ASC')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_42(self):
        assert_that(self.process(sortable, '$ent.key Asc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_43(self):
        assert_that(self.process(sortable, '$ent.key asc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_44(self):
        assert_that(self.process(sortable, '$ent.key ASCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_45(self):
        assert_that(self.process(sortable, '$ent.key Ascending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_46(self):
        assert_that(self.process(sortable, '$ent.key ascending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_47(self):
        assert_that(self.process(sortable, '$ent.key DESC')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_48(self):
        assert_that(self.process(sortable, '$ent.key Desc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_49(self):
        assert_that(self.process(sortable, '$ent.key desc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_50(self):
        assert_that(self.process(sortable, '$ent.key DESCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_51(self):
        assert_that(self.process(sortable, '$ent.key Descending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_52(self):
        assert_that(self.process(sortable, '$ent.key descending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_53(self):
        assert_that(self.process(sortable, '$ent."key"')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_54(self):
        assert_that(self.process(sortable, '$ent."key" ASC')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_55(self):
        assert_that(self.process(sortable, '$ent."key" Asc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_56(self):
        assert_that(self.process(sortable, '$ent."key" asc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_57(self):
        assert_that(self.process(sortable, '$ent."key" ASCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_58(self):
        assert_that(self.process(sortable, '$ent."key" Ascending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_59(self):
        assert_that(self.process(sortable, '$ent."key" ascending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_60(self):
        assert_that(self.process(sortable, '$ent."key" DESC')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_61(self):
        assert_that(self.process(sortable, '$ent."key" Desc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_62(self):
        assert_that(self.process(sortable, '$ent."key" desc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_63(self):
        assert_that(self.process(sortable, '$ent."key" DESCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_64(self):
        assert_that(self.process(sortable, '$ent."key" Descending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_65(self):
        assert_that(self.process(sortable, '$ent."key" descending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_66(self):
        assert_that(self.process(sortable, "$ent.'key'")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_67(self):
        assert_that(self.process(sortable, "$ent.'key' ASC")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_68(self):
        assert_that(self.process(sortable, "$ent.'key' Asc")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_69(self):
        assert_that(self.process(sortable, "$ent.'key' asc")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_70(self):
        assert_that(self.process(sortable, "$ent.'key' ASCENDING")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_71(self):
        assert_that(self.process(sortable, "$ent.'key' Ascending")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_72(self):
        assert_that(self.process(sortable, "$ent.'key' ascending")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_73(self):
        assert_that(self.process(sortable, "$ent.'key' DESC")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_74(self):
        assert_that(self.process(sortable, "$ent.'key' Desc")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_75(self):
        assert_that(self.process(sortable, "$ent.'key' desc")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_76(self):
        assert_that(self.process(sortable, "$ent.'key' DESCENDING")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_77(self):
        assert_that(self.process(sortable, "$ent.'key' Descending")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_78(self):
        assert_that(self.process(sortable, "$ent.'key' descending")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_79(self):
        assert_that(self.process(sortable, 'name')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    @staticmethod
    def process(scope, content) -> dict:
        parser = ParserPython(scope)
        parse_tree = parser.parse(content)
        return visit_parse_tree(parse_tree, KnowledgeVisitor())
