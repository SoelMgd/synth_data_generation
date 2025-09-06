import os
import re
import json
import random
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv
from mistralai import Mistral

from .types import PII, PIIProblem
from .random_pii import generate_random_pii, get_available_pii_types

load_dotenv()


DOCUMENT_TYPES = {
    "letter": "A part of an administrative or commercial letter",
    "medical": "A part of a medical or health document",
    "financial": "A part of a financial or banking document", 
    "contract": "A part of a job contract or legal document",
}

def get_mistral_client() -> Mistral:
    """Initialize and return Mistral client."""
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable is required")
    return Mistral(api_key=api_key)

def select_pii_types() -> List[str]:
    """
    Select random PII types respecting constraints:
    - Between 1 and 10 total PII values
    - Must include at least FIRSTNAME AND LASTNAME
    """
    available_types = get_available_pii_types()
    

    selected_types = ["FIRSTNAME", "LASTNAME"]
    
    num_additional = random.randint(0, 8)
    if num_additional > 0:
        additional_types = random.sample(
            available_types, 
            min(num_additional, len(available_types))
        )
        selected_types.extend(additional_types)
    
    return selected_types

def generate_pii_values(pii_types: List[str]) -> Dict[str, List[str]]:
    """
    Generate PII values for the selected types.
    """
    pii_values = {}
    
    for pii_type in pii_types:
        value = generate_random_pii(pii_type)
        pii_values[pii_type] = [value]
    
    return pii_values

def create_prompt(document_type: str, pii_values: Dict[str, List[str]]) -> str:
    """Create a prompt for Mistral to generate a document with PII."""
        
    pii_list = []
    for entity_type, values in pii_values.items():
        for value in values:
            pii_list.append(f"- {value}")
    
    pii_instructions = "\n".join(pii_list)
    
    all_pii_types = """
PERSONAL IDENTIFIERS that exist and should NOT be added unless specified:
- PREFIX (titles like M., Mme, Dr)
- FIRSTNAME (first names)
- LASTNAME (last names) 
- DATE (dates in DD/MM/YYYY format)
- TIME (times in HH:MM format)
- PHONE (phone numbers)
- USERNAME (usernames)
- GENDER (gender information)
- CITY (city names)
- STATE (regions/states)
- URL (web addresses)
- JOBAREA (job fields)
- EMAIL (email addresses)
- JOBTYPE (job contract types)
- COMPANYNAME (company names)
- JOBTITLE (job titles)
- STREET (street addresses)
- COUNTY (departments/counties)
- AGE (age numbers)
- ACCOUNTNAME (account names)
- ACCOUNTNUMBER (account numbers)
- PASSWORD (passwords)
- IBAN (bank account numbers)
"""
    
    prompt = f"""Create {DOCUMENT_TYPES[document_type]} in French which naturally contains ONLY the following personal information :

{pii_instructions}

{all_pii_types}

CRITICAL INSTRUCTIONS :
1. The text must be realistic and consistent, written in natural flowing French
2. Integrate ALL and ONLY the information listed above naturally into sentences
3. Use EXACTLY the values provided (do not modify them)
4. Write in French correctly and professionally
5. DO NOT ADD ANY OTHER PERSONAL INFORMATION beyond what is listed above
6. DO NOT invent additional names, emails, phones, addresses, or any other PII
7. DO NOT use placeholder tags like [Date], [Nom], [JJ/MM/AAAA], [Montant], etc.
8. DO NOT use anonymized fields or brackets for missing information
9. DO NOT write like a form with "Date:", "Nom:", etc. - write in natural sentences
10. If you need to reference people or places not in the list, use generic terms like "l'entreprise", "le service", "notre équipe", "la société"
11. Avoid mentioning specific information you don't have - rephrase sentences to work around missing details
12. Write flowing, natural text that doesn't look like a template or form

WRONG examples (DO NOT do this):
- "Date : [JJ/MM/AAAA]" 
- "Nom : **Marie Dubois**"
- "Montant : [À compléter]"
- "Référence : [Numéro de dossier]"

CORRECT example for "Marie", "Dubois", "marie.dubois@example.com":
"Madame Marie Dubois,
Nous accusons réception de votre demande et vous remercions de votre confiance. Notre équipe a bien pris en compte votre dossier. Pour toute question, n'hésitez pas à nous contacter à l'adresse marie.dubois@example.com. Nous restons à votre disposition pour vous accompagner dans vos démarches."

Generate the requested document :"""
    
    return prompt

