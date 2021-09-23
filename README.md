# EDR_Telemetry_Generation
This python script is designed to generate telemetry in which can be tracked by Red Canary's EDR tool.

How to use:
     python telegen.py <option1> <argument1> <option2> <argument2> ....

Command Line Options:
     -h, --help
          show this help message and exit
     --startprocess <process>
          start a process/shell command
     --createfile <file_path>
          create a file at the specified location
     --modfile <file_path>
          modify a file at the specified location
     --deletefile <file_path>
          delete a file at the specified location
     --startconnection     
          start a connection with google.com and transmit data
