# HTML Format Validation Task

## Overview

This task evaluates Large Language Models (LLMs) on their ability to detect HTML syntax errors in complex, realistic web pages. The system generates dynamic HTML content across various themes and introduces subtle syntax errors to test the model's validation capabilities.

## Task Description

The LLM is presented with HTML code and must determine whether it is syntactically valid or contains errors. This tests the model's understanding of:

- **HTML syntax rules**: Proper tag opening/closing, attribute formatting
- **Nesting validation**: Correct element hierarchy and structure  
- **Error detection**: Identifying subtle syntax mistakes in complex code
- **Format analysis**: Parsing and understanding structured markup

## Problem Generation

### Dynamic HTML Generation

The system generates realistic HTML pages using 5 different themes:

- **E-commerce**: Product pages with shopping carts, forms, galleries
- **Blog**: Article layouts with navigation, comments, sidebars
- **Corporate**: Business sites with services, teams, contact forms
- **Portfolio**: Creative showcases with galleries, about sections
- **Dashboard**: Analytics interfaces with stats, charts, tables

### HTML Complexity Features

Each generated HTML page includes:

- **Rich metadata**: SEO tags, Open Graph, Schema.org markup
- **Complex navigation**: Multi-level dropdowns, mega menus
- **Interactive forms**: Validation, multiple input types, fieldsets
- **Dynamic content**: Random text, unique IDs, Bootstrap classes
- **Modern structure**: Semantic HTML5, accessibility attributes
- **Embedded scripts**: JavaScript for interactivity and validation

### Error Introduction

For invalid HTML samples, the system introduces **exactly one subtle error** from three categories:

1. **Unclosed Tags**: Removes closing tags like `</div>`, `</section>`
2. **Malformed Attributes**: Removes closing quotes: `class="btn-primary` 
3. **Invalid Nesting**: Creates illegal structures: `<p><div>content</div></p>`

## HTML Validation System

### External Library Validation

The system uses **html5lib** (the same library used by web browsers) to ensure generated HTML is syntactically correct:

- **Standards Compliant**: Validates according to official HTML5 specifications
- **Browser-Grade Parsing**: Uses the same parsing logic as Chrome/Firefox
- **Robust Error Detection**: Identifies real syntax issues that browsers would catch
- **Automatic Fallback**: Falls back to custom validator if html5lib unavailable

### Quality Guarantee Process

1. **Generate HTML**: Create complex, themed HTML content dynamically
2. **Validate with html5lib**: Parse HTML using browser-standard validation
3. **Auto-Regenerate**: If invalid, regenerate up to 3 times automatically
4. **Error Introduction**: Optionally introduce single subtle syntax error
5. **Final Quality Check**: Ensure only valid base HTML is used for problems

### Validation Rules

The system checks for:
- ✅ **Proper tag closure**: All opening tags have matching closing tags
- ✅ **Correct nesting**: Tags are properly nested without overlap
- ✅ **Attribute syntax**: Quotes around attribute values, no duplicates
- ✅ **Self-closing tags**: Proper handling of `<img>`, `<br>`, `<input>`
- ✅ **HTML5 compliance**: Standards-compliant structure and syntax

## Expected LLM Analysis

The LLM should analyze the HTML structure and provide a verdict:

**For Valid HTML:**
```
<verdict>VALID</verdict>
```

**For Invalid HTML:**
```
<verdict>INVALID</verdict>
```

The model should identify syntax errors like missing closing tags, malformed attributes, or invalid nesting while ignoring semantic or accessibility issues.

## Performance Metrics

Current LLM performance on this task:
- **Success Rate**: ~75% (15/20 problems correctly identified)
- **Task Difficulty**: Intermediate to Advanced
- **Average HTML Length**: ~19,600 characters
- **Error Types**: Balanced distribution across all error categories

## Usage

### Generate Problems

```bash
# Generate 10 HTML validation problems (default)
uv run python -m format_validation.generate

# Generate custom number of problems
uv run python -m format_validation.generate --num-samples 20

# Specify output file
uv run python -m format_validation.generate --num-samples 15 --output custom_problems.jsonl
```

### Run Evaluation

```bash
# Evaluate LLM performance (silent mode)
uv run python -m format_validation.test

# Verbose mode with detailed results
uv run python -m format_validation.test --verbose

# Use custom problems file
uv run python -m format_validation.test --problems-file custom_problems.jsonl

# Save results to file
uv run python -m format_validation.test --output evaluation_results.json
```

### Example Output

```
============================================================
EVALUATION SUMMARY
============================================================

Success rate: 80.00%
