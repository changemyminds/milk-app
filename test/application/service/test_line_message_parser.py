import unittest

from app.application.service.line_message_parser import LineMessageParser


class TestLineMessageParser(unittest.TestCase):
    def test_parse_breast_milk_record(self):
        line_message_parser = LineMessageParser()         
        test_cases = [
            ("12:40-13:00 10cc", ("12:40-13:00", 10)),
            ("12:40-1300 11cc", ("12:40-13:00", 11)),
            ("12:40-1300 12cc", ("12:40-13:00", 12)),
            ("12:40-1300 13cc", ("12:40-13:00", 13)),
            ("12:40-1300 14", ("12:40-13:00", 14)),
            ("1240  -   1300     15", ("12:40-13:00", 15)),
            ("1240  -1300     16cc", ("12:40-13:00", 16)),
            ("12:40  -1300     17cc", ("12:40-13:00", 17)),
            ("12:40  -  13:00     18cc", ("12:40-13:00", 18)),
            ("12:40 19cc", ("12:40", 19)),
            ("12:40 20", ("12:40", 20)),
            ("12:40 21cc", ("12:40", 21)),
            ("1240 22", ("12:40", 22)),
            ("1240   23cc", ("12:40", 23)),
            ("1240     24", ("12:40", 24)),
            ("1240", ValueError),
            ("1240   ", ValueError),
            ("12:40", ValueError),
            ("12:40     ", ValueError),
        ]

        for input_str, expected in test_cases:
            with self.subTest(input=input_str, expected=expected):
                if isinstance(expected, type) and issubclass(expected, Exception):
                    with self.assertRaises(expected):
                        result, cc = line_message_parser.parse_breast_milk_record(input_str)
                        print(cc)
                else:
                    result = line_message_parser.parse_breast_milk_record(
                        input_str)
                    self.assertEqual(result, expected)

    def test_extract_cc(self):
        line_message_parser = LineMessageParser()
        cc = 10
        test_cases = [
            ("12:40-13:00 10cc",cc),
            ("12:40-1300 10cc", cc),
            ("12:40-1300 10cc", cc),
            ("12:40-1300 10cc", cc),
            ("12:40-1300 10", cc),
            ("1240  -   1300     10", cc),
            ("1240  -1300     10cc", cc),
            ("12:40  -1300     10cc", cc),
            ("12:40  -  13:00     10cc", cc),
            ("12:40 10cc", cc),
            ("12:40 10", cc),
            ("12:40 10cc", cc),
            ("1240 10", cc),
            ("1240   10cc", cc),
            ("1240     10", cc),
            ("1240", ValueError),
            ("1240   ", ValueError),
            ("12:40", ValueError),
            ("12:40     ", ValueError),
        ]

        for input_str, expected in test_cases:
            with self.subTest(input=input_str, expected=expected):
                if isinstance(expected, type) and issubclass(expected, Exception):
                    with self.assertRaises(expected):
                        line_message_parser.extract_cc(input_str)
                else:
                    result = line_message_parser.extract_cc(
                        input_str)
                    self.assertEqual(result, expected)