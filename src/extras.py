from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

def list_upcoming_birthdays(people):
    birthdayList = []
    for person in people:
        if person.birthday is not None:
            if (date.today() - person.birthday).days < 30:
                birthdayList.append(person)
    return birthdayList


def fewer_than_15_siblings(families): 
    for family in families:
        if len(family.children) > 15:
            return False
    return True
