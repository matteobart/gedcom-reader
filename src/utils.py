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
    married_date = family.married
    husband = people[family.husbandId]
    wife = people[family.wifeId]
    if not wife.alive:
        if (married_date - wife.death).days > 0:
            raise Exception(
                "Married Date should be before death date of wife in family:", family.id)
    if not husband.alive:
        if (married_date - husband.death).days > 0:
            raise Exception(
                "Married Date should be before death date of husband in family:", family.id)
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
    if  (death_date - birth_date).days < 0:
        print( death_date- birth_date )
        print(birth_date)
        print(death_date)

        raise Exception(
            "Death Date should not be before birth date of person:", person.id)
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

    if (married_date - wife.birthday).days < 0:
        raise Exception(
            "Married Date should  not be before birth date of wife in family:", family.id)

    if (married_date - husband.birthday).days < 0:
        raise Exception(
            "Married Date should  not be before birth date of husband in family:", family.id)
    return True


def reject_illegitimate_dates(date):
    formatted_date = parse_date(date)
    try:
        datetime(year=formatted_date.year,
                 month=formatted_date.month, day=formatted_date.day)
        return True
    except ValueError:
        return False
