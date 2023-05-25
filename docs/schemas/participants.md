# Overview

This page details the input schema required for the `validate_participants` method of the `validate` module and the `generate_participants` method of the `generate` module.

## Parameters

A top level array of valid participants is expected as a paramenter. Each participant should be an object with the following properties:

### participant_id

A participant identifier of the form sub-'label', matching a participant entity found in the dataset. Values in participant_id MUST be unique.

| Type   | Default value | Required | Accepted values                    |
| ------ | ------------- | -------- | ---------------------------------- |
| String | None          | yes      | sub-'label' where label is your id |

### species

The species column SHOULD be a binomial species name from the NCBI Taxonomy (for example, `homo sapiens`, `mus musculus`, `rattus norvegicus`). For backwards compatibility, if species is absent, the participant is assumed to be homo sapiens.

| Type   | Default value  | Required | Accepted values              |
| ------ | -------------- | -------- | ---------------------------- |
| String | 'homo sapiens' | no       | Any value from NCBI Taxonomy |

### age

The age of the subject in terms of years. Decimal numbers are also accepted in this field.

| Type   | Default value | Required | Accepted values                  |
| ------ | ------------- | -------- | -------------------------------- |
| Number | 0             | no       | Any numeric value greater than 0 |

### sex

String value indicating phenotypical sex, one of `male`, `female`, `other`.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | ""            | no       | Valid string    |

The following values are accepted:

- male
- m
- M
- MALE
- Male
- female
- f
- F
- FEMALE
- Female
- other
- o
- O
- OTHER
- Other

### handedness

String value indicating one of `left`, `right`, `ambidextrous`.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | ""            | no       | Valid string    |

The following values are accepted:

- left
- l
- L
- LEFT
- Left
- right
- r
- R
- RIGHT
- Right
- ambidextrous
- a
- A
- AMBIDEXTROUS
- Ambidextrous

### strain

For species different from homo sapiens, string value indicating the strain of the species, for example: `C57BL/6J`.

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | ""            | no       | Valid string    |

### strain_rrid

For species different from homo sapiens, research resource identifier (RRID) of the strain of the species, for example: `RRID:IMSR_JAX:000664`

| Type   | Default value | Required | Accepted values |
| ------ | ------------- | -------- | --------------- |
| String | ""            | no       | Valid string    |
