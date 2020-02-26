from prettytable import PrettyTable
import person
import family
from datetime import datetime


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
    if not wife.alive:
        if (married_date - wife.death).days > 0:
            print("\nERROR: FAMILY: US05: marriage_before_death(): Family {}: married Date {} should be before death date of wife on {}".format(
                family.id, married_date, wife.death))
            return False
    if not husband.alive:
        if (married_date - husband.death).days > 0:
            print("\nERROR: FAMILY: US05: marriage_before_death(): Family {}: married Date {} should be before death date of husband on {}".format(
                family.id, married_date, husband.death))
            return False
    return True


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
    try:
        return parse_date(date)
    except ValueError:
        print("\nERROR: DATE: US42: reject_illegitimate_dates(): " +
              date + " is an invalid date")
        return False
