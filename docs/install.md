# Installation Guide


## Windows



### useVNStudio


#### 1.downloadVNStudio （Python 3.7 64Place）

VNStudioYesvn.pyTeam packed their own version of a key installation，Integration：
- Python 3.7（Community official version)
- vn.pyFrameworks and other related libraries
- VN StationQuantify workstation（vn.pyFrame graphical management tool）

download link：[vnstudio-2.0.6.exe](https://download.vnpy.com/vnstudio-2.0.6.exe)

&nbsp;


#### 2.installationVNStudio

Click on the way“The next step”To completeVNStudioinstallation，After the installation is complete, you can view the run directory：

- VNStudioThe default installation path isC:\vnstudio；
- VNStudiodefaultjsonConfiguration files and database pathC:\Users\Administrator\.vntrader
- VN StationQuantify workstation running directoryC:\vnstudio\Scripts\vnstation.exe；
- vnpyRun directoryC:\vnstudio\Lib\site-packages\vnpy（After entering the directory，Users can modifyvnpyRelated functions）


&nbsp;

#### 3.LandedVNStation

Enter the account password login or micro-channel scan codeVNStation。（Community account through the micro channel scan code available）

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/install.bat/login_VNConda.png "enter image title here")

&nbsp;

#### 4.useVNStation
After logging will enter intoVN StationThe main interface。
![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/install.bat/login_VNConda_2.png "enter image title here")

There are window below5Options：
- VN Trade Lite：Run directlyVN Trader (onlyCTPinterface)
- VN Trader Pro：First select the relevant save temporary files directory，Then runVN Trader (And optionally an upper layer application module interfaces)
- Jupyter Notebook：First select the relevant save temporary files directory，Then runJupyter Notebook
- Question for help：Asked questions，Administrators will regularly answer every day
- Background updating：A key updateVN Station


&nbsp;

#### 5.UpdateVNStation
UpdateVNStationapart from“A key update”outer；You can also uninstall the old version，Install the new version；OrgithubDownload the latest ondevBranch，Unpack the root directoryvnpyfolder，CorrectC:\vnstudio\Lib\site-packages\vnpyReplacement。



&nbsp;
&nbsp;


### Installation Manual

#### 1.Download and install the latest versionAnaconda3.7 64Place

Download the following address：[Anaconda Distribution](https://www.anaconda.com/distribution/)

(More lightweightMinicondaaddress：[MiniConda Distribution](https://docs.conda.io/en/latest/miniconda.html))

&nbsp;

#### 2.Download and unzipvnpy

entervnpyofgithubHome[vnpy](https://github.com/vnpy/vnpy)。
In the leftBranchOptions，masterCorrespondence is the latest stable version，devIt corresponds to the latest test version；
Then the home page to the right of the greenclone or downloadOptions，selectDownload ZIPTo download the compressed version to your local computer。

&nbsp;

#### 3.installationvnpy
Double-clickinstall.batA key installationvnpy：
- Installta_libLibrary andib api
- Then installrequirements.txtThe paper dependent libraries.
- Finally CopyvnpyToAnacondaInside

&nbsp;

#### 4.start upVN Trader
In the Foldertests\traderFoundrun.pyfile。Press and hold“Shift” + Right into thecmdwindow，Enter the following command to startVN Trader。
```
python run.py 
```

&nbsp;
&nbsp;


## Ubuntu


### 1. Download and install the latest versionAnacondaorMiniconda （Python 3.7 64Place）

WithMiniCondaA Case Study，Downloaded into the good Miniconda3-latest-Linux-x86_64.sh Directory，Terminal run the following command to start the installation。
```
$ bash Miniconda3-latest-Linux-x86_64.sh
```

The installation process can always press“Enter”Key to continue，In addition to this the following points：

When asked if theMinicondaSet asPython When the default environment，The default"no"Change“yes”。The reason isUbuntu 18.04There comesPython 3.6versusPython 2.7。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/install.bat/install_Miniconda_ubuntu.png "enter image title here")



RestartUbuntuRear，Open the direct input terminal"python" then press“Enter”key: If there is shown below，Said the successMinicondaSet asPythonDefault environment。

![](https://vnpy-community.oss-cn-shanghai.aliyuncs.com/forum_experience/yazhang/install.bat/Conda_Python_version.png "enter image title here")

&nbsp;

### 2. Download and unzipvnpy
LinuxUsers selecttar.gzCompressed version。Download the following address：[vnpy releases](https://github.com/vnpy/vnpy/releases)

&nbsp;

### 3. installationvnpy
Installgcctranslater，Used to compileC++Class interface。Enter the following command can be in the terminal。
```
sudo apt-get  install  build-essential
```


ThenvnpyOpen a terminal root directory，Enter the following command to install a keyvnpy。
```
bash install.sh
```

Installation process is divided into4step：
- Download and installta_libLibrary andnumpy
- installationrequirements.txtThe paper dependent libraries.
- Install Chinese encoding（For the English system）
- copyvnpyToAnacondaInside（If running on a virtual machine，Memory adjusted to the needs4g，Otherwise error）

&nbsp;

### 4.start upVN Trader
In the Foldertests\traderFoundrun.pyfile。Right into the terminal，Enter the following command to startVN Trader。
```
python run.py 
```
