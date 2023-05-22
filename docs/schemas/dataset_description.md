# Overview

This page details the input schema required for the `validate_dataset_description` method of the `validate` module and the `generate_dataset_description` method of the `generate` module.

## Parameters

The keys required for this parameter are detailed below:

#### Title

The title of the dataset or study.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | yes      | Any string      |

#### Identifier

The identifier of the dataset or study. Only DOIs are currently supported.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | yes      | Any DOI         |

A regex expression is used to validate the DOI. The expression is `^10\.\d{4,9}/[-._;()/:A-Za-z0-9]+$`.

#### IdentifierType

The type of identifier used. Only DOIs are currently supported.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | yes      | "DOI"           |

#### Subject

A list of keywords or phrases describing the dataset or study.

| Type  | Default value | Required | Accepted values |
| ----- | ------------- | -------- | --------------- |
| Array | None          | no       | Any string      |

Empty arrays are not allowed. At least one keyword or phrase is required if this key is present in the data object.

#### Description

A description of the dataset or study.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | no       | Any string      |

#### Language

The language of the dataset or study. Only two letter ISO 639-1 language codes are currently supported.

| Type   | Default value | Required | Accepted values         |
| ------ | ------------- | -------- | ----------------------- |
| String | None          | no       | Any valid language code |

#### StudyTitle

The title of the study.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | no       | Any string      |

#### StudyID

The ID of the study.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | no       | Any string      |

#### Creator

A list of contributors to the dataset or study.

| Type  | Default value | Required | Accepted values |
| ----- | ------------- | -------- | --------------- |
| Array | None          | no       | -               |

!!! Note

    The  `ContributorName`, `NameType`, and `ContributorType` keys are required for each contributor.

The following keys are accepted for each contributor:

**ContributorName**

The name of the contributor.

**NameType**

The type of name. The following values are accepted:

- Personal
- Organizational

**Affiliation**

The affiliation of the contributor.

**ContributorType**

The type of contributor. The following values are accepted:

- ContactPerson
- DataCollector
- DataCurator
- DataManager
- Distributor
- Editor
- HostingInstitution
- Producer
- ProjectLeader
- ProjectManager
- ProjectMember
- RegistrationAgency
- RegistrationAuthority
- RelatedPerson
- Researcher
- ResearchGroup
- RightsHolder
- Sponsor
- Supervisor
- WorkPackageLeader
- Other

**ORCID**

The ORCID of the contributor.

#### RelatedItem

A list of related items.

| Type  | Default value | Required | Accepted values |
| ----- | ------------- | -------- | --------------- |
| Array | None          | no       | -               |

!!! Note

    The  `RelatedIdentifier`, `RelatedIdentifierType`, `RelatedItemType` and `RelationType` keys are required for each related item.

The following keys are accepted for each related item:

**RelatedIdentifier**

The identifier of the related item. Only DOIs are currently accepted for this field.

**RelatedIdentifierType**

The type of identifier used for the related item. The following values are accepted:

- ARK
- arXiv
- bibcode
- DOI
- EAN13
- EISSN
- Handle
- IGSN
- ISBN
- ISSN
- ISTC
- LISSN
- LSID
- PMID
- PURL
- UPC
- URL
- URN
- w3id

**RelatedItemType**

The type of related item. The following values are accepted:

- Audiovisual
- Book
- BookChapter
- Collection
- ComputationalNotebook
- ConferencePaper
- DataPaper
- Dataset
- Dissertation
- Event
- Image
- InteractiveResource
- Journal
- JournalArticle
- Model
- OutputManagementPlan
- PeerReview
- PhysicalObject
- Preprint
- Report
- Service
- Software
- Sound
- Standard
- Text
- Workflow
- Other

**RelationType**

The type of relation between the dataset or study and the related item. The following values are accepted:

- IsCitedBy
- Cites
- IsSupplementTo
- IsSupplementedBy
- IsContinuedBy
- Continues
- IsDescribedBy
- Describes
- HasMetadata
- IsMetadataFor
- HasVersion
- IsVersionOf
- IsNewVersionOf
- IsPreviousVersionOf
- IsPartOf
- HasPart
- IsPublishedIn
- IsReferencedBy
- References
- IsDocumentedBy
- Documents
- IsCompiledBy
- Compiles
- IsVariantFormOf
- IsOriginalFormOf
- IsIdenticalTo
- IsReviewedBy
- Reviews
- IsDerivedFrom
- IsSourceOf
- IsRequiredBy
- Requires
- IsObsoletedBy

