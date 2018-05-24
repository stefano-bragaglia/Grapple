from unittest import TestCase

from arpeggio import NoMatch, ParserPython, visit_parse_tree
from assertpy import assert_that

from grapple.parsing.grammar import order_by, sortable
from grapple.parsing.visitor import KnowledgeVisitor


class TestParsing(TestCase):
    def test_sortable_000(self):
        assert_that(self.process) \
            .raises(NoMatch) \
            .when_called_with(sortable, '~other~') \
            .starts_with("Expected entity or entity or ''' or '\"' or identifier at position")

    def test_sortable_001(self):
        assert_that(self.process(sortable, '$ent')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent'}}})

    def test_sortable_002(self):
        assert_that(self.process(sortable, '$ent ASC')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent'}}})

    def test_sortable_003(self):
        assert_that(self.process(sortable, '$ent Asc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent'}}})

    def test_sortable_004(self):
        assert_that(self.process(sortable, '$ent asc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent'}}})

    def test_sortable_005(self):
        assert_that(self.process(sortable, '$ent ASCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent'}}})

    def test_sortable_006(self):
        assert_that(self.process(sortable, '$ent Ascending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent'}}})

    def test_sortable_007(self):
        assert_that(self.process(sortable, '$ent ascending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent'}}})

    def test_sortable_008(self):
        assert_that(self.process(sortable, '$ent DESC')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent'}}})

    def test_sortable_009(self):
        assert_that(self.process(sortable, '$ent Desc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent'}}})

    def test_sortable_010(self):
        assert_that(self.process(sortable, '$ent desc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent'}}})

    def test_sortable_011(self):
        assert_that(self.process(sortable, '$ent DESCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent'}}})

    def test_sortable_012(self):
        assert_that(self.process(sortable, '$ent Descending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent'}}})

    def test_sortable_013(self):
        assert_that(self.process(sortable, '$ent descending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent'}}})

    def test_sortable_014(self):
        assert_that(self.process(sortable, '$ent.')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent'}}})

    def test_sortable_015(self):
        assert_that(self.process(sortable, '$ent. ASC')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'ASC'}}})

    def test_sortable_016(self):
        assert_that(self.process(sortable, '$ent. Asc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'Asc'}}})

    def test_sortable_017(self):
        assert_that(self.process(sortable, '$ent. asc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'asc'}}})

    def test_sortable_018(self):
        assert_that(self.process(sortable, '$ent. ASCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'ASCENDING'}}})

    def test_sortable_019(self):
        assert_that(self.process(sortable, '$ent. Ascending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'Ascending'}}})

    def test_sortable_020(self):
        assert_that(self.process(sortable, '$ent. ascending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'ascending'}}})

    def test_sortable_021(self):
        assert_that(self.process(sortable, '$ent. DESC')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'DESC'}}})

    def test_sortable_022(self):
        assert_that(self.process(sortable, '$ent. Desc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'Desc'}}})

    def test_sortable_023(self):
        assert_that(self.process(sortable, '$ent. desc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'desc'}}})

    def test_sortable_024(self):
        assert_that(self.process(sortable, '$ent. DESCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'DESCENDING'}}})

    def test_sortable_025(self):
        assert_that(self.process(sortable, '$ent. Descending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'Descending'}}})

    def test_sortable_026(self):
        assert_that(self.process(sortable, '$ent. descending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'descending'}}})

    def test_sortable_027(self):
        assert_that(self.process(sortable, '$ent .')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent'}}})

    def test_sortable_028(self):
        assert_that(self.process(sortable, '$ent . ASC')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'ASC'}}})

    def test_sortable_029(self):
        assert_that(self.process(sortable, '$ent . Asc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'Asc'}}})

    def test_sortable_030(self):
        assert_that(self.process(sortable, '$ent . asc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'asc'}}})

    def test_sortable_031(self):
        assert_that(self.process(sortable, '$ent . ASCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'ASCENDING'}}})

    def test_sortable_032(self):
        assert_that(self.process(sortable, '$ent . Ascending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'Ascending'}}})

    def test_sortable_033(self):
        assert_that(self.process(sortable, '$ent . ascending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'ascending'}}})

    def test_sortable_034(self):
        assert_that(self.process(sortable, '$ent . DESC')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'DESC'}}})

    def test_sortable_035(self):
        assert_that(self.process(sortable, '$ent . Desc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'Desc'}}})

    def test_sortable_036(self):
        assert_that(self.process(sortable, '$ent . desc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'desc'}}})

    def test_sortable_037(self):
        assert_that(self.process(sortable, '$ent . DESCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'DESCENDING'}}})

    def test_sortable_038(self):
        assert_that(self.process(sortable, '$ent . Descending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'Descending'}}})

    def test_sortable_039(self):
        assert_that(self.process(sortable, '$ent . descending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'descending'}}})

    def test_sortable_040(self):
        assert_that(self.process(sortable, '$ent.key')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_041(self):
        assert_that(self.process(sortable, '$ent.key ASC')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_042(self):
        assert_that(self.process(sortable, '$ent.key Asc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_043(self):
        assert_that(self.process(sortable, '$ent.key asc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_044(self):
        assert_that(self.process(sortable, '$ent.key ASCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_045(self):
        assert_that(self.process(sortable, '$ent.key Ascending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_046(self):
        assert_that(self.process(sortable, '$ent.key ascending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_047(self):
        assert_that(self.process(sortable, '$ent.key DESC')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_048(self):
        assert_that(self.process(sortable, '$ent.key Desc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_049(self):
        assert_that(self.process(sortable, '$ent.key desc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_050(self):
        assert_that(self.process(sortable, '$ent.key DESCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_051(self):
        assert_that(self.process(sortable, '$ent.key Descending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_052(self):
        assert_that(self.process(sortable, '$ent.key descending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_053(self):
        assert_that(self.process(sortable, '$ent."key"')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_054(self):
        assert_that(self.process(sortable, '$ent."key" ASC')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_055(self):
        assert_that(self.process(sortable, '$ent."key" Asc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_056(self):
        assert_that(self.process(sortable, '$ent."key" asc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_057(self):
        assert_that(self.process(sortable, '$ent."key" ASCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_058(self):
        assert_that(self.process(sortable, '$ent."key" Ascending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_059(self):
        assert_that(self.process(sortable, '$ent."key" ascending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_060(self):
        assert_that(self.process(sortable, '$ent."key" DESC')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_061(self):
        assert_that(self.process(sortable, '$ent."key" Desc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_062(self):
        assert_that(self.process(sortable, '$ent."key" desc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_063(self):
        assert_that(self.process(sortable, '$ent."key" DESCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_064(self):
        assert_that(self.process(sortable, '$ent."key" Descending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_065(self):
        assert_that(self.process(sortable, '$ent."key" descending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_066(self):
        assert_that(self.process(sortable, "$ent.'key'")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_067(self):
        assert_that(self.process(sortable, "$ent.'key' ASC")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_068(self):
        assert_that(self.process(sortable, "$ent.'key' Asc")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_069(self):
        assert_that(self.process(sortable, "$ent.'key' asc")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_070(self):
        assert_that(self.process(sortable, "$ent.'key' ASCENDING")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_071(self):
        assert_that(self.process(sortable, "$ent.'key' Ascending")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_072(self):
        assert_that(self.process(sortable, "$ent.'key' ascending")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_073(self):
        assert_that(self.process(sortable, "$ent.'key' DESC")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_074(self):
        assert_that(self.process(sortable, "$ent.'key' Desc")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_075(self):
        assert_that(self.process(sortable, "$ent.'key' desc")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_076(self):
        assert_that(self.process(sortable, "$ent.'key' DESCENDING")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_077(self):
        assert_that(self.process(sortable, "$ent.'key' Descending")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_078(self):
        assert_that(self.process(sortable, "$ent.'key' descending")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'entity': '$ent', 'field': 'key'}}})

    def test_sortable_079(self):
        assert_that(self.process(sortable, 'reference')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'name': 'reference'}}})

    def test_sortable_080(self):
        assert_that(self.process(sortable, "reference ASC")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'name': 'reference'}}})

    def test_sortable_081(self):
        assert_that(self.process(sortable, "reference Asc")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'name': 'reference'}}})

    def test_sortable_082(self):
        assert_that(self.process(sortable, "reference asc")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'name': 'reference'}}})

    def test_sortable_083(self):
        assert_that(self.process(sortable, "reference ASCENDING")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'name': 'reference'}}})

    def test_sortable_084(self):
        assert_that(self.process(sortable, "reference Ascending")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'name': 'reference'}}})

    def test_sortable_085(self):
        assert_that(self.process(sortable, "reference ascending")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'name': 'reference'}}})

    def test_sortable_086(self):
        assert_that(self.process(sortable, "reference DESC")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'name': 'reference'}}})

    def test_sortable_087(self):
        assert_that(self.process(sortable, "reference Desc")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'name': 'reference'}}})

    def test_sortable_088(self):
        assert_that(self.process(sortable, "reference desc")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'name': 'reference'}}})

    def test_sortable_089(self):
        assert_that(self.process(sortable, "reference DESCENDING")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'name': 'reference'}}})

    def test_sortable_090(self):
        assert_that(self.process(sortable, "reference Descending")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'name': 'reference'}}})

    def test_sortable_091(self):
        assert_that(self.process(sortable, "reference descending")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'name': 'reference'}}})

    def test_sortable_092(self):
        assert_that(self.process(sortable, "'reference'")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'name': 'reference'}}})

    def test_sortable_093(self):
        assert_that(self.process(sortable, "'reference' ASC")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'name': 'reference'}}})

    def test_sortable_094(self):
        assert_that(self.process(sortable, "'reference' Asc")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'name': 'reference'}}})

    def test_sortable_095(self):
        assert_that(self.process(sortable, "'reference' asc")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'name': 'reference'}}})

    def test_sortable_096(self):
        assert_that(self.process(sortable, "'reference' ASCENDING")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'name': 'reference'}}})

    def test_sortable_097(self):
        assert_that(self.process(sortable, "'reference' Ascending")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'name': 'reference'}}})

    def test_sortable_098(self):
        assert_that(self.process(sortable, "'reference' ascending")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'name': 'reference'}}})

    def test_sortable_099(self):
        assert_that(self.process(sortable, "'reference' DESC")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'name': 'reference'}}})

    def test_sortable_100(self):
        assert_that(self.process(sortable, "'reference' Desc")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'name': 'reference'}}})

    def test_sortable_101(self):
        assert_that(self.process(sortable, "'reference' desc")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'name': 'reference'}}})

    def test_sortable_102(self):
        assert_that(self.process(sortable, "'reference' DESCENDING")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'name': 'reference'}}})

    def test_sortable_103(self):
        assert_that(self.process(sortable, "'reference' Descending")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'name': 'reference'}}})

    def test_sortable_104(self):
        assert_that(self.process(sortable, "'reference' descending")) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'name': 'reference'}}})

    def test_sortable_105(self):
        assert_that(self.process(sortable, '"reference"')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'name': 'reference'}}})

    def test_sortable_106(self):
        assert_that(self.process(sortable, '"reference" ASC')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'name': 'reference'}}})

    def test_sortable_107(self):
        assert_that(self.process(sortable, '"reference" Asc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'name': 'reference'}}})

    def test_sortable_108(self):
        assert_that(self.process(sortable, '"reference" asc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'name': 'reference'}}})

    def test_sortable_109(self):
        assert_that(self.process(sortable, '"reference" ASCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'name': 'reference'}}})

    def test_sortable_110(self):
        assert_that(self.process(sortable, '"reference" Ascending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'name': 'reference'}}})

    def test_sortable_111(self):
        assert_that(self.process(sortable, '"reference" ascending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': True, 'name': 'reference'}}})

    def test_sortable_112(self):
        assert_that(self.process(sortable, '"reference" DESC')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'name': 'reference'}}})

    def test_sortable_113(self):
        assert_that(self.process(sortable, '"reference" Desc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'name': 'reference'}}})

    def test_sortable_114(self):
        assert_that(self.process(sortable, '"reference" desc')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'name': 'reference'}}})

    def test_sortable_115(self):
        assert_that(self.process(sortable, '"reference" DESCENDING')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'name': 'reference'}}})

    def test_sortable_116(self):
        assert_that(self.process(sortable, '"reference" Descending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'name': 'reference'}}})

    def test_sortable_117(self):
        assert_that(self.process(sortable, '"reference" descending')) \
            .contains_only('data') \
            .contains_entry({'data': {'sortable': {'ascending': False, 'name': 'reference'}}})

    @staticmethod
    def process(scope, content) -> dict:
        parser = ParserPython(scope)
        parse_tree = parser.parse(content)
        return visit_parse_tree(parse_tree, KnowledgeVisitor())
