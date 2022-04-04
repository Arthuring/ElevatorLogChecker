# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import subprocess
import re

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def check_inout(list, usr_list, max_size):

    stack = []
    in_tot = 0
    out_tot = 0
    # print(list)
    for item in list:
        if item["type"] == "IN" or item["type"] == "OUT":
            if item["type"] == "IN":
                stack.append(item["usrId"])
                if usr_list[item["usrId"]-1]["fromf"] == item["floor"] :
                    pass
                else:
                    print("misMatch fromf:")
                    print(item)
                    return
                in_tot = in_tot + 1
                if len(stack) > max_size:
                    print("too much in Elevator:")
                    print(item)
                    return
            try:
                if item["type"] == "OUT":
                    if usr_list[item["usrId"]-1]["tof"] == item["floor"]:
                        pass
                    else:
                        print("misMatch tof:")
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
        print("IN/OUT CHECK OK")
    else:
        print("SOMEONE LEFT")
        print(stack)
    return in_tot


def timeChecer(last_time):
    command = r".\datacheck1.exe"
    sb = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    str = sb.stdout.read().decode("utf-8")
    bb = re.match(r'Your input is valid,base time is (.*),max time is (.*)', str, re.M | re.I)
    base = float(bb.group(1))
    max = float(bb.group(2))
    if last_time < base * 0.9:
        print("excellent time:{}/{}".format(last_time, base))
    elif last_time < base:
        print("acceptable time:{}/{}".format(last_time, base))
    else:
        print("time:{}/{}".format(last_time, base))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    stdin = open("stdin.txt", "r")
    out = open("out.txt", "r")
    linesIn = stdin.readlines()
    linesOut = out.readlines()
    sizeIn = len(linesIn)
    sizeOut = len(linesOut)
    usr_list = []
    for item in linesIn:
        m = re.match(r'\[(.*)\](.*)-FROM-(.*)-(.*)-TO-(.*)-(.*)')





# See PyCharm help at https://www.jetbrains.com/help/pycharm/
