import unittest
import extras
import ged_parser
from family import Family
from person import Person

class TestGedcomMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_example_name(self):
        self.assertTrue(3, 2+1)
    
    def test_fewer_than_15_siblings_true(self):
        testFam = Family("@F1@", children=["@12@", "@5@"])
        self.assertEqual(True, extras.fewer_than_15_siblings(testFam))

    def test_fewer_than_15_siblings_false(self):
        testFam = Family("@F2@", children=["@12@", "@5@", "@US_3@", "@5@", "@II@", "@JA@", "@US_31@", "@I3@","@I4@", "@o_9@", "@TRUE@", "@\n@", "@NULL@", "@Szx@", "@Cr@", "@_1_@"])
        self.assertEqual(False, extras.fewer_than_15_siblings(testFam))

    def test_fewer_than_15_siblings_edge(self):
        testFam = Family("@F3@")
        self.assertEqual(True, extras.fewer_than_15_siblings(testFam))




#make sure your functions start with the word 'test' and have one 
#parameter self (just because its in a class dw about why)
#ex test_great_name_(self):

if __name__ == '__main__':
    unittest.main()