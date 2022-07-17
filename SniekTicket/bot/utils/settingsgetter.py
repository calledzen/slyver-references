import utils.database as db


def getLogChannelID(name):
    return db.convertData(db.getData("ticketsettings", "logchannel", f"ticketname='{name}'"), "int")


def getCreateChannel(name):
    return db.convertData(db.getData("ticketsettings", "createchannel", f"ticketname='{name}'"), "int")


def getTeamRoleID(name):
    return db.convertData(db.getData("ticketsettings", "teamroleid", f"ticketname='{name}'"), "int")



