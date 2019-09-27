#  installation guide 


## Windows



###  use VNStudio


#### 1. download VNStudio （Python 3.7 64 place ）

VNStudio yes vn.py team packed their own version of a key installation ， integration ：
- Python 3.7（ community official version )
- vn.py frameworks and other related libraries 
- VN Station quantify workstation （vn.py frame graphical management tool ）

 download link ：[vnstudio-2.0.6.exe](https://download.vnpy.com/vnstudio-2.0.6.exe)

&nbsp;


#### 2. installation VNStudio

 click on the way “ the next step ” to complete VNStudio installation ， after the installation is complete, you can view the run directory ：

- VNStudio the default installation path is C:\vnstudio；
- VNStudio default json configuration files and database path C:\Users\Administrator\.vntrader
- VN Station quantify workstation running directory C:\vnstudio\Scripts\vnstation.exe；
- vnpy run directory C:\vnstudio\Lib\site-packages\vnpy（ after entering the directory ， users can modify vnpy related functions ）


&nbsp;

#### 3. landed VNStation

 enter the account password login or micro-channel scan code VNStation. （ community account through the micro channel scan code available ）

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/install.bat/login_VNConda.png "enter image title here")

&nbsp;

#### 4. use VNStation
 after logging will enter into VN Station the main interface . 
![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/install.bat/login_VNConda_2.png "enter image title here")

 there are window below 5 options ：
- VN Trade Lite： run directly VN Trader ( only CTP interface )
- VN Trader Pro： first select the relevant save temporary files directory ， then run VN Trader ( and optionally an upper layer application module interfaces )
- Jupyter Notebook： first select the relevant save temporary files directory ， then run Jupyter Notebook
-  question for help ： asked questions ， administrators will regularly answer every day 
-  background updating ： a key update VN Station


&nbsp;

#### 5. update VNStation
 update VNStation apart from “ a key update ” outer ； you can also uninstall the old version ， install the new version ； or github download the latest on dev branch ， unpack the root directory vnpy folder ， correct C:\vnstudio\Lib\site-packages\vnpy replacement . 



&nbsp;
&nbsp;


###  installation manual 

#### 1. download and install the latest version Anaconda3.7 64 place 

 download the following address ：[Anaconda Distribution](https://www.anaconda.com/distribution/)

( more lightweight Miniconda address ：[MiniConda Distribution](https://docs.conda.io/en/latest/miniconda.html))

&nbsp;

#### 2. download and unzip vnpy

 enter vnpy of github home [vnpy](https://github.com/vnpy/vnpy). 
 in the left Branch options ，master correspondence is the latest stable version ，dev it corresponds to the latest test version ；
 then the home page to the right of the green clone or download options ， select Download ZIP to download the compressed version to your local computer . 

&nbsp;

#### 3. installation vnpy
 double-click install.bat a key installation vnpy：
-  install ta_lib library and ib api
-  then install requirements.txt the paper dependent libraries. 
-  finally copy vnpy to Anaconda inside 

&nbsp;

#### 4. start up VN Trader
 in the folder tests\trader found run.py file .  press and hold “Shift” +  right into the cmd window ， enter the following command to start VN Trader. 
```
python run.py 
```

&nbsp;
&nbsp;


## Ubuntu


### 1.  download and install the latest version Anaconda or Miniconda （Python 3.7 64 place ）

 with MiniConda a case study ， downloaded into the good  Miniconda3-latest-Linux-x86_64.sh  directory ， terminal run the following command to start the installation . 
```
$ bash Miniconda3-latest-Linux-x86_64.sh
```

 the installation process can always press “Enter” key to continue ， in addition to this the following points ：

 when asked if the Miniconda set as Python  when the default environment ， the default "no" change “yes”.  the reason is Ubuntu 18.04 there comes Python 3.6 versus Python 2.7. 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/install.bat/install_Miniconda_ubuntu.png "enter image title here")



 restart Ubuntu rear ， open the direct input terminal "python"  then press “Enter” key :  if there is shown below ， said the success of the Miniconda set as Python default environment . 

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/install.bat/Conda_Python_version.png "enter image title here")

&nbsp;

### 2.  download and unzip vnpy
Linux users select tar.gz compressed version .  download the following address ：[vnpy releases](https://github.com/vnpy/vnpy/releases)

&nbsp;

### 3.  installation vnpy
 install gcc translater ， used to compile C++ class interface .  enter the following command can be in the terminal . 
```
sudo apt-get  install  build-essential
```


 then vnpy open a terminal root directory ， enter the following command to install a key vnpy. 
```
bash install.sh
```

 installation process is divided into 4 step ：
-  download and install ta_lib library and numpy
-  installation requirements.txt the paper dependent libraries. 
-  install chinese encoding （ for the english system ）
-  copy vnpy to Anaconda inside （ if running on a virtual machine ， memory adjusted to the needs 4g， otherwise error ）

&nbsp;

### 4. start up VN Trader
 in the folder tests\trader found run.py file .  right into the terminal ， enter the following command to start VN Trader. 
```
python run.py 
```
