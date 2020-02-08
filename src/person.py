class Person:
    # Args:
    # Gender: True -> Male, False -> Female
    # id: String, name: String, gender: bool, birthday: String, age: int, alive: bool, death: String, children: [String (id)], spouse: [String (id)]
    def __init__(self, id, name, gender, birthday, age, alive, death, children, spouse):
        self.id = id
        self.name = name
        self.gender = gender
        self.birthday = birthday
        self.age = age
        self.alive = alive
        self.death = death
        self.children = children
        self.spouse = spouse


    def __str__(self):
        print("{}|{}|{}|{}|{}|{}|{}|{}|{}".format(
            self.id, 
            self.name,
            "M" if self.gender else "F",
            self.birthday,
            self.age,
            self.alive,
            self.death,
            self.child,
            self.spouse))

    def __lt__(self, other):
        return self.id < other.id
    def __le__(self, other):
        return self.id <= other.id
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        return False
    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self.id != other.id
        return True
    def __gt__(self, other):
        return self.id > other.id
    def __ge__(self, other):
        return self.id >= other.id
