# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from cmath import inf
import functools
import subprocess
import re
import os
from tkinter import E


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def status_check(statusList, elevator_list):
    print("////////////////////////////////////////////////////////////////////////")
    elevator_log = {}
    ans = 0
    for item in statusList:
        if(str(item["elevatorId"]) in elevator_log.keys()):
            elevator_log[item["elevatorId"]].append(item)
        else:
            elevator_log[str(item["elevatorId"])] = []
            elevator_log[str(item["elevatorId"])].append(item)

    for i in elevator_log.keys():
        ans = checkStatus(elevator_log[i], elevator_list)
        if(ans == 1):
            print("status check done")
            print("-------------------------------------------------------------")
        else:
            print("status WA")
            print("-------------------------------------------------------------")
            return 0
    print("ALL STATUS TEST END")
    print("////////////////////////////////////////////////////////////////////////")
    return 1

def couldOpenHere(building, switch):
    return ((switch >> (ord(building) - ord('A'))) & 1) == 1

def checkStatus(list, elevatorList):
    openTime = 0
    closeTime = 0
    this_id = list[0]["elevatorId"]
    print("-------------------------------------------------------------")
    print( "elevatorId--" + this_id + "; Type--" + elevatorList[int(this_id)]["type"])
    # print(list)
    pos_building = elevatorList[int(this_id)]["origin_building"]
    pos_floor = elevatorList[int(this_id)]["origin_floor"]

    if(len(list)==0):
        return
    cnt = 0
    lastLog = []
    nowLog = list[0]
    lastStatus = ""
    nowStatus = list[cnt]["type"]
    nowStatusTime = float( list[cnt]["Time"])
    if (nowStatus == "OPEN"):
        openTime += 1
    elif (nowStatus == "CLOSE"):
        closeTime += 1
        print("Why close at first???")
        return 0

    lenlist = len(list)

    if (nowStatus == "OPEN" and not couldOpenHere(list[cnt]["building"], elevatorList[int(list[cnt]["elevatorId"])]["switch"])):
        print("Could not open at building " + list[cnt]["building"])
        return 0
    if (nowStatus == "ARRIVE"):
        if (abs(ord(list[cnt]["building"]) - ord(pos_building)) + abs(list[cnt]["floor"] - pos_floor) != 1 and \
            (list[cnt]["building"] != "A" or pos_building != "E" or  list[cnt]["floor"] != pos_floor) and \
                (list[cnt]["building"] != "E" or pos_building != "A" or list[cnt]["floor"] != pos_floor) \
            ) or \
            not list[cnt]["building"] in ['A', 'B', 'C', 'D', 'E'] or \
            list[cnt]["floor"] > 10 or list[cnt]["floor"] < 1:
            print("Can not arrive from " + pos_building + str(pos_floor) + " to " + list[cnt]["building"] + str(list[cnt]["floor"]))
            return 0
        pos_building = list[cnt]["building"]
        pos_floor = list[cnt]["floor"]

    cnt = cnt + 1
    state ={
     "ARRIVE": {"ARRIVE": 1, "IN": 0, "OUT": 0, "OPEN": 0, "CLOSE": 1},
     "IN":     {"ARRIVE": 0, "IN": 1, "OUT": 1, "OPEN": 1, "CLOSE": 0},
     "OUT":    {"ARRIVE": 0, "IN": 1, "OUT": 1, "OPEN": 1, "CLOSE": 0},
     "OPEN":   {"ARRIVE": 1, "IN": 0, "OUT": 0, "OPEN": 0, "CLOSE": 1},
     "CLOSE":  {"ARRIVE": 0, "IN": 1, "OUT": 1, "OPEN": 1, "CLOSE": 0}}
    for i in range(cnt, lenlist):
        lastStatus = nowStatus
        nowStatus = list[i]["type"]
        lastLog = nowLog
        nowLog = list[i]
        if(nowStatus == "OPEN"):
            openTime += 1
        if(nowStatus == "CLOSE"):
            closeTime +=1
        if(state[nowStatus][lastStatus] != 1):
            print("Elevator Statue wrong in elevator " + list[0]["elevatorId"])
            print("lastStatus:" + lastStatus + " nowStatus:" + nowStatus)
            return 0
        if (nowStatus == "OPEN" and not couldOpenHere(list[i]["building"], elevatorList[int(list[i]["elevatorId"])]["switch"])):
            print("Could not open at building " + list[i]["building"])
            return 0
        if (nowStatus == "ARRIVE" or \
            (nowStatus == "OPEN" and lastStatus == "CLOSE")):
            lastStatusTime = nowStatusTime
            nowStatusTime = float( list[i]["Time"])
            if (nowStatus == "ARRIVE"):
                limitTime = elevatorList[int(list[i]["elevatorId"])]["speed"]
            else:
                limitTime = 0.4
            if(nowStatusTime-lastStatusTime <= limitTime - 0.00001):
                print("Toooo fast, last time: " + str(lastStatusTime))
                print("last log:")
                print(lastLog)
                print("now Log")
                print(list[i])
                return 0
        if (nowStatus == "ARRIVE"):
            if (abs(ord(list[i]["building"]) - ord(pos_building)) + abs(list[i]["floor"] - pos_floor) != 1 and \
                (list[i]["building"] != "A" or pos_building != "E" or  list[i]["floor"] != pos_floor) and \
                    (list[i]["building"] != "E" or pos_building != "A" or list[i]["floor"] != pos_floor) \
                ) or \
                not list[i]["building"] in ['A', 'B', 'C', 'D', 'E'] or \
                list[i]["floor"] > 10 or list[i]["floor"] < 1:
                print("Can not arrive from " + pos_building + str(pos_floor) + " to " + list[i]["building"] + str(list[i]["floor"]))
                return 0
            pos_building = list[i]["building"]
            pos_floor = list[i]["floor"]
        else:
            if list[i]["building"] != pos_building or list[i]["floor"] != pos_floor:
                print("Position Error")
                return 0

    if(openTime != closeTime):
        print("openNum--"+ str(openTime) + " | closeNum--" + str(closeTime))
        print("NEED MORE OPEN OR CLOSE")

        return 0
    else:
        print("openNum--" + str(openTime) + " | closeNum--" + str(closeTime))

    return 1

