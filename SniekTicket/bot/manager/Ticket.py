import utils.database as db

class Ticket:

    def __init__(self, ticketid, ownerid, channelid, timestamp, concern, detailedconcern, ticketformular):

        self.ticketid = ticketid
        self.ownerid = ownerid
        self.channelid = channelid
        self.timestamp = timestamp
        self.modid = 0
        self.state = 'open'
        self.concern = concern
        self.detailedconcern = detailedconcern
        self.ticketformular = ticketformular
        db.insertData("tickets", "ticketid, ownerid, channelid, timestamp, modid, state, concern, detailedconcern, ticketform", f"{self.ticketid}, {self.ownerid}, {self.channelid}, {self.timestamp}, {self.modid}, '{self.state}', '{self.concern}', '{self.detailedconcern}', '{self.ticketformular}'")



    def setModerator(self, id: int):
        self.modid = id
        db.updateData("tickets", "modid = {}".format(self.modid), "ticketid = {}".format(self.ticketid))


    def setState(self, state: str):
        self.state = state
        db.updateData("tickets", "state = '{}'".format(self.state), "ticketid = {}".format(self.ticketid))

    def setConcern(self, concern: str):
        self.concern = concern
        db.updateData("tickets", "concern = '{}'".format(self.concern), "ticketid = {}".format(self.ticketid))

    def setDetailedConcern(self, detailedconcern: str):
        self.detailedconcern = detailedconcern
        db.updateData("tickets", "detailedconcern = '{}'".format(self.detailedconcern), "ticketid = {}".format(self.ticketid))




def getAllOpenTickets():
    return list(db.getData("tickets", "*", "state = 'open'"))


def getCurrentTicketID():
    _d =  db.convertData(db.executeGet(f"SELECT ticketid FROM tickets WHERE state = 'open' ORDER BY ticketid DESC LIMIT 1;"), "int")
    if _d == None:
        return 0
    else:
        return _d


