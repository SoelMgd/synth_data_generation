import json
import re
from typing import Dict, List, Optional
from html.parser import HTMLParser
from .types import HTMLValidationProblem

class HTMLValidator(HTMLParser):
    """Custom HTML parser to validate HTML syntax."""
    
    def __init__(self):
        super().__init__()
        self.errors = []
        self.tag_stack = []
        
    def error(self, message):
        self.errors.append(message)
        
    def handle_starttag(self, tag, attrs):
        # Check for malformed attributes
        for attr_name, attr_value in attrs:
            if attr_value is None:
                continue
        
        # Track opening tags (except self-closing ones)
        if tag not in ['img', 'br', 'hr', 'input', 'meta', 'link']:
            self.tag_stack.append(tag)
    
    def handle_endtag(self, tag):
        if not self.tag_stack:
            self.errors.append(f"Unexpected closing tag: {tag}")
            return
            
        if self.tag_stack[-1] == tag:
            self.tag_stack.pop()
        else:
            # Check if tag exists somewhere in stack (invalid nesting)
            if tag in self.tag_stack:
                self.errors.append(f"Invalid nesting: {tag}")
            else:
                self.errors.append(f"Unmatched closing tag: {tag}")

def is_html_valid(html_string: str) -> bool:
    """Check if an HTML string is syntactically valid."""
    try:
        validator = HTMLValidator()
        validator.feed(html_string)
        
        # Check for unclosed tags
        if validator.tag_stack:
            return False
            
        # Check for parsing errors
        if validator.errors:
            return False
            
        return True
        
    except Exception:
        return False

def parse_llm_verdict(llm_response: str) -> Optional[bool]:
    """Parse LLM response to extract verdict from <verdict> tags."""
    pattern = r'<verdict>(.*?)</verdict>'
    matches = re.findall(pattern, llm_response, re.IGNORECASE | re.DOTALL)
    
    if not matches:
        return None
    
    verdict = matches[0].strip().upper()
    
    if verdict == "VALID":
        return True
    elif verdict == "INVALID":
        return False
    else:
        return None

def verify_solution(problem: HTMLValidationProblem, llm_response: str) -> bool:
    """Verify if LLM response correctly identifies HTML validity."""
    ground_truth = problem.is_valid
    llm_verdict = parse_llm_verdict(llm_response)
    
    if llm_verdict is None:
        return False
    
    return ground_truth == llm_verdict

def get_validation_details(problem: HTMLValidationProblem, llm_response: str) -> Dict:
    """Get detailed validation results."""
    ground_truth = problem.is_valid
    llm_verdict = parse_llm_verdict(llm_response)
    
    result = {
        "success": False,
        "verdict_extracted": llm_verdict is not None,
        "ground_truth": ground_truth,
        "llm_verdict": llm_verdict,
        "html_length": len(problem.html_string),
        "parsing_error": None
    }
    
    if llm_verdict is None:
        result["parsing_error"] = "No verdict found in <verdict> tags or invalid verdict format"
        return result
    
    result["success"] = ground_truth == llm_verdict
    
    return result

def load_problems_from_file(file_path: str) -> List[HTMLValidationProblem]:
    """Load HTML validation problems from file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    problems = []
    for item in data:
        problem = HTMLValidationProblem(
            html_string=item['html_string'],
            is_valid=item['is_valid']
        )
        problems.append(problem)
    
    return problems

def evaluate_single_problem(problem: HTMLValidationProblem, llm_response: str) -> Dict:
    """Evaluate LLM performance on a single HTML validation problem."""
    try:
        if not llm_response:
            return {
                "success": False,
                "error": "Failed to get LLM response",
                "details": None
            }
        
        success = verify_solution(problem, llm_response)
        details = get_validation_details(problem, llm_response)
        
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

def evaluate_all_problems(problems: List[HTMLValidationProblem], llm_responses: List[str]) -> Dict:
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
    
    verdict_extraction_failures = sum(1 for r in results if r["details"] and not r["details"]["verdict_extracted"])
    api_errors = sum(1 for r in results if r["error"] is not None)
    
    summary = {
        "total_problems": total,
        "successful": successful,
        "success_rate": success_rate,
        "verdict_extraction_failures": verdict_extraction_failures,
        "api_errors": api_errors,
        "detailed_results": results
    }
    
    return summary 