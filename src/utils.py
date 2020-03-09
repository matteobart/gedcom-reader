from prettytable import PrettyTable
import person
import family
from datetime import datetime
from dateutil.relativedelta import relativedelta

list_of_months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY',
                  'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']


def parse_date(date_str):
    return datetime.strptime(date_str, "%d %b %Y")


def print_families(families):
    table = PrettyTable(("ID",
                         "Married",
                         "Divorced",
                         "HusbandId",
                         "HusbandName",
                         "WifeId",
                         "WifeName",
                         "Children"))
    for family in families:
        table.add_row(family.toTuple())
    table.sortby = "ID"
    print(table)


def print_people(people):
    table = PrettyTable(("ID",
                         "Name",
                         "Gender",
                         "Birthday",
                         "Age",
                         "Alive",
                         "Death",
                         "Child",
                         "Spouse"))
    for person in people:
        table.add_row(person.toTuple())
    table.sortby = "ID"
    print(table)


def marriage_before_death(family, people):
    # family, singluar. people, entire dict of individuals
    # called RIGHT AFTER family is married, so married date assumed to be set
    # returns false if death before marriage
    # returns true if valid
    married_date = family.married
    husband = people[family.husbandId]
    wife = people[family.wifeId]
    returnable = True
    if not wife.alive:
        if (married_date - wife.death).days > 0:
            print("\nERROR: FAMILY: US05: marriage_before_death(): Family {}: married Date {} should be before death date of wife on {}".format(
                family.id, married_date, wife.death))
            returnable = False
    if not husband.alive:
        if (married_date - husband.death).days > 0:
            print("\nERROR: FAMILY: US05: marriage_before_death(): Family {}: married Date {} should be before death date of husband on {}".format(
                family.id, married_date, husband.death))
            returnable = False
    return returnable


def birth_before_death(person):
    """
    Checks person's birthday is in fact before death

    written by: Chaeli and Brenden

    :param person: person object
    :return: Boolean
    """
    birth_date = person.birthday
    death_date = person.death
    if birth_date is None or death_date is None:
        return True
    if (death_date - birth_date).days < 0:
        print("\nERROR: PERSON: US03: birth_before_death(): Person {}:  "
              "birth date {} should be before death_ date {} of person:".format(person.id, birth_date, death_date))
        return False
    return True


def marriage_before_divorce(family):
    """
    Checks marriage date is in fact before divorce of both spouses

    written by: Brenden

    :param family: family object
    :param people: person dictionary
    :return: Boolean
    """
    married_date = family.married
    divorce_date = family.divorced
    if married_date is None or divorce_date is None:
        return True
    if (divorce_date - married_date).days < 0:
        print("\nERROR: FAMILY: US04: marriage_before_divorce(): Family {}:  "
              "marriage date {} should be before divorce date {} of family:".format(family.id,
                                                                                    married_date,
                                                                                    divorce_date))
        return False

    return True


def birth_before_marriage(family, people):
    """
    Checks marriage date is in fact after birth of both spouses

    written by: Chaeli and Brenden

    :param family: family object
    :param people: person dictionary
    :return: Boolean
    """
    married_date = family.married
    husband = people[family.husbandId]
    wife = people[family.wifeId]
    if married_date is None:
        print("\nERROR: FAMILY: US08: birth_before_marriage(): Family {}:  "
              "invalid marriage date {} :".format(family.id, married_date))
        return False
    if wife.birthday is not None and (married_date - wife.birthday).days < 0:
        print("\nERROR: FAMILY: US08: birth_before_marriage(): Family {}:  "
              "birth date {} should be before marriage date {} of wife {}:".format(family.id, wife.birthday,
                                                                                   married_date,
                                                                                   wife.id))
        return False

    if husband.birthday is not None and (married_date - husband.birthday).days < 0:
        print("\nERROR: FAMILY: US08: birth_before_marriage(): Family {}:  "
              "birth date {} should be before marriage date {} of husband {}:".format(family.id, husband.birthday,
                                                                                      married_date,
                                                                                      husband.id))
        return False
    return True


