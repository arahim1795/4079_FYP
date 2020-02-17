# 4079_FYP

4079 Final Year Project

**Requirements:**

1. [Python](https://www.python.org/)
2. [Pipenv](https://github.com/pypa/pipenv)
3. [Scrapy](https://scrapy.org/)

**Setup:**

1. Download and Install Python from [here](https://www.python.org/)
2. Navigate to your Python installation directory and copy path
3. Open _cmd_ in administrator mode
4. Input `cd <paste copied path from 2>` in _cmd_
5. Input `py -x.x -m pip install --upgrade pip` in _cmd_
   1. Replace `x.x` with Python version number (i.e. downloaded: **3.8**.1, x.x: **3.8**)
6. Input `py -x.x -m pip install --upgrade setuptools` in _cmd_
   1. Replace `x.x` with Python version number (i.e. downloaded: **3.8**.1, x.x: **3.8**)
7. Input `py -x.x -m pip install --user pipenv` in _cmd_
   1. Replace `x.x` with Python version number (i.e. downloaded: **3.8**.1, x.x: **3.8**)
   2. Copy path presented after successful installation: _looks like_ `C:\Users\<Username>\AppData\Roaming\Python<Version>\Scripts`
8. Add path into user's environment path
9. Close _cmd_
10. Clone/Download project to a desired directory
11. Copy path to cloned/downloaded project directory after successful clone/download
12. Open _cmd_
13. Input `cd <paste copied path from 11>` in _cmd_
14. Input `pipenv install` in _cmd_
15. Download `Twisted-19.10.0-cp38-cp38-win_amd64.whl` from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted)
16. Input `pipenv run pip install "<path to download .whl file>"`
17. Input `pipenv install Twisted`
18. Input `pipenv install scrapy`

**Execution:**

1. To run, input `pipenv run python <file>.py`
