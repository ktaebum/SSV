import unittest

from parser.tt import TTParser


class TestTTParser(unittest.TestCase):

  def test_construct_parser_by_directory_name(self):
    path = './data/p600_BliNi2'
    parser = TTParser(path)
    del parser

  def test_construct_parser_by_filename(self):
    path = './data/p600_BliNi2/p600_BliNi2.tt'
    parser = TTParser(path)
    del parser


if __name__ == "__main__":
  unittest.main()
