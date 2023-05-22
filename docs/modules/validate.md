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

More information about the required data can be found in the [dataset_description](../schemas/dataset_description.md) schema.

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
    "IdentifierType": "DOI"
}

output = validate.validate_dataset_description(data)

print(output)  # True
```
