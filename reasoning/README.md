# Reasoning - Sequence Pattern Recognition

## Task Description

This task evaluates LLM performance on mathematical reasoning by analyzing numerical sequences. Given a partial sequence, the model must identify the underlying pattern and write Python code that generates the complete sequence using the discovered formula.

**Success Rate: 20%**

## Sequence Types

### 1. Arithmetic-Geometric Sequences
Combine exponential growth with linear terms:
- `a * r^n + b*n + c` - Exponential base with linear progression
- `a * r^n + b*n` - Simplified version

### 2. Polynomial Sequences
Mathematical polynomials with random coefficients:
- **Quadratic**: `a*n² + b*n + c` - Second-degree polynomials
- **Cubic**: `a*n³ + b*n² + c*n + d` - Third-degree polynomials  
- **Alternating**: Different polynomial formulas for odd/even positions

### 3. Modular Sequences
Use modular arithmetic to create cyclic patterns:
- **Linear Modular**: `(a*n + b) mod m` - Linear function with modulo
- **Quadratic Modular**: `(a*n² + b*n + c) mod m` - Quadratic with modulo
- **Polynomial Modular**: `(a*n² + b*n) mod m + n` - Modulo then addition

## Testing

The LLM must:
1. Analyze the pattern in the given 10-element sequence
2. Write a Python function implementing the mathematical formula
3. Generate exactly 20 elements (not just the 10 shown)
4. Store result in a variable named `result`
5. Use `<python>` and `</python>` tags around the code

## Expected Response Format

```python
<python>
def generate_sequence():
    sequence = []
    for i in range(1, 21):  # Generate 20 elements
        value = 2 * (i**2) + 3 * i + 1
        sequence.append(value)
    return sequence

result = generate_sequence()
</python>
```

## Evaluation

To prevent hardcoding and ensure genuine pattern recognition:

1. LLM sees only the first 10 elements of the sequence
2. LLM must generate 20 elements using its discovered formula
3. Verification compares against the full 20-element sequence

Success condition: The generated code must execute without errors and produce the exact 20-element target sequence.

Verification process:
1. Extract code from `<python>` tags using regex
2. Execute code in safe environment  
3. Compare generated 20-element sequence with expected sequence
4. Success only if sequences match exactly

## Usage

### Generate Problems
```bash
uv run python -m reasoning.generate --num-samples 15 --output reasoning/data/problems.json
```

### Evaluate LLM Performance
Requires `MISTRAL_API_KEY` environment variable:
```bash
export MISTRAL_API_KEY=<your_key>
uv run python -m reasoning.test --problems-file reasoning/data/problems.json --verbose
```