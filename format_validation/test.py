import os
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv
from mistralai import Mistral

from .types import HTMLValidationProblem
from .verify import load_problems_from_file, evaluate_all_problems

load_dotenv()

def get_mistral_client() -> Mistral:
    """Initialize and return Mistral client."""
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable is required")
    return Mistral(api_key=api_key)

def create_validation_prompt(html_string: str) -> str:
    """Create prompt for LLM to validate HTML syntax."""
    
    prompt = f"""Analyze the following HTML and determine if it is syntactically valid.

HTML TO VALIDATE:
```html
{html_string}
```

INSTRUCTIONS:
1. Check for proper HTML syntax including:
   - Properly closed tags
   - Correct attribute formatting (quotes around values)
   - Valid nesting (no block elements inside inline elements)
   - No duplicate attributes
   - Proper tag structure

2. Respond with your verdict in the specified format below
3. Only determine if it is syntactically valid as-is

RESPONSE FORMAT:
<verdict>VALID</verdict> or <verdict>INVALID</verdict>

Your analysis and verdict:"""

    return prompt

def validate_html_with_llm(html_string: str, client: Mistral, max_retries: int = 3) -> Optional[str]:
    """Use LLM to validate HTML syntax."""
    prompt = create_validation_prompt(html_string)
    
    for attempt in range(max_retries):
        try:
            response = client.chat.complete(
                model="mistral-medium-latest",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            if response.choices and response.choices[0].message:
                return response.choices[0].message.content.strip()
                
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise
    
    return None

def run_evaluation(problems_file: str, verbose: bool = False) -> Dict:
    """Run evaluation on all problems from a file."""
    problems = load_problems_from_file(problems_file)
    client = get_mistral_client()
    
    print(f"Evaluating {len(problems)} HTML validation problems...")
    
    llm_responses = []
    for i, problem in enumerate(problems):
        print(f"Getting LLM response for problem {i + 1}/{len(problems)}...")
        
        try:
            llm_response = validate_html_with_llm(problem.html_string, client)
            llm_responses.append(llm_response if llm_response else "")
        except Exception as e:
            print(f"Error getting response for problem {i + 1}: {e}")
            llm_responses.append("")
    
    results = evaluate_all_problems(problems, llm_responses)
    
    if verbose:
        for i, (problem, result) in enumerate(zip(problems, results["detailed_results"])):
            print(f"\nProblem {i + 1}:")
            print(f"HTML length: {len(problem.html_string)} characters")
            print(f"Ground truth: {'VALID' if problem.is_valid else 'INVALID'}")
            print(f"Success: {result['success']}")
            if result["details"]:
                llm_verdict = result["details"]["llm_verdict"]
                print(f"LLM verdict: {'VALID' if llm_verdict else 'INVALID' if llm_verdict is not None else 'UNPARSEABLE'}")
                if result["details"]["parsing_error"]:
                    print(f"Parsing error: {result['details']['parsing_error']}")
            if result["error"]:
                print(f"Error: {result['error']}")
            print("-" * 50)
    
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate LLM performance on HTML validation")
    parser.add_argument(
        "--problems-file",
        type=str,
        default="format_validation/data/problems.jsonl",
        help="Path to JSONL file containing HTML validation problems"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed results for each problem"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Save detailed results to JSON file"
    )
    
    args = parser.parse_args()
    
    if not Path(args.problems_file).exists():
        print(f"Error: Problems file {args.problems_file} does not exist")
        print("Generate problems first using: uv run python -m format_validation.generate --num-samples 10")
        exit(1)
    
    results = run_evaluation(args.problems_file, args.verbose)
    
    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)
    print(f"Total problems: {results['total_problems']}")
    print(f"Successful validations: {results['successful']}")
    print(f"Success rate: {results['success_rate']:.2%}")
    print(f"Verdict extraction failures: {results['verdict_extraction_failures']}")
    print(f"API errors: {results['api_errors']}")
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nDetailed results saved to {args.output}") 