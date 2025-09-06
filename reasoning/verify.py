import re
import json
from typing import Optional, List, Any, Dict
from pathlib import Path
from .types import CodeProblem

def extract_python_code(llm_response: str) -> Optional[str]:
    """Extract Python code from LLM response using regex."""
    pattern = r'<python>(.*?)</python>'
    matches = re.findall(pattern, llm_response, re.DOTALL)
    
    if not matches:
        return None
    
    return matches[0].strip()

def execute_code_safely(code: str) -> Optional[List[Any]]:
    """Execute Python code safely and return the result."""
    try:
        local_vars = {}
        exec(code, {}, local_vars)
        
        if 'result' not in local_vars:
            return None
        
        return local_vars['result']
        
    except Exception:
        return None

def verify_solution(problem: CodeProblem, llm_response: str) -> bool:
    """Verify if LLM response correctly solves the code generation problem."""
    python_code = extract_python_code(llm_response)
    
    if python_code is None:
        return False
    
    generated_sequence = execute_code_safely(python_code)
    
    if generated_sequence is None:
        return False
    
    return generated_sequence == problem.sequence_long

def get_verification_details(problem: CodeProblem, llm_response: str) -> dict:
    """Get detailed verification results."""
    python_code = extract_python_code(llm_response)
    
    result = {
        "success": False,
        "code_extracted": python_code is not None,
        "extracted_code": python_code,
        "expected_sequence": problem.sequence_long,
        "generated_sequence": None,
        "execution_error": None
    }
    
    if python_code is None:
        result["execution_error"] = "No Python code found in <python> tags"
        return result
    
    try:
        local_vars = {}
        exec(python_code, {}, local_vars)
        
        if 'result' not in local_vars:
            result["execution_error"] = "No 'result' variable found"
            return result
        
        generated_sequence = local_vars['result']
        result["generated_sequence"] = generated_sequence
        result["success"] = generated_sequence == problem.sequence_long
        
    except Exception as e:
        result["execution_error"] = str(e)
    
    return result

def load_problems_from_file(file_path: str) -> List[CodeProblem]:
    """Load code generation problems from JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    problems = []
    for item in data:
        problem = CodeProblem(
            sequence_short=item['sequence_short'],
            sequence_long=item['sequence_long'],
            description=item['description']
        )
        problems.append(problem)
    
    return problems

def evaluate_single_problem(problem: CodeProblem, llm_response: str) -> Dict:
    """Evaluate LLM performance on a single code generation problem."""
    try:
        if not llm_response:
            return {
                "success": False,
                "error": "Failed to get LLM response",
                "details": None
            }
        
        success = verify_solution(problem, llm_response)
        details = get_verification_details(problem, llm_response)
        
        return {
            "success": success,
            "error": None,
            "details": details,
            "llm_response": llm_response
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "details": None
        }

def evaluate_all_problems(problems: List[CodeProblem], llm_responses: List[str]) -> Dict:
    """Evaluate LLM performance on all problems."""
    results = []
    successful = 0
    total = len(problems)
    
    for i, (problem, llm_response) in enumerate(zip(problems, llm_responses)):
        result = evaluate_single_problem(problem, llm_response)
        results.append(result)
        
        if result["success"]:
            successful += 1
    
    success_rate = successful / total if total > 0 else 0
    
    code_extraction_failures = sum(1 for r in results if r["details"] and not r["details"]["code_extracted"])
    execution_errors = sum(1 for r in results if r["details"] and r["details"]["execution_error"])
    api_errors = sum(1 for r in results if r["error"] is not None)
    
    summary = {
        "total_problems": total,
        "successful": successful,
        "success_rate": success_rate,
        "code_extraction_failures": code_extraction_failures,
        "execution_errors": execution_errors,
        "api_errors": api_errors,
        "detailed_results": results
    }
    
    return summary 