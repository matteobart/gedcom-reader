from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from family import Family
from person import Person
import utils

# Arguments:
# lines: [file_lines] - Type: [String]
# Return:
# ([people, families]) - Type: ([Person object], [Family object])


def parse(lines):
    # data structures!
    people = {}  # id -> person - Type: (String -> Person object)
    families = {}  # id -> family - Type: (String -> Family object)

    # this line is oh so important to keep the code clean
    iterator = iter(lines)
    current_entity = None  # reference to the last edited object!

    for line in iterator:
        # this is probably the most confusing line
        split = line.strip().replace("\n", "").split(" ", 2)
        if (len(split) == 2):
            split.append("")

        line_num = utils.get_line_number(line, lines) # lets just roll with it

        if split[0] == "0":  # level 0 tag
            if split[2] == "INDI":  # PERSON ONLY
                id = split[1].replace("@", "")
                if people.get(id) != None:
                    print("ERROR: Line {}: PERSON: US22: This INDI ID is not unique: {}".format(
                        utils.get_line_number(line, lines),
                        id))
                # NOTE children & spouse must be set here otherwise Python will share list across all instances
                current_entity = Person(
                    id, alive=True, children=[], spouse=[])  # ASSUME alive!
                people[id] = current_entity
            elif split[2] == "FAM":  # FAMILY ONLY
                id = split[1].replace("@", "")
                if families.get(id) != None:
                    print("ERROR: Line {}: FAMILY: US22: This FAM ID is not unique: {}".format(
                        utils.get_line_number(line, lines),
                        id))
                # NOTE children must be set here otherwise Python will share list across all instances
                current_entity = Family(id, children=[])
                # create a family add it to the dict
                families[id] = current_entity
            elif split[1] == "HEAD":
                pass
            elif split[1] == "TRLR":
                pass
            elif split[1] == "NOTE":
                pass
            else:
                pass

        elif split[0] == "1":  # level 1 tag
            if split[1] == "NAME":  # PERSON ONLY
                current_entity.name = split[2]
                utils.check(line_num, utils.check_unique_birth_and_name, current_entity, people)
            elif split[1] == "SEX":  # PERSON ONLY
                current_entity.gender = split[2]
            elif split[1] == "BIRT":  # PERSON ONLY
                next_line = next(iterator)
                next_split = next_line.replace("\n", "").split(" ", 2)
                date = utils.check(line_num, utils.reject_illegitimate_dates, next_split[2])
                diff = relativedelta(datetime.now(), date)
                current_entity.age = diff.years
                current_entity.birthday = date
                utils.check(line_num, utils.check_unique_birth_and_name, current_entity, people)
            elif split[1] == "DEAT":
                # can check if "Y" is in split[2] if youd like
                current_entity.alive = False
                next_line = next(iterator)
                next_split = next_line.replace("\n", "").split(" ", 2)
                date = utils.check(line_num, utils.reject_illegitimate_dates, next_split[2])
                current_entity.death = date
            elif split[1] == "FAMC":
                childId = split[2].replace("@", "")
                current_entity.children.append(childId)
            elif split[1] == "FAMS":
                spouseId = split[2].replace("@", "")
                current_entity.spouse.append(spouseId)
            elif split[1] == "MARR":  # FAMILY ONLY
                next_line = next(iterator)
                next_split = next_line.replace("\n", "").split(" ", 2)

                date = utils.check(line_num, utils.reject_illegitimate_dates, next_split[2])
                current_entity.married = date
                utils.check(line_num, utils.birth_before_marriage, current_entity, people)
                utils.check(line_num, utils.marriage_after_14, current_entity, people)
                utils.check(line_num, utils.marriage_before_death,current_entity, people)
                utils.check(line_num, utils.no_marriage_to_children, current_entity, people)
                utils.check(line_num, utils.no_marriage_to_siblings, current_entity, people)
            elif split[1] == "HUSB":  # FAMILY ONLY
                husbandId = split[2].replace("@", "")
                husband = people[husbandId]
                current_entity.husbandId = husbandId
                current_entity.husbandName = husband.name
            elif split[1] == "WIFE":  # FAMILY ONLY
                wifeId = split[2].replace("@", "")
                wife = people[wifeId]
                current_entity.wifeId = wifeId
                current_entity.wifeName = wife.name
            elif split[1] == "CHIL":  # FAMILY ONLY
                childId = split[2].replace("@", "")
                current_entity.children.append(childId)
            elif split[1] == "DIV":  # FAMILY ONLY
                next_line = next(iterator)
                next_split = next_line.replace("\n", "").split(" ", 2)
                date = utils.check(line_num, utils.reject_illegitimate_dates,next_split[2])
                current_entity.divorced = date
                utils.check(line_num, utils.divorce_before_death, current_entity, people)
                utils.check(line_num, utils.marriage_before_divorce, current_entity)
            else:
                pass

        elif split[0] == "2":  # level 2 tag
            if split[1] == "DATE":

                date = utils.check(line_num, utils.reject_illegitimate_dates, split[2])
                # this tag can be used for either person OR family
                if isinstance(current_entity, Person):
                    # code should never come here
                    # please see BIRT
                    pass
                elif isinstance(current_entity, Family):
                    # code should never come here
                    # please see DIV & MARR
                    pass
                else:
                    raise Exception(
                        "DATE was called before an entity was defined")
            else:
                pass
                # raise Exception("Invalid level 2 line:", split[1], "is not a valid tag")

        else:  # not a level 0, 1, or 2
            raise Exception("Invalid level", split[0], "does not exist!")

    return (people.values(), families.values())
