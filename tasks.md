# Synthetic Data Tasks

This project implements three distinct problems and their evaluation tasks for LLMs, each designed to test different capabilities.

## 1. Sequence Reasoning (`reasoning/`)

Task: Analyze mathematical sequences and generate continuation code  
Challenge: Discover underlying patterns in 10-element sequences and write Python code to generate 20 elements  
Success Rate: ~20%  

## 2. PII Extraction (`pii_extraction/`)

Task: Extract Personally Identifiable Information from French documents  
Challenge: Identify and extract all PII entities (names, emails, addresses, etc.) from complex text  
Success Rate: ~36%


## 3. HTML Format Validation (`format_validation/`)

Task: Detect syntax errors in complex HTML documents  
Challenge: Identify subtle HTML syntax errors hidden in realistic, multi-theme web pages  
Success Rate: ~75%  

Each task generates synthetic problems dynamically, ensuring varied difficulty.