class Person:
    def __init__(self,
                 id,
                 name=None,
                 sur_name=None,
                 gender=None,
                 birthday=None,
                 age=None,
                 alive=None,
                 death=None,
                 children=[],
                 spouse=[]):
        self.id = id
        self.name = name
        self.sur_name =sur_name
        self.gender = gender
        self.birthday = birthday
        self.age = age
        self.alive = alive
        self.death = death
        self.children = children
        self.spouse = spouse

    def toTuple(self):
        return(
            self.id,
            self.name,
            self.gender,
            self.birthday,
            self.age,
            self.alive,
            self.death,
            self.children,
            self.spouse)

    def __str__(self):
        return("{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(
            self.id,
            self.name,
            self.sur_name,
            "M" if self.gender == "M" else "F",
            self.birthday,
            self.age,
            self.alive,
            self.death,
            self.children,
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
