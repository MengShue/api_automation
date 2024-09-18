# API Test Framework

This project is an API testing framework built with Python and pytest, designed to test the [URLhaus API](https://urlhaus-api.abuse.ch/). The framework includes a base HTTP client, configuration management via `config.yaml`, and structured test cases with setup and teardown processes.

## Table of Contents

- [Test Cases](#test-cases)
- [Installation](#installation)
  - [1. Install pyenv](#1-install-pyenv)
  - [2. Set Up Python Environment](#2-set-up-python-environment)
  - [3. Install Dependencies](#3-install-dependencies)
- [Running Tests](#running-tests)
  - [Basic Usage](#basic-usage)
  - [Specify Case or Class](#specify-case-or-class)
- [Project Structure](#project-structure)


## Test Cases

The following table outlines the test cases included in this framework. The third column is what I tested, actual result.

| **Test Case Name**                                                                                   | **Assert Validates**                                                                                   | **Notes**                                      |
|------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|------------------------------------------------|
| **GET Recent URLs Valid** -> v1/urls/recent/limit/3/                                                 | Asserts that the response contains the 'urls' key, 'urls' is a list, and the length is ≤ 3.            |                                                |
| **GET Recent URLs Invalid - Limit = "gg"** -> v1/urls/recent/limit/gg/                               | Asserts that the status code is 400 and the error message is "Invalid parameter: limit must be an integer". | But actually Return 404                        |
| **GET Recent URLs Invalid - Limit = "-1"** -> v1/urls/recent/limit/-1/                               | Asserts that the status code is 400 and the error message is "Invalid parameter: limit must be a positive integer". | But actually Return 404                        |
| **GET Recent URLs Invalid - Limit = None** -> v1/urls/recent/limit//                                 | Asserts that the status code is 400 and the error message is "Missing parameter: limit".               | But Actually Return all urls                   |
| **POST Tag Valid** -> curl -X POST -d "tag=Retefe" https://urlhaus-api.abuse.ch/v1/tag/              | Asserts that the response contains the 'success' key and its value is `True`.                          |                                                |
| **POST Tag Invalid - Tag = "kkk"** -> curl -X POST -d "tag=kkk" https://urlhaus-api.abuse.ch/v1/tag/ | Asserts that the status code is 400 and the error message is "Invalid tag format".                      | But Actually Return 200 OK with no_results msg |
| **POST Tag Invalid - Tag = ""** -> curl -X POST -d "tag=" https://urlhaus-api.abuse.ch/v1/tag/       | Asserts that the status code is 400 and the error message is "Tag cannot be empty".                    | But Actually Return all tags                   |
| **POST Tag Invalid - Tag = None** -> curl -X POST https://urlhaus-api.abuse.ch/v1/tag/               | Asserts that the status code is 400 and the error message is "Missing parameter: tag".                 | But Actually Return Empty String               |


## Installation

### 1. Install pyenv

[`pyenv`](https://github.com/pyenv/pyenv) allows you to easily switch between multiple versions of Python. Follow the installation instructions for your operating system.
Basically, for Mac, just run below command.
```bash
brew update
brew install pyenv
```
and paste below code to `~/.zshrc`
```bash
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```
### 2. Set Up Python Environment
#### macOS/Linux

- Python for Mac, for short

  - install python3.8 `pyenv install 3.8`
  - use python3.8 `pyenv global 3.8`
- Please see detail installation, https://github.com/pyenv/pyenv

### 3. Install Dependencies

install all requirements `pip install -r requirements.txt`
Or you can download PyCharm Community Edition, and open this project, PyCharm will guide you.

## Running Tests

### Basic Usage

To run all tests with default settings:
```bash
pytest
```

### Specify Case or Class
```bash
# specific case
pytest tests/test_urlhaus_api.py::TestURLhausAPI::test_get_recent_urls
# specific class
pytest tests/test_urlhaus_api.py::TestURLhausAPI
```

After running, if you have pytest-html installed, a test report `report.html` will be generated.

## Project Structure
```bash
api_test_framework/
│
├── config/
│   └── config.yaml
│
├── api/
│   ├── __init__.py
│   ├── base_client.py
│   └── urlhaus_client.py
│
├── tests/
│   ├── __init__.py
│   ├── base_test.py
│   └── test_urlhaus_api.py
│
├── conftest.py
├── requirements.txt
├── pytest.ini
└── README.md
```
