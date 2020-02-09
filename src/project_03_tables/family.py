class Family:
    # Args:
    # id: String, married: String/None, divorced: String/None, husband: Person, wife: Person, children: [String (id)]
    def __init__(self, id, married='NA', divorced='NA', husbandId='NA', husbandName='NA', wifeName='NA', wifeId='NA', children=[]):
        self.id = id
        self.married = married
        self.divorced = divorced
        self.husbandId = husbandId
        self.husbandName = husbandName
        self.wifeId = wifeId
        self.wifeName = wifeName
        self.children = children
    def format_tuple(self):
        return {'id': self.id, 'married': self.married, 'divorced': self.divorced, 'husbandId': self.husbandId, 'husbandName': self.husbandName, 'wifeId': self.wifeId, 'wifeName': self.wifeName, 'children': self.children}
    def __str__(self):
        return("{}|{}|{}|{}|{}|{}|{}|{}".format(
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
