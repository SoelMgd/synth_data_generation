# PII Extraction Task

## Task Description

This task evaluates LLM performance on **Personally Identifiable Information (PII) extraction** from French documents. The model must identify and extract all PII entities from text and return them in a structured JSON format.

## PII Types Supported

- **FIRSTNAME, LASTNAME** - Names (always required)
- **EMAIL, PHONE** - Contact information  
- **DATE, TIME** - Temporal information
- **CITY, STATE, STREET, COUNTY** - Location data
- **IBAN, ACCOUNTNUMBER** - Financial identifiers
- **COMPANYNAME, JOBTITLE, JOBAREA, JOBTYPE** - Professional information
- **USERNAME, PASSWORD, AGE, GENDER** - Personal attributes
- **URL** - Web addresses

## Evaluation Criteria

**Success condition**: The LLM must extract **ALL** ground truth PII entities. Missing any required PII = failure.

**False positives ignored**: Extra PII entities detected by the LLM don't count as errors as the data generator may still have introduced additional PII by itseld.

## Current Performance

**Success rate: 35.71%** (5/14 problems solved correctly)

## Usage

Add your Mistral API key
Generate problems:
```bash
export MISTRAL_API_KEY=<key>
```

Generate problems:
```bash
uv run python -m pii_extraction.generate --num-samples 15 --output pii_extraction/data/problems.json
```

Evaluate LLM:
```bash
uv run python -m pii_extraction.test --problems-file pii_extraction/data/problems.json --verbose
```
