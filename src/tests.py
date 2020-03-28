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
            "28 MAR 2015"), alive=True)
        p3 = Person("@42@", birthday=utils.parse_date(
            "1 MAR 1900"), alive=False)
        p4 = Person("@22@", birthday=utils.parse_date(
            "30 APR 1965"), alive=True)
        self.assertEqual(
            [p2.id], extras.list_upcoming_birthdays([p1, p2, p3, p4]))

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
            "29 MAR 1960"), alive=True)
        p5 = Person("@21@", birthday=utils.parse_date("19 FEB 1960"))
        p6 = Person("@20@", birthday=utils.parse_date(
            "21 FEB 1961"), alive=True)
        self.assertEqual([p4.id], extras.list_upcoming_birthdays(
            [p1, p2, p3, p4, p5, p6]))

    def test_parse_un_unique_indi_ids(self):
        ged_parser.parse(["0 @32@ INDI", "0 @43@ INDI", "0 @43@ INDI"])

    def test_parse_un_unique_fam_ids(self):
        ged_parser.parse(["0 @32@ FAM", "0 @43@ FAM", "0 @43@ FAM"])

    # this test is RELATIVE to the actual day of code running
    def test_recent_birthday_some(self):
        # MUST USE THE PYTHON MOCK LIBRARY!
        # MOCK SHOULD PRETEND TODAY IS FEB 20, 2020
        # BETTER TO USE DATETIME DIRECTLY HERE RATHER THAN utils.parse_date()
        p1 = Person("@54@")
        p2 = Person("@43@", birthday=utils.parse_date("20 FEB 2020"))
        p3 = Person("@42@")
        p4 = Person("@22@", birthday=utils.parse_date("19 FEB 2020"))
        p5 = Person("@21@", birthday=utils.parse_date("19 JAN 2019"))
        p6 = Person("@20@", birthday=utils.parse_date("1 FEB 1961"))
        self.assertEqual([], extras.list_recent_births(
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
        testPeeps = {"@22@": Person("@22@", alive=False, death=utils.parse_date(
            "28 FEB 1960")), "@21@": Person("@21@", alive=False, death=utils.parse_date("19 FEB 1960"))}
        testFam = Family("@F1@", married=utils.parse_date(
            "5 MAY 1959"), husbandId="@22@",  wifeId="@21@")
        self.assertEqual(True, utils.marriage_before_death(testFam, testPeeps))

    def test_marriage_before_death_exception(self):
        testPeeps = {"@22@": Person("@22@", alive=False, death=utils.parse_date(
            "28 FEB 1965")), "@21@": Person("@21@", alive=False, death=utils.parse_date("19 FEB 1960"))}
        testFam = Family("@F1@", married=utils.parse_date(
            "5 MAY 1961"), husbandId="@22@",  wifeId="@21@")
        self.assertEqual(
            False, utils.marriage_before_death(testFam, testPeeps))

# make sure your functions start with the word 'test' and have at least one
# parameter self (just because its in a class dw about why)
# ex test_great_name_(self, other_params):

    def test_birth_before_marriage(self):

        testFam = Family("@F1@", married=utils.parse_date("5 MAY 1970"),
                         divorced=utils.parse_date("5 MAY 1980"), husbandId="@22@", wifeId="@21@")
        testPeople = {"@22@": Person("@22@", alive=False, birthday=utils.parse_date("28 FEB 1960")),
                      "@21@": Person("@21@", alive=False, birthday=utils.parse_date("19 FEB 1960"))}

        self.assertEqual(
            True, utils.birth_before_marriage(testFam, testPeople))

    def test_birth_before_marriage_exception(self):
        testFam = Family("@F1@", married=utils.parse_date("5 MAY 1950"),
                         divorced=utils.parse_date("5 MAY 1980"), husbandId="@22@", wifeId="@21@")
        testPeople = {"@22@": Person("@22@", alive=False, birthday=utils.parse_date("28 FEB 1960")),
                      "@21@": Person("@21@", alive=False, birthday=utils.parse_date("19 FEB 1960"))}

        self.assertEqual(
            False, utils.birth_before_marriage(testFam, testPeople))

    def test_birth_before_death(self):
        testPerson = Person("@22@", alive=False, birthday=utils.parse_date("28 FEB 1960"),
                            death=utils.parse_date("28 FEB 1980"))

        self.assertEqual(True, utils.birth_before_death(testPerson))

    def test_birth_before_death_exception(self):
        testPerson = Person("@22@", alive=False, birthday=utils.parse_date("28 FEB 1980"),
                            death=utils.parse_date("28 FEB 1960"))

        self.assertEqual(False, utils.birth_before_death(testPerson))

    def test_divorce_before_death(self):
        testFam = Family("@F1@", married=utils.parse_date("5 MAY 1961"),
                         divorced=utils.parse_date("5 MAY 1965"), husbandId="@22@", wifeId="@21@")
        testPeople = {"@22@": Person("@22@", alive=False, birthday=utils.parse_date("28 FEB 1960"),
                                     death=utils.parse_date("28 FEB 1970")),
                      "@21@": Person("@21@", alive=False, birthday=utils.parse_date("19 FEB 1960"),
                                     death=utils.parse_date("28 FEB 1970"))}
        self.assertEqual(True, utils.divorce_before_death(testFam, testPeople))

    def test_divorce_before_death_exception(self):
        testFam = Family("@F1@", married=utils.parse_date("5 MAY 1961"),
                         divorced=utils.parse_date("5 MAY 1980"), husbandId="@22@", wifeId="@21@")
        testPeople = {"@22@": Person("@22@", alive=False, birthday=utils.parse_date("28 FEB 1960"),
                                     death=utils.parse_date("28 FEB 1970")),
                      "@21@": Person("@21@", alive=False, birthday=utils.parse_date("19 FEB 1960"),
                                     death=utils.parse_date("28 FEB 1970"))}
        self.assertEqual(
            False, utils.divorce_before_death(testFam, testPeople))

    def test_marriage_before_divorce(self):
        testFam = Family("@F1@", married=utils.parse_date("5 MAY 1960"),
                         divorced=utils.parse_date("5 MAY 1980"), husbandId="@22@",  wifeId="@21@")

        self.assertEqual(True, utils.marriage_before_divorce(testFam))

    def test_marriage_before_divorce_exception(self):
        testFam = Family("@F1@", married=utils.parse_date("5 MAY 1980"),
                         divorced=utils.parse_date("5 MAY 1960"), husbandId="@22@", wifeId="@21@")

        self.assertEqual(False, utils.marriage_before_divorce(testFam))

    def test_reject_illegitimate_dates_edge_case(self):
        self.assertNotEqual(
            False, utils.reject_illegitimate_dates("29 FEB 2016"))

    def test_reject_illegitimate_false(self):
        self.assertEqual(None, utils.reject_illegitimate_dates("31 FEB 2021"))

    def test_reject_illegitimate_dates_true(self):
        self.assertNotEqual(
            False, utils.reject_illegitimate_dates("26 MAR 2010"))

    def test_accept_partial_dates_month_year(self):
        self.assertEqual('1 JAN 2000', utils.accept_partial_dates("JAN 2000"))

    def test_accept_partial_dates_year(self):
        self.assertEqual('1 JAN 2000', utils.accept_partial_dates("2000"))

    def test_get_line_number(self):
        self.assertEqual(3, utils.get_line_number(
            "hello",
            ["this", "is", "hello"]))

    def test_get_line_number_1(self):
        self.assertEqual(1, utils.get_line_number(
            "hello",
            ["hello", "is", "hello"]))

    def test_get_line_number_err(self):
        self.assertRaises(ValueError, utils.get_line_number,
                          "hello",
                          ["this", "is", "a", "test"])

    def test_check_unique_name_and_birth(self):
        p1 = Person("@15@",
                    name="john",
                    birthday=utils.parse_date("15 MAY 1999"))
        p2 = Person("@1@",
                    name="luke",
                    birthday=utils.parse_date("15 MAY 1999"))
        p3 = Person("@13@",
                    name="john",
                    birthday=utils.parse_date("16 MAY 1999"))
        d = {"@15@": p1, "@1@": p2, "@13@": p3}
        self.assertEqual(True,
                         utils.check_unique_birth_and_name(p1, d))
        self.assertEqual(True,
                         utils.check_unique_birth_and_name(p2, d))
        self.assertEqual(True,
                         utils.check_unique_birth_and_name(p3, d))

    def test_check_un_unique_name_and_birth_(self):
        p1 = Person("@15@",
                    name="john",
                    birthday=utils.parse_date("15 MAY 1999"))
        p2 = Person("@1@",
                    name="luke",
                    birthday=utils.parse_date("15 MAY 1999"))
        p3 = Person("@13@",
                    name="john",
                    birthday=utils.parse_date("15 MAY 1999"))
        d = {"@15@": p1, "@1@": p2, "@13@": p3}
        self.assertEqual(False,
                         utils.check_unique_birth_and_name(p1, d))
        self.assertEqual(True,
                         utils.check_unique_birth_and_name(p2, d))
        self.assertEqual(False,
                         utils.check_unique_birth_and_name(p3, d))

    def test_marriage_before_14(self):
        testFam = Family("@F1@", married=utils.parse_date("5 MAY 1970"),
                         divorced=utils.parse_date("5 MAY 1980"), husbandId="@22@", wifeId="@21@")
        testPeople = {"@22@": Person("@22@", alive=True, birthday=utils.parse_date("28 FEB 1960")),
                      "@21@": Person("@21@", alive=True, birthday=utils.parse_date("19 FEB 1960"))}

        self.assertEqual(False, utils.marriage_after_14(testFam, testPeople))

    def test_marriage_after_14(self):
        testFam = Family("@F1@", married=utils.parse_date("5 MAY 1979"),
                         divorced=utils.parse_date("5 MAY 1980"), husbandId="@22@", wifeId="@21@")
        testPeople = {"@22@": Person("@22@", alive=True, birthday=utils.parse_date("28 FEB 1960")),
                      "@21@": Person("@21@", alive=True, birthday=utils.parse_date("19 FEB 1960"))}

        self.assertEqual(True, utils.marriage_after_14(testFam, testPeople))

    # this test is RELATIVE to the actual day of code running
    def test_list_recent_deaths_some(self):
        p1 = Person("@54@")
        p2 = Person("@43@", death=utils.parse_date("1 MAR 2020"))
        p3 = Person("@42@")
        p4 = Person("@22@", death=utils.parse_date("2 MAR 2020"))
        p5 = Person("@21@", death=utils.parse_date("19 JAN 2019"))
        p6 = Person("@20@", death=utils.parse_date("1 FEB 1961"))
        self.assertEqual([p2.id, p4.id], extras.list_recent_deaths(
            [p1, p2, p3, p4, p5, p6]))

    # this test is RELATIVE to the actual day of code running
    def test_list_recent_deaths_none(self):
        p1 = Person("@54@")
        p2 = Person("@43@", death=utils.parse_date("29 FEB 2016"))
        p3 = Person("@42@")
        p4 = Person("@22@", death=utils.parse_date("29 FEB 1960"))
        p5 = Person("@21@", death=utils.parse_date("19 FEB 1960"))
        p6 = Person("@20@", death=utils.parse_date("20 FEB 1961"))
        self.assertEqual([], extras.list_recent_deaths(
            [p1, p2, p3, p4, p5, p6]))

    def test_list_deceased(self):
        p1 = Person("@54@")
        p2 = Person("@43@", death=utils.parse_date("20 FEB 2011"))
        p3 = Person("@42@")
        p4 = Person("@22@", death=utils.parse_date("29 FEB 1960"))
        p5 = Person("@21@", death=utils.parse_date("19 FEB 1960"))
        p6 = Person("@20@", death=utils.parse_date("20 FEB 1961"))
        self.assertEqual([p2.id, p4.id, p5.id, p6.id], extras.list_deceased(
            [p1, p2, p3, p4, p5, p6]))

    def test_get_parents(self):
        p1 = Person("@54@", children=["@43@", "@42@"])
        p2 = Person("@43@")
        p3 = Person("@42@")
        p4 = Person("@22@", children=["@43@", "@42@"])
        p5 = Person("@21@", children=["@54@"])
        p6 = Person("@20@")
        self.assertEqual([p1, p4], utils.get_parents("@43@",
                                                     [p1, p2, p3, p4, p5, p6]))

    def test_get_silblings(self):
        p1 = Person("@54@", children=["@43@", "@42@"])
        p2 = Person("@43@")
        p3 = Person("@42@")
        p4 = Person("@22@", children=["@43@", "@20@"])
        p5 = Person("@21@", children=["@54@"])
        p6 = Person("@20@")
        self.assertEqual([p3, p6], utils.get_siblings("@43@",
                                                      [p1, p2, p3, p4, p5, p6]))

    def test_no_first_cousin_marriage(self):
        p1 = Person("@54@", children=["@43@", "@42@"])
        p2 = Person("@43@", children=["@22@"])
        p3 = Person("@42@", children=["@21@"])
        p4 = Person("@22@")
        p5 = Person("@21@", spouse=["@20@"])
        p6 = Person("@20@", spouse=["@21@"])
        f1 = Family("@F1@", married=utils.parse_date("5 MAY 1970"),
                    divorced=utils.parse_date("5 MAY 1980"), husbandId="@20@", wifeId="@21@")
        self.assertEqual(True, utils.no_first_cousin_marriage(f1,
                                                              [p1, p2, p3, p4, p5, p6]))

    def test_no_first_cousin_marriage_err(self):
        p1 = Person("@54@", children=["@43@", "@42@"])
        p2 = Person("@43@", children=["@22@"])
        p3 = Person("@42@", children=["@21@"])
        p4 = Person("@22@", spouse=["@21@"])
        p5 = Person("@21@", spouse=["@22@"])
        p6 = Person("@20@")
        f1 = Family("@F1@", married=utils.parse_date("5 MAY 1970"),
                    divorced=utils.parse_date("5 MAY 1980"), husbandId="@22@", wifeId="@21@")
        self.assertEqual(False, utils.no_first_cousin_marriage(f1,
                                                               [p1, p2, p3, p4, p5, p6]))

    def test_no_aunts_and_uncles(self):
        p1 = Person("@54@", children=["@43@", "@42@"])
        p2 = Person("@43@", children=["@22@"])
        p3 = Person("@42@", children=["@21@"])
        p4 = Person("@22@")
        p5 = Person("@21@", spouse=["@20@"])
        p6 = Person("@20@", spouse=["@21@"])
        f1 = Family("@F1@", married=utils.parse_date("5 MAY 1970"),
                    divorced=utils.parse_date("5 MAY 1980"), husbandId="@20@", wifeId="@21@")
        self.assertEqual(True, utils.no_aunts_and_uncles(
            f1, [p1, p2, p3, p4, p5, p6]))

    def test_no_aunts_and_uncles_err(self):
        p1 = Person("@54@", children=["@43@", "@42@"])
        p2 = Person("@43@", children=["@22@"])
        p3 = Person("@42@", children=["@21@"])
        p4 = Person("@22@")
        p5 = Person("@21@", spouse=["@43@"])
        p6 = Person("@20@")
        f1 = Family("@F1@", married=utils.parse_date("5 MAY 1970"),
                    divorced=utils.parse_date("5 MAY 1980"), husbandId="@21@", wifeId="@43@")
        self.assertEqual(False, utils.no_aunts_and_uncles(
            f1, [p1, p2, p3, p4, p5, p6]))

    def test_no_marriage_to_children(self):
        testFam = Family("@F1@", married=utils.parse_date("5 MAY 1979"),
                         divorced=utils.parse_date("5 MAY 1980"), husbandId="@22@", wifeId="@21@")
        testPeople = {"@22@": Person("@22@", alive=True, birthday=utils.parse_date("28 FEB 1960"), children=["@23@"]),
                      "@21@": Person("@21@", alive=True, birthday=utils.parse_date("19 FEB 1960")),
                      "@23@": Person("@23@", alive=True, birthday=utils.parse_date("19 FEB 1978"))}

        self.assertEqual(
            True, utils.no_marriage_to_children(testFam, testPeople))

    def test_no_marriage_to_children_err(self):
        testFam = Family("@F1@", married=utils.parse_date("5 MAY 1979"),
                         divorced=utils.parse_date("5 MAY 1980"), husbandId="@22@", wifeId="@21@")
        testPeople = {"@22@": Person("@22@", alive=True, birthday=utils.parse_date("28 FEB 1960"), children=["@21@"]),
                      "@21@": Person("@21@", alive=True, birthday=utils.parse_date("19 FEB 1960"))}

        self.assertEqual(
            False, utils.no_marriage_to_children(testFam, testPeople))

    def test_no_marriage_to_siblings(self):
        testFam = Family("@F1@", married=utils.parse_date("5 MAY 1979"),
                         divorced=utils.parse_date("5 MAY 1980"), husbandId="@22@", wifeId="@21@")
        testPeople = {"@22@": Person("@22@", alive=True, birthday=utils.parse_date("28 FEB 1960"), children=["@23@", "@24@"]),
                      "@21@": Person("@21@", alive=True, birthday=utils.parse_date("19 FEB 1960"), children=["@23@", "@24@"]),
                      "@23@": Person("@23@", alive=True, birthday=utils.parse_date("19 FEB 1978")),
                      "@24@": Person("@24@", alive=True, birthday=utils.parse_date("19 FEB 1978"))}

        self.assertEqual(
            True, utils.no_marriage_to_siblings(testFam, testPeople))

    def test_no_marriage_to_siblings_err(self):
        testFam = Family("@F1@", married=utils.parse_date("5 MAY 1998"),
                         divorced=utils.parse_date("6 MAY 1998"), husbandId="@24@", wifeId="@23@")
        testPeople = {"@22@": Person("@22@", alive=True, birthday=utils.parse_date("28 FEB 1960"), children=["@23@", "@24@"]),
                      "@21@": Person("@21@", alive=True, birthday=utils.parse_date("19 FEB 1960"), children=["@23@", "@24@"]),
                      "@23@": Person("@23@", alive=True, birthday=utils.parse_date("19 FEB 1978")),
                      "@24@": Person("@24@", alive=True, birthday=utils.parse_date("19 FEB 1978"))}

        self.assertEqual(
            False, utils.no_marriage_to_siblings(testFam, testPeople))

    def test_order_siblings_by_age(self):
        testFam = Family("@F1@", children=["@21@", "@22@", "@23@"])
        p4 = Person("@21@", birthday=utils.parse_date("2 MAR 2020"))
        p5 = Person("@22@", birthday=utils.parse_date("19 JAN 2019"))
        p6 = Person("@23@", death=utils.parse_date("19 JAN 2019"))
        self.assertEqual(["@22@", "@21@", "@23@"], utils.order_siblings_by_age(
            testFam.children, [p4, p5, p6]))
        print("INFO: FAMILY: US28: order_siblings_by_age: Test Passed! Sibling ids from oldest to youngest:",
              utils.order_siblings_by_age(testFam.children, [p4, p5, p6]))

    def test_dates_before_current_date(self):
        self.assertEqual(True, utils.dates_before_current_date(
            utils.parse_date("5 MAY 1960")))

    def test_dates_after_current_date(self):
        self.assertEqual(False, utils.dates_before_current_date(
            utils.parse_date("25 MAY 2020")))

    def test_orphans(self):
        testFamilies = [Family("@F1@", married=utils.parse_date("5 MAY 1979"),
                               husbandId="@22@", wifeId="@21@", children=["@23@", "@24@"])]
        testPeople = [Person("@22@", alive=False, death=utils.parse_date("6 MAY 1980"), children=["@23@", "@24@"]),
                      Person("@21@", alive=False, death=utils.parse_date(
                          "6 MAY 1980"), children=["@23@", "@24@"]),
                      Person("@23@", alive=True, age=14),
                      Person("@24@", alive=True)]
        self.assertEqual(extras.list_orphans(
            testPeople, testFamilies), ["@23@"])

    def test_orphans_none(self):
        testFamilies = [Family("@F1@", married=utils.parse_date("5 MAY 1979"),
                               husbandId="@22@", wifeId="@21@", children=["@23@", "@24@"])]
        testPeople = [Person("@22@", alive=False, death=utils.parse_date("6 MAY 1980"), children=["@23@", "@24@"]),
                      Person("@21@", alive=True, children=["@23@", "@24@"]),
                      Person("@23@", alive=True, age=14),
                      Person("@24@", alive=True)]
        self.assertEqual(extras.list_orphans(testPeople, testFamilies), [])

    def test_orphans_empty(self):
        self.assertEqual(extras.list_orphans([], []), [])

    def test_age_gap(self):
        testFamilies = [Family("@F1@", married=utils.parse_date("5 MAY 2019"),
                               husbandId="@22@", wifeId="@21@")]
        testPeople = [Person("@22@", alive=False, birthday=utils.parse_date("6 MAY 1980")),
                      Person("@21@", alive=False,
                             birthday=utils.parse_date("6 MAY 2017")),
                      Person("@23@", alive=True, age=14),
                      Person("@24@", alive=True)]
        self.assertEqual(extras.list_large_age_gap(
            testPeople, testFamilies), ["@F1@"])

    def test_age_gap_none(self):
        testFamilies = [Family("@F1@", married=utils.parse_date("5 MAY 2019"),
                               husbandId="@22@", wifeId="@21@"),
                        Family("@F2@"),
                        Family("@F3@", wifeId="@23@", husbandId="@24@")]
        testPeople = [Person("@22@"),
                      Person("@21@"),
                      Person("@23@", alive=True, age=14),
                      Person("@24@", alive=True)]
        self.assertEqual(extras.list_large_age_gap(
            testPeople, testFamilies), [])

    def test_include_individual_dates_zero(self):
        testPerson = Person("@21@", birthday=utils.parse_date("2 MAR 2020"))
        self.assertEqual((extras.include_individual_ages(testPerson).age), 0)

    def test_include_individual_dates_fifty(self):
        testPerson = Person("@21@", birthday=utils.parse_date("22 JAN 1970"))
        self.assertEqual((extras.include_individual_ages(testPerson).age), 50)

    def test_include_individual_dates_hundred(self):
        testPerson = Person("@21@", birthday=utils.parse_date("29 FEB 1920"))
        self.assertEqual((extras.include_individual_ages(testPerson).age), 100)

    def test_correct_gender_for_role_false(self):
        testFamilies = [Family("@F1@", married=utils.parse_date("5 MAY 2019"),
                               husbandId="@22@", wifeId="@21@")]
        testPeople = [Person("@22@", name="Bob Smith", gender="F"),
                      Person("@21@", name="Mary Smith", gender="M"),
                      ]
        self.assertEqual(extras.correct_gender_for_role(
            testPeople, testFamilies), False)

    def test_correct_gender_for_role_true(self):
        testFamilies = [Family("@F1@", married=utils.parse_date("5 MAY 2019"),
                               husbandId="@22@", wifeId="@21@")]
        testPeople = [Person("@22@", name="Bob Smith", gender="M"),
                      Person("@21@", name="Mary Smith", gender="F"),
                      ]
        self.assertEqual(extras.correct_gender_for_role(
            testPeople, testFamilies), True)


# make sure your functions start with the word 'test' and have at least one
# parameter self (just because its in a class dw about why)
# ex test_great_name_(self, other_params):
if __name__ == '__main__':
    unittest.main()
