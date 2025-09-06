import json
from typing import Dict, List, Optional
from .types import PII, PIIProblem

def parse_llm_response(response: str) -> Optional[PII]:
    """
    Parse LLM response to extract PII entities.
    Expected format: {"PII": {"ENTITY_TYPE": ["value1", "value2", ...]}}
    """
    try:
        response = response.strip()
        
        start_idx = response.find('{')
        end_idx = response.rfind('}')
        
        if start_idx == -1 or end_idx == -1:
            return None
            
        json_str = response[start_idx:end_idx + 1]
        
        parsed = json.loads(json_str)
        
        if "PII" in parsed and isinstance(parsed["PII"], dict):
            pii = PII()
            for entity_type, values in parsed["PII"].items():
                if isinstance(values, list):
                    for value in values:
                        if isinstance(value, str):
                            pii.add_entity(entity_type, value)
                elif isinstance(values, str):
                    pii.add_entity(entity_type, values)
            return pii
            
        return None
        
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"Error parsing LLM response: {e}")
        return None

def compare_pii(ground_truth: PII, extracted: PII) -> bool:
    """
    Check if all ground truth PII entities are included in extracted PII.
    False positives (extra entities) are ignored - only missing entities matter.
    """
    for entity_type, gt_values in ground_truth.entities.items():
        if entity_type not in extracted.entities:
            return False
        
        gt_values_set = set(gt_values)
        ext_values_set = set(extracted.entities[entity_type])
        
        if not gt_values_set.issubset(ext_values_set):
            return False
    
    return True

def verify_solution(problem: PIIProblem, llm_response: str) -> bool:
    """
    Verify if an LLM response correctly solves a PII extraction problem.
    """
    extracted_pii = parse_llm_response(llm_response)
    
    if extracted_pii is None:
        return False
    
    return compare_pii(problem.pii, extracted_pii)

def get_extraction_details(problem: PIIProblem, llm_response: str) -> Dict:
    """
    Get detailed information about PII extraction performance.
    """
    extracted_pii = parse_llm_response(llm_response)
    
    result = {
        "success": False,
        "parsed_successfully": extracted_pii is not None,
        "ground_truth": problem.pii.entities,
        "extracted": extracted_pii.entities if extracted_pii else {},
        "missing_entities": {},
        "incorrect_values": {}
    }
    
    if extracted_pii is None:
        result["missing_entities"] = problem.pii.entities
        return result
    
    for entity_type, gt_values in problem.pii.entities.items():
        if entity_type not in extracted_pii.entities:
            result["missing_entities"][entity_type] = gt_values
        else:
            ext_values = set(extracted_pii.entities[entity_type])
            gt_values_set = set(gt_values)
            missing_values = gt_values_set - ext_values
            if missing_values:
                result["incorrect_values"][entity_type] = {
                    "missing": list(missing_values),
                    "expected": gt_values,
                    "extracted": list(ext_values)
                }
    
    result["success"] = len(result["missing_entities"]) == 0
    
    return result

def load_problems_from_file(file_path: str) -> List[PIIProblem]:
    """Load PII problems from JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    problems = []
    for item in data:
        pii = PII(entities=item['pii']['entities'])
        problem = PIIProblem(
            text=item['text'],
            pii=pii,
            document_type=item.get('document_type', 'unknown')
        )
        problems.append(problem)
    
    return problems

def evaluate_single_problem(problem: PIIProblem, llm_response: str) -> Dict:
    """Evaluate LLM performance on a single PII problem."""
    try:
        if not llm_response:
            return {
                "success": False,
                "error": "Failed to get LLM response",
                "details": None
            }
        
        success = verify_solution(problem, llm_response)
        details = get_extraction_details(problem, llm_response)
        
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

def evaluate_all_problems(problems: List[PIIProblem], llm_responses: List[str]) -> Dict:
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
    
    parsing_failures = sum(1 for r in results if r["details"] and not r["details"]["parsed_successfully"])
    extraction_errors = sum(1 for r in results if r["error"] is not None)
    
    summary = {
        "total_problems": total,
        "successful": successful,
        "success_rate": success_rate,
        "parsing_failures": parsing_failures,
        "extraction_errors": extraction_errors,
        "detailed_results": results
    }
    
    return summary 