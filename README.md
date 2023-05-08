<div align="center">

<img src="https://freesvg.org/img/1653682897science-svgrepo-com.png" alt="logo" width="200" height="auto" />

<br />

<h1>fairdatatools</h1>

<p>
Python package for working with FAIR data
</p>

<br />

<p>
  <a href="https://github.com/AI-READI/fairdatatools/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/AI-READI/fairdatatools.svg?style=flat-square" alt="contributors" />
  </a>
  <a href="https://github.com/AI-READI/fairdatatools/stargazers">
    <img src="https://img.shields.io/github/stars/AI-READI/fairdatatools.svg?style=flat-square" alt="stars" />
  </a>
  <a href="https://github.com/AI-READI/fairdatatools/issues/">
    <img src="https://img.shields.io/github/issues/AI-READI/fairdatatools.svg?style=flat-square" alt="open issues" />
  </a>
  <a href="https://github.com/AI-READI/fairdatatools/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/AI-READI/fairdatatools.svg?style=flat-square" alt="license" />
  </a>
  <a href="https://fairdataihub.org/fairshare">
    <img src="https://raw.githubusercontent.com/fairdataihub/FAIRshare/main/badge.svg" alt="Curated with FAIRshare" />
  </a>
</p>
<p>
  <a href="https://github.com/AI-READI/fairdatatools/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/AI-READI/fairdatatools/main.yml?branch=main&label=linux" alt="Unix Build Status" />
  </a>
  <a href="https://ci.appveyor.com/project/AI-READI/fairdatatools">
    <img src="https://img.shields.io/appveyor/ci/AI-READI/fairdatatools.svg?label=windows" alt="Windows Build Status" />
  </a>
  <a href="https://codecov.io/gh/AI-READI/fairdatatools">
    <img src="https://img.shields.io/codecov/c/gh/AI-READI/fairdatatools" alt="Coverage Status" />
  </a>
  <a href="https://scrutinizer-ci.com/g/AI-READI/fairdatatools">
    <img src="https://img.shields.io/scrutinizer/g/AI-READI/fairdatatools.svg" alt="Scrutinizer Code Quality" />
  </a>
  <a href="https://pypi.org/project/fairdatatools">
    <img src="https://img.shields.io/pypi/l/fairdatatools.svg" alt="PyPI License" />
  </a>
  <a href="https://pypi.org/project/fairdatatools">
    <img src="https://img.shields.io/pypi/v/fairdatatools.svg" alt="PyPI Version" />
  </a>
  <a href="https://pypistats.org/packages/fairdatatools">
    <img src="https://img.shields.io/pypi/dm/fairdatatools.svg?color=orange" alt="PyPI Downloads" />
  </a>
</p>

<h4>
    <a href="https://ai-readi.github.io/fairdatatools/">Documentation</a>
  <span> · </span>
    <a href="https://ai-readi.github.io/fairdatatools/about/changelog/">Changelog</a>
  <span> · </span>
    <a href="https://github.com/AI-READI/fairdatatools/issues/">Report Bug</a>
  <span> · </span>
    <a href="#">Request Feature</a>
  </h4>
</div>

<br />

---

## Description

fairdatatools is a Python package for working with FAIR data. A collection of helpful functions for extracting, transforming raw data, generating relevant metadata files and validating the data and metadata files against the FAIR data principles.

## Getting started

### Prerequisites/Dependencies

You will need the following installed on your system:

- Python 3.8+
- [Pip](https://pip.pypa.io/en/stable/)
- [Poetry](https://poetry.eustace.io/)

### Installing

Install it directly into an activated virtual environment:

```text
pip install fairdatatools
```

or add it to your [Poetry](https://poetry.eustace.io/) project:

```text
poetry add fairdatatools
```

### Inputs and Outputs

#### Usage

After installation, the package can be imported:

```text
$ python
>>> import fairdatatools
>>> fairdatatools.__version__
```

- Describe the inputs and outputs of your application. Include code snippets and screenshots if needed.

## Contributing

<a href="https://github.com/AI-READI/fairdatatools/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=AI-READI/fairdatatools" />
</a>

Contributions are always welcome!

If you are interested in reporting/fixing issues and contributing directly to the code base, please see [CONTRIBUTING.md](CONTRIBUTING.md) for more information on what we're looking for and how to get started.

For any developmental standards to follow, add them directly to the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## Issues and Feedback

To report any issues with the software, suggest improvements, or request a new feature, please open a new issue via the [Issues](https://github.com/AI-READI/fairdatatools/issues) tab. Provide adequate information (operating system, steps leading to error, screenshots) so we can help you efficiently.

### Setup

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

## License

This work is licensed under
[MIT](https://opensource.org/licenses/mit). See [LICENSE](https://github.com/AI-READI/fairdatatools/blob/main/LICENSE) for more information.

<a href="https://aireadi.org" >
  <img src="https://www.channelfutures.com/files/2017/04/3_0.png" height="30" />
</a>

## How to cite

If you are using this software or reusing the source code from this repository for any purpose, please cite:

```bash
    ADD Citation here
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