#### FundingReference

A list of funding references.

| Type  | Default value | Required | Accepted values |
| ----- | ------------- | -------- | --------------- |
| Array | None          | no       | -               |

!!! Note

    The  `FunderName` key is required for each funding reference.

The following keys are accepted for each funding reference:

**FunderName**

The name of the funder.

**FunderIdentifier**

The identifier of the funder.

**FunderIdentifierType**

The type of identifier used for the funder. The following values are accepted:

- Crossref Funder ID
- GRID
- ISNI
- ROR
- Other

#### Version

The version of the dataset or study.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | no       | Any string      |

We recommend using [Semantic Versioning](https://semver.org/) for this field.

#### Date

Date of publication of the current version.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | no       | Any valid date  |

The valid formats for this field are:

- YYYY
- YYYY-MM-DD
- YYYYMM-DDThh:mm:ssTZD

#### AccessType

The type of access to the dataset or study.

| Type    | Default value | Required | Accepted values                               |
| ------- | ------------- | -------- | --------------------------------------------- |
| Integer | None          | no       | 12, 11, 20, 13, 14, 15, 16, 17, 18, 19, 90, 0 |

The lookup table for this field can be found here: [http://ecrin-mdr.online/index.php/Object_access_types](http://ecrin-mdr.online/index.php/Object_access_types)

#### Rights

The license or rights statement for the dataset or study.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| Object | None          | no       | -               |

The following keys are accepted for this field:

**RightsURI**

The web URL of the license or rights statement.

**RightsIdentifier**

A short, standardized version of the license name. A list of identifiers for commonly-used licenses may be found here: [https://spdx.org/licenses/](https://spdx.org/licenses/)

Example: CC-BY-3.0

**RightsIdentifierScheme**

The scheme used for the rights identifier.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | None          | no       | SPDX            |

**SchemeURI**

The web URL of the metadata schema used for the dataset or study.

| Type   | Default value | Required | Accepted values            |
| ------ | ------------- | -------- | -------------------------- |
| String | None          | no       | https://spdx.org/licenses/ |

## Data Schema

The full JSON schema for the dataset metadata is as follows.

!!! warning

    There is additional validation performed within the method itself. This schema is only used for validation of the JSON data before it is sent to the method.

```json
{
  "$id": "https://schema.fairhub.org/dataset_description.json",
  "title": "Dataset Description",
  "description": "Additional text here",
  "type": "object",
  "properties": {
    "Title": {
      "type": "string"
    },
    "Identifier": {
      "type": "string",
      "pattern": "^10\\.\\d{4,9}/[-._;()/:A-Za-z0-9]+$"
    },
    "IdentifierType": {
      "type": "string",
      "pattern": "DOI",
      "minLength": 3,
      "maxLength": 3
    },
    "Subject": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "minItems": 1
    },
    "Description": {
      "type": "string"
    },
    "Language": {
      "type": "string",
      "pattern": "^[a-z]{2}$",
      "minLength": 2,
      "maxLength": 2
    },
    "StudyTitle": {
      "type": "string"
    },
    "StudyID": {
      "type": "string"
    },
    "Creator": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "ContributorName": {
            "type": "string"
          },
          "NameType": {
            "type": "string",
            "enum": ["Personal", "Organizational"]
          },
          "Affiliation": {
            "type": "string"
          },
          "ContributorType": {
            "type": "string",
            "enum": [
              "ContactPerson",
              "DataCollector",
              "DataCurator",
              "DataManager",
              "Distributor",
              "Editor",
              "HostingInstitution",
              "Producer",
              "ProjectLeader",
              "ProjectManager",
              "ProjectMember",
              "RegistrationAgency",
              "RegistrationAuthority",
              "RelatedPerson",
              "Researcher",
              "ResearchGroup",
              "RightsHolder",
              "Sponsor",
              "Supervisor",
              "WorkPackageLeader",
              "Other"
            ]
          },
          "ORCID": {
            "type": "string"
          }
        },
        "required": ["ContributorName", "NameType", "ContributorType"]
      },
      "minItems": 1
    },
    "RelatedItem": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "RelatedItemIdentifier": {
            "type": "string",
            "pattern": "^10\\.\\d{4,9}/[-._;()/:A-Za-z0-9]+$"
          },
          "RelatedItemIdentifierType": {
            "type": "string",
            "enum": [
              "ARK",
              "arXiv",
              "bibcode",
              "DOI",
              "EAN13",
              "EISSN",
              "Handle",
              "IGSN",
              "ISBN",
              "ISSN",
              "ISTC",
              "LISSN",
              "LSID",
              "PMID",
              "PURL",
              "UPC",
              "URL",
              "URN",
              "w3id"
            ]
          },
          "RelatedItemType": {
            "type": "string",
            "enum": [
              "Audiovisual",
              "Book",
              "BookChapter",
              "Collection",
              "ComputationalNotebook",
              "ConferencePaper",
              "DataPaper",
              "Dataset",
              "Dissertation",
              "Event",
              "Image",
              "InteractiveResource",
              "Journal",
              "JournalArticle",
              "Model",
              "OutputManagementPlan",
              "PeerReview",
              "PhysicalObject",
              "Preprint",
              "Report",
              "Service",
              "Software",
              "Sound",
              "Standard",
              "Text",
              "Workflow",
              "Other"
            ]
          },
          "RelationType": {
            "type": "string",
            "enum": [
              "IsCitedBy",
              "Cites",
              "IsSupplementTo",
              "IsSupplementedBy",
              "IsContinuedBy",
              "Continues",
              "IsDescribedBy",
              "Describes",
              "HasMetadata",
              "IsMetadataFor",
              "HasVersion",
              "IsVersionOf",
              "IsNewVersionOf",
              "IsPreviousVersionOf",
              "IsPartOf",
              "HasPart",
              "IsPublishedIn",
              "IsReferencedBy",
              "References",
              "IsDocumentedBy",
              "Documents",
              "IsCompiledBy",
              "Compiles",
              "IsVariantFormOf",
              "IsOriginalFormOf",
              "IsIdenticalTo",
              "IsReviewedBy",
              "Reviews",
              "IsDerivedFrom",
              "IsSourceOf",
              "IsRequiredBy",
              "Requires",
              "IsObsoletedBy"
            ]
          }
        },
        "required": [
          "RelatedItemIdentifier",
          "RelatedItemIdentifierType",
          "RelatedItemType",
          "RelationType"
        ]
      }
    },
    "FundingReference": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "FunderName": {
            "type": "string"
          },
          "FunderIdentifier": {
            "type": "string"
          },
          "FunderIdentifierType": {
            "type": "string",
            "enum": ["Crossref Funder ID", "GRID", "ISNI", "ROR", "Other"]
          }
        },
        "required": ["FunderName"],
        "minItems": 1
      }
    },
    "Version": {
      "type": "string",
      "description": "The version of the resource. This property is used to capture the version of the resource being described. It is recommended to use the Semantic Versioning (SemVer) convention (https://semver.org/)."
    },
    "Date": {
      "type": "string",
      "pattern": "^(?:\\d{4}|\\d{4}-\\d{2}-\\d{2}|\\d{8}T\\d{2}:\\d{2}:\\d{2}[+-]\\d{2}:\\d{2})$"
    },
    "AccessType": {
      "type": "integer",
      "description": "The type of  access to the object. The look-up list is available at http://ecrin-mdr.online/index.php/Object_access_types",
      "enum": [12, 11, 20, 13, 14, 15, 16, 17, 18, 19, 90, 0]
    },
    "Rights": {
      "type": "object",
      "properties": {
        "RightsURI": {
          "type": "string",
          "pattern": "^https?://"
        },
        "RightsIdentifier": {
          "type": "string"
        },
        "RightsIdentifierScheme": {
          "type": "string",
          "enum": ["SPDX"]
        },
        "schemeURI": {
          "type": "string",
          "pattern": "https://spdx.org/licenses/"
        }
      }
    }
  },
  "required": ["Title", "Identifier", "IdentifierType"]
}
```
