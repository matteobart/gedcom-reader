class Family:
    # Args:
    # id: String, married: String/None, divorced: String/None, husband: Person, wife: Person, children: [String (id)]
    def __init__(self, id, married, divorced, husband, wife, children):
        self.id = id
        self.married = married
        self.divorced = divorced
        self.husbandId = husband.id
        self.husbandName = husband.name
        self.wifeId = wife.id
        self.wifeName = wife.name
        self.children = children

    def __str__(self):
        print("{}|{}|{}|{}|{}|{}|{}|{}".format(
            self.id, 
            self.married,
            self.divorced,
            self.husbandId,
            self.husbandName,
            self.wifeId,
            self.wifeName,
            self.children))
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
