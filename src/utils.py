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