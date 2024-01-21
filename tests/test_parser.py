import unittest
from tire_codes import TireCodeParser
from tests.sample_codes import sample_codes


class TestTireCodeParser(unittest.TestCase):
    
    def test_tire_code_parser(self):
        for tire_code in sample_codes:
            with self.subTest(tire_code=tire_code):
                parser = TireCodeParser(tire_code)
                self.assertIsNotNone(parser.specs)




if __name__ == '__main__':
    unittest.main()