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

#-------------------------------------------------------------------------------
# logData()
# takes data from array and writes it to the given path of a csv file
#
# :param log_path: a string denoting the path of a CSV file in which we wish to
#                  write log info to
# :param elements: array of elements that will coordinate to rows in csv
#-------------------------------------------------------------------------------
def logData(log_path, elements):
    try:
        with open(log_path, 'a+', newline='') as fileObj:
            csvWriter = writer(fileObj)
            csvWriter.writerow(elements)
    except Exception as a:
        print("ERROR: There was an error attempting to write to log " + log_path)
        print("Exception: ")
        print(a)

#-------------------------------------------------------------------------------
# aggregateFileData()
# Aggregates all log data regarding file mods, creation, and deletion
#
# :param activity_arg: A string denoting whether were deleting, modding,
#                      or creating a file
# :param filePath: A string denoting the path of the file we are acting on
#-------------------------------------------------------------------------------
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

#-------------------------------------------------------------------------------
# startProcess()
# starts the given process with specified commandline args
#
# :param command: A string denoting the command in which we would like to run
#-------------------------------------------------------------------------------
def startProcess(command):
    print("Starting Process: " + str(command))
    commandArr = command.split(" ")
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

#-------------------------------------------------------------------------------
# createFile()
# Creates a file at a specified path
#
# :param filePath: A string denoting the path in which the file will be created
# :return None: Only return if an error is thrown
#-------------------------------------------------------------------------------
def createFile(filePath):

    ### Checks if file exists
    if os.path.exists(filePath):
        print("ERROR: This file already exists")
        print("Cancelling file creation...")
        return None

    ### Error handles any other problems
    try:
        f=open(filePath, "a+")
    except Exception as a:
        print("ERROR: There was an error attempting to modify the file at " + filePath)
        print("Cancelling file modification...")
        print("Exception: ")
        print(a)
        return None
    print("File has been created at " + filePath)

    ### Aggregate logging info
    aggregrateFileData("create", filePath)

    print("Data from the process has been logged at <telegen.py_directory>/logs/file_log.csv")

#-------------------------------------------------------------------------------
# modifyFile()
# Modifies file at a specified path
#
# :param filePath: A string denoting the path in which the file will be created
# :return None: Only return if an error is thrown
#-------------------------------------------------------------------------------
def modifyFile(filePath):

    ### Checks if file doesn't exist
    if not os.path.exists(filePath):
        print("ERROR: This file doesn't exist exists")
        print("Cancelling file modification...")
        return None

    ### Error handles any other problems
    try:
        f=open(filePath, "a+")
    except Exception as a:
        print("ERROR: There was an error attempting to modify the file at " + filePath)
        print("Cancelling file modification...")
        print("Exception: ")
        print(a)
        return None

    f.write("THIS IS A FILE MODIFICATION")
    print("File has been modified at " + filePath)

    ### Aggregate logging info
    aggregrateFileData("modify", filePath)

    print("Data from the process has been logged at <telegen.py_directory>/logs/file_log.csv")

#-------------------------------------------------------------------------------
# deleteFile()
# Deletes a file at the specified path
#
# :param filePath: A string denoting the path in which the file will be created
# :return None: Only return if an error is thrown
#-------------------------------------------------------------------------------
def deleteFile(filePath):
    try:
        os.remove(filePath)
    except Exception as a:
        print("ERROR: There was an error trying to remove the file at " + filePath)
        print("Cancelling file deletion...")
        print("Exception: ")
        print(a)
        return None

    print("File has been removed at " + filePath)

    ### Aggregate logging info
    aggregrateFileData("delete", filePath)

    print("Data from the process has been logged at <telegen.py_directory>/logs/file_log.csv")

#-------------------------------------------------------------------------------
# establishConnection()
# Establishes a connection to google.com and transmits data
#
# :return None: Only return if an error is thrown
#-------------------------------------------------------------------------------
def establishConnection():

    print("Establish a connection at google.com:80")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('google.com', 80))
        request = b'GET google.com HTTP/1.1\n\n'
        s.send(request)

        print("Request has been sent")
    except Exception as a:
        print("ERROR: there was an error while connecting")
        print("Cancelling connection...")
        print("Exception: ")
        print(a)
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

    ### Change to file directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    print(os.getcwd())
    ### argparse is used to create command line arguments for the framework
    parser = argparse.ArgumentParser(description='Red Canary Telemetry Generation')

    parser.add_argument('--startprocess', metavar='\"<process>\"', type=str,
                        help="start a process/shell command", required=False)

    parser.add_argument('--createfile', metavar='<file_path>', type=str,
                        help="create a file at the specified location", required=False)

    parser.add_argument('--modfile', metavar='<file_path>', type=str,
                        help="modify a file at the specified location", required=False)

    parser.add_argument('--deletefile', metavar='<file_path>', type=str,
                        help="delete a file at the specified location", required=False)

    parser.add_argument('--startconnection',
                        help="start a connection with google.com and transmit data",
                        required=False, action='store_true')

    args = parser.parse_args()

    ### Would prefer to use a switch statement here.. but python doesn't support that ###
    if args.startprocess:
        startProcess(args.startprocess)
    if args.createfile:
        createFile(args.createfile)
    if args.modfile:
        modifyFile(args.modfile)
    if args.deletefile:
        deleteFile(args.deletefile)
    if args.startconnection:
        establishConnection()
    if not (args.startprocess or args.createfile or args.modfile or args.deletefile or args.startconnection):
        print(args)
