from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

import person
from mock import patch, MagicMock


def list_upcoming_birthdays(people):
    birthdayList = []
    for person in people:
        if person.birthday is not None:
            today = datetime.now()
            month = person.birthday.month
            day = person.birthday.day
            year = today.year
            # if birthday passed go next year
            if (month < today.month or (month == today.month and day < today.day)):
                year += 1
            # if birthday is on leap day and not leap year
            if (month == 2 and day == 29 and year % 4 != 0):
                month = 3
                day = 1
            next_birthday = datetime(year, month, day)

            # actual check
            if ((next_birthday-today).days) < 30 and person.alive:
                birthdayList.append(person.id)
    # if(len(birthdayList) > 0):
    #     for member in birthdayList:
    #         print("\nANAMOLY: INDIVIDUALS: US38: list_upcoming_birthdays(): Person '" +
    #               member.id + "' has an upcoming birthday")
    print("INFO: PEOPLE: US38: list_upcoming_birthdays: The following INDIVIDUALS have upcoming birthdays:", birthdayList)
    return birthdayList


def fewer_than_15_siblings(family):
    # returns False if any family has more than 15 siblings, and prints the family
    # otherwise True
    if (family.children and len(family.children) > 15):
        print("\nANOMALY: FAMILY: US15: fewer_than_15_siblings(): Family {} has more than 15 child siblings".format(family.id))
        return False
    return True


def list_recent_births(people):
    ret = []
    for person in people:
        if person.birthday is not None:
            today = datetime.now()
            if (today - person.birthday).days < 30:
                ret.append(person.id)
    print("\nINFO: PEOPLE: US35: list_recent_births(): The following INDIVIDUALS were recently born:", ret)
    return ret


def list_recent_deaths(people):
    ret = []
    for person in people:
        if person.death is not None:
            today = datetime.now()
            if (today - person.death).days < 30:
                ret.append(person.id)
    print("\nINFO: PEOPLE: US36: list_recent_deaths(): The following INDIVIDUALS recently died:", ret)
    return ret


def list_deceased(people):
    deceased = []
    for person in people:
        if person.death is not None:
            deceased.append(person.id)
    print("\nINFO: PEOPLE: US29: list_deceased(): the following individuals are deceased: ", deceased)
    return deceased


def list_orphans(people, families):
    people_dict = {people[i].id: people[i] for i in range(0, len(people))}
    ret = []
    for family in families:
        if family.husbandId == None or family.wifeId == None:
            continue
        husband = people_dict.get(family.husbandId)
        wife = people_dict.get(family.wifeId)
        if husband == None or wife == None:
            continue
        if husband.death == None or wife.death == None:
            continue
        # we now know both parents have passed
        for childId in family.children:
            child = people_dict.get(childId)
            if child != None and child.age != None and child.age < 18:
                ret.append(childId)
    print("\nINFO: PEOPLE: US33: list_orphans: The following people are orphans: " + str(ret))
    return ret


def list_large_age_gap(people, families):
    people_dict = {people[i].id: people[i] for i in range(0, len(people))}
    ret = []
    for family in families:
        if family.husbandId == None or family.wifeId == None or family.married == None:
            continue
        date = family.married
        husband = people_dict.get(family.husbandId)
        wife = people_dict.get(family.wifeId)
        if husband == None or wife == None:
            continue
        hBirth = husband.birthday
        wBirth = wife.birthday
        if hBirth == None or wBirth == None:
            continue
        hAge = relativedelta(hBirth, date)
        wAge = relativedelta(wBirth, date)
        if hAge.years * 2 < wAge.years or wAge.years * 2 < hAge.years:
            ret.append(family.id)
    print("\nINFO: FAMILY: US34: list_large_age_gap: The following families have large age gaps between husband/wife: " + str(ret))
    return ret


def include_individual_ages(person):
    diff = relativedelta(datetime.now(), person.birthday)
    person.age = diff.years
    return person


def correct_gender_for_role(people, family):
    for person in people:
        if(person.gender == 'F' and person.id == family.husbandId):
            print('\nINFO: PEOPLE: US21: correct_gender_for_role: ERROR in family ' + family.id + ': ' + person.name + '`s gender is ' +
                  person.gender + '(emale) but his role is `Husband` as seen by husbandId:', family.husbandId)
            return False
        elif(person.gender == 'M' and person.id == family.wifeId):
            print('\nINFO: PEOPLE: US21: correct_gender_for_role: In family ' + family.id + ': ' + person.name + '`s gender is ' +
                  person.gender + '(ale) but her role is `Wife` as seen by wifeId:', family.wifeId)
            return False
    return True


