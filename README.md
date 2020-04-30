# 4079 Final Year Project

## Description

Code: **SCSE 19-0230**

Title: **Sentiment Analysis on Online Text Articles**

Submitted in the Partial Fulfillment of the Requirements for the Degree of Bachelor of Engineering (Computer Science) of the Nanyang Technological University.

---

## Requirements

### Mandatory

1. Python
2. PostgreSQL Database Server

### Recommended

1. Pipenv

---

## Installation

1. Download and install
   1. [Python](https://www.python.org/) [3.8]
   2. [PostgreSQL](https://www.postgresql.org/) [12.2]
      - set postgres password: root
      - add to path:

        ```markdown
        [installation directory]\PostgreSQL\12\bin
        [installation directory]\PostgreSQL\12\lib
        ```

   3. (Recommended) [Pipenv](https://pypi.org/project/pipenv/)
2. Clone repository
3. CD into project root folder
4. Install via

   ```markdown
   # with pip
   pip install -r requirements.txt

   or

   # with pipenv
   pipenv install
   ```

5. Run once

   ```markdown
   # with pip
   python -m backend.init

   or

   # with pipenv
   pipenv run python -m backend.init
   ```

---

## Execution

1. Navigate to project root directory
2. To run
   - Project

     ```markdown
     # with pip
     python -m backend.main

     or

     # with pipenv
     pipenv run python -m backend.main
     ```

   - Web Application

     ```markdown
     # with pip
     python -m frontend.server

     or

     # with pipenv
     pipenv run python -m frontend.server
     ```
