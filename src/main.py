import argparse
import ged_parser
import extras
from utils import print_families
from utils import print_people
from utils import order_siblings_by_age

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='The best GEDCOM reader')
    parser.add_argument('GEDCOM_file', type=str,
                        help='The file to read (must be in GEDCOM format')
    args = parser.parse_args()

    with open(args.GEDCOM_file) as file:
        lines = file.readlines()
        tup = ged_parser.parse(lines)
        people = list(tup[0])
        families = list(tup[1])
        for family in families:
            # run ALL family-based tests
            extras.fewer_than_15_siblings(family)
            family.children = order_siblings_by_age(family.children, people)
            extras.correct_gender_for_role(people, family)
            



        print_families(families)
        print_people(people)
        
        extras.list_upcoming_birthdays(people)

        # MIKE please uncomment when done:
        # x = list_living_married(families)
        # extras.list_upcoming_anniverseries(x)
        extras.list_recent_births(people)
        extras.list_living_married(people, families)
        extras.list_recent_survivors(people, families)
        extras.list_recent_deaths(people)
        extras.list_deceased(people)
        extras.less_than_150yo(people)
        extras.list_orphans(people, families)
        extras.list_large_age_gap(people, families)
        extras.check_corresponding_entries(people, families)