def inoutCheck(log_list, usr_list,elevator_list):
    elevator_log = {}
    ans = -1
    if(len(usr_list) == 0):
        ans = 1
        print("---------This test point contain no passenger---------")
    for item in log_list:
        if (str(item["elevatorId"]) in elevator_log.keys()):
            elevator_log[item["elevatorId"]].append(item)
        else:
            elevator_log[str(item["elevatorId"])] = []
            elevator_log[str(item["elevatorId"])].append(item)
    # print("\n\n\n")
    # print(elevator_log.keys())
    # print("\n\n\n")
    for i in elevator_log.keys():
        ans = check_inout(elevator_log[i], usr_list, elevator_list[int(i)]["cap"])
        # ans = check_inout(elevator_log[i], usr_list, 6)
    for id,item in usr_list.items():
        if item["setOut"] == 1 and item["arrived"] == 1:
            pass
        else:
            print(item)
            if item["setOut"] == 0:
                print("passenger--" + str(item["usrId"]) + "--not setOut")
            if item["arrived"] == 0:
                print("passenger--" + str(item["usrId"]) + "--not arrive")
            return 0
    if ans != 1:
        return 0
    print("All passengers went to the right floor, wuhoooooooooo!")
    return 1

def check_inout(list, usr_list, max_size):
    capacity_error = False
    stack = []
    in_tot = 0
    out_tot = 0
    elevatorId = list[0]["elevatorId"]
    # print(list)
    for item in list:
        if item["type"] == "IN" or item["type"] == "OUT":
            if item["type"] == "IN":
                stack.append(item["usrId"])
                if  usr_list[item["usrId"]]["fromf"] == item["floor"] and usr_list[item["usrId"]]["fromb"] == item["building"]:
                    usr_list[item["usrId"]]["setOut"] = 1
                in_tot = in_tot + 1
                if len(stack) > max_size:
                    print("too much in Elevator:")
                    print(item)
                    capacity_error = True
            try:
                if item["type"] == "OUT":
                    if usr_list[item["usrId"]]["tof"] == item["floor"] and usr_list[item["usrId"]]["tob"] == item["building"]:
                        usr_list[item["usrId"]]["arrived"] = 1
                    out_tot = out_tot + 1
                    stack.remove(item["usrId"])
            except:
                print("too few in Elevator, fatal error!!!")
                print(item)
                return 0
            # print(item)
    

    if not capacity_error and len(stack) == 0:
        print("IN/OUT CHECK OK" + " in elevator " + str(elevatorId))
        return 1
    else:
        print("SOMEONE LEFT or CAPACITY ERROR")
        print(stack)
        return 0


def cmp_dic(dic1, dic2):
    return ((int)(dic1["usrId"]) - (int)(dic2["usrId"]))


def Check(stdinFileCheck, outFileCheck):
    print("////////////////////////////////////////////////////////////////////////")
