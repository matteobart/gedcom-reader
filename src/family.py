class Family:
    def __init__(self,
                 id, 
                 married=None, 
                 divorced=None, 
                 husbandId=None, 
                 husbandName=None, 
                 wifeName=None, 
                 wifeId=None, 
                 children=[]):
        self.id = id
        self.married = married
        self.divorced = divorced
        self.husbandId = husbandId
        self.husbandName = husbandName
        self.wifeId = wifeId
        self.wifeName = wifeName
        self.children = children

    def toTuple(self):
        return(
            self.id, 
            self.married,
            self.divorced,
            self.husbandId,
            self.husbandName,
            self.wifeId,
            self.wifeName,
            self.children)

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
