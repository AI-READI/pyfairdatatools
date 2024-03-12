<div align="center">

<img src="https://raw.githubusercontent.com/AI-READI/pyfairdatatools/main/logo.svg" alt="logo" width="200" height="auto" />

<br />

<h1>pyfairdatatools</h1>

<p>
Python package for the FAIR tools of fairhub.io
</p>

<br />

<p>
  <a href="https://github.com/AI-READI/pyfairdatatools/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/AI-READI/pyfairdatatools.svg?style=flat-square" alt="contributors" />
  </a>
  <a href="https://github.com/AI-READI/pyfairdatatools/stargazers">
    <img src="https://img.shields.io/github/stars/AI-READI/pyfairdatatools.svg?style=flat-square" alt="stars" />
  </a>
  <a href="https://github.com/AI-READI/pyfairdatatools/issues/">
    <img src="https://img.shields.io/github/issues/AI-READI/pyfairdatatools.svg?style=flat-square" alt="open issues" />
  </a>
  <a href="https://github.com/AI-READI/pyfairdatatools/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/AI-READI/pyfairdatatools.svg?style=flat-square" alt="license" />
  </a>
  <a href="https://fairdataihub.org/fairshare">
    <img src="https://raw.githubusercontent.com/fairdataihub/FAIRshare/main/badge.svg" alt="Curated with FAIRshare" />
  </a>
</p>
<p>
  <a href="https://github.com/AI-READI/pyfairdatatools/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/AI-READI/pyfairdatatools/main.yml?branch=main&label=linux" alt="Unix Build Status" />
  </a>
  <a href="https://ci.appveyor.com/project/AI-READI/pyfairdatatools">
    <img src="https://img.shields.io/appveyor/ci/AI-READI/pyfairdatatools.svg?label=windows" alt="Windows Build Status" />
  </a>
  <a href="https://codecov.io/gh/AI-READI/pyfairdatatools">
    <img src="https://img.shields.io/codecov/c/gh/AI-READI/pyfairdatatools" alt="Coverage Status" />
  </a>
  <a href="https://scrutinizer-ci.com/g/AI-READI/pyfairdatatools">
    <img src="https://img.shields.io/scrutinizer/g/AI-READI/pyfairdatatools.svg" alt="Scrutinizer Code Quality" />
  </a>
  <a href="https://pypi.org/project/pyfairdatatools">
    <img src="https://img.shields.io/pypi/l/pyfairdatatools.svg" alt="PyPI License" />
  </a>
  <a href="https://pypi.org/project/pyfairdatatools">
    <img src="https://img.shields.io/pypi/v/pyfairdatatools.svg" alt="PyPI Version" />
  </a>
  <a href="https://pypistats.org/packages/pyfairdatatools">
    <img src="https://img.shields.io/pypi/dm/pyfairdatatools.svg?color=orange" alt="PyPI Downloads" />
  </a>
</p>

<h4>
    <a href="https://ai-readi.github.io/pyfairdatatools/">Documentation</a>
  <span> · </span>
    <a href="https://ai-readi.github.io/pyfairdatatools/about/changelog/">Changelog</a>
  <span> · </span>
    <a href="https://github.com/AI-READI/pyfairdatatools/issues/">Report Bug</a>
  <span> · </span>
    <a href="#">Request Feature</a>
  </h4>
</div>

<br />

---

## Description

pyfairdatatools is a Python package that includes functions of fairhub.io for making data FAIR. This consists of a collection of helpful functions for extracting, transforming raw data, generating relevant metadata files and validating the data and metadata files against the FAIR guidelines adopted by the AI-READI project. Beside supporting fairhub.io, our aim is that the package can be used by anyone wanting to make their data FAIR according to the AI-READI FAIR guidelines.

## Getting started

### Prerequisites/Dependencies

You will need the following installed on your system:

