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
    people = {} # id -> person - Type: (String -> Person object)
    families = {} # id -> family - Type: (String -> Family object)

    iterator = iter(lines) # this line is oh so important to keep the code clean
    current_entity = None # reference to the last edited object!

    for line in iterator:
        # clean up the line
        split = line.strip().replace("\n", "").split(" ", 2) #this is probably the most confusing line
        if (len(split) == 2):
           split.append("")

        if split[0] == "0": # level 0 tag
            if split[2] == "INDI": # PERSON ONLY
                id = split[1].replace("@","")
                # NOTE children & spouse must be set here otherwise Python will share list across all instances
                current_entity = Person(id, alive=True, children=[], spouse=[]) # ASSUME alive!  
                people[id] = current_entity
                print(current_entity)
            elif split[2] == "FAM": # FAMILY ONLY
                id = split[1].replace("@","")
                # NOTE children must be set here otherwise Python will share list across all instances
                current_entity = Family(id, children=[])
                families[id] = current_entity # create a family add it to the dict
            elif split[1] == "HEAD": 
                pass
            elif split[1] == "TRLR":
                pass
            elif split[1] == "NOTE":
                pass
            else:
                pass
                # following line ASSUMES that the tag is the second element in line, could be third
                # raise Exception("Invalid level 0 line:", split[1], "is not a valid tag") 
        
        elif split[0] == "1": # level 1 tag
            if split[1] == "NAME": # PERSON ONLY
                current_entity.name = split[2]
            elif split[1] == "SEX": # PERSON ONLY
                current_entity.gender = split[2]
            elif split[1] == "BIRT": # PERSON ONLY
                # NOT YET USED!
                pass
            elif split[1] == "DEAT":
                current_entity.alive = False
                current_entity.death = split[2] # possible better to format this
            elif split[1] == "FAMC":
                childId = split[2].replace("@","")
                current_entity.children.append(childId)
            elif split[1] == "FAMS":
                spouseId = split[2].replace("@","")
                current_entity.spouse.append(spouseId)
            elif split[1] == "MARR": # FAMILY ONLY
                next_line = next(iterator)
                next_split = next_line.replace("\n","").split(" ", 2)
                date = utils.parse_date(next_split[2])
                current_entity.married = date
            elif split[1] == "HUSB": # FAMILY ONLY
                husbandId = split[2].replace("@","")
                husband = people[husbandId]
                current_entity.husbandId = husbandId
                current_entity.husbandName = husband.name
            elif split[1] == "WIFE": # FAMILY ONLY
                wifeId = split[2].replace("@","")
                wife = people[wifeId]
                current_entity.wifeId = wifeId
                current_entity.wifeName = wife.name
            elif split[1] == "CHIL": # FAMILY ONLY
                childId = split[2].replace("@","")
                current_entity.children.append(childId)
            elif split[1] == "DIV": # FAMILY ONLY
                next_line = next(iterator)
                next_split = next_line.replace("\n","").split(" ", 2)
                date = utils.parse_date(next_split[2])
                current_entity.divorced = date
            else:
                pass 
                # this following line is a-okay!
                # raise Exception("Invalid level 1 line:", split[2], "is not a valid tag")
        
        elif split[0] == "2": #level 2 tag
            if split[1] == "DATE":
                date = utils.parse_date(split[2])
                # this tag can be used for either person OR family
                if isinstance(current_entity, Person):
                    diff = relativedelta(datetime.now(), date)
                    current_entity.age = diff.years
                    current_entity.birthday = date
                elif isinstance(current_entity, Family):
                    # code should never come here 
                    # please see DIV & MARR
                    pass
                else:
                    raise Exception("DATE was called before an entity was defined")
            else:
                pass
                # raise Exception("Invalid level 2 line:", split[1], "is not a valid tag")

        else: # not a level 0, 1, or 2
            raise Exception("Invalid level", split[0], "does not exist!")

    return (people.values(), families.values())
