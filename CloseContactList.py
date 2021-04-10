class Case:
    # data = {nric, name, location, checkInDate, checkInTime, checkOutTime}
    def __init__(self, data):
        self.data = data
        self.next = None

class CloseContactList:
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

    def search(self, key):
        # Initialize current to head
        current = self.head
        res = None
  
        # loop till current not equal to None
        while current != None:
            if current.data["nric"] == key:
                res = current.data
                # print(res)
              
            current = current.next
        
        if res != None:
            return res

    def printList(self,start):
        first = start
        temp = self.head
        listStr = first + " -> "
        edges = []
        while temp is not None:
            sinep = listStr + temp.data["nric"]
            # edges.append([first, temp.data["nric"]])
            # print(sinep)
            tt = temp.data["nric"]
            temp = temp.next
            if temp is not None:
                if tt == temp.data["nric"]:
                    temp = temp.next
        # return edges

    def edges(self,start):
        first = start
        temp = self.head
        edges = []
        while temp is not None:
            edges.append([first, temp.data["nric"]])
            tt = temp.data["nric"]
            temp = temp.next
            if temp is not None:
                if tt == temp.data["nric"]:
                    temp = temp.next
        return edges