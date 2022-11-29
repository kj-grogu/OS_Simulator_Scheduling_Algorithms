# OS_Simulator_Scheduling_Algorithms



#### Install PyCharm - 
https://www.jetbrains.com/pycharm/download/#section=windows
#### Open the project in Pycharm - 
(choose existing repo location or create an empty one and bring in the files)
#### Install required modules - 
This will be done by pycharm, goto the osm_1.py file, goto top where imports are defined, there would be an error on modules that require installation, click and install them. Untill there are no more reds. You can also try insstalling modules from terminal inside PyCharm
#### Running - 
Open Terminal in Pycharm, its at the bottom
#### Run command - 
### python3 .\osm_1.py (for windows) 




#### OSM in actions

### FCFS
![FCFS](https://github.com/kj-grogu/OS_Simulator_Scheduling_Algorithms/blob/main/io/osm_fcfs_00.gif)

### Priority
![Priority](https://github.com/kj-grogu/OS_Simulator_Scheduling_Algorithms/blob/main/io/osm_Priority_00.gif)


### RoundRobin
![RoundRobin](https://github.com/kj-grogu/OS_Simulator_Scheduling_Algorithms/blob/main/io/osm_rr_00.gif)


![Image00](https://github.com/kj-grogu/OS_Simulator_Scheduling_Algorithms/blob/main/io/image00.png)

![Image01](https://github.com/kj-grogu/OS_Simulator_Scheduling_Algorithms/blob/main/io/image01.png)


#### Main Files -
 **osm_1.py** (UI Component)
 **myos** package - Has different schedulers

 **myos\FirstComeFirstServe.py** - FirstComeFirstServe scheduler

 **myos\RoundRobin.py** - RoundRobin scheduler

 **myos\ShortestJobFirst.py** - ShortestJobFirst scheduler

 **myos\ShortestRemainingTimeFirst.py** - ShortestRemainingTimeFirst scheduler




<br/>
<br/>
<br/>
<br/>
Tools Used

PyQtDesigner - https://pythonbasics.org/qt-designer-python/

Generate .ui file and compile to python file using below command

PyQt Complilation 
C:\Users\<user>\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\LocalCache\local-packages\Python39\Scripts\pyuic5.exe -x first.ui -o first.py