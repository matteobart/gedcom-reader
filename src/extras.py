from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

def list_upcoming_birthdays(people):
    birthdayList = []
    for person in people:
        if person.birthday is not None:
            if (date.today() - person.birthday).days < 30:
                birthdayList.append(person)
    return birthdayList

# returns False if any family has more than 15 siblings
# otherwise True
def fewer_than_15_siblings(family): 
    return False if (family.children and len(family.children) > 15) else True
