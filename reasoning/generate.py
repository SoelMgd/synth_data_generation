import random
import json
import argparse
from pathlib import Path
from typing import List, Any, Tuple
from .types import CodeProblem

def generate_arithmetic_geometric(length_short: int = 10, length_long: int = 20) -> Tuple[List[int], List[int], str]:
    """Generate arithmetic-geometric sequence: a*r^n + b*n + c"""
    a, b, c = random.randint(1, 4), random.randint(1, 3), random.randint(0, 5)
    r = random.randint(2, 3)
    
    sequence_short = [a * (r**i) + b * i + c for i in range(1, length_short + 1)]
    sequence_long = [a * (r**i) + b * i + c for i in range(1, length_long + 1)]
    description = f"Arithmetic-geometric: {a} * {r}^n + {b}n + {c}"
    return sequence_short, sequence_long, description

def generate_quadratic_polynomial(length_short: int = 10, length_long: int = 20) -> Tuple[List[int], List[int], str]:
    """Generate quadratic polynomial: an² + bn + c"""
    a, b, c = random.randint(1, 4), random.randint(-3, 4), random.randint(0, 6)
    
    sequence_short = [a * (i**2) + b * i + c for i in range(1, length_short + 1)]
    sequence_long = [a * (i**2) + b * i + c for i in range(1, length_long + 1)]
    description = f"Quadratic polynomial: {a}n² + {b}n + {c}"
    return sequence_short, sequence_long, description

def generate_cubic_polynomial(length_short: int = 10, length_long: int = 20) -> Tuple[List[int], List[int], str]:
    """Generate cubic polynomial: an³ + bn² + cn + d"""
    a, b, c, d = random.randint(1, 2), random.randint(-2, 3), random.randint(-2, 3), random.randint(0, 5)
    
    sequence_short = [a * (i**3) + b * (i**2) + c * i + d for i in range(1, length_short + 1)]
    sequence_long = [a * (i**3) + b * (i**2) + c * i + d for i in range(1, length_long + 1)]
    description = f"Cubic polynomial: {a}n³ + {b}n² + {c}n + {d}"
    return sequence_short, sequence_long, description

def generate_modular_linear(length_short: int = 10, length_long: int = 20) -> Tuple[List[int], List[int], str]:
    """Generate modular linear: (an + b) mod m"""
    a, b = random.randint(2, 6), random.randint(1, 5)
    mod_val = random.randint(5, 10)
    
    sequence_short = [(a * i + b) % mod_val for i in range(1, length_short + 1)]
    sequence_long = [(a * i + b) % mod_val for i in range(1, length_long + 1)]
    description = f"Modular linear: ({a}n + {b}) mod {mod_val}"
    return sequence_short, sequence_long, description

def generate_modular_quadratic(length_short: int = 10, length_long: int = 20) -> Tuple[List[int], List[int], str]:
    """Generate modular quadratic: (an² + bn + c) mod m"""
    a, b, c = random.randint(1, 3), random.randint(1, 4), random.randint(0, 3)
    mod_val = random.randint(6, 12)
    
    sequence_short = [(a * (i**2) + b * i + c) % mod_val for i in range(1, length_short + 1)]
    sequence_long = [(a * (i**2) + b * i + c) % mod_val for i in range(1, length_long + 1)]
    description = f"Modular quadratic: ({a}n² + {b}n + {c}) mod {mod_val}"
    return sequence_short, sequence_long, description

def generate_geometric_plus_linear(length_short: int = 10, length_long: int = 20) -> Tuple[List[int], List[int], str]:
    """Generate geometric plus linear: a*r^n + bn"""
    a, b = random.randint(1, 3), random.randint(1, 4)
    r = random.randint(2, 3)
    
    sequence_short = [a * (r**i) + b * i for i in range(1, length_short + 1)]
    sequence_long = [a * (r**i) + b * i for i in range(1, length_long + 1)]
    description = f"Geometric plus linear: {a} * {r}^n + {b}n"
    return sequence_short, sequence_long, description

def generate_polynomial_modular(length_short: int = 10, length_long: int = 20) -> Tuple[List[int], List[int], str]:
    """Generate polynomial with modular result: (an² + bn) mod m + n"""
    a, b = random.randint(1, 4), random.randint(1, 3)
    mod_val = random.randint(5, 9)
    
    sequence_short = [(a * (i**2) + b * i) % mod_val + i for i in range(1, length_short + 1)]
    sequence_long = [(a * (i**2) + b * i) % mod_val + i for i in range(1, length_long + 1)]
    description = f"Polynomial modular: ({a}n² + {b}n) mod {mod_val} + n"
    return sequence_short, sequence_long, description

def generate_alternating_polynomial(length_short: int = 10, length_long: int = 20) -> Tuple[List[int], List[int], str]:
    """Generate alternating polynomial: an² + bn for odd n, cn + d for even n"""
    a, b, c, d = random.randint(1, 3), random.randint(1, 4), random.randint(2, 5), random.randint(0, 3)
    
    def compute_value(i):
        if i % 2 == 1:
            return a * (i**2) + b * i
        else:
            return c * i + d
    
    sequence_short = [compute_value(i) for i in range(1, length_short + 1)]
    sequence_long = [compute_value(i) for i in range(1, length_long + 1)]
    description = f"Alternating polynomial: {a}n² + {b}n for odd n, {c}n + {d} for even n"
    return sequence_short, sequence_long, description

GENERATORS = [
    generate_arithmetic_geometric,
    generate_quadratic_polynomial,
    generate_cubic_polynomial,
    generate_modular_linear,
    generate_modular_quadratic,
    generate_geometric_plus_linear,
    generate_polynomial_modular,
    generate_alternating_polynomial,
]

def generate_code_problem() -> CodeProblem:
    """Generate a random code generation problem."""
    generator = random.choice(GENERATORS)
    sequence_short, sequence_long, description = generator()
    
    return CodeProblem(
        sequence_short=sequence_short,
        sequence_long=sequence_long,
        description=description
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate code generation problems")
    parser.add_argument("--num-samples", type=int, default=5, help="Number of problems to generate")
    parser.add_argument("--output", type=str, help="Output file path")
    
    args = parser.parse_args()
    
    problems = []
    print(f"Generating {args.num_samples} code generation problems...")
    
    for i in range(args.num_samples):
        problem = generate_code_problem()
        problems.append(problem.model_dump())
        print(f"Problem {i + 1}: {problem.description}")
        print(f"Short sequence (shown to LLM): {problem.sequence_short}")
        print(f"Long sequence (for verification): {problem.sequence_long}")
        print()
    
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(problems, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(problems)} problems to {args.output}")
    else:
        print("Generated problems:")
        print("=" * 50)
        print(json.dumps(problems, indent=2, ensure_ascii=False)) 