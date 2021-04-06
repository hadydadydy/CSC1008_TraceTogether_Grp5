class PositiveCase:
    # data = {nric, name, location, checkInDate, checkInTime, checkOutTime}
    def __init__(self, data):
        # self.name = name
        # self.nric = nric
        # self.location = location
        # self.checkInDate = checkInDate
        # self.checkInTime = checkInTime
        # self.checkOutTime = checkOutTime
        self.data = data
        self.next = None
    # def __init__(self, data):
    #     self.data = data

class CCList:
    def __init__(self):
        self.head = None

    def insert(self, case):
        if self.head is None:
            self.head = case
        else:
            temp = self.head
            while temp.next is not None:
                temp = temp.next
            temp.next = case

    def printList(self):
        temp = self.head
        listStr = "\nClose contacts: \n"
        while temp is not None:
            listStr = listStr + temp.data["name"] + " -> "
            temp = temp.next
        print(listStr)
