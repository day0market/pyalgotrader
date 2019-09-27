#  contributing code 

---
##  create PR
 we welcome anyone to contribute code vn.py.   
 if you want to contribute code to use github of PR(Pull Request) process . 

PR process is as follows ：

---
1. [ create  Issue][CreateIssue] -  for larger changes ( as new features ， large-scale reconstruction, etc. ) a good idea to open issue discuss ，  smaller improvement( such as documentation improvements ，bugfix wait ) sent directly PR to 

2. Fork [vn.py][#GithubVnpy] -  click on the top right **Fork** push button 

3. Clone your own fork: ```git clone https://github.com/$userid/vnpy.git```
	>  if your fork outdated ， need to manually [sync][GithubDocForSync]

4.  from **dev** create your own branch: ```git checkout -b $my_feature_branch dev```

5.  in $my_feature_branch on modify and amend push your turn Fork after the warehouse 

6.  creating your fork of $my_feature_branch branch to the main project **dev** branch [Pull Request]:  
 [ point to open here ][CreatePR] ， then click on **compare across forks**， select the desired fork with branch create PR

---

 creating end PR please be patient after ： once we have free will check PR， once your code is useful and [ meet the requirements ](# code style )， it will be consolidated ！


---
##  code style 
 for the vn.py write the code ， we need to follow some basic rules ， otherwise your code may not be merge. 
 these rules include ：
1. [ naming rules ](# naming rules )
2. [ code format ](# code format )
3. [ check the code quality ](# check the code quality )


###  naming rules 
 naming our code is as follows ：

*  class properties ,  class methods ,  parameters and variables in the form of lower case underlined 
*  class names using camel named 
*  constant use of forms of capital underlined 

 e.g ：
```python
DEFAULT_PATH = "/tmp/vn.py/"
class ClassA:
    def __init__(self, arg_one: int, arg_two: str):
        if arg_two is None:
            arg_two = DEFAULT_PATH
        self.property_one = arg_one
        variable_one = "some string"
```


###  code format 
 we do not have particularly stringent requirements of the code format ， but at least in line with pep8 standard ， and additionally in classes and to bring all the following functions docstring( that is, a period of """"""). 

 to make compliance with the code pep8 standard ， after writing the code to use [autopep8](https://github.com/hhatto/autopep8) formatting your code on it :  
```bash
autopep8 --in-place --recursive . 
```

###  check the code quality 
 use [flake8](https://pypi.org/project/flake8/) check your code ， ensure that no error with warning. 
 run in the project root directory ```flake8``` you can check out the local code is not written in a rigorous .  if you check out error or warning， the code that you need to make some changes to improve quality . 

[GithubVnpy]:https://github.com/vnpy/vnpy
[GithubDocForSync]:https://help.github.com/articles/syncing-a-fork/
[CreateIssue]:https://github.com/vnpy/vnpy/issues/new
[CreatePR]:https://github.com/vnpy/vnpy/compare?expand=1

