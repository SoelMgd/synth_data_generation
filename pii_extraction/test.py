import os
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv
from mistralai import Mistral

from .verify import load_problems_from_file, evaluate_all_problems

load_dotenv()

def get_mistral_client() -> Mistral:
    """Initialize and return Mistral client."""
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable is required")
    return Mistral(api_key=api_key)

def create_extraction_prompt(text: str) -> str:
    """
    Create a prompt for LLM to extract PII from text.
    """
    prompt = f"""Extract all personally identifiable information (PII) from the following French text.

TEXT TO ANALYZE:
{text}

INSTRUCTIONS:
1. Identify ALL personal information in the text
2. Classify each piece of information by type
3. Return ONLY a JSON object in this exact format: {{"PII": {{"ENTITY_TYPE": ["value1", "value2"]}}}}
4. Use these entity types ONLY:
     - FIRSTNAME
     - LASTNAME
     - DATE
     - TIME
     - PHONE
     - USERNAME
     - GENDER
     - CITY
     - STATE
     - URL
     - JOBAREA
     - EMAIL
     - JOBTYPE
     - COMPANYNAME
     - JOBTITLE
     - STREET
     - COUNTY
     - AGE
     - ACCOUNTNAME
     - ACCOUNTNUMBER
     - PASSWORD
     - IBAN

5. Do not include any explanation, only return the JSON
6. If multiple values exist for the same type, put them in a list
7. Be precise and extract exactly what appears in the text

JSON Response:"""

    return prompt

def extract_pii_with_llm(text: str, client: Mistral, max_retries: int = 3) -> Optional[str]:
    """
    Use LLM to extract PII from text.
    """
    prompt = create_extraction_prompt(text)
    
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
                max_tokens=1000
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
    
    print(f"Evaluating {len(problems)} PII extraction problems...")
    
    llm_responses = []
    for i, problem in enumerate(problems):
        print(f"Getting LLM response for problem {i + 1}/{len(problems)}...")
        
        try:
            llm_response = extract_pii_with_llm(problem.text, client)
            llm_responses.append(llm_response if llm_response else "")
        except Exception as e:
            print(f"Error getting response for problem {i + 1}: {e}")
            llm_responses.append("")
    
    results = evaluate_all_problems(problems, llm_responses)
    
    if verbose:
        for i, (problem, result) in enumerate(zip(problems, results["detailed_results"])):
            print(f"\nProblem {i + 1}: {problem.document_type}")
            print(f"Success: {result['success']}")
            if result["details"]:
                print(f"Ground truth: {result['details']['ground_truth']}")
                print(f"Extracted: {result['details']['extracted']}")
                if not result['success']:
                    print(f"Missing: {result['details']['missing_entities']}")
            if result["error"]:
                print(f"Error: {result['error']}")
            print("-" * 50)
    
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate LLM performance on PII extraction")
    parser.add_argument(
        "--problems-file",
        type=str,
        default="pii_extraction/data/problems.json",
        help="Path to JSON file containing PII problems"
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
        print("Generate problems first using: uv run python -m pii_extraction.generate --output pii_extraction/data/problems.json")
        exit(1)
    
    results = run_evaluation(args.problems_file, args.verbose)
    
    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)
    print(f"Total problems: {results['total_problems']}")
    print(f"Successful extractions: {results['successful']}")
    print(f"Success rate: {results['success_rate']:.2%}")
    print(f"Parsing failures: {results['parsing_failures']}")
    print(f"Extraction errors: {results['extraction_errors']}")
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nDetailed results saved to {args.output}") 