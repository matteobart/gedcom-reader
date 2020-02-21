import unittest
import extras
import ged_parser
import datetime
import utils
from family import Family
from person import Person

class TestGedcomMethods(unittest.TestCase):
    
    def test_fewer_than_15_siblings_true(self):
        testFam = Family("@F1@", children=["@12@", "@5@"])
        self.assertEqual(True, extras.fewer_than_15_siblings(testFam))

    def test_fewer_than_15_siblings_false(self):
        testFam = Family("@F2@", children=["@12@", "@5@", "@US_3@", "@5@", "@II@", "@JA@", "@US_31@", "@I3@","@I4@", "@o_9@", "@TRUE@", "@\n@", "@NULL@", "@Szx@", "@Cr@", "@_1_@"])
        self.assertEqual(False, extras.fewer_than_15_siblings(testFam))

    def test_fewer_than_15_siblings_edge(self):
        testFam = Family("@F3@")
        self.assertEqual(True, extras.fewer_than_15_siblings(testFam))

    def test_birthday_simple(self): # this test is RELATIVE to the actual day of code running
        # MUST USE THE PYTHON MOCK LIBRARY!
        # MOCK SHOULD PRETEND TODAY IS FEB 20, 2020
        p1 = Person("@54@", birthday=utils.parse_date("12 MAY 2019"), alive=True)
        p2 = Person("@43@", birthday=utils.parse_date("28 FEB 2015"), alive=True)
        p3 = Person("@42@", birthday=utils.parse_date("1 MAR 1900"), alive=False)
        p4 = Person("@22@", birthday=utils.parse_date("30 APR 1965"), alive=True)
        self.assertEqual([p2],extras.list_upcoming_birthdays([p1, p2, p3, p4]))
    
    def test_birthday_edge(self): # this test is RELATIVE to the actual day of code running
        # MUST USE THE PYTHON MOCK LIBRARY!
        # MOCK SHOULD PRETEND TODAY IS FEB 20, 2020
        #BETTER TO USE DATETIME DIRECTLY HERE RATHER THAN utils.parse_date()
        p1 = Person("@54@")
        p2 = Person("@43@", birthday=utils.parse_date("29 FEB 2016"), alive=False)
        p3 = Person("@42@")
        p4 = Person("@22@", birthday=utils.parse_date("29 FEB 1960"), alive=True)
        p5 = Person("@21@", birthday=utils.parse_date("19 FEB 1960"))
        p6 = Person("@20@", birthday=utils.parse_date("20 FEB 1961"), alive=True)
        self.assertEqual([p4, p6], extras.list_upcoming_birthdays([p1, p2, p3, p4, p5, p6]))

    def test_parse_un_unique_indi_ids(self):
        self.assertRaises(
            Exception, 
            ged_parser.parse, 
            ["0 @32@ INDI", "0 @43@ INDI", "0 @43@ INDI"])

    def test_parse_un_unique_fam_ids(self):
        self.assertRaises(
            Exception, 
            ged_parser.parse, 
            ["0 @32@ FAM", "0 @43@ FAM", "0 @43@ FAM"])

#make sure your functions start with the word 'test' and have one 
#parameter self (just because its in a class dw about why)
#ex test_great_name_(self):

if __name__ == '__main__':
    unittest.main()