- Python 3.8+
- [Pip](https://pip.pypa.io/en/stable/)
- [Poetry](https://poetry.eustace.io/)

### Installing

Install it directly into an activated virtual environment:

```bash
pip install pyfairdatatools
```

or add it to your [Poetry](https://poetry.eustace.io/) project:

```bash
poetry add pyfairdatatools
```

### Usage

After installation, the package can be imported:

```bash
$ python
>>> import pyfairdatatools
>>> pyfairdatatools.__version__
```

### Inputs and Outputs

The input of most functions will be a json format schema (see "Standards followed" sections) that contain data and metadata related information. The outputs of most functions will be standards metadata files, structured data, etc.

## Standards followed

This software is being developed following the [Software Development Best Practices of the AI-READI Project](https://github.com/AI-READI/software-development-best-practices), which include following the [FAIR-BioRS guidelines](https://github.com/FAIR-BioRS/Guidelines). Amongs other, we are following closely the [PEP 8 Style Guide for Python Code](https://peps.python.org/pep-0008/).

The input structure of the function is currently being developed but anticipated to follow existing schemas such as schema.org and bioschemas.org.

## Contributing

<a href="https://github.com/AI-READI/pyfairdatatools/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=AI-READI/pyfairdatatools" />
</a>

Contributions are always welcome!

If you are interested in reporting/fixing issues and contributing directly to the code base, please see [CONTRIBUTING.md](CONTRIBUTING.md) for more information on what we're looking for and how to get started.

## Issues and Feedback

To report any issues with the software, suggest improvements, or request a new feature, please open a new issue via the [Issues](https://github.com/AI-READI/pyfairdatatools/issues) tab. Provide adequate information (operating system, steps leading to error, screenshots) so we can help you efficiently.

### Setup

If you would like to update the package, please follow the instructions below.

1. Create a local virtual environment and activate it:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   If you are using Anaconda, you can create a virtual environment with:

   ```bash
   conda create -n pyfairdatatools-env python=3.8
   conda activate pyfairdatatools-env
   ```

2. Install the dependencies for this package. We use [Poetry](https://poetry.eustace.io/) to manage the dependencies:

   ```bash
   pip install poetry==1.3.2
   poetry install
   ```

   You can also use version 1.2.0 of Poetry, but you will need to run `poetry lock` after installing the dependencies.

3. Add your modifications and run the tests. You can also use the command `poe test` for running the tests.

   ```bash
   poetry run pytest
   ```

   If you need to add new python packages, you can use Poetry to add them:

   ```bash
    poetry add <package-name>
   ```

4. Format the code:

   ```bash
   poe format
   ```

5. Check the code quality:

   ```bash
   poetry run flake8 pyfairdatatools tests
   ```

6. Run the tests and check the code coverage:

   ```bash
   poe test
   poe test --cov=pyfairdatatools
   ```

7. Build the package:

   Update the version number in `pyproject.toml` and `pyfairdatatools/__init__.py` and then run:

   ```text
   poetry build
   ```

8. Publish the package:

   ```bash
   poetry publish
   ```

   Set your API token for PyPI in your environment variables:

   ```bash
   poetry config pypi-token.pypi your-api-token
   ```

## License

This work is licensed under
[MIT](https://opensource.org/licenses/mit). See [LICENSE](https://github.com/AI-READI/pyfairdatatools/blob/main/LICENSE) for more information.

<a href="https://aireadi.org" >
  <img src="https://www.channelfutures.com/files/2017/04/3_0.png" height="30" />
</a>

## How to cite

If you are using this package or reusing the source code from this repository for any purpose, please cite:

```text
    Coming soon...
```

## Acknowledgements

This project is funded by the NIH under award number 1OT2OD032644. The content is solely the responsibility of the authors and does not necessarily represent the official views of the NIH.

Add any other acknowledgements here.

<br />

---

<br />

<div align="center">

<a href="https://aireadi.org">
  <img src="https://github.com/AI-READI/AI-READI-logo/raw/main/logo/png/option2.png" height="200" />
</a>

</div>
