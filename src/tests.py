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
        testFam = Family("@F2@", children=["@12@", "@5@", "@US_3@", "@5@", "@II@", "@JA@", "@US_31@",
                                           "@I3@", "@I4@", "@o_9@", "@TRUE@", "@\n@", "@NULL@", "@Szx@", "@Cr@", "@_1_@"])
        self.assertEqual(False, extras.fewer_than_15_siblings(testFam))

    def test_fewer_than_15_siblings_edge(self):
        testFam = Family("@F3@")
        self.assertEqual(True, extras.fewer_than_15_siblings(testFam))

    # this test is RELATIVE to the actual day of code running
    def test_birthday_simple(self):
        # MUST USE THE PYTHON MOCK LIBRARY!
        # MOCK SHOULD PRETEND TODAY IS FEB 20, 2020
        p1 = Person("@54@", birthday=utils.parse_date(
            "12 MAY 2019"), alive=True)
        p2 = Person("@43@", birthday=utils.parse_date(
            "28 FEB 2015"), alive=True)
        p3 = Person("@42@", birthday=utils.parse_date(
            "1 MAR 1900"), alive=False)
        p4 = Person("@22@", birthday=utils.parse_date(
            "30 APR 1965"), alive=True)
        self.assertEqual(
            [p2], extras.list_upcoming_birthdays([p1, p2, p3, p4]))

    # this test is RELATIVE to the actual day of code running
    def test_birthday_edge(self):
        # MUST USE THE PYTHON MOCK LIBRARY!
        # MOCK SHOULD PRETEND TODAY IS FEB 20, 2020
        # BETTER TO USE DATETIME DIRECTLY HERE RATHER THAN utils.parse_date()
        p1 = Person("@54@")
        p2 = Person("@43@", birthday=utils.parse_date(
            "29 FEB 2016"), alive=False)
        p3 = Person("@42@")
        p4 = Person("@22@", birthday=utils.parse_date(
            "29 FEB 1960"), alive=True)
        p5 = Person("@21@", birthday=utils.parse_date("19 FEB 1960"))
        p6 = Person("@20@", birthday=utils.parse_date(
            "21 FEB 1961"), alive=True)
        self.assertEqual([p4], extras.list_upcoming_birthdays(
            [p1, p2, p3, p4, p5, p6]))

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

    # this test is RELATIVE to the actual day of code running
    def test_recent_birthday_some(self):
        # MUST USE THE PYTHON MOCK LIBRARY!
        # MOCK SHOULD PRETEND TODAY IS FEB 20, 2020
        # BETTER TO USE DATETIME DIRECTLY HERE RATHER THAN utils.parse_date()
        p1 = Person("@54@")
        p2 = Person("@43@", birthday=utils.parse_date("20 FEB 2020"))
        p3 = Person("@42@")
        p4 = Person("@22@", birthday=utils.parse_date("1 FEB 2020"))
        p5 = Person("@21@", birthday=utils.parse_date("19 JAN 2019"))
        p6 = Person("@20@", birthday=utils.parse_date("1 FEB 1961"))
        self.assertEqual([p2, p4], extras.list_recent_births(
            [p1, p2, p3, p4, p5, p6]))

    # this test is RELATIVE to the actual day of code running
    def test_recent_birthday_none(self):
        # MUST USE THE PYTHON MOCK LIBRARY!
        # MOCK SHOULD PRETEND TODAY IS FEB 20, 2020
        # BETTER TO USE DATETIME DIRECTLY HERE RATHER THAN utils.parse_date()
        p1 = Person("@54@")
        p2 = Person("@43@", birthday=utils.parse_date("29 FEB 2016"))
        p3 = Person("@42@")
        p4 = Person("@22@", birthday=utils.parse_date("29 FEB 1960"))
        p5 = Person("@21@", birthday=utils.parse_date("19 FEB 1960"))
        p6 = Person("@20@", birthday=utils.parse_date("20 FEB 1961"))
        self.assertEqual([], extras.list_recent_births(
            [p1, p2, p3, p4, p5, p6]))

    def test_marriage_before_death(self):
        ged_parser.parse(["0 @I32@ INDI", "1 DEAT Y", "2 DATE 6 MAY 1961", "1 FAMS @F1@",
                              "0 @I43@ INDI", "1 DEAT Y", "2 DATE 6 MAY 1971", "1 FAMS @F1@",
                              "0 @F1@ FAM", "1 HUSB @I32@", "1 WIFE @I43@", "1 MARR", "2 DATE 5 MAY 1961"])


    def test_marriage_before_death_exception(self):
        self.assertRaises(
            Exception,
            ged_parser.parse,
            ["0 @I32@ INDI", "1 DEAT Y", "2 DATE 6 MAY 1961", "1 FAMS @F1@",
             "0 @I43@ INDI", "1 DEAT Y", "2 DATE 6 MAY 1971", "1 FAMS @F1@",
             "0 @F1@ FAM", "1 HUSB @I32@", "1 WIFE @I43@", "1 MARR", "2 DATE 3 MAY 1962"])

