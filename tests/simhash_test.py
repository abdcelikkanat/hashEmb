from unittest import main, TestCase
from simhash import *


class TestSimhash(TestCase):

    def test_int_value(self):
        self.assertEqual(SimHash(0).input, 0)
        self.assertEqual(SimHash(4390059585430954713).input, 4390059585430954713)
        self.assertEqual(SimHash(9223372036854775808).input, 9223372036854775808)

    def test_value(self):
        self.assertEqual(SimHash(['aaa', 'bbb']).input, 57087923692560392)

    def test_distance(self):
        sh = SimHash('How are you? I AM fine. Thanks. And you?')
        sh2 = SimHash('How old are you ? :-) i am fine. Thanks. And you?')
        self.assertTrue(sh.distance(sh2) > 0)

        sh3 = SimHash(sh2)
        self.assertEqual(sh2.distance(sh3), 0)

        self.assertNotEqual(SimHash('1').distance(SimHash('2')), 0)

    def test_insertion(self):
        sh = SimHash(['aaa'])
        sh.update_signature_insert('bbb')
        self.assertEqual(sh.input, SimHash(['aaa', 'bbb']).input)

    def test_deletion(self):
        sh = SimHash(['aaa', 'bbb', 'ccc'])
        sh.update_signature_delete('ccc')
        self.assertEqual(sh.input, SimHash(['aaa', 'bbb']).input)

    def test_deletion2(self):
        sh = SimHash(['aaa', 'bbb', 'ccc'])
        sh.update_signature_delete('bbb')
        self.assertEqual(sh.input, SimHash(['aaa', 'ccc']).input)