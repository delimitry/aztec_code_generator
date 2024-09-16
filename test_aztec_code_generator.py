#!/usr/bin/env python
#-*- coding: utf-8 -*-

import unittest
from unittest.mock import patch, mock_open, MagicMock
from aztec_code_generator import (
    reed_solomon,
    find_optimal_sequence,
    optimal_sequence_to_bits,
    get_data_codewords,
    SvgFactory,
    AztecCode,
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
        self.assertEqual(find_optimal_sequence('a' + '\xff' * 31), ['B/S', 0, 1, 'a'] + ['\xff'] * 31)
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
            'B/S', 5, '0', 'a', '|', '5', 'T', 'L/L', 'f', 'P/S', '.', 'l'])
        self.assertEqual(find_optimal_sequence('*V1\x0c {Pa'), [
            'P/S', '*', 'V', 'B/S', 5, '1', '\x0c', ' ', '{', 'P', 'L/L', 'a'])
        self.assertEqual(find_optimal_sequence('~Fxlb"I4'), [
            'B/S', 7, '~', 'F', 'x', 'l', 'b', '"', 'I', 'D/L', '4'])
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

class TestSvgFactory(unittest.TestCase):
    def test_init(self):
        data = '<svg><text>example svg data</text></svg>'
        instance = SvgFactory(data)
        self.assertEqual(instance.svg_str, data)
    
    @patch('builtins.open', new_callable=mock_open)
    def test_save(self, mock):
        data = '<svg></svg>'
        filename = 'example_filename.svg'
        instance = SvgFactory(data)
        mock.reset_mock()
        instance.save(filename)
        mock.assert_called_once_with(filename, "w")
        mock().write.assert_called_once_with(data)

    def test_create_svg(self):
        CASES = [
            dict(
                matrix = [['#','#','#'], [' ',' ',' '], ['#','#','#']],
                snapshot = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 5 5"><rect x="0" y="0" width="5" height="5" fill="white" /><path d="M1 1 h3 M1 3 h3 Z" stroke="black" stroke-width="1" style="transform:translateY(0.5px);" /></svg>',
            ),
            dict(
                matrix = [['#',' ',' '], [' ','#',' '], [' ',' ','#']],
                snapshot = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 5 5"><rect x="0" y="0" width="5" height="5" fill="white" /><path d="M1 1 h1 M2 2 h1 M3 3 h1 Z" stroke="black" stroke-width="1" style="transform:translateY(0.5px);" /></svg>',
            ),
            dict(
                matrix = [['#',' '], [' ','#']],
                snapshot = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4 4"><rect x="0" y="0" width="4" height="4" fill="white" /><path d="M1 1 h1 M2 2 h1 Z" stroke="black" stroke-width="1" style="transform:translateY(0.5px);" /></svg>'
            ),
            dict(
                matrix = [['#',' '], [' ','#']],
                border = 3,
                snapshot = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 8 8"><rect x="0" y="0" width="8" height="8" fill="white" /><path d="M3 3 h1 M4 4 h1 Z" stroke="black" stroke-width="1" style="transform:translateY(0.5px);" /></svg>'
            ),
            dict(
                matrix = [[1,0], [0,1]],
                matching_fn = lambda x: x == 1,
                snapshot = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4 4"><rect x="0" y="0" width="4" height="4" fill="white" /><path d="M1 1 h1 M2 2 h1 Z" stroke="black" stroke-width="1" style="transform:translateY(0.5px);" /></svg>'
            ),
        ]
        for case in CASES:
            if "border" in case:
                instance = SvgFactory.create_svg(case["matrix"], border=case["border"])
            elif "matching_fn" in case:
                instance = SvgFactory.create_svg(case["matrix"], matching_fn=case["matching_fn"])
            else:
                instance = SvgFactory.create_svg(case["matrix"])
            self.assertIsInstance(instance, SvgFactory)
            self.assertEqual(
                instance.svg_str,
                case["snapshot"],
                'should match snapshot'
            )

class TestAztecCode(unittest.TestCase):
    def test_save_should_support_svg(self):
        """ Should call SvgFactory.save if file extension ends with .svg """
        mock_svg_factory_save = MagicMock()
        SvgFactory.save = mock_svg_factory_save
        aztec_code = AztecCode('example data')
        filename = 'file.svg'
        aztec_code.save(filename)
        mock_svg_factory_save.assert_called_once_with(filename)


if __name__ == '__main__':
    unittest.main(verbosity=2)
