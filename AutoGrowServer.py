import time, json
import urllib.request as urllib2
import TerminalControl as TerminalControl
import threading
import mysql.connector
import os
import sys
from decimal import Decimal

tCntrl = TerminalControl.TerminalControl()
pauseDashboard = False

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

#  __                               ___            _             _ _
# / _\ ___ _ __  ___  ___  _ __    / __\___  _ __ | |_ _ __ ___ | | | ___ _ __
# \ \ / _ \ '_ \/ __|/ _ \| '__|  / /  / _ \| '_ \| __| '__/ _ \| | |/ _ \ '__|
# _\ \  __/ | | \__ \ (_) | |    / /__| (_) | | | | |_| | | (_) | | |  __/ |
# \__/\___|_| |_|___/\___/|_|    \____/\___/|_| |_|\__|_|  \___/|_|_|\___|_|
def regulateHumidity():
    if (Decimal(getHumidity()) <= 55):
        sql = "UPDATE Tents SET HumidifierStatus = %s WHERE ID = %s"
        vals = ("1", tents[0][0])
        mycursor.execute(sql, vals)
        mydb.commit()
    elif (Decimal(getHumidity()) >= 65):
        sql = "UPDATE Tents SET HumidifierStatus = %s WHERE ID = %s"
        vals = ("0", tents[0][0])
        mycursor.execute(sql, vals)
        mydb.commit()
    else:
        sql = "UPDATE Tents SET HumidifierStatus = %s WHERE ID = %s"
        vals = ("-1", tents[0][0])
        mycursor.execute(sql, vals)
        mydb.commit()

def soilMoistureOn():
    sql = "UPDATE Plants SET SMSensorStatus = %s WHERE ID = %s"
    vals = ("1", plants[0][0])
    mycursor.execute(sql, vals)
    mydb.commit()

def soilMoistureOff():
    sql = "UPDATE Plants SET SMSensorStatus = %s WHERE ID = %s"
    vals = ("0", plants[0][0])
    mycursor.execute(sql, vals)
    mydb.commit()

def waterOn():
    sql = "UPDATE Tents SET WaterStatus = %s WHERE ID = %s"
    vals = ("1", tents[0][0])
    mycursor.execute(sql, vals)
    mydb.commit()

def waterOff():
    sql = "UPDATE Tents SET WaterStatus = %s WHERE ID = %s"
    vals = ("0", tents[0][0])
    mycursor.execute(sql, vals)
    mydb.commit()

def setLastUpdated(hour, minute, sec, year, month, day):
    sql = "UPDATE Tents SET LastUpdated = %s WHERE ID = %s"
    date = str(year) + '/' + str(month) + '/' + str(day) + ' ' + str(hour) + ':' + str(minute) + ':' + str(sec)
    vals = (date, tents[0][0])
    mycursor.execute(sql, vals)
    mydb.commit()

#     ___            _             _ _
#   / __\___  _ __ | |_ _ __ ___ | | | ___ _ __
#  / /  / _ \| '_ \| __| '__/ _ \| | |/ _ \ '__|
# / /__| (_) | | | | |_| | | (_) | | |  __/ |
# \____/\___/|_| |_|\__|_|  \___/|_|_|\___|_|

def logData(hour, minute, sec, year, month, day):
    fileName = str(year) + '-' + str(month) + '-' + str(day) + '_' + str(hour) + ':' + str(minute) + '.txt'

    with open(fileName, 'w') as f:
        f.write(str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(hour) + ':' + str(minute) + '\n'
            + 'Humidity: ' + str(getHumidity())
            + '\n smLeft: ' + str(getSml())
            + '\n smRight: ' + str(getSmr()))
        f.close

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

def runShell():
    while True:
        val = input(">")
        pauseDashboard == True
        print("Type help for a list of commands.")
        
