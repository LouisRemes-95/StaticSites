import unittest
from unittest.mock import patch

from markdown_processing import extract_title

class Test_Markdown_Processing(unittest.TestCase):
    def test_extract_title_1(self):
        markdown = "# A Title"
        self.assertEqual(extract_title(markdown), "A Title")

    def test_extract_title_2(self):
        markdown = " #A Title    "
        self.assertEqual(extract_title(markdown), "A Title")

    def test_extract_title_3(self):
        markdown = """ ## Not a Title   
#####
# A Title"""
        self.assertEqual(extract_title(markdown), "A Title")

    def test_extract_title_4(self):
        markdown = """ # A Title   
# Second Title"""
        self.assertEqual(extract_title(markdown), "A Title")

    def test_extract_title_5(self):
        markdown = """ ## Not a Title   
#### Not A Title"""
        with self.assertRaises(Exception) as content:
            extract_title(markdown)
        self.assertEqual(str(content.exception), "No title found (single #)")

if __name__ == "__main__":
    unittest.main()