def divorce_before_death(family, people):
    """
    Checks divorce date is in fact beofre death of both spouses

    written by: Chaeli

    :param family: family object
    :param people: person dictionary
    :return: Boolean
    """
    divorce_date = family.divorced
    husband = people[family.husbandId]
    wife = people[family.wifeId]

    if divorce_date is None:
        print("\nERROR: FAMILY: US06: divorce_before_death(): Family {}:  "
              "invalid divorce date {} :".format(family.id, divorce_date))
        return False

    if (divorce_date - wife.death).days > 0:
        print("\nERROR: FAMILY: US06: divorce_before_death(): Family {}:  "
              "divorce date {} should be before death_ date {} of wife {}:".format(family.id, divorce_date, wife.death,
                                                                                   wife.id))
        return False

    if (divorce_date - husband.death).days > 0:
        print("\nERROR: FAMILY: US06: divorce_before_death(): Family {}:  "
              "divorce date {} should be before death_ date {} of husbdan {}:".format(family.id, divorce_date, husband.death,
                                                                                      husband.id))
        return False
    return True


def reject_illegitimate_dates(date):
    this_date = accept_partial_dates(date)
    try:
        return parse_date(this_date)
    except ValueError:
        print("\nERROR: DATE: US42: reject_illegitimate_dates(): " +
              this_date + " is an invalid date")
        return False


def accept_partial_dates(date):
    month = None
    day = None
    year = None
    flag = False
    partial = date.split(' ')
    for part in partial:
        if(part in list_of_months):
            month = part
        elif(len(part) <= 2):
            day = part
        elif(len(part) > 3):
            year = part
    if month is None:
        month = 'JAN'
        flag = True
    if day is None:
        day = '1'
        flag = True
    if year is None:
        year = '2000'
        flag = True
    ret = day + ' ' + month + ' ' + year
    if(flag == True):
        print("\nUS41: accept_partial_dates: Accepting: " + date + ' as valid')
    return ret
# given the line (str) and lines ([str])
# will return the line number (int) [index starting @ 1]
# WARNING: If two lines are the same in the file, will ALWAYS return the first one


def get_line_number(line, lines):
    return lines.index(line) + 1

# given a person (Person) and people (id:Person)
# will return a boolean if person's name and birthday is unique


def check_unique_birth_and_name(person, people):
    if person.name == None or person.birthday == None:
        return True  # not enough information yet
    for p in people.values():
        if p.id == person.id:
            continue
        if p.name == person.name and p.birthday == person.birthday:
            return False  # not unique
    return True


def marriage_after_14(family, people):
    # family, singluar. people, entire dict of individuals
    # called RIGHT AFTER family is married, so married date assumed to be set
    # returns false if death before marriage
    # returns true if valid
    married_date = family.married
    husband = people[family.husbandId]
    wife = people[family.wifeId]
    returnable = True
    date_cutoff = get_delta_years(14, married_date)  # get date 14 years ago
    if wife.birthday is not None and (date_cutoff - wife.birthday).days < 0:
        print("\nERROR: FAMILY: US10: marriage_after_14(): Family {}:  "
              "marriage date {} should be at least 14 years after birth date {} of wife {}:".format(family.id, married_date, wife.birthday, wife.id))
        returnable = False

    if husband.birthday is not None and (date_cutoff - husband.birthday).days < 0:
        print("\nERROR: FAMILY: US10: marriage_after_14(): Family {}:  "
              "marriage date {} should be at least 14 years after birth date {} of husband {}:".format(family.id, married_date, husband.birthday, husband.id))
        returnable = False
    return returnable

def get_parents(person, people):
    """
        Gets list of parents

        written by: Chaeli

        :param person: person id
        :param people: person dictionary
        :return: list of ids of parents of person
     """
    parents = []
    i = 0
    for x in people:
        curr = x
        children = curr.children
        if person in children:
            if not(curr in parents):
                parents.append(curr)
                i += 1
                if i == 2:
                    break
    return parents

