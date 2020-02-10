import argparse
from family import Family
# from person import Person
import sys
from prettytable import PrettyTable
from datetime import datetime
from dateutil.relativedelta import relativedelta

optional_tags = ['death', 'spouse', 'child']
people = []
families = []
parsed_output = []
formatted_families = []
individual_headers = ["id", "name", "gender", "birthday",
                      "age", "alive", "death", "child", "spouse"]
family_headers = ["id", "married", "divorced", "husbandId",
                  "husbandName", "wifeId", "wifeName", "children"]

individual_table = PrettyTable()
family_table = PrettyTable()

# given an array of strings parse the GEDCOM information
# there is no return but will print to console


def create_individual_list(parsed_output):
    start_case = False
    for line in parsed_output:
        if line[0] == "INDI":
            if start_case == True:
                if not 'alive' in new_person_map.keys():
                    new_person_map['alive'] = True
                for tag in optional_tags:
                    if not tag in new_person_map.keys():
                        new_person_map[tag] = 'NA'
                people.append(new_person_map)
            start_case = True
            line[1] = line[1].replace('@', '')
            new_person_map = {'id': line[1]}
        elif line[0] == 'NAME':
            new_person_map['name'] = line[1]
        elif line[0] == 'SEX':
            new_person_map['gender'] = line[1]
        elif line[0] == 'DATE':
            date = datetime.strptime(line[1], '%d %b %Y')
            diff = relativedelta(datetime.now(), date)
            date = str(date)
            birthday = date.split(' ')
            new_person_map['birthday'] = birthday[0]
            new_person_map['age'] = diff.years
        elif line[0] == 'FAMS':
            line[1] = line[1].replace('@', '')
            if 'spouse' in new_person_map.keys():
                new_person_map['spouse'].append(line[1])
            else:
                new_person_map['spouse'] = [line[1]]
        elif line[0] == 'FAMC':
            line[1] = line[1].replace('@', '')
            if 'child' in new_person_map.keys():
                new_person_map['child'].append(line[1])
            else:
                new_person_map['child'] = [line[1]]
        elif line[0] == 'DEAT':
            new_person_map['alive'] = False
            new_person_map['death'] = line[1]
    if not 'alive' in new_person_map.keys():
        new_person_map['alive'] = True
    for tag in optional_tags:
        if not tag in new_person_map.keys():
            new_person_map[tag] = 'NA'
    people.append(new_person_map)


def create_family_list(parsed_output):
    prev_is_married = False
    prev_is_divorced = False
    start_case = False
    for line in parsed_output:
        if line[0] == "FAM":
            if start_case == True:
                families.append(z)
            start_case = True
            line[1] = line[1].replace('@', '')
            z = Family(line[1])
        elif line[0] == "MARR":
            prev_is_married = True
        elif line[0] == "DATE" and prev_is_married == True:
            z.married = line[1]
            prev_is_married = False
        elif line[0] == "DIV":
            prev_is_divorced = True
        elif line[0] == "DATE" and prev_is_divorced == True:
            z.divorced = line[1]
            prev_is_married = False
        elif line[0] == "HUSB":
            line[1] = line[1].replace('@', '')
            z.husbandId = line[1]
            z.husbandName = person_lookup(line[1])
        elif line[0] == "WIFE":
            line[1] = line[1].replace('@', '')
            z.wifeId = line[1]
            z.wifeName = person_lookup(line[1])
        elif line[0] == "CHIL":
            line[1] = line[1].replace('@', '')
            if len(z.children) > 0:
                z.children.append(line[1])
            else:
                z.children = [line[1]]
    families.append(z)


def person_lookup(ID):
    for person in people:
        if person['id'] == ID:
            return person['name']


def build_table(table, headers, data):
    for header in headers:
        column = [item[header] for item in data]
        table.add_column(header, column)
    table.sortby = "id"
    print(table)

def parse(lines):
    for line in lines:
        line = line.strip()
        line = line.replace("\n", "")
        split = line.split(" ", 2)
        if len(split) == 2:  # if it has no extra args, add an empty one
            split.append("")
        if split[0] == "0":
            if split[2] == "INDI":
                print_out(0, "INDI", True, split[1])
            elif split[2] == "FAM":
                print_out(0, "FAM", True, split[1])
            elif split[1] == "HEAD":
                print_out(0, "HEAD", True, split[2])
            elif split[1] == "TRLR":
                print_out(0, "TRLR", True, split[2])
            elif split[1] == "NOTE":
                print_out(0, "NOTE", True, split[2])
            else:
                print_out(0, split[1], False, split[2])
        elif split[0] == "1":
            possible_tags = [
                "NAME",
                "SEX",
                "BIRT",
                "DEAT",
                "FAMC",
                "FAMS",
                "MARR",
                "HUSB",
                "WIFE",
                "CHIL",
                "DIV"
            ]
            if split[1] in possible_tags:
                print_out(1, split[1], True, split[2])
            else:
                print_out(1, split[1], False, split[2])
        elif split[0] == "2":
            if split[1] == "DATE":
                print_out(2, "DATE", True, split[2])
            else:
                print_out(2, split[1], False, split[2])
        else:
            print_out(split[0], split[1], False, split[2])


def print_in(str):
    print("-->", str)


def print_out(level, tag, valid, arg):
    if valid:
        # valid_str = "<--" + str(level) + "|" + str(tag) + "|" + ("Y" if valid else "N") + "|" + str(arg)
        valid_str_arr = [str(tag), str(arg)]
        parsed_output.append(valid_str_arr)
        # print(parsed_output[-1])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Homemade GEDCOM reader')
    parser.add_argument('GEDCOM_file', type=str,
                        help='The file to read (must be in GEDCOM format')
    args = parser.parse_args()

    with open(args.GEDCOM_file) as file:
        lines = file.readlines()
        parse(lines)
    create_individual_list(parsed_output)
    create_family_list(parsed_output)
    for family in families:
        family = family.format_tuple()
        formatted_families.append(family)
    print("----------------------------------------INDIVIDUAL TABLE----------------------------------------")
    build_table(individual_table, individual_headers, people)
    print("\n-------------------------------------------------------FAMILY TABLE-------------------------------------------------------")
    build_table(family_table, family_headers, formatted_families)
