import unittest
import random
import re
from kadai_gui.utils import utils


class TestUtils(unittest.TestCase):
    def test_get_random_string(self):
        regex_match = r"\b[a-z]{6}\b"
        random_string = utils.getRandomString(6)
        regex = re.compile(regex_match)
        match = regex.match(random_string)

        self.assertIsNot(match, None)

    def test_resizeString(self):
        length = 2 * random.randint(5, 20)
        cut_length = 2 * random.randint(1, (length / 2) - 2)

        string = utils.getRandomString(length)
        resized_string = utils.resizeString(string, cut_length)

        regex_match = (
            r"\b[a-z]{"
            + str(int(cut_length / 2))
            + r"}\.\.\.[a-z]{"
            + str(int(cut_length / 2))
            + r"}\b"
        )
        regex = re.compile(regex_match)
        match = regex.match(resized_string)

        self.assertIsNot(match, None)

    def test_getScaledDimensions(self):
        dimensions = (random.randint(100, 1000), random.randint(100, 1000))
        new_width = random.randint(100, 1000)

        new_dimensions = utils.getScaledDimensions(dimensions, new_width)
        self.assertEqual(
            new_dimensions,
            (new_width, int(dimensions[1] / (dimensions[0] / new_width))),
        )
