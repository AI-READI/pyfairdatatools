# Generation

## Introduction

The generate module provides a way of generating metadata files that follow the FAIR guidelines adopted by the AI-READI project.

!!! warning

    The generate module is still under development.

!!! note

    The `generate` module of this package uses the `validate` module internally to verify that the input data follows the required schema.

## Methods

The following methods are available in the `generate` module. Each method is described in detail below.

### Generate Dataset Description

You can call the `generate_dataset_description` method to generate a dataset_description file.

#### Parameters

##### data

Provide the data required for your `dataset_description` file in this paramater.

| Type   | Default value | Required | Accepted values                            |
| ------ | ------------- | -------- | ------------------------------------------ |
| Object | {}            | yes      | Data object following the required schemas |

More information about the required data can be found in the [dataset_description](../schemas/dataset_description.md) schema.

##### file_path

Provide the path to the file where you want to save the generated dataset_description file.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | yes      | Any string      |

##### file_type

Provide the file type of the file where you want to save the generated dataset_description file.

| Type   | Default value | Required | Accepted values              |
| ------ | ------------- | -------- | ---------------------------- |
| String | None          | yes      | `json`, `xml`, `xlsx`, `csv` |

#### Returns

| Type   | Description                                                             |
| ------ | ----------------------------------------------------------------------- |
| String | Returns the path to the generated dataset_description file as a string. |

#### How to use

```python
from pyfairdatatools import generate

data  = {
    "Title": "My Dataset",
    "Identifier": "10.5281/zenodo.1234567",
    "IdentifierType": "DOI"
}

output = generate.generate_dataset_description(data = data, file_path = "dataset_description.json", file_type = "json")

print(output)  # dataset_description.json
```

### Generate Readme

You can call the `generate_readme` method to generate a readme file.

#### Parameters

##### data

Provide the data required for your readme file in this paramater.

| Type   | Default value | Required | Accepted values                            |
| ------ | ------------- | -------- | ------------------------------------------ |
| Object | {}            | yes      | Data object following the required schemas |

More information about the required data can be found in the [readme](../schemas/readme.md) schema.

##### file_path

Provide the path to the file where you want to save the generated readme file.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | yes      | Any string      |

##### file_type

Provide the file type of the file where you want to save the generated readme file.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | yes      | `md`, `txt`     |

#### Returns

| Type   | Description                                                |
| ------ | ---------------------------------------------------------- |
| String | Returns the path to the generated readme file as a string. |

#### How to use

```python
from pyfairdatatools import generate

data  = {
    "Title": "My Dataset",
    "Identifier": "10.5281/zenodo.1234567",
    "Version": "1.0.0",
}

output = generate.generate_readme(data = data, file_path = "readme.md", file_type = "md")

print(output)  # readme.md
```

### Generate Changelog

You can call the `generate_changelog` method to generate a changelog file.

#### Parameters

##### data

Provide the content of the changelog file in this paramater.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | yes      | Any string      |

##### file_path

Provide the path to the file where you want to save the generated changelog file.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | yes      | Any string      |

##### file_type

Provide the file type of the file where you want to save the generated changelog file.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | yes      | `md`, `txt`     |

#### Returns

| Type   | Description                                                   |
| ------ | ------------------------------------------------------------- |
| String | Returns the path to the generated changelog file as a string. |

#### How to use

```python
from pyfairdatatools import generate

data  = """
# Changelog

## 1.0.0

- Initial release
"""

output = generate.generate_changelog(data = data, file_path = "changelog.md", file_type = "md")

print(output)  # changelog.md
```

### Generate License

You can call the `generate_license` method to generate a license file.

#### Parameters

##### identifier

Provide the identifier of the license you want to use in this paramater.

| Type   | Default value | Required | Accepted values         |
| ------ | ------------- | -------- | ----------------------- |
| String | ""            | yes      | SPDX license identifier |

For a list of all SPDX license identifiers, see [here](https://spdx.org/licenses/).

!!! warning

    If you provide an invalid identifier, the method will raise an error. If you want to use a custom license, use the `data` parameter instead and provide the content of the license file. Leave this parameter empty if you are using  custom license text.

##### data

Provide the content of the license file in this paramater.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | yes      | Any string      |

!!! warning

    Use this parameter if you want to use a custom license. Leave this parameter empty if you are using a SPDX license identifier. If you provide a SPDX license identifier, the method will prioritize this parameter over the `identifier` parameter.

##### file_path

Provide the path to the file where you want to save the generated license file.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | yes      | Any string      |

##### file_type

Provide the file type of the file where you want to save the generated license file.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | yes      | `md`, `txt`     |

#### Returns

| Type   | Description                                                 |
| ------ | ----------------------------------------------------------- |
| String | Returns the path to the generated license file as a string. |

#### How to use

```python
from pyfairdatatools import generate

data  = """
MIT License

SPDX short identifier: MIT

Further resources on the MIT License

- [Text](https://spdx.org/licenses/MIT.html)
- [JSON](https://spdx.org/licenses/MIT.json)
- [RDF](https://spdx.org/licenses/MIT.rdf)
- [HTML](https://spdx.org/licenses/MIT.html)
"""

output = generate.generate_license(identifier = "MIT", data = data, file_path = "license.md", file_type = "md")

print(output)  # license.md
```