def get_siblings(person, people):
    """
        Gets list of siblings of given person

        written by: Chaeli

        :param person: person id
        :param people: person dictionary
        :return: list of siblings of person
    """
    parents = get_parents(person, people)
    siblings = []
    result = []
    for x in parents:
        children = x.children
        for y in children:
            if person != y and (not(y in siblings)):
                siblings.append(y)
    for x in siblings:
        for y in people:
            if y.id == x:
                result.append(y)
    return result


def no_first_cousin_marriage(family, people):
    """
       Checks that there is not marriage between first cousins

       written by: Chaeli

       :param family: family object
       :param people: person dictionary
       :return: Boolean
    """
    husband = family.husbandId
    wife = family.wifeId
    parentsW = get_parents(wife, people)
    parentsH= get_parents(husband, people)
    aunts = []
    cousins = []

    for x in parentsW:
        aunts += get_siblings(x.id, people)
    for x in parentsH:
        aunts += get_siblings(x.id, people)
    for x in aunts:
        cousins += x.children

    if husband in cousins or wife in cousins:
        print("\nERROR: FAMILY: US19: no_first_cousin_marriage(): Family {}:  "
              "invalid marriage".format(family.id))
        return False

    return True


def no_aunts_and_uncles(family, people):
    """
       Checks that there is not marriage between a person and their aunt/uncle

       written by: Chaeli

       :param family: family object
       :param people: person dictionary
       :return: Boolean
    """
    husband = family.husbandId
    wife = family.wifeId
    parentsW = get_parents(wife, people)
    parentsH = get_parents(husband, people)
    aunts = []

    for x in parentsW:
        aunts += get_siblings(x.id, people)

    for x in parentsH:
        aunts += get_siblings(x.id, people)

    for x in aunts:
        if (husband == x.id) or (wife == x.id):
            print("\nERROR: FAMILY: US20: no_aunts_and_uncles(): Family {}:  "
                  "invalid marriage".format(family.id))
            return False

    return True

# inspired by SO question 765797, integrated into project by Daniel Kramer
def get_delta_years(years, from_date=None):
    if from_date is None:
        from_date = datetime.now()
    return from_date - relativedelta(years=years)


def no_marriage_to_siblings(family, people: dict):
    """
       Checks to see if marriage is not between siblings

       written by: Brenden

       :param family: family object
       :param people: person dictionary
       :return: Boolean
       """
    husband = people[family.husbandId]
    wife = people[family.wifeId]

    # Find parents of husband and wife
    parents = []
    for curr in people.values():
        children = curr.children
        for child in children:
            if husband.id == child:
                if not(curr in parents):
                    parents.append(curr)
                    if len(parents) == 2:
                        break
    for curr in people.values():
        children = curr.children
        for child in children:
            if wife.id == child:
                if not (curr in parents):
                    parents.append(curr)
                    if len(parents) == 2:
                        break

    # Find siblings of parents
    siblings = []
    for parent in parents:
        children = parent.children
        for child in children:
            if person != child and (not (child in siblings)):
                siblings.append(people[child])

    # Make sure they are not siblings
    for sibling in siblings:
        if wife.id == sibling.id or husband.id == sibling.id:
            print("\nERROR: FAMILY: US18: no_marriage_to_siblings: Family {}:  "
                  "husband {}  and wife {} are siblings:".format(family.id, husband.id, wife.id,))
            return False
    return True


def no_marriage_to_children(family, people):
    """
       Checks to see a marriage is not between an adult and a child

       written by: Brenden

       :param family: family object
       :param people: person dictionary
       :return: Boolean
       """
    husband = people[family.husbandId]
    wife = people[family.wifeId]

    children_of_husband = husband.children
    children_of_wife = wife.children

    result = True

    for child in children_of_wife:
        if husband.id == child:
            print("\nERROR: FAMILY: US17: no_marriage_to_children: Family {}:  "
                  "wife {} is a parent of husband {}:".format(family.id, wife.id, husband.id, ))
            result = False

    for child in children_of_husband:
        if wife.id == child:
            print("\nERROR: FAMILY: US17: no_marriage_to_children: Family {}:  "
                  "husband {} is a parent of wife {}:".format(family.id, husband.id, wife.id,))
            result = False

    return result
