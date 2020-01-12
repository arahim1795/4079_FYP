# 4079_FYP

4079 Final Year Project

**Requirements:**

1. [Python](https://www.python.org/)
2. [Pipenv](https://github.com/pypa/pipenv)
3. [Scrapy](https://scrapy.org/)

**Setup:**

1. Download and Install Python
2. Navigate to your Python installation directory and copy path
3. Open _cmd_ in administrator mode
4. Input `cd <paste copied path>`
5. Input `py -x.x -m pip install --upgrade pip`
   1. Replace `x.x` with Python version number (i.e. downloaded: **3.8**.1, x.x: **3.8**)
6. Input `py -x.x -m pip install --upgrade setuptools`
   1. Replace `x.x` with Python version number (i.e. downloaded: **3.8**.1, x.x: **3.8**)
7. Input `py -x.x -m pip install --user pipenv`
   1. Replace `x.x` with Python version number (i.e. downloaded: **3.8**.1, x.x: **3.8**)
   2. Copy path presented after successfull installation: _looks like_ `C:\Users\<Username>\AppData\Roaming\Python<Version>\Scripts`
8. Add path into system's environment path
9.  Minimise _cmd_
10. Clone/Download project to a desired directory
11. Copy path to cloned/downloaded project directory after successful clone/download
12. Input `cd <path to cloned/download project path>`
13. Input `pipenv install scrapy`

**Execution:**

1. To run, input `pipenv run python <file>.py`