def get_delta_years(years, from_date=None):
    if from_date is None:
        from_date = datetime.now()
    return from_date - relativedelta(years=years)


def less_than_150yo(people):
    returnable = True
    for person in people:
        if person.alive == True:
            if person.age >= 150:
                returnable = False
                print("\nANOMALY: PEOPLE: US07: less_than_150yo(): Person {} should not be more than 150 years old. (born {})".format(
                    person.id, person.birthday))
        else:
            if person.birthday < get_delta_years(150, person.death):
                returnable = False
                print("\nANOMALY: PEOPLE: US07: less_than_150yo(): Person {} was more than 150 years old. (born {}, died {})".format(
                    person.id, person.birthday, person.death))
    return returnable


def list_upcoming_anniversaries(couples):
    """
    Input expected as [(husbID: string, wifeID: string, marrDate: date}, ...]
    Dependant on list_living_married() (US30)
    """
    a_list = []
    for couple in couples:
        today = datetime.now()
        month = couple[2].month
        day = couple[2].day
        year = today.year
        # if birthday passed go next year
        if (month < today.month or (month == today.month and day < today.day)):
            year += 1
        # if birthday is on leap day and not leap year
        if (month == 2 and day == 29 and year % 4 != 0):
            month = 3
            day = 1
        ann = datetime(year, month, day)

        # actual check
        if ((ann-today).days) < 30:
            a_list.append((couple[0], couple[1]))
    print("\nINFO: FAMILY: US39: list_upcoming_anniverseries: The following (husband,wife) id COUPLES have upcoming anniverseries:", a_list)
    return a_list


def check_corresponding_entries(people, families):
    people_dict = {people[i].id: people[i] for i in range(0, len(people))}
    family_dict = {families[i].id: families[i]
                   for i in range(0, len(families))}
    for family in families:
        hId = family.husbandId
        wId = family.wifeId
        cIds = family.children
        husband = people_dict.get(hId)
        wife = people_dict.get(wId)
        if hId == None:
            print("\nINFO: FAMILY: US26: check_corresponding_entries: Husband id is missing from family ({})".format(
                family.id))
        elif husband == None:  # check to make sure person exists
            print("\nINFO: PEOPLE: US26: check_corresponding_entries: Husband ({}) is in family ({}), but missing from people".format(
                hId, family.id))
        else:
            if husband.name != family.husbandName:  # check names match
                print("\nINFO: PEOPLE: US26: check_corresponding_entries: Husband ({}) is in family ({}), but have different names".format(
                    hId, family.id))
            if family.id not in husband.spouse:  # check his family is listed under spouses
                print("\nINFO: PEOPLE: US26: check_corresponding_entries: Husband ({}) is missing his family ({}), from his person".format(
                    hId, family.id))
        if wId == None:
            print("\nINFO: FAMILY: US26: check_corresponding_entries: Wife id is missing from family ({})".format(
                family.id))
        elif wife == None:  # check to make sure person exists
            print("\nINFO: PEOPLE: US26: check_corresponding_entries: Wife ({}) is in family ({}), but missing from people".format(
                wId, family.id))
        else:
            if wife.name != family.wifeName:  # check names match
                print("\nINFO: PEOPLE: US26: check_corresponding_entries: Wife ({}) is in family ({}), but have different names".format(
                    wId, family.id))
            if family.id not in wife.spouse:  # check his family is listed under spouses
                print("\nINFO: PEOPLE: US26: check_corresponding_entries: Wife ({}) is missing her family ({}), from her person".format(
                    wId, family.id))

        for cId in cIds:
            child = people_dict.get(cId)
            if child == None:
                print("\nINFO: PEOPLE: US26: check_corresponding_entries: Child ({}) is in family ({}), but missing from people".format(
                    cId, family.id))
            else:
                if family.id not in child.children:
                    print("\nINFO: PEOPLE: US26: check_corresponding_entries: Child ({}) is in family ({}), but missing its family id from person children property".format(
                        cId, family.id))

    for person in people:
        for familyId in person.children:
            family = family_dict.get(familyId)
            if family == None:
                print("\nINFO: FAMILY: US26 Family ({}), that person ({}) is a child in, is missing from families".format(
                    familyId, person.id))
            else:
                if person.id not in family.children:
                    print("\nINFO: FAMILY: US26 Family ({}) is missing their child ({}). Should be in children list".format(
                        familyId, person.id))

        for familyId in person.spouse:
            family = family_dict.get(familyId)
            if family == None:
                print("\nINFO: FAMILY: US26 Family ({}), that person ({}) is a spouse in, is missing from families".format(
                    familyId, person.id))
            else:
                if person.gender == "M" and person.id != family.husbandId:
                    print("\nINFO: FAMILY: US26 Person ({}) says they are part of family ({}), but they are not the father!".format(
                        person.id, familyId))

                if person.gender == "F" and person.id != family.wifeId:
                    print("\nINFO: FAMILY: US26 Person ({}) says they are part of family ({}), but they are not the mother!".format(
                        person.id, familyId))


