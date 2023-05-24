# Overview

This page details the input schema required for the `validate_readme` method of the `validate` module and the `generate_readme` method of the `generate` module.

## Parameters

The data required for this item is detailed below:

### Title

The name of the dataset.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | yes      | Any string      |

### Identifier

A formal identifier that is used to identify this resource in a global registry. Identifiers should be in the form of a resolvable persistent identifier. Only DOIs are currently supported.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | no       | Any DOI         |

A regex expression is used to validate the DOI. The expression is `^10\.\d{4,9}/[-._;()/:A-Za-z0-9]+$`.

### Version

The version of the resource. This property is used to capture the version of the resource being described.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | no       | Any string      |

It is recommended to use the [Semantic Versioning](https://semver.org/) convention.

### PublicationDate

The date of formal issuance (e.g., publication) of the resource.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | no       | Any valid date  |

The valid formats for this field are:

- YYYY
- YYYY-MM-DD
- YYYYMM-DDThh:mm:ssTZD

### About

A short high-level description of the resource. This property is used to capture a short description of the resource being described.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | no       | Any string      |

### DatasetDescription

Describe the number of study participants and their characteristics (refer to the participants.json file described in a later section for additional information), the data types collected, the overall number of files and total size of the dataset.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | no       | Any string      |

### DatasetAccess

Describe how to access the data, including any credentials or software needed to access the data. If the data is not publicly available, describe the process by which access may be requested.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | no       | Any string      |

### StandardsFollowed

Mention the standards followed to structure the dataset, format the data files, etc. Make sure to include identifiers of the standards when available and/or link to the associated documentation.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | no       | Any string      |

### Resources

Any external resources that may be either required to use the data or useful when using the data (e.g. the project website aireadi.org, the documentation of fairhub.io at docs.fairhub.io, etc.). Make sure to include identifiers and/or links to the resources.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | no       | Any string      |

### License

Brief description of the terms for reusing the data with full name and abbreviation of the license (refer to the LICENSE.txt file for additional details).

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | no       | Any string      |

### HowToCite

Brief description of how to cite the data (refer to the CITATION.txt file for additional details).

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | no       | Any string      |

### Acknowledgement

Brief description of how to acknowledge the data (refer to the ACKNOWLEDGEMENTS.txt file for additional details).

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | no       | Any string      |

## Data Schema

The full JSON schema for the dataset metadata is as follows.

You can also use the JSON validator hosted at [https://www.jsonschemavalidator.net/s/aNSmlcv1](https://www.jsonschemavalidator.net/s/aNSmlcv1) to validate your JSON data against this schema.

!!! warning

    There is additional validation performed within the method itself. This schema is only used for validation of the JSON data before it is sent to the method.

```json
{
  "$id": "https://schema.fairhub.org/readme.json",
  "title": "README",
  "description": "Additional text here",
  "type": "object",
  "properties": {
    "Title": {
      "type": "string",
      "description": "Name of the dataset"
    },
    "Identifier": {
      "type": "string",
      "pattern": "^10\\.\\d{4,9}/[-._;()/:A-Za-z0-9]+$",
      "description": "A formal identifier that is used to identify this resource in a global registry. Identifiers should be in the form of a resolvable persistent identifier."
    },
    "Version": {
      "type": "string",
      "description": "The version of the resource. This property is used to capture the version of the resource being described. It is recommended to use the Semantic Versioning (SemVer) convention (https://semver.org/)."
    },
    "PublicationDate": {
      "type": "string",
      "pattern": "^(?:\\d{4}|\\d{4}-\\d{2}-\\d{2}|\\d{8}T\\d{2}:\\d{2}:\\d{2}[+-]\\d{2}:\\d{2})$",
      "description": "The date of formal issuance (e.g., publication) of the resource."
    },
    "About": {
      "type": "string",
      "description": "A short high-level description of the resource. This property is used to capture a short description of the resource being described."
    },
    "DatasetDescription": {
      "type": "string",
      "description": "Describe the number of study participants and their characteristics (refer to the participants.json file described in a later section for additional information), the data types collected, the overall number of files and total size of the dataset."
    },
    "DatasetAccess": {
      "type": "string",
      "description": "Describe how the dataset can be accessed and any conditions/restrictions for accessing it."
    },
    "StandardsFollowed": {
      "type": "string",
      "description": "Mention the standards followed to structure the dataset, format the data files, etc. Make sure to include identifiers of the standards when available and/or link to the associated documentation."
    },
    "Resources": {
      "type": "string",
      "description": "Any external resources that may be either required to use the data or useful when using the data (e.g. the project website aireadi.org, the documentation of fairhub.io at docs.fairhub.io, etc.). Make sure to include identifiers and/or links to the resources."
    },
    "License": {
      "type": "string",
      "description": "Brief description of the terms for reusing the data with full name and abbreviation of the license (refer to the LICENSE.txt file for additional details)."
    },
    "HowToCite": {
      "type": "string",
      "description": "Brief description of how to cite the dataset, in APA format (refer to the CITATION.txt file for additional details)."
    },
    "Acknowledgement": {
      "type": "string",
      "description": "Brief description of how to acknowledge the dataset, in APA format (refer to the ACKNOWLEDGEMENT.txt file for additional details)."
    }
  },
  "required": ["Title"]
}
```
