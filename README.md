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
   1. Replace `x.x` with Python version number (i.e. downloaded: **3.7**.4, x.x: **3.7**)
6. Input `py -x.x -m pip install --upgrade setuptools`
   1. Replace `x.x` with Python version number (i.e. downloaded: **3.7**.4, x.x: **3.7**)
7. Input `pip install --user pipenv`
   1. Copy path presented after successfull installation: _looks like_ `C:\Users\<Username>\AppData\Roaming\Python<Version>\Scripts`
8. Input abovementioned path into system's path
9. Input `pipenv install scrapy`

**Execution:**

1. To run, input `pipenv run python <file>.py`
