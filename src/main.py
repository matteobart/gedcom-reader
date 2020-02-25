import argparse
import ged_parser
import extras
from utils import print_families
from utils import print_people

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='The best GEDCOM reader')
    parser.add_argument('GEDCOM_file', type=str,
                        help='The file to read (must be in GEDCOM format')
    args = parser.parse_args()

    with open(args.GEDCOM_file) as file:
        lines = file.readlines()
        tup = ged_parser.parse(lines)
        people = tup[0]
        families = tup[1]
        print_families(families)
        print_people(people)
        birthday_list = extras.list_upcoming_birthdays(people)
        print("\nUPCOMING BIRTHDAY(S): ", birthday_list)
        for family in families:
            # run ALL family-based "extras" tests
            extras.fewer_than_15_siblings(family)
