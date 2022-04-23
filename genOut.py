import re
import os
import subprocess
import time
import _thread

def gen(threadName, command):
    print(threadName)
    os.system(command)


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

                print(GetProgressBar(count, totalDataCount, inFile))

                if (not os.path.isfile(outFile)):
                    if (runningCount % 10 == 0 and runningCount != 0):
                        print("Testing reached 10, sleep 60 sec")
                        time.sleep(60)
                    print("Generating...")
                    testDir = ".\\test" + str(runningCount)
                    os.system("mkdir "+ testDir)
                    os.system("copy " + os.path.join(dataDirRoot, fileName) + " " + testDir + "\\stdin.txt")
                    os.system("copy " + ".\\datainput_student_win64.exe" + " " + testDir + "\\datainput_student_win64.exe")
                    os.system("copy " + ".\\HomeWork.jar" + " " + testDir + "\\HomeWork.jar")
                    #command = "datainput_student_win64.exe | java -jar HomeWork.jar > " + os.path.join(dataDirRoot, "out.out")
                    command = ".\\run.bat "+ testDir + " ..\\" + os.path.join(dataDirRoot, "out.out")
                    #os.system("datainput_student_win64.exe | java -jar HomeWork.jar > " + os.path.join(dataDirRoot, "out.out"))
                    p = subprocess.Popen(r".\run.bat "+testDir + " ..\\"+os.path.join(dataDirRoot, "out.out"), creationflags=subprocess.CREATE_NEW_CONSOLE )
                    runningCount = runningCount + 1
                    #runningCount = runningCount + 1
                    # try:
                    #     _thread.start_new_thread(gen,("Thread-"+str(runningCount),command))
                    #     runningCount = runningCount + 1
                    #
                    # except:
                    #     print("Error: 无法启动线程")

                count = count + 1

    if(runningCount != 0):
        print("All file have generated ")
        print("waiting running end, sleep 90")
        time.sleep(20)
    # for i in range (0,runningCount):
    #     testDir =  ".\\test" + str(i)
    #     ls = os.listdir(testDir)
    #     for j in ls:
    #         c_path = os.path.join(testDir, j)
    #         os.remove(c_path)
    #     os.rmdir(testDir)