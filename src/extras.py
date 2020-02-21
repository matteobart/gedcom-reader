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
            if (month < today.month or (month == today.month and day < today.day)): # if birthday passed go next year
                year += 1
            if (month == 1 and day == 29 and year % 4 != 0): # if birthday is on leap day and not leap year 
                month = 2
                day = 1
            next_birthday = datetime(year, month, day)
            
            # actual check
            if ((next_birthday-today).days) < 30 and person.alive:
                birthdayList.append(person)
    return birthdayList









def fewer_than_15_siblings(family): 
    # returns False if any family has more than 15 siblings
    # otherwise True
    return False if (family.children and len(family.children) > 15) else True

def marriage_before_death(family, people):
    #family, singluar. people, entire dict of individuals
    married_date = family.married #called RIGHT AFTER family is married, so married date assumed to be set
    husband = people[family.husbandId]
    wife = people[family.wifeId]
    today = datetime.now()
    if not wife.alive:
        
    return True
    # husband = husbCall #replace with database call on individuals table with id of husband, for now assume correct results
    # wife = wifeCall #replace with database call on individuals table with id of husband, for now assume correct results
    # if not husband.alive or not wife.alive:
    return True

def list_recent_births(people):
    ret = []
    for person in people:
        if person.birthday is not None:
            today = datetime.now()
            if (today - person.birthday).days < 30:
                ret.append(person)
    return ret 