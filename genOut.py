import re
import os
import subprocess
import time


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
totalDataCount = 0
if __name__ == '__main__':
    for dataDirRoot, dataDirDirs, dataDirFiles in os.walk(dataDir):
        for fileName in dataDirFiles:
            if (fileName == "stdin.txt"):
                totalDataCount = totalDataCount + 1

    print("total test data count: " + str(totalDataCount))

    print(GetProgressBar(name = "testing ..."))
    correctCount = 0
    count = 0
    runningCount = 0
    for dataDirRoot, dataDirDirs, dataDirFiles in os.walk(dataDir):
        for fileName in dataDirFiles:
            if (fileName == "stdin.txt"):
                inFile = os.path.join(dataDirRoot, fileName)
                outFile = os.path.join(dataDirRoot, "out.out")
                if(runningCount % 10 == 0 and runningCount != 0):
                    print("Testing reached 10, sleep 60 sec")
                    time.sleep(60)
                print(GetProgressBar(count, totalDataCount, inFile))

                if (not os.path.isfile(outFile)):
                    print("Generating...")
                    testDir = ".\\test" + str(runningCount)
                    os.system("mkdir "+ testDir)
                    os.system("copy " + os.path.join(dataDirRoot, fileName) + " "+testDir+"\\stdin.txt")
                    os.system("copy " + " .\\datainput_student_win64.exe" + " " + testDir + "\\datainput_student_win64.exe")
                    os.system("copy " + " .\\HomeWork.jar" + " " + testDir + "\\HomeWork.jar")
                    command = testDir+"\\datainput_student_win64.exe | java -jar "+testDir+"\\HomeWork.jar > " + os.path.join(dataDirRoot, "out.out")
                    #os.system("datainput_student_win64.exe | java -jar HomeWork.jar > " + os.path.join(dataDirRoot, "out.out"))
                    subprocess.Popen(command,shell=True)
                    runningCount = runningCount + 1
                count = count + 1

    if(runningCount != 0):
        print("All file have generated ")
        print("waiting running end, sleep 90")
        time.sleep(90)
    for i in range (0,runningCount):
        testDir =  ".\\test" + str(i)
        ls = os.listdir(testDir)
        for j in ls:
            c_path = os.path.join(testDir, j)
            os.remove(c_path)
        os.rmdir(testDir)