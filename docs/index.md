# Overview

`pyfairdatatools` is a Python package that includes functions of [fairhub.io](https://fairhub.io) for making data FAIR. This consists of a collection of helpful functions for extracting, transforming raw data, generating relevant metadata files and validating the data and metadata files against the FAIR guidelines adopted by the AI-READI project.

Beside supporting [fairhub.io](https://fairhub.io), our aim is that the package can be used by anyone wanting to make their data FAIR according to the AI-READI FAIR guidelines.

## Installation

To install `pyfairdatatools`, run this command in your terminal:

If you use a dependency manager (such as [pipenv](https://pipenv.pypa.io/en/latest/), [poetry](https://python-poetry.org/), or [conda](https://docs.conda.io/en/latest/)), you can install as follows:

```bash
poetry add pyfairdatatools
```

This is the preferred method to install pyfairdatatools, as it will always install the most recent stable release.

```bash
pipenv install pyfairdatatools
```

```bash
conda install pyfairdatatools
```

If you use [pip](https://pip.pypa.io), you can install it as follows:

```bash
pip install pyfairdatatools
```

If you don't have [pip](https://pip.pypa.io) installed, this [Python installation guide](http://docs.python-guide.org/en/latest/starting/installation/) can guide you through the process.

## Usage

The `pyfairdatatools` package contains a collection of methods for working with FAIR data. The package is divided into two main modules: `pyfairdatatools.validate` and `pyfairdatatools.generate`. Each module has a collection of methods for validating and generating FAIR data, respectively.

### Validate

The `pyfairdatatools.validate` module contains methods for validating data against the FAIR guidelines adopted by the AI-READI project. You can learn more about the methods and how to use them in the [validate](modules/validate.md) documentation.

### Generate

The `pyfairdatatools.generate` module contains methods for generating data and metadata files that follow the FAIR guidelines adopted by the AI-READI project. You can learn more about the methods and how to use them in the [generate](modules/generate.md) documentation.
