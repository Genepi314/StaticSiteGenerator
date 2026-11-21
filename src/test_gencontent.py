from unittest import TestCase
from gencontent import extract_title

class TestGencontent(TestCase):

    def test_extract_title(self):
        md = """#   Hello!  """
        self.assertEqual(
            extract_title(md),
            "Hello!"
        )
        md = """# Hello!"""
        self.assertEqual(
            extract_title(md),
            "Hello!"
        )
        md = """chuchoti chuchota
#   Hello!  """
        self.assertEqual(
            extract_title(md),
            "Hello!"
        )
