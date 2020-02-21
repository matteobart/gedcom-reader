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
    #family, singluar. people, entire dict of individuals
    married_date = family.married #called RIGHT AFTER family is married, so married date assumed to be set
    husband = people[family.husbandId]
    wife = people[family.wifeId]
    if not wife.alive:
        if (married_date - wife.death) < 0: raise RuntimeError("Married Date should be before death date of wife in family {}".format(family.id))
    if not husband.alive:
        if (married_date - husband.death) < 0: raise RuntimeError("Married Date should be before death date of husband in family {}".format(family.id))
    return True
