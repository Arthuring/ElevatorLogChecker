# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from cmath import inf
import functools
import subprocess
import re
import os


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def status_check(statusList, elevator_type_list):
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
        ans = checkStatus(elevator_log[i],elevator_type_list)
        if(ans == 1):
            print("status check done")
            print("-------------------------------------------------------------")
        else:
            print("status WA")
            print("-------------------------------------------------------------")
    print("ALL STATUS TEST END")
    print("////////////////////////////////////////////////////////////////////////")
    if (ans == 1):
        return 1
    return 0

def checkStatus(list, elevator_type_list):
    openTime = 0
    closeTime = 0
    speed = {"building": 0.4, "floor": 0.2}
    this_id = list[0]["elevatorId"]
    print("-------------------------------------------------------------")
    print( "elevatorId--" + this_id + "; Type--" + elevator_type_list[this_id])
    if(len(list)==0):
        return
    cnt = 0
    lastLog = []
    nowLog = list[0]
    lastStatus = ""
    nowStatus = list[cnt]["type"]
    nowStatusTime = float( list[cnt]["Time"])
    lenlist = len(list)
    cnt = cnt + 1
    state ={
     "ARRIVE": {"ARRIVE": 1, "IN": 0, "OUT": 0, "OPEN": 0, "CLOSE": 1},
     "IN":     {"ARRIVE": 0, "IN": 1, "OUT": 1, "OPEN": 1, "CLOSE": 0},
     "OUT":    {"ARRIVE": 0, "IN": 1, "OUT": 1, "OPEN": 1, "CLOSE": 0},
     "OPEN":   {"ARRIVE": 1, "IN": 0, "OUT": 0, "OPEN": 0, "CLOSE": 1},
     "CLOSE":  {"ARRIVE": 0, "IN": 1, "OUT": 1, "OPEN": 0, "CLOSE": 0}}
    for i in range(cnt, lenlist):
        lastStatus = nowStatus
        nowStatus = list[i]["type"]
        lastLog = nowLog
        nowLog = list[i]
        if(nowStatus == "OPEN"):
            openTime += 1
        if(nowStatus == "CLOSE"):
            closeTime +=1
        if(state[nowStatus][lastStatus] == 1):
            pass
        else:
            print("Elevator Statue wrong in elevator " + list[0]["elevatorId"])
            print("lastStatus:" + lastStatus + " nowStatus:" + nowStatus)
            return 0
        if (nowStatus == "ARRIVE" or \
            (nowStatus == "OPEN" and lastStatus == "CLOSE") or \
                (nowStatus == "CLOSE" and (lastStatus == "ARRIVE" or lastStatus == "OPEN"))):
        # if (nowStatusTime == "ARRIVE" or nowStatus == "OPEN" or nowStatus == "CLOSE"):
            lastStatusTime = nowStatusTime
            nowStatusTime = float( list[i]["Time"])
            if(nowStatusTime-lastStatusTime <= speed[elevator_type_list[this_id]] - 0.00001):
                print("Toooo fast, last time: " + str(lastStatusTime))
                print("last log:")
                print(lastLog)
                print("now Log")
                print(list[i])

                return 0
    if(openTime != closeTime):
        print("openNum--"+ str(openTime) + "; closeNum--" + str(closeTime))
        print("NEED MORE OPEN OR CLOSE")

        return 0
    else:
        print("openNum--" + str(openTime) + "; closeNum--" + str(closeTime))

    return 1

def inoutCheck(log_list, usr_list):
    elevator_log = {}
    ans = 0
    for item in log_list:
        if (str(item["elevatorId"]) in elevator_log.keys()):
            elevator_log[item["elevatorId"]].append(item)
        else:
            elevator_log[str(item["elevatorId"])] = []
            elevator_log[str(item["elevatorId"])].append(item)
    for i in elevator_log.keys():
        ans += check_inout(elevator_log[i],usr_list,6)
    return ans

def check_inout(list, usr_list, max_size):
    stack = []
    in_tot = 0
    out_tot = 0
    elevatorId = list[0]["elevatorId"]
    # print(list)
    for item in list:
        if item["type"] == "IN" or item["type"] == "OUT":
            if item["type"] == "IN":
                stack.append(item["usrId"])
                if  usr_list[item["usrId"]]["fromf"] == item["floor"]:
                    pass
                else:
                    print("misMatch fromfloor:")
                    print(item)
                    return
                if  usr_list[item["usrId"]]["fromb"] == item["building"]:
                    pass
                else:
                    print("misMatch fromBuilding:")
                    print(item)
                    return
                in_tot = in_tot + 1
                if len(stack) > max_size:
                    print("too much in Elevator:")
                    print(item)
                    return
            try:
                if item["type"] == "OUT":
                    if usr_list[item["usrId"]]["tof"] == item["floor"]:
                        pass
                    else:
                        print("misMatch tof:")
                        print(item)
                        return
                    if usr_list[item["usrId"]]["tob"] == item["building"]:
                        pass
                    else:
                        print("misMatch toBuiding:")
                        print(item)
                        return
                    out_tot = out_tot + 1
                    stack.remove(item["usrId"])
            except:
                print("too few in Elevator:")
                print(item)
                return
            # print(item)

    if len(stack) == 0:
        print("IN/OUT CHECK OK" + " in elevator " + str(elevatorId))
        return 1
    else:
        print("SOMEONE LEFT")
        print(stack)
        return 0


def cmp_dic(dic1, dic2):
    return ((int)(dic1["usrId"]) - (int)(dic2["usrId"]))


def Check(stdinFileCheck, outFileCheck):
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
    elevator_type_list = {"1":"building","2":"building","3":"building","4":"building","5":"building"}
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
                   "fromf": int(fromFloor), "tob": toBuilding, "tof": (int)(toFloor)}
            usr_list[str(id)] = dic
        m = re.match(r'\[(.*)]ADD-building-(.*)-(.*)',item,re.M|re.I)
        if(m != None):
            elevator_id = m.group(2)
            elevator_type_list[elevator_id] = "building"
        m = re.match(r'\[(.*)]ADD-floor-(.*)-(.*)', item, re.M | re.I)
        if(m != None):
            elevator_id = m.group(2)
            elevator_type_list[elevator_id] = "floor"

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

    #timeChecer((float)(log_list[len(log_list) - 1]["Time"]))

    totalIn = inoutCheck(log_list, usr_list)

    if (totalIn != len(usr_list)):
        print("someone left outside!!")
        return 0
    else:
        print("All passengers went to the right floor, wuhoooooooooo!")
    return status_check(status_list, elevator_type_list)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

def GetProgressBar(count = 0, totalCount = 1, name = ""):
    bar = "|"
    plusCount = 50 * count // totalCount
    for _ in range(plusCount):
        bar = bar + "#"
    for _ in range(50 - plusCount):
        bar = bar + "-"
    bar = bar + "|" + str(round(100 * count / totalCount, 2)).rjust(10) + "%" + name.rjust(50)
    return bar

dataDir = "..\\data\\" 


if __name__ == '__main__':
    totalDataCount = 0
    for dataDirRoot, dataDirDirs, dataDirFiles in os.walk(dataDir):
        for fileName in dataDirFiles:
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