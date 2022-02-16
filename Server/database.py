import mysql.connector

mydb = mysql.connector.connect(
  host="192.168.0.162",
  user="doev3",
  password="Wowc78wowc!!#",
  database="AutoGrow"
)
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM Tents")
tents = mycursor.fetchall()

mycursor.execute("SELECT * FROM Plants")
plants = mycursor.fetchall()

def getTemperature():
    return tents[0][1]

def getHumidity():
    return tents[0][2]

def getHumidStatus():
    return tents[0][4]

def getWaterPumpStatus():
    return tents[0][3]

def getSMsensorStatus():
    return tents[0][5]

def getSml():
    return plants[0][1]

def getSmr():
    return plants[1][1]

def getLightStatus():
    return tents[0][6]
