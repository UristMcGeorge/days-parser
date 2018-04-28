import unittest
import unittest.mock
from io import StringIO
import sys
from collections import OrderedDict
from days_parser.days_parser import DaysParser


class TestDaysParser(unittest.TestCase):

    @unittest.mock.patch('sys.stdout', new_callable=StringIO)
    def assert_stdout(self, test, mock_stdout):
        parser = DaysParser(test['filename'])
        parser.print_parsed()
        self.assertEqual(mock_stdout.getvalue(), test['expected_output'])

    def test_print_parsed(self):
        tests = [
            {'filename': 'tests/1.csv',
             'expected_output':
'''[{'day': 'mon', 'description': 'first_desc 1', 'square': 1, 'value': 1},
 {'day': 'tue', 'description': 'first_desc 25', 'square': 25, 'value': 5},
 {'day': 'wed', 'description': 'first_desc 4', 'square': 4, 'value': 2},
 {'day': 'thu', 'description': 'first_desc 6', 'double': 6, 'value': 3},
 {'day': 'fri', 'description': 'first_desc 6', 'double': 6, 'value': 3}]
'''
            },
            {'filename': 'tests/2.csv',
             'expected_output':
'''[{'day': 'mon', 'description': 'second_desc 4', 'square': 4, 'value': 2},
 {'day': 'tue', 'description': 'second_desc 4', 'square': 4, 'value': 2},
 {'day': 'wed', 'description': 'second_desc 4', 'square': 4, 'value': 2},
 {'day': 'thu', 'description': 'second_desc 4', 'double': 4, 'value': 2},
 {'day': 'fri', 'description': 'second_desc 6', 'double': 6, 'value': 3}]
'''
            },
            {'filename': 'tests/3.csv',
             'expected_output':
'''[{'day': 'mon', 'description': 'third_desc 9', 'square': 9, 'value': 3},
 {'day': 'tue', 'description': 'third_desc 9', 'square': 9, 'value': 3},
 {'day': 'wed', 'description': 'third_desc 4', 'square': 4, 'value': 2},
 {'day': 'thu', 'description': 'third_desc 4', 'double': 4, 'value': 2},
 {'day': 'fri', 'description': 'third_desc 2', 'double': 2, 'value': 1}]
'''
            },
        ]
        for test in tests:
            self.assert_stdout(test)

    def test_get_parsed(self):
        tests = [
            {'filename': 'tests/1.csv',
             'expected_output':
[{'day': 'mon', 'description': 'first_desc 1', 'square': 1, 'value': 1},
 {'day': 'tue', 'description': 'first_desc 25', 'square': 25, 'value': 5},
 {'day': 'wed', 'description': 'first_desc 4', 'square': 4, 'value': 2},
 {'day': 'thu', 'description': 'first_desc 6', 'double': 6, 'value': 3},
 {'day': 'fri', 'description': 'first_desc 6', 'double': 6, 'value': 3}]
            },
            {'filename': 'tests/2.csv',
             'expected_output':
[{'day': 'mon', 'description': 'second_desc 4', 'square': 4, 'value': 2},
 {'day': 'tue', 'description': 'second_desc 4', 'square': 4, 'value': 2},
 {'day': 'wed', 'description': 'second_desc 4', 'square': 4, 'value': 2},
 {'day': 'thu', 'description': 'second_desc 4', 'double': 4, 'value': 2},
 {'day': 'fri', 'description': 'second_desc 6', 'double': 6, 'value': 3}]
            },
            {'filename': 'tests/3.csv',
             'expected_output':
[{'day': 'mon', 'description': 'third_desc 9', 'square': 9, 'value': 3},
 {'day': 'tue', 'description': 'third_desc 9', 'square': 9, 'value': 3},
 {'day': 'wed', 'description': 'third_desc 4', 'square': 4, 'value': 2},
 {'day': 'thu', 'description': 'third_desc 4', 'double': 4, 'value': 2},
 {'day': 'fri', 'description': 'third_desc 2', 'double': 2, 'value': 1}]
            },
        ]
        for test in tests:
            parser = DaysParser(test['filename'])
            self.assertEqual(parser.get_parsed(), test['expected_output'])

    def test_duplicated_day_replaced(self):
        row = OrderedDict([
            ('mon-fri', '5'),
            ('mon', '1'),
            ('description', 'example')
            ])
        expected_output = \
[{'day': 'mon', 'description': 'example 1', 'square': 1, 'value': 1},
 {'day': 'tue', 'description': 'example 25', 'square': 25, 'value': 5},
 {'day': 'wed', 'description': 'example 25', 'square': 25, 'value': 5},
 {'day': 'thu', 'description': 'example 10', 'double': 10, 'value': 5},
 {'day': 'fri', 'description': 'example 10', 'double': 10, 'value': 5}]
        parser = DaysParser(None)
        self.assertEqual(parser.parse_input_row(row), expected_output)

    def test_missing_days_accept(self):
        row = OrderedDict([
            ('mon', '1'),
            ('description', 'example')
            ])
        expected_output = \
[{'day': 'mon', 'description': 'example 1', 'square': 1, 'value': 1}]
        parser = DaysParser(None)
        self.assertEqual(parser.parse_input_row(row), expected_output)

    def test_no_days_accept(self):
        row = OrderedDict([
            ('description', 'example')
            ])
        expected_output = []
        parser = DaysParser(None)
        self.assertEqual(parser.parse_input_row(row), expected_output)

    def test_three_range_skip(self):
        row = OrderedDict([('mon-wed-fri', '1'), ('description', 'example')])
        expected_output = []
        parser = DaysParser(None)
        self.assertEqual(parser.parse_input_row(row), expected_output)

    def test_two_lines_fail(self):
        parser = DaysParser('tests/1-two-lines.csv')
        with self.assertRaises(ValueError):
            parser.get_parsed()

    def test_backward_days_fail(self):
        row = OrderedDict([('fri-mon', '1'), ('description', 'example')])
        parser = DaysParser(None)
        with self.assertRaises(ValueError):
            parser.parse_input_row(row)

    def test_non_day_end_range_fail(self):
        row = OrderedDict([('mon-erreur', '1'), ('description', 'example')])
        parser = DaysParser(None)
        with self.assertRaises(ValueError):
            parser.parse_input_row(row)

    def test_non_day_start_range_fail(self):
        row = OrderedDict([('beer-fri', '1'), ('description', 'example')])
        parser = DaysParser(None)
        with self.assertRaises(ValueError):
            parser.parse_input_row(row)


if __name__ == '__main__':
    unittest.main()
