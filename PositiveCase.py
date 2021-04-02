class PositiveCase:
    # data = {nric, name, location, checkInDate, checkInTime, checkOutTime}
    def __init__(self, name, nric, location, checkInDate, checkInTime, checkOutTime):
        self.name = name
        self.nric = nric
        self.location = location
        self.checkInDate = checkInDate
        self.checkInTime = checkInTime
        self.checkOutTime = checkOutTime

    # def __init__(self, data):
    #     self.data = data
