# HTML Format Validation Task

## Overview

This task evaluates LLM on their ability to detect HTML syntax errors in complex web pages. The system generates dynamic HTML content across various themes and introduces subtle syntax errors to test the model's validation capabilities.

Success Rate**: ~75%

## Task Description

The LLM is presented with HTML code and must determine whether it is syntactically valid or contains errors. This tests the model's understanding of:

## Problem Generation

### Dynamic HTML Generation

The system generates realistic HTML pages using 5 different themes:

- E-commerce: Product pages with shopping carts, forms, galleries
- Blog: Article layouts with navigation, comments, sidebars
- Corporate: Business sites with services, teams, contact forms
- Portfolio: Creative showcases with galleries, about sections
- Dashboard: Analytics interfaces with stats, charts, tables


### Error Introduction

For invalid HTML samples, the system introduces one subtle error from three categories:

1. Unclosed Tags: Removes closing tags like `</div>`, `</section>`
2. Malformed Attributes: Removes closing quotes: `class="btn-primary` 
3. Invalid Nesting: Creates illegal structures: `<p><div>content</div></p>`

## HTML Validation System

### External Library Validation

The system uses html5lib (the same library used by web browsers) to ensure generated HTML is syntactically correct

### Quality Guarantee Process

1. Generate HTML: Create complex, themed HTML content dynamically
2. Validate with html5lib: Parse HTML using browser-standard validation
3. Auto-Regenerate: If invalid, regenerate up to 3 times automatically
4. Error Introduction: Optionally introduce single subtle syntax error


## Usage



```bash
uv run python -m format_validation.generate
uv run python -m format_validation.test --output evaluation_results.json
```