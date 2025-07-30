# Validation

## Introduction

The validation module provides a way to validate data against a set of rules.

!!! warning

    The validation module is still under development.

!!! note

    The `generate` module of this package uses this `validate` module internally to verify that the input data follows the required schema.

## Methods

The following methods are available in the `validate` module. Each method is described in detail below.

### Validate Dataset Description

You can call the `validate_dataset_description` method to validate the data needed to create a dataset_description file.

#### Parameters

##### data

Provide the data required for your `dataset_description` file in this paramater.

| Type   | Default value | Required | Accepted values                            |
| ------ | ------------- | -------- | ------------------------------------------ |
| Object | {}            | yes      | Data object following the required schemas |

More information about the required data can be found in the [dataset_description](https://github.com/AI-READI/high-level-dataset-structure/blob/specifications/main/v1.0.0/schemas/dataset_description.schema.json) schema.

You can the hosted validator [here](https://www.jsonschemavalidator.net/s/makBzCFq) if you want a better understanding or visualization of the schema for the input.

#### Returns

| Type    | Description                                             |
| ------- | ------------------------------------------------------- |
| Boolean | Returns `True` if the data is valid, `False` otherwise. |

#### How to use

```python
from pyfairdatatools import validate

data  = {
    "Title": "My Dataset",
    "Identifier": "10.5281/zenodo.1234567",
    "IdentifierType": "DOI"
}

output = validate.validate_dataset_description(data = data)

print(output)  # True
```

### Validate Study Description

You can call the `validate_study_description` method to validate the data needed to create a study_description file.

#### Parameters

##### data

Provide the data required for your `study_description` file in this paramater.

| Type   | Default value | Required | Accepted values                            |
| ------ | ------------- | -------- | ------------------------------------------ |
| Object | {}            | yes      | Data object following the required schemas |

More information about the required data can be found in the [study_description](https://github.com/AI-READI/high-level-dataset-structure/blob/specifications/main/v1.0.0/schemas/dataset_description.schema.json) schema.

You can the hosted validator [here](https://www.jsonschemavalidator.net/s/cmkkqm9P) if you want a better understanding or visualization of the schema for the input.

#### Returns

| Type    | Description                                             |
| ------- | ------------------------------------------------------- |
| Boolean | Returns `True` if the data is valid, `False` otherwise. |

#### How to use

```python
from pyfairdatatools import validate

data  = {
    "Title": "My Dataset",
    "Identifier": "10.5281/zenodo.1234567",
    "IdentifierType": "DOI"
}

output = validate.validate_study_description(data = data)

print(output)  # True
```

### Validate Readme

You can call the `validate_readme` method to validate the data needed to create a README file.

#### Parameters

##### data

Provide the data required for your `README` file in this paramater.

| Type   | Default value | Required | Accepted values                            |
| ------ | ------------- | -------- | ------------------------------------------ |
| Object | {}            | yes      | Data object following the required schemas |

More information about the required data can be found in the [README](../schemas/README.md) schema.

You can the hosted validator [here](https://www.jsonschemavalidator.net/s/aNSmlcv1) if you want a better understanding or visualization of the schema for the input.

#### Returns

| Type    | Description                                             |
| ------- | ------------------------------------------------------- |
| Boolean | Returns `True` if the data is valid, `False` otherwise. |

#### How to use

```python
from pyfairdatatools import validate

data  = {
    "Title": "My Dataset",
    "Identifier": "10.5281/zenodo.1234567",
    "Version": "1.0.0",
}

output = validate.validate_readme(data = data)

print(output)  # True
```

### Validate License

You can call the `validate_license` method to validate the data needed to create a LICENSE file.

#### Parameters

##### identifier

Provide the identifier of the license you want to validate.

| Type   | Default value | Required | Accepted values         |
| ------ | ------------- | -------- | ----------------------- |
| String | ""            | yes      | SPDX license identifier |

For a list of all SPDX license identifiers, see [here](https://spdx.org/licenses/).

#### Returns

| Type    | Description                                             |
| ------- | ------------------------------------------------------- |
| Boolean | Returns `True` if the data is valid, `False` otherwise. |

#### How to use

```python
from pyfairdatatools import validate

identifier = "CC-BY-4.0"

output = validate.validate_license(identifier = identifier)

print(output)  # True
```

### Validate Participants

You can call the `validate_participants` method to validate the data needed to create a participants.tsv file.

#### Parameters

##### data

Provide the data required for your `participants.tsv` file in this paramater.

| Type   | Default value | Required | Accepted values                            |
| ------ | ------------- | -------- | ------------------------------------------ |
| Object | {}            | yes      | Data object following the required schemas |

More information about the required data can be found in the [participants](../schemas/participants.md) schema.

You can the hosted validator [here](https://www.jsonschemavalidator.net/s/aNSmlcv1) if you want a better understanding or visualization of the schema for the input.

#### Returns

| Type    | Description                                             |
| ------- | ------------------------------------------------------- |
| Boolean | Returns `True` if the data is valid, `False` otherwise. |

#### How to use

```python
from pyfairdatatools import validate

data = {
    "participant_id": 'sub-id1',
    "species": 'rattus norvegicus',
    "age": 2
}

output = validate.validate_participants(data = data)

print(output)  # True
```
