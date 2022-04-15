# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import functools
import subprocess
import re


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def status_check(statusList):
    elevator_log = {}
    ans = 0
    for item in statusList:
        if(str(item["elevatorId"]) in elevator_log.keys()):
            elevator_log[item["elevatorId"]].append(item)
        else:
            elevator_log[str(item["elevatorId"])] = []
            elevator_log[str(item["elevatorId"])].append(item)

    for i in elevator_log.keys():
        ans = checkStatus(elevator_log[i])
    if(ans == 1):
        print("status check done")
    else:
        print("status WA")
    return

def checkStatus(list):

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
            if(nowStatusTime-lastStatusTime <= 0.4 - 0.00001):
                print("Toooo fast, last time: " + str(lastStatusTime))
                print("last log:")
                print(lastLog)
                print("now Log")
                print(list[i])
                return 0

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
    else:
        print("SOMEONE LEFT")
        print(stack)
    return in_tot


def cmp_dic(dic1, dic2):
    return ((int)(dic1["usrId"]) - (int)(dic2["usrId"]))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # stdinFile = input("input: ")
    # outFile = input("out: ")
    stdinFile = "stdin.txt"
    outFile = "out.out"
    stdin = open(stdinFile, "r")
    out = open(outFile,"r")
    linesIn = stdin.readlines()
    linesOut = out.readlines()
    print("read out OK")
    sizeIn = len(linesIn)
    sizeOut = len(linesOut)
    usr_list = {}
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
    totalIn = inoutCheck(log_list, usr_list)

    if (totalIn != len(usr_list)):
        print("someone left outside!!")
    else:
        print("All passengers went to the right floor, wuhoooooooooo!")
    status_check(status_list)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
