### telegen.py
### 9/21/2021
### Created by: Noah Hansen

import argparse
import os
import datetime
import sys
import getpass
import socket

from csv import writer
from subprocess import Popen, PIPE

### logData ###
### Method for writing data to our specified log ###
def logData(log_path, elements):
    with open(log_path, 'a+', newline='') as fileObj:
        csvWriter = writer(fileObj)
        csvWriter.writerow(elements)

### aggregrateFileData ###
### Method for aggregating all log data regarding file mods, creation, and deletion ###
def aggregrateFileData(activity_arg, filePath):
    dateTime = datetime.datetime.now()
    path = os.path.abspath(filePath)
    activity = activity_arg

    user = getpass.getuser()

    processName = "telegen.py"

    commandLine = "python "
    tmpString = " ".join(sys.argv)

    commandLine = commandLine + tmpString

    pid = os.getpid()

    elements = [dateTime, path, activity, user, processName, commandLine, pid]
    logData("./logs/file_log.csv", elements)


### startProcess ###
### Method for starting the given process with specified commandline args ###
def startProcess(command):
    print("Starting Process: " + str(command))
    commandArr = command.split(" ")
    #process = os.system(command)
    #print(sys.platform)
    process = Popen(commandArr, stdout=PIPE, stdin=PIPE, shell=True)

    ### this has to be done so the command doesn't throw a write error
    output = process.stdout.read()

    ### Aggregate logging info
    user = getpass.getuser()
    dateTime = datetime.datetime.now()
    pid = os.getpid()

    processName = "telegen.py"


    commandLine = "python "
    tmpString = " ".join(sys.argv)

    commandLine = commandLine + tmpString

    elements = [dateTime, user, processName, commandLine, pid]
    logData("./logs/process_log.csv", elements)

    print("Data from the process has been logged at <telegen.py_directory>/logs/process_log.csv")

### createFile ###
### method for creating a file at the specified path ###
def createFile(filePath):
    if os.path.exists(filePath):
        print("ERROR: This file already exists")
        print("Cancelling file creation...")
        return None

    f=open(filePath, "w+")
    print("File has been created at " + filePath)

    ### Aggregate logging info
    aggregrateFileData("create", filePath)

    print("Data from the process has been logged at <telegen.py_directory>/logs/file_log.csv")

### modifyFile ###
### method for modifying a file at the specified path ###
def modifyFile(filePath):

    if not os.path.exists(filePath):
        print("ERROR: This file doesn't exist exists")
        print("Cancelling file modification...")
        return None

    f=open(filePath, "a+")
    f.write("THIS IS A FILE MODIFICATION")
    print("File has been modified at " + filePath)

    ### Aggregate logging info
    aggregrateFileData("modify", filePath)

    print("Data from the process has been logged at <telegen.py_directory>/logs/file_log.csv")

### deleteFile ###
### method for deleting a file at the specified path ###
def deleteFile(filePath):
    try:
        os.remove(filePath)
    except Exception:
        print("ERROR: File does not exist at " + filePath)
        print("Cancelling file deletion...")
        return None

    print("File has been removed at " + filePath)

    ### Aggregate logging info
    aggregrateFileData("delete", filePath)

    print("Data from the process has been logged at <telegen.py_directory>/logs/file_log.csv")

### establishConnection ###
### method for establishing a connection and transmitting data ###
def establishConnection():

    print("Establish a connection at google.com:80")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('google.com', 80))
        request = b'GET google.com HTTP/1.1\n\n'
        s.send(request)

        print("Request has been sent")
    except Exception:
        print("ERROR: there was an error while connecting")
        print("Cancelling connection...")
        return None


    ### Aggregate logging info
    dateTime = datetime.datetime.now()
    user = getpass.getuser()
    destination = "google.com:80"
    source = str(socket.gethostbyname(socket.gethostname())) + ":" + str(s.getsockname()[1])

    ### No calc needed here since request is already a byte object
    dataSize = len(request)

    protocol = "HTTP"
    processName = "telegen.py"

    commandLine = "python "
    tmpString = " ".join(sys.argv)
    commandLine = commandLine + tmpString
    pid = os.getpid()
    elements = [dateTime, user, destination, source, dataSize, protocol, processName, commandLine, pid]
    logData("./logs/connection_log.csv", elements)

    print("Data from the connection has been logged at <telegen.py_directory>/logs/connection_log.csv")





if __name__ == "__main__":

    ###Change to file directory###
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    print(os.getcwd())
    ### argparse is used to create command line arguments for the framework
    parser = argparse.ArgumentParser(description='Red Canary Telemetry Generation')

    parser.add_argument('--startprocess', metavar='<process>', type=str,
                        help="start a process with a path to an executable file", required=False)

    parser.add_argument('--createfile', metavar='<file_path>', type=str,
                        help="create a file at the specified location", required=False)

    parser.add_argument('--modfile', metavar='<file_path>', type=str,
                        help="modify a file at the specified location", required=False)

    parser.add_argument('--deletefile', metavar='<file_path>', type=str,
                        help="delete a file at the specified location", required=False)

    parser.add_argument('--startconnection', help="delete a file at the specified location",
                        required=False, action='store_true')

    args = parser.parse_args()

    startprocess_arg = args.startprocess
    createfile_arg = args.createfile
    modfile_arg = args.modfile
    deletefile_arg = args.deletefile
    startconnection_arg = args.startconnection

    ### Would prefer to use a switch statement here.. but python doesn't support that ###
    if startprocess_arg:
        startProcess(startprocess_arg)
    if createfile_arg:
        createFile(createfile_arg)
    if modfile_arg:
        modifyFile(modfile_arg)
    if deletefile_arg:
        deleteFile(deletefile_arg)
    if startconnection_arg:
        establishConnection()
    if not (startprocess_arg or createfile_arg or modfile_arg or deletefile_arg or startconnection_arg):
        print(args)