# Press the green button in the gutter to run the script.
    # stdinFileCheck = input("input: ")
    # outFileCheck = input("out: ")
    stdin = open(str(stdinFileCheck), "r")
    out = open(str(outFileCheck),"r")
    linesIn = stdin.readlines()
    linesOut = out.readlines()
    print("read out OK")
    sizeIn = len(linesIn)
    sizeOut = len(linesOut)
    usr_list = {}
    elevator_list = {}
    for i in range(1, 6):
        elevator_list[i] = {
            "id": str(i),
            "type": "building",
            "speed": 0.6,
            "cap": 8,
            "switch": -1,
            "origin_building": str(chr(ord('A') + i - 1)),
            "origin_floor": 1
        }
    elevator_list[6] = {
        "id": "6",
        "type": "floor",
        "speed": 0.6,
        "cap": 8,
        "switch": 0x1f,
        "origin_building": "A",
        "origin_floor": 1
    }

    log_list = []
    status_list = []

    for item in linesIn:
        m = re.match(r'\[(.*)](.*)-FROM-(.*)-(.*)-TO-(.*)-(.*)',item,re.M|re.I)
        if(m != None):
            time = m.group(1)
            id = m.group(2)
            fromBuiding = m.group(3)
            fromFloor = m.group(4)
            toBuilding = m.group(5)
            toFloor = m.group(6)
            dic = {"Time": time, "usrId": id, "fromb": fromBuiding,
                   "fromf": int(fromFloor), "tob": toBuilding, "tof": (int)(toFloor),
                   "arrived": 0, "setOut":0}
            usr_list[str(id)] = dic
        m = re.match(r'\[(.*)]ADD-building-(.*)-(.*)-(.*)-(.*)',item,re.M|re.I)
        if(m != None):
            elevator_id = m.group(2)
            elevator_cap = m.group(4)
            elevator_speed = m.group(5)
            elevator_list[int(elevator_id)] = {
                "id": elevator_id,
                "type": "building",
                "speed": float(elevator_speed),
                "cap": int(elevator_cap),
                "switch": -1,
                "origin_building": m.group(3),
                "origin_floor": int(1)
            }
        m = re.match(r'\[(.*)]ADD-floor-(.*)-(.*)-(.*)-(.*)-(.*)', item, re.M | re.I)
        if(m != None):
            elevator_id = m.group(2)
            elevator_cap = m.group(4)
            elevator_speed = m.group(5)
            elevator_switch = m.group(6)
            elevator_list[int(elevator_id)] = {
                "id": elevator_id,
                "type": "floor",
                "speed": float(elevator_speed),
                "cap": int(elevator_cap),
                "switch": int(elevator_switch),
                "origin_building": "A",
                "origin_floor": int(m.group(3))
            }

    for item in linesOut:
        m = re.match(r'\[(.*)](.*)-(.*)-(.*)-(.*)-(.*)', item, re.M | re.I)
        if( m != None):
            time2 = m.group(1)
            type = m.group(2)
            id = m.group(3)
            building = m.group(4)
            floor = int(m.group(5))
            elevatorId = m.group(6)

            dic = {"Time": time2, "type": type,"usrId":id, "building": building,
                   "floor": int(floor), "elevatorId": elevatorId}
            log_list.append(dic)
            status_list.append(dic)
        else:
            m = re.match(r'\[(.*)](.*)-(.*)-(.*)-(.*)', item, re.M | re.I)
            if (m != None):
                time2 = m.group(1)
                type = m.group(2)
                building = m.group(3)
                floor = int(m.group(4))
                elevatorId = m.group(5)

                dic = {"Time": time2, "type": type, "building": building,
                       "floor": int(floor), "elevatorId": elevatorId}
                status_list.append(dic)

    if(len(log_list)>0):
        print("Total time |" + str(log_list[len(log_list) - 1]["Time"]))

    totalIn = inoutCheck(log_list, usr_list,elevator_list)

    if (totalIn != 1):
        print("Some thing wrong with passenger!")
        return 0
    # print("status_list = ")
    # print(status_list)

    # print("\n\nelevator_list = ")
    # print(elevator_list)
    tmp = status_check(status_list, elevator_list)
    return tmp 

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

def GetProgressBar(count = 0, totalCount = 1, name = ""):
    bar = "|"
    plusCount = 50 * count // totalCount
    for _ in range(plusCount):
        bar = bar + ">"
    for _ in range(50 - plusCount):
        bar = bar + "-"
    bar = bar + "|" + str(round(100 * count / totalCount, 2)).rjust(10) + "%" + name.rjust(50)
    return bar

dataDir = "..\\data\\"


if __name__ == '__main__':
    totalDataCount = 0
    for dataDirRoot, dataDirDirs, dataDirFiles in os.walk(dataDir):
        for fileName in dataDirFiles:
            if (fileName == "stdin.txt"):
                totalDataCount = totalDataCount + 1

    print("total test data count: " + str(totalDataCount))

    print(GetProgressBar(name = "testing ..."))
    correctCount = 0
    count = 0
    for dataDirRoot, dataDirDirs, dataDirFiles in os.walk(dataDir):
        for fileName in dataDirFiles:
            if (fileName == "stdin.txt"):
                inFile = os.path.join(dataDirRoot, fileName)
                outFile = os.path.join(dataDirRoot, "out.out")

                print(GetProgressBar(count, totalDataCount, inFile))

                if (not os.path.isfile(outFile)):
                    print("Generating...")
                    os.system("copy " + os.path.join(dataDirRoot, fileName) + " .\\stdin.txt")
                    os.system("datainput_student_win64.exe | java -jar HomeWork.jar > " + os.path.join(dataDirRoot, "out.out"))

                count = count + 1

                if (Check(inFile, outFile) == 1):
                    correctCount = correctCount + 1
                else:
                    print("Wrong Answer in " + os.path.join(dataDirRoot, fileName))

    print(GetProgressBar(totalDataCount, totalDataCount, "Done."))

    if count == correctCount:
        print("All Accepted.")
    else:
        print("Wrong behavior.")