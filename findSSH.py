import socket
import threading
import sys

class bruteThread (threading.Thread):
    def __init__(self, threadId, numThreads):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.numThreads = numThreads
    def run(self):
        findSSH(self.threadId, self.numThreads)

def iterIPs(start, end):
    resultList = []
    print (start, end)
    class0 = list(map(int, start.split(".")))
    class1 = list(map(int, end.split(".")))
    for classA in range(class0[0], class1[0] + 1, 1):
        for classB in range(class0[1], class1[1] + 1, 1):
            for classC in range(class0[2], class1[2] + 1, 1):
                for classD in range(class0[3], class1[3] + 1, 1):
                    resultList.append(str(classA) + "." + str(classB) + "." + str(classC) + "." + str(classD))
    return resultList


def findSSH(threadId, numThreads):
    rangeIPs = []
    with open(sys.argv[2]) as f:
        for line in f:
            rangeIPs.append([line.split(",")[0], line.split(",")[1]])

    closedPorts = open("closed-" + str(threadId), "w")
    openPorts = open("open-" + str(threadId), "w")
    for i in range(len(rangeIPs)):
        start = rangeIPs[i][0]
        end = rangeIPs[i][1]
        listIPs = iterIPs(start, end.strip())
        for j in range(threadId, len(listIPs), numThreads):
            ip = listIPs[j]
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((ip, 22))

            if result == 0:
                print("port open: " + ip)
                openPorts.write(ip + "\n")
                openPorts.flush()
            else:
                closedPorts.write(ip + "\n")
                closedPorts.flush()
    closedPorts.close()
    openPorts.close()


def main(numThreads):
    threadList = []
    for i in range(numThreads):
        threadList.append(bruteThread(i, numThreads))
        threadList[i].start()

    for t in threadList:
        t.join()
if len(sys.argv) == 3:
    main(int(sys.argv[1]))
else:
    print("Usage: python3 findSSH.py NUM_THREADS COUNTRY")