def verify_pii_in_text(text: str, pii_values: Dict[str, List[str]]) -> Tuple[bool, Dict[str, List[str]]]:
    """
    Verify that all PII values are present in the generated text.
    Returns (all_found, missing_pii).
    """
    text_lower = text.lower()
    missing_pii = {}
    
    for entity_type, values in pii_values.items():
        missing_values = []
        for value in values:
            escaped_value = re.escape(value.lower())
            if not re.search(escaped_value, text_lower):
                missing_values.append(value)
        
        if missing_values:
            missing_pii[entity_type] = missing_values
    
    all_found = len(missing_pii) == 0
    return all_found, missing_pii

def generate_text_with_mistral(prompt: str, client: Mistral, max_retries: int = 3) -> Optional[str]:
    """Generate text using Mistral API with retries."""
    
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
                temperature=0.7,
                max_tokens=500
            )
            
            if response.choices and response.choices[0].message:
                return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise
    
    return None

def generate_pii_problem(max_retries: int = 3) -> PIIProblem:
    """
    Generate a complete PII masking problem.
    
    Returns:
        PIIProblem with text containing PII and ground truth labels
    """
    client = get_mistral_client()
    
    for attempt in range(max_retries):
        try:
            document_type = random.choice(list(DOCUMENT_TYPES.keys()))
            
            pii_types = select_pii_types()
            
            pii_values = generate_pii_values(pii_types)
            
            total_values = sum(len(values) for values in pii_values.values())
            if total_values < 2 or total_values > 10:
                continue
            
            prompt = create_prompt(document_type, pii_values)
            
            generated_text = generate_text_with_mistral(prompt, client)
            if not generated_text:
                continue
            
            all_found, missing_pii = verify_pii_in_text(generated_text, pii_values)
            
            if all_found:
                pii_obj = PII()
                for entity_type, values in pii_values.items():
                    for value in values:
                        pii_obj.add_entity(entity_type, value)
                
                return PIIProblem(
                    text=generated_text,
                    pii=pii_obj,
                    document_type=document_type
                )
            else:
                print(f"Attempt {attempt + 1}: Missing PII in generated text: {missing_pii}")
                
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
    
    raise Exception(f"Failed to generate valid PII problem after {max_retries} attempts")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate PII masking problems")
    parser.add_argument(
        "--num-samples", 
        type=int, 
        default=3, 
        help="Number of problems to generate (default: 3)"
    )
    parser.add_argument(
        "--output", 
        type=str, 
        help="Output file path (default: print to stdout)"
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=3,
        help="Maximum retries per problem (default: 3)"
    )
    
    args = parser.parse_args()
    
    problems = []
    print(f"Generating {args.num_samples} PII masking problems...")
    
    for i in range(args.num_samples):
        try:
            print(f"Generating problem {i + 1}/{args.num_samples}...")
            problem = generate_pii_problem(max_retries=args.max_retries)
            problems.append(problem.model_dump())
            print(f"  Problem {i + 1} generated successfully")
            print(f"  Document type: {problem.document_type}")
            print(f"  PII summary: {problem.get_pii_summary()}")
            print()
        except Exception as e:
            print(f"✗ Failed to generate problem {i + 1}: {e}")
    
    if problems:
        output_json = json.dumps(problems, indent=2, ensure_ascii=False)
        
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output_json)
            print(f"Generated {len(problems)} problems and saved to {args.output}")
        else:
            print("Generated problems:")
            print("=" * 50)
            print(output_json)
    else:
        print("No problems were generated successfully.") 