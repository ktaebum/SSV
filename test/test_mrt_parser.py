import unittest

from parser.mrt import MRTParser


class TestMRTParser(unittest.TestCase):

  def test_construct_parser_by_directory_name(self):
    path = './data/p600_BliNi2'
    parser = MRTParser(path)
    del parser

  def test_construct_parser_by_filename(self):
    path = './data/p600_BliNi2/p600_BliNi2.mrt'
    parser = MRTParser(path)
    del parser


if __name__ == "__main__":
  unittest.main()
