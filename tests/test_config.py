from generic_online_ml_scoring.utils import load_properties
import unittest


class TestConfig(unittest.TestCase):
    def test_load_properties(self):
        p1, p2, p3 = load_properties("../data/testconfig.conf")
        self.assertDictEqual(p1, {"prop1": "test1", "test.1": "foo"})
        self.assertDictEqual(p2, {"prop2": "test2", "test.1": "foo"})
        self.assertDictEqual(p3, {"toto": "titi"})


if __name__ == '__main__':
    unittest.main()