def list_living_married(people, families):
    """
    Returns a list of all individuals who are currently alive and their spouse is alive

    written by: Brenden

    :param people: list of person objects
    :param families: dict of family objects
    :return: List
    """
    people_dict = {people[i].id: people[i] for i in range(0, len(people))}
    ret = []
    for family in families:
        if family.husbandId == None or family.wifeId == None:
            continue
        husband = people_dict.get(family.husbandId)
        wife = people_dict.get(family.wifeId)
        if husband == None or wife == None or family.divorced == True:
            continue
        if husband.alive and wife.alive:
            ret.append(family.husbandId)
            ret.append(family.wifeId)

    unique_ret = []
    for x in ret:
        if x not in unique_ret:
            unique_ret.append(x)
    print(
        "\nINFO: PEOPLE: US30: list_living_married: The following ID's are of people who currently are married and alive: " + str(
            unique_ret))
    return unique_ret


def list_recent_survivors(people, families):
    """
    Returns a list of all individuals whose spouse has died in the past 30 days

    written by: Brenden

    :param people: list of person objects
    :param families: dict of family objects
    :return: List
    """
    people_dict = {people[i].id: people[i] for i in range(0, len(people))}
    today = datetime.today()
    ret = []
    for family in families:
        if family.husbandId == None or family.wifeId == None:
            continue
        husband = people_dict.get(family.husbandId)
        wife = people_dict.get(family.wifeId)
        if husband.alive == None or wife.alive == None:
            continue
        if husband.alive and not wife.alive:
            if wife.death != None:
                if today - wife.death < timedelta(days=30):
                    ret.append(family.husbandId)
        if not husband.alive and wife.alive:
            if husband.death != None:
                if today - husband.death < timedelta(days=30):
                    ret.append(family.wifeId)
    unique_ret = []
    for x in ret:
        if x not in unique_ret:
            unique_ret.append(x)
    print(
        "\nINFO: PEOPLE: US37: list_recent_survivors: The following ID's are of people whose spouse has died in the past 30 days: " + str(
            unique_ret))
    return unique_ret


def birth_after_marriage_of_parents(people, families):
    """
    Checks to see that a person is born after marriage of mother and father

    written by: Chaeli

    """
    list = []
    for person in people:
        for family in families:
            if person.birthday != None:
                if person.id in family.children:
                    birth = person.birthday
                    if family.divorced != None:
                        divorce = family.divorced
                        r = relativedelta(birth, divorce)
                        months = r.months
                        if months > 9:
                            list.append(person.id)
                    elif family.married != None:
                        marriage = family.married
                        if (marriage - birth).days > 0:
                            list.append(person.id)
                    else:
                        list.append(person.id)
    print("\nINFO: FAMILY: US08: birth_after_marriage_of_parents: People born before marriage of parents/over 9 months after divorce {}".format(
                                list))
    return list


def list_living_single(people, families):
    singles_list = []
    for person in people:
        if(person.age > 30 and person.alive and len(person.spouse) == 0):
            for family in families:
                if(person.id != family.husbandId and person.id != family.wifeId):
                    if(person.id not in singles_list):
                        singles_list.append(person.id)
    print('INFO: PEOPLE: US31: list_living_single: The following individuals are older than 30 and single ', singles_list)
    return singles_list
