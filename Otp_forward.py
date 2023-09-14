import os
import json
import datetime
import os.path
import time
interV = 15 
looper = False  
print(f"Welcome to SMS Forwarder v:1.1 by")
print('''

 ██████╗██╗     ██╗ ██████╗██╗  ██╗███████╗                           
██╔════╝██║     ██║██╔════╝██║ ██╔╝██╔════╝                           
██║     ██║     ██║██║     █████╔╝ ███████╗                           
██║     ██║     ██║██║     ██╔═██╗ ╚════██║                           
╚██████╗███████╗██║╚██████╗██║  ██╗███████║                           
 ╚═════╝╚══════╝╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝                           

             █████╗ ███╗   ██╗██████╗     ██████╗ ██╗████████╗███████╗
            ██╔══██╗████╗  ██║██╔══██╗    ██╔══██╗██║╚══██╔══╝██╔════╝
            ███████║██╔██╗ ██║██║  ██║    ██████╔╝██║   ██║   ███████╗
            ██╔══██║██║╚██╗██║██║  ██║    ██╔══██╗██║   ██║   ╚════██║
            ██║  ██║██║ ╚████║██████╔╝    ██████╔╝██║   ██║   ███████║
            ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝     ╚═════╝ ╚═╝   ╚═╝   ╚══════╝

''')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def smsforward(looping=False):
    global looper 
    lastSMS = datetime.datetime.now()
    tmpFile = "tmpLastTime.txt"
    cfgFile = "config.txt"
    if not os.path.exists(cfgFile):
        cfile = open(cfgFile, "a")
        filters = input(f"{bcolors.BOLD}Please enter keyword filter(s) separated by comma (',') : {bcolors.ENDC}")
        filter_s = filters.split(",")
        cfile.write(filters.lower())
        cfile.write("\n")
        print("")
        print("")
        mnumbers = input(f"{bcolors.BOLD}Please enter mobile number(s) separated by comma (',') : {bcolors.ENDC}")
        mnumber_s = mnumbers.split(",")
        cfile.write(mnumbers)
        cfile.close()
    else:
        rst = "1"
        if not looping:
            print(f"""{bcolors.BOLD}Old configuration file found! What do You want to do?{bcolors.ENDC}
                {bcolors.OKGREEN}1) Continue with old settings{bcolors.ENDC}
                {bcolors.WARNING}2) Remove old settings and start afresh{bcolors.ENDC}""")
            rst = input("Please enter your choice number: ")
        if rst == "1":
            print(f"{bcolors.OKGREEN}Starting with old settings...........{bcolors.ENDC}")
            cfile = open(cfgFile, "r")
            cdata = cfile.read().splitlines()
            filter_s = cdata[0].split(",")
            mnumber_s = cdata[1].split(",")
        elif rst == "2":
            print(f"{bcolors.WARNING}Removing old Configuration files..........{bcolors.ENDC}")
            os.remove(cfgFile)
            os.remove(tmpFile)
            print(f"{bcolors.WARNING}Old configuration files removed. Please enter new settings{bcolors.ENDC}")
            smsforward()
    if not os.path.exists(tmpFile):
        print("Last time not found. Setting it to current Date-Time")
        tfile = open(tmpFile, "w")
        tfile.write(str(lastSMS))
        tfile.close()
    else:
        tfile = open(tmpFile, "r")
        lastSMS = datetime.datetime.fromisoformat(tfile.read())
        tfile.close()
    if not looper:
        lop = input(f"Keep running after each {interV} second (y/n): ")
        if lop == "y":
            looper = True
            print("You can stop the script anytime by pressing Ctrl+C")
    print(f"Last SMS forwarded on {lastSMS}")
    jdata = os.popen("termux-sms-list -l 50").read()  
    jd = json.loads(jdata)
    print(f"Reading {len(jd)} latest SMSs")
    for j in jd:
        if datetime.datetime.fromisoformat(j['received']) > lastSMS: 
            for f in filter_s:
                if f in j['body'].lower() and j['type'] == "inbox": 
                    print(f"{f} found")
                    for m in mnumber_s:
                        print(f"Forwarding to {m}")
                        resp = os.popen(f"termux-sms-send -n {m} {j['body']}") 
                        tfile = open(tmpFile, "w")
                        tfile.write(j['received'])
                        tfile.close()
smsforward()
while looper:
    time.sleep(interV)
    smsforward(looping=True)
