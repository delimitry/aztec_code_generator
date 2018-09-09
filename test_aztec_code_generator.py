#!/usr/bin/env python
#-*- coding: utf-8 -*-

import unittest
from aztec_code_generator import (
    reed_solomon, find_optimal_sequence, optimal_sequence_to_bits, get_data_codewords,
)


class Test(unittest.TestCase):
    """
    Test aztec_code_generator module
    """

    def test_reed_solomon(self):
        """ Test reed_solomon function """
        cw = []
        reed_solomon(cw, 0, 0, 0, 0)
        self.assertEqual(cw, [])
        cw = [0, 0] + [0, 0]
        reed_solomon(cw, 2, 2, 16, 19)
        self.assertEqual(cw, [0, 0, 0, 0])
        cw = [9, 50, 1, 41, 47, 2, 39, 37, 1, 27] + [0, 0, 0, 0, 0, 0, 0]
        reed_solomon(cw, 10, 7, 64, 67)
        self.assertEqual(cw, [9, 50, 1, 41, 47, 2, 39, 37, 1, 27, 38, 50, 8, 16, 10, 20, 40])
        cw = [0, 9] + [0, 0, 0, 0, 0]
        reed_solomon(cw, 2, 5, 16, 19)
        self.assertEqual(cw, [0, 9, 12, 2, 3, 1, 9])

    def test_find_optimal_sequence(self):
        """ Test find_optimal_sequence function """
        self.assertEqual(find_optimal_sequence(''), [])
        self.assertEqual(find_optimal_sequence('ABC'), ['A', 'B', 'C'])
        self.assertEqual(find_optimal_sequence('abc'), ['L/L', 'a', 'b', 'c'])
        self.assertEqual(find_optimal_sequence('Wikipedia, the free encyclopedia'), [
            'W', 'L/L', 'i', 'k', 'i', 'p', 'e', 'd', 'i', 'a', 'P/S', ', ', 't', 'h', 'e',
            ' ', 'f', 'r', 'e', 'e', ' ', 'e', 'n', 'c', 'y', 'c', 'l', 'o', 'p', 'e', 'd', 'i', 'a'])
        self.assertEqual(find_optimal_sequence('Code 2D!'), [
            'C', 'L/L', 'o', 'd', 'e', 'D/L', ' ', '2', 'U/S', 'D', 'P/S', '!'])
        self.assertEqual(find_optimal_sequence('a\xff'), ['B/S', 2, 'a', '\xff'])
        self.assertEqual(find_optimal_sequence('a' + '\xff' * 30), ['B/S', 31, 'a'] + ['\xff'] * 30)
        self.assertEqual(find_optimal_sequence('a' + '\xff' * 31), ['B/S', 0, 32, 'a'] + ['\xff'] * 31)
        self.assertEqual(find_optimal_sequence('!#$%&?'), ['M/L', 'P/L', '!', '#', '$', '%', '&', '?'])
        self.assertEqual(find_optimal_sequence('!#$%&?\xff'), [
            'M/L', 'P/L', '!', '#', '$', '%', '&', '?', 'U/L', 'B/S', 1, '\xff'])
        self.assertEqual(find_optimal_sequence('!#$%&\xff'), ['B/S', 6, '!', '#', '$', '%', '&', '\xff'])
        self.assertEqual(find_optimal_sequence('@\xff'), ['B/S', 2, '@', '\xff'])
        self.assertEqual(find_optimal_sequence('. @\xff'), ['P/S', '. ', 'B/S', 2, '@', '\xff'])
        self.assertIn(find_optimal_sequence('. : '), [['P/S', '. ', 'P/S', ': '], ['M/L', 'P/L', '. ', ': ']])
        self.assertEqual(find_optimal_sequence('\r\n\r\n\r\n'), ['M/L', 'P/L', '\r\n', '\r\n', '\r\n'])
        self.assertEqual(find_optimal_sequence('Code 2D!'), [
            'C', 'L/L', 'o', 'd', 'e', 'D/L', ' ', '2', 'U/S', 'D', 'P/S', '!'])
        self.assertEqual(find_optimal_sequence('test 1!test 2!'), [
            'L/L', 't', 'e', 's', 't', 'D/L', ' ', '1', 'P/S', '!', 'U/L',
            'L/L', 't', 'e', 's', 't', 'D/L', ' ', '2', 'P/S', '!'])
        self.assertEqual(find_optimal_sequence('Abc-123X!Abc-123X!'), [
            'A', 'L/L', 'b', 'c', 'D/L', 'P/S', '-', '1', '2', '3', 'U/L', 'X', 'P/S', '!',
            'A', 'L/L', 'b', 'c', 'D/L', 'P/S', '-', '1', '2', '3', 'U/S', 'X', 'P/S', '!'])
        self.assertEqual(find_optimal_sequence('ABCabc1a2b3e'), [
            'A', 'B', 'C', 'L/L', 'a', 'b', 'c', 'B/S', 5, '1', 'a', '2', 'b', '3', 'e'])
        self.assertEqual(find_optimal_sequence('ABCabc1a2b3eBC'), [
            'A', 'B', 'C', 'L/L', 'a', 'b', 'c', 'B/S', 6, '1', 'a', '2', 'b', '3', 'e', 'M/L', 'U/L', 'B', 'C'])
        self.assertEqual(find_optimal_sequence('0a|5Tf.l'), [
            'D/L', '0', 'U/L', 'L/L', 'a', 'M/L', '|', 'U/L',
            'D/L', '5', 'U/L', 'L/L', 'U/S', 'T', 'f', 'P/S', '.', 'l'])
        self.assertEqual(find_optimal_sequence('*V1\x0c {Pa'), [
            'P/S', '*', 'V', 'B/S', 2, '1', '\x0c', ' ', 'P/S', '{', 'P', 'L/L', 'a'])
        self.assertEqual(find_optimal_sequence('~Fxlb"I4'), [
            'M/L', '~', 'U/L', 'D/L', 'U/S', 'F', 'U/L', 'L/L', 'x', 'l', 'b', 'D/L', 'P/S', '"', 'U/S', 'I', '4'])
        self.assertEqual(find_optimal_sequence('\\+=R?1'), [
            'M/L', '\\', 'P/L', '+', '=', 'U/L', 'R', 'D/L', 'P/S', '?', '1'])

    def test_optimal_sequence_to_bits(self):
        """ Test optimal_sequence_to_bits function """
        self.assertEqual(optimal_sequence_to_bits([]), '')
        self.assertEqual(optimal_sequence_to_bits(['P/S']), '00000')
        self.assertEqual(optimal_sequence_to_bits(['A']), '00010')
        self.assertEqual(optimal_sequence_to_bits(['B/S', 1, '\xff']), '111110000111111111')
        self.assertEqual(optimal_sequence_to_bits(['B/S', 0, 1, '\xff']), '11111000000000000000111111111')
        self.assertEqual(optimal_sequence_to_bits(['A']), '00010')

    def test_get_data_codewords(self):
        """ Test get_data_codewords function """
        self.assertEqual(get_data_codewords('000010', 6), [0b000010])
        self.assertEqual(get_data_codewords('111100', 6), [0b111100])
        self.assertEqual(get_data_codewords('111110', 6), [0b111110, 0b011111])
        self.assertEqual(get_data_codewords('000000', 6), [0b000001, 0b011111])
        self.assertEqual(get_data_codewords('111111', 6), [0b111110, 0b111110])
        self.assertEqual(get_data_codewords('111101111101', 6), [0b111101, 0b111101])


if __name__ == '__main__':
    unittest.main(verbosity=2)