def runDashboard():   
    while pauseDashboard == False:
        # Gets current date and time
        year = str(time.localtime().tm_year)
        month = str(time.localtime().tm_mon)
        day = str(time.localtime().tm_mday)
        hour = time.localtime().tm_hour
        minute = time.localtime().tm_min
        sec = time.localtime().tm_sec

        # Gets latest data from DB
        mycursor.execute("SELECT * FROM Tents")
        tents = mycursor.fetchall()
        mycursor.execute("SELECT * FROM Plants")
        plants = mycursor.fetchall()

        # Sets python variables to the new data
        temperature = getTemperature()
        humidity = getHumidity()
        soilMoistureLeft = getSml()
        soilMoistureRight = getSmr()
        humidifierStatus = getHumidStatus()
        waterPumpStatus = getWaterPumpStatus()
        soilMoistureStatus = getSMsensorStatus()

        
        # if (smComplete == False and hour%2==0):
        #     soilMoistureOn()
        #     soilMoistureStatus = getSMsensorStatus()
        #     soilMoistureOff()
        #     smComplete = True
        # elif (smComplete == True and hour%2!=0):
        #     smComplete = False

        # if (sec%30 == 0):
        #     temperature = getTemperature()
        #     humidity = getHumidity()
        #     soilMoistureLeft = getSml()
        #     soilMoistureRight = getSmr()
        #     humidifierStatus = getHumidStatus()
        #     waterPumpStatus = getWaterPumpStatus()
        #     regulateHumidity(humidity, temperature)

        regulateHumidity()

        if (hour < 10):
            temp = hour
            hour = str(0) + str(temp)

        if (minute < 10):
            temp = minute
            minute = str(0) + str(temp)
        if (sec < 10):
            temp = sec
            sec = str(0) + str(temp)

        if (int(minute)%20 == 0):
            logData(hour, minute, sec, year, month, day)
        
        printResults(hour, minute, sec, year, month, day)

        time.sleep(1)

def printResults(hour, minute, sec, year, month, day):

    print("\033[H\033[J")
    tCntrl.printLogo
    print("\n\t\t\t\t===============================")
    print("\t\t\t\t==|   Time   | |    Date    |==")
    print("\t\t\t\t===============================")

    print("\t\t\t\t==| " + str(hour) + ":" + str(minute) + ":" + str(sec) +
            " | | " + year + "/" + month + "/" + day + "  |== ")

    print("\t\t\t\t===============================\n")

    print("\n\t\t\t\t ==============================")
    print("\t\t\t\t ==|  Database Status", end=" ")
    if (mydb.is_connected() == True):
        print("(On)  |==")
    else:
        print("(Off) |==")
    print("\t\t\t\t ==============================")

    print("\n\t=====================================================================================")
    print("\t= |   Tent   | |    Temp    | |   Humid   | | Soil Moisture L | | Soil Moisture R | =")
    print("\t====================================================================================")
    print("\t= |    1     | |     " + getTemperature() + "     | |    " + getHumidity() + "     | |       " + getSml() + "       | |       " + getSmr() + "       | =")
    print("\t=====================================================================================\n")
    
    #Checks status code and outputs translated status
    print("Soil Moisture Sensors [" + '\x1b[6;30;42m', end ="")
    if (getSMsensorStatus() == '1'):
        print('ON\x1b[0m' + "]")
    elif (getSMsensorStatus() == '0'):
        print('OFF\x1b[0m' + "]")
    else:
        print('SENSOR FAIL\x1b[0m' + "]")

    print("Humidifier [" + '\x1b[6;30;42m', end ="")
    if (getHumidStatus() == '1'):
        print('ON\x1b[0m' + "]")
    elif (getHumidStatus() == '0'):
        print('OFF\x1b[0m' + "]")
    else:
        print('SENSOR FAIL\x1b[0m' + "]")

    print("Water Pump and Valve [" + '\x1b[6;30;42m', end ="")
    if (getWaterPumpStatus() == '1'):
        print('ON\x1b[0m' + "]")
    elif (getWaterPumpStatus() == '0'):
        print('OFF\x1b[0m' + "]")
    else:
        print('SENSOR FAIL\x1b[0m' + "]")

    print("Light Status [" + '\x1b[6;30;42m', end ="")
    if (getLightStatus() == '1'):
        print('ON\x1b[0m' + "]")
    elif (getLightStatus() == '0'):
        print('OFF\x1b[0m' + "]")
    else:
        print('SENSOR FAIL\x1b[0m' + "]")

#     ___      _
#    /   \_ __(_)_   _____ _ __
#   / /\ / '__| \ \ / / _ \ '__|
#  / /_//| |  | |\ V /  __/ |
# /___,' |_|  |_| \_/ \___|_|

def main():
    dashboard = threading.Thread(target=runDashboard, args=())
    dashboard.start()

    x = threading.Thread(target=runShell, args=())
    x.start()

if __name__=="__main__":
    main()