# make sure your functions start with the word 'test' and have at least one
# parameter self (just because its in a class dw about why)
# ex test_great_name_(self, other_params):

    def test_birth_before_marriage(self):
        try:
            ged_parser.parse(["0 @I32@ INDI", "1 BIRT Y", "2 DATE 6 MAY 1961", "1 FAMS @F1@",
                              "0 @I43@ INDI", "1 BIRT Y", "2 DATE 6 MAY 1971", "1 FAMS @F1@",
                              "0 @F1@ FAM", "1 HUSB @I32@", "1 WIFE @I43@", "1 MARR", "2 DATE 5 MAY 2000"])
        except Exception:
            self.fail("marriage_before_death() raised Exception unexpectedly!")

    def test_birth_before_marriage_exception(self):
        self.assertRaises(
            Exception,
            ged_parser.parse,
            ["0 @I32@ INDI", "1 BIRT Y", "2 DATE 6 MAY 1961", "1 FAMS @F1@",
             "0 @I43@ INDI", "1 BIRT Y", "2 DATE 6 MAY 1971", "1 FAMS @F1@",
             "0 @F1@ FAM", "1 HUSB @I32@", "1 WIFE @I43@", "1 MARR", "2 DATE 3 MAY 1962"])

    def test_birth_before_death(self):
        try:
            ged_parser.parse(["0 @I32@ INDI", "1 BIRT Y", "2 DATE 6 MAY 1961",
                              "1 DEAT Y", "2 DATE 6 MAY 1962",  "1 FAMS @F1@"])
        except Exception:
            self.fail("marriage_before_death() raised Exception unexpectedly!")

    def test_birth_before_death_exception(self):
        self.assertRaises(
            Exception,
            ged_parser.parse,
            ["0 @I32@ INDI", "1 BIRT Y", "2 DATE 6 MAY 1961", "1 DEAT Y", "2 DATE 6 MAY 1960",  "1 FAMS @F1@"])

    def test_divorce_before_death(self):
        ged_parser.parse(["0 @I32@ INDI", "1 DEAT Y", "2 DATE 6 MAY 1961", "1 FAMS @F1@",
                              "0 @I43@ INDI", "1 DEAT Y", "2 DATE 6 MAY 1971", "1 FAMS @F1@",
                              "0 @F1@ FAM", "1 HUSB @I32@", "1 WIFE @I43@", "1 DIV", "2 DATE 5 MAY 1930"])

    def test_divorce_before_death_exception(self):
        self.assertRaises(
            Exception,
            ged_parser.parse,
            ["0 @I32@ INDI", "1 DEAT Y", "2 DATE 6 MAY 1961", "1 FAMS @F1@",
             "0 @I43@ INDI", "1 DEAT Y", "2 DATE 6 MAY 1971", "1 FAMS @F1@",
             "0 @F1@ FAM", "1 HUSB @I32@", "1 WIFE @I43@", "1 DIV", "2 DATE 3 MAY 1966"])

    def test_marriage_before_divorce(self):
        pass
        #ged_parser.parse(["0 @F1@ FAM", "1 MARR", "2 DATE 3 MAY 1962", "1 DIV", "2 DATE 5 MAY 1970"])

    def test_marriage_before_divorce_exception(self):
        self.assertRaises(
            Exception,
            ged_parser.parse,
            ["0 @F1@ FAM", "1 HUSB @I32@", "1 WIFE @I43@", "1 MARR", "2 DATE 3 MAY 1962", "1 DIV", "2 DATE 5 MAY 1930"])

#make sure your functions start with the word 'test' and have at least one 
#parameter self (just because its in a class dw about why)
#ex test_great_name_(self, other_params):

    def test_reject_illegitimate_dates_edge_case(self):
        self.assertEqual(True, utils.reject_illegitimate_dates("29 FEB 2016"))

    def test_reject_illegitimate_false(self):
        self.assertEqual(False, utils.reject_illegitimate_dates("31 FEB 2021"))

    def test_reject_illegitimate_dates_true(self):
        self.assertEqual(True, utils.reject_illegitimate_dates("26 MAR 2010"))

# make sure your functions start with the word 'test' and have at least one
# parameter self (just because its in a class dw about why)
# ex test_great_name_(self, other_params):

if __name__ == '__main__':
    unittest.main()
