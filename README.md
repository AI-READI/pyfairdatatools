# fairdatatools

[![Unix Build Status](https://img.shields.io/github/actions/workflow/status/AI-READI/fairdatatools/main.yml?branch=main&label=linux)](https://github.com/AI-READI/fairdatatools/actions)
[![Windows Build Status](https://img.shields.io/appveyor/ci/AI-READI/fairdatatools.svg?label=windows)](https://ci.appveyor.com/project/AI-READI/fairdatatools)
[![Coverage Status](https://img.shields.io/codecov/c/gh/AI-READI/fairdatatools)](https://codecov.io/gh/AI-READI/fairdatatools)
[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/AI-READI/fairdatatools.svg)](https://scrutinizer-ci.com/g/AI-READI/fairdatatools)
[![PyPI License](https://img.shields.io/pypi/l/fairdatatools.svg)](https://pypi.org/project/fairdatatools)
[![PyPI Version](https://img.shields.io/pypi/v/fairdatatools.svg)](https://pypi.org/project/fairdatatools)
[![PyPI Downloads](https://img.shields.io/pypi/dm/fairdatatools.svg?color=orange)](https://pypistats.org/packages/fairdatatools)

## Overview

fairdatatools is a Python package for working with FAIR data. A collection of helpful functions for extracting, transforming raw data, generating relevant metadata files and validating the data and metadata files against the FAIR data principles.

For more information, please visit the [documentation](https://fairdatatools.readthedocs.io/en/latest/).

## Setup

If you would like to update the package, please follow the instructions below.

1. Create a local virtual environment and activate it:

   ```text
   python -m venv .venv
   source .venv/bin/activate
   ```

   If you are using Anaconda, you can create a virtual environment with:

   ```text
   conda create -n fairdatatools-env python
   conda activate fairdatatools-env
   ```

2. Install the dependencies for this package. We use [Poetry](https://poetry.eustace.io/) to manage the dependencies:

   ```text
   pip install poetry==1.3.2
   poetry install
   ```

3. Add your modifications and run the tests:

   ```text
   poetry run pytest
   ```

   If you need to add new python packages, you can use Poetry to add them:

   ```text
    poetry add <package-name>
   ```

4. Format the code:

   ```text
   poe format
   ```

5. Check the code quality:

   ```text
   poetry run flake8 fairdatatools tests
   ```

6. Run the tests and check the code coverage:

   ```text
   poe test
   poe test --cov=fairdatatools
   ```

7. Build the package:

   Update the version number in `pyproject.toml` and `fairdatatools/__init__.py` and then run:

   ```text
   poetry build
   ```

8. Publish the package:

   ```text
   poetry publish
   ```

### Requirements

- Python 3.8+
- [Pip](https://pip.pypa.io/en/stable/)
- [Poetry](https://poetry.eustace.io/)

### Installation

Install it directly into an activated virtual environment:

```text
pip install fairdatatools
```

or add it to your [Poetry](https://poetry.eustace.io/) project:

```text
poetry add fairdatatools
```

## Usage

After installation, the package can be imported:

```text
$ python
>>> import fairdatatools
>>> fairdatatools.__version__
```
