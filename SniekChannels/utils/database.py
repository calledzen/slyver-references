import sqlite3
import mariadb
import os


def connect(type: str):
    global con
    global cur
    if(type == "sqlite"):
        con = sqlite3.connect(f"../{os.getenv('SQL_DATABASE')}.db")

    elif(type == "mariadb"):
        try:
            con = mariadb.connect(
                user=os.getenv('SQL_USER'),
                password=os.getenv('SQL_PASSWORD'),
                host=os.getenv('SQL_HOST'),
                port=int(os.getenv('SQL_PORT')),
                database=os.getenv('SQL_DATABASE')

            )
            print("SQL: Connected to database")
        except mariadb.Error as e:
            print(f"SQL: Error connecting to MariaDB Platform: {e}")

    cur = con.cursor()
    print("SQL: Connection ready")
    cur.execute("SET autocommit=1;")

def tableSetup():

    cur.execute("CREATE TABLE IF NOT EXISTS `settings` ("
                "`teamid` VARCHAR(25), "
                "`categoryid` VARCHAR(25), "
                "`settingschannelid` VARCHAR(75), "
                "`createchannelid` VARCHAR(25)"
                ");")

    cur.execute("CREATE TABLE IF NOT EXISTS `banneduser` ("
                "`channelid` VARCHAR(25), "
                "`userid` VARCHAR(25)"
                ");")

    cur.execute("CREATE TABLE IF NOT EXISTS `channels` ("
                "`channelid` VARCHAR(25), "
                "`ownerid` VARCHAR(25)"
                ");")
    con.commit()
    print("SQL: Table created")




def disconnect():
    con.close()



def getConnection():
    return con

def getCursor():
    return cur

def execute(query):
    cur.execute(query)

def executeGet(query):
    cur.execute(query)
    return cur.fetchall()


def getData(table, data_vars, wheretxt = None):
    if wheretxt == None:
        cur.execute(f"SELECT {data_vars} FROM {table};")
        return cur.fetchall()
    else:
        cur.execute(f"SELECT {data_vars} FROM {table} WHERE {wheretxt};")
        return cur.fetchall()

def checkData(table, datavar, wheretxt = None):
    if wheretxt == None:
        cur.execute(f"SELECT {datavar} FROM {table} LIMIT 1;")
        if cur.fetchall() == []:
            return False
        else:
            return True
    else:
        cur.execute(f"SELECT 1 FROM {table} WHERE {wheretxt};")
        if cur.fetchall() == []:
            return False
        else:
            return True


def insertData(table, data_args, data_value, wheretxt = None):
    if wheretxt == None:
        cur.execute(f"INSERT INTO {table} ({data_args}) VALUES ({data_value});")
        con.commit()
    else:
        cur.execute(f"INSERT INTO {table} ({data_args}) VALUES ({data_value}) WHERE {wheretxt};")
        con.commit()

def updateData(table, datatxt, wheretxt = None):
    if wheretxt == None:
        cur.execute(f"UPDATE {table} SET {datatxt};")
        con.commit()
    else:
        cur.execute(f"UPDATE {table} SET {datatxt} WHERE {wheretxt};")
        con.commit()


def setData(table, data: dict, wheretxt = None):
    _datavars = ""
    _datavalues = ""
    _preparedStatement = ""
    for item in data:
        _datavars += f"{item},"
        _datavalues += f"{data[item]},"
        _preparedStatement += f"{item} = {data[item]},"
    _datavars = _datavars[:-1]
    _datavalues = _datavalues[:-1]
    _preparedStatement = _preparedStatement[:-1]
    if wheretxt == None:
        print(_datavars)
        if(checkData(table, _datavars)):
            cur.execute(f"UPDATE {table} SET {_preparedStatement};")
            con.commit()
        else:
            cur.execute(f"INSERT INTO {table} ({_datavars}) VALUES ({_datavalues});")
            con.commit()
    else:
        if(checkData(table, _datavars)):
            cur.execute(f"UPDATE {table} SET {_preparedStatement} WHERE {wheretxt};")
            con.commit()
        else:
            cur.execute(f"INSERT INTO {table} ({_datavars}) VALUES ({_datavalues}) WHERE {wheretxt};")
            con.commit()



def convertData(response, type):
    if type == "int":
        try:
          return int(str(response).replace('(','').replace(')', '').replace("'", "").replace(",", "").replace("[", "").replace("]", ""))
        except ValueError:
            pass
    elif type == "str":
        try:
            return str(response).replace('(', '').replace(')', '').replace("'", "").replace(",", "").replace("[", "").replace("]", "")
        except ValueError:
            pass
    elif type == "list":
        try:
            _l = []
            for item in response:
                _l.append(str(item).replace('(', '').replace(')', '').replace("'", "").replace(",", "").replace("[", "").replace("]", ""))

            return _l
        except ValueError:
            pass



