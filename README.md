# Redfin Take Home Coding Exercise

## Table of Contents

- [Assignment](#RedfinTakeHomePrompt.md)
- [Requirements](#requirements)
- [Setup](#setup)
- [Execution](#execution)
- [Overview](#overview)

### Requirements

* Python 3.6.x and above

### Setup

* Install Python 3.6.x and above. You can use your favourite tool to install the software such as HomeBrew or  pyenv etc.

* Set up virtualenv with the following command ``virtualenv -p `which python3` env``. Activate the virtual environment using the command `source env/bin/activate`

* Install the python packages required by the project by executing `pip install -r requirements.txt` command.

## Execution

* Run the command `python show_open_food_trucks.py` to execute the program.

* Run the command `pytest` to run the unit tests. The generated code coverage reports will be displayed on the console.

## Overview

The implementation uses `requests` library to make HTTP requests to the SF Data gov.