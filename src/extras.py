from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

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
            if (month == 1 and day == 29 and year % 4 != 0):
                month = 2
                day = 1
            next_birthday = datetime(year, month, day)

            # actual check
            if ((next_birthday-today).days) < 30 and person.alive:
                birthdayList.append(person)

    print("ANAMOLY: INDIVIDUALS: US38: Person {} has an upcoming birthday").format(
        person.id)

    return birthdayList


def fewer_than_15_siblings(family):
    # returns False if any family has more than 15 siblings, and prints the family
    # otherwise True
    if (family.children and len(family.children) > 15):
        print("ERROR: FAMILY: US15: fewer_than_15_siblings(): Family {} has more than 15 child siblings".format(family.id))
        return False
    return True


def list_recent_births(people):
    ret = []
    for person in people:
        if person.birthday is not None:
            today = datetime.now()
            if (today - person.birthday).days < 30:
                ret.append(person)
    return ret
