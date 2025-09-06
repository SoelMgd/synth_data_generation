import random
import argparse
from pathlib import Path
from typing import List
from .types import HTMLValidationProblem

def load_html_from_file(file_path: str) -> str:
    """Load HTML content from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"HTML file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading HTML file {file_path}: {e}")

def get_html_template() -> str:
    """Return HTML content from the specified file."""
    html_file_path = Path(__file__).parent / "HTML" / "1.html"
    return load_html_from_file(html_file_path)

def introduce_html_error(valid_html: str) -> str:
    """Introduce a single subtle HTML error."""
    
    error_functions = [
        introduce_unclosed_tag_error,
        introduce_malformed_attribute_error,
        introduce_invalid_nesting_error
    ]
    
    error_function = random.choice(error_functions)
    return error_function(valid_html)

def introduce_unclosed_tag_error(html: str) -> str:
    """Introduce an unclosed tag error."""
    lines = html.split('\n')
    
    tag_lines = []
    for i, line in enumerate(lines):
        if '<div' in line or '<span' in line or '<p' in line or '<section' in line or '<article' in line:
            if not line.strip().endswith('/>') and '</' not in line:
                tag_lines.append(i)
    
    if tag_lines:
        target_line = random.choice(tag_lines)
        line_content = lines[target_line]
        
        if '<div' in line_content:
            tag_name = 'div'
        elif '<span' in line_content:
            tag_name = 'span'
        elif '<p' in line_content:
            tag_name = 'p'
        elif '<section' in line_content:
            tag_name = 'section'
        elif '<article' in line_content:
            tag_name = 'article'
        else:
            return html  # Fallback
        
        closing_tag = f'</{tag_name}>'
        for i in range(target_line + 1, len(lines)):
            if closing_tag in lines[i]:
                lines[i] = lines[i].replace(closing_tag, '', 1)
                break
    
    return '\n'.join(lines)

def introduce_malformed_attribute_error(html: str) -> str:
    """Introduce a malformed attribute error."""
    lines = html.split('\n')
    
    attr_lines = []
    for i, line in enumerate(lines):
        if '="' in line and any(attr in line for attr in ['class=', 'id=', 'src=', 'href=', 'type=', 'name=']):
            attr_lines.append(i)
    
    if attr_lines:
        target_line = random.choice(attr_lines)
        line_content = lines[target_line]
        
        import re
        pattern = r'(\w+)="([^"]*)"'
        match = re.search(pattern, line_content)
        
        if match:
            full_attr = match.group(0)
            broken_attr = full_attr[:-1]
            lines[target_line] = line_content.replace(full_attr, broken_attr, 1)
    
    return '\n'.join(lines)

def introduce_invalid_nesting_error(html: str) -> str:
    """Introduce an invalid nesting error."""
    lines = html.split('\n')
    
    p_lines = []
    for i, line in enumerate(lines):
        if '<p' in line and not line.strip().endswith('/>'):
            p_lines.append(i)
    
    if p_lines:
        target_line = random.choice(p_lines)
        
        for i in range(target_line, min(target_line + 5, len(lines))):
            if lines[i].strip() and not lines[i].strip().startswith('<'):
                content = lines[i].strip()
                if content:
                    lines[i] = lines[i].replace(content, f'<div>{content}</div>', 1)
                    break
    
    return '\n'.join(lines)

def generate_html_validation_problem() -> HTMLValidationProblem:
    """Generate an HTML validation problem (valid or invalid)."""
    
    valid_html = get_html_template()
    
    if random.choice([True, False]):
        return HTMLValidationProblem(
            html_string=valid_html,
            is_valid=True
        )
    else:
        invalid_html = introduce_html_error(valid_html)
        return HTMLValidationProblem(
            html_string=invalid_html,
            is_valid=False
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate HTML validation problems")
    parser.add_argument("--num-samples", type=int, default=5, help="Number of problems to generate")
    parser.add_argument("--output", type=str, help="Output file path")
    
    args = parser.parse_args()
    
    problems = []
    print(f"Generating {args.num_samples} HTML validation problems...")
    
    for i in range(args.num_samples):
        problem = generate_html_validation_problem()
        problems.append(problem.model_dump())
        
        status = "VALID" if problem.is_valid else "INVALID"
        print(f"Problem {i + 1}: {status}")
        print(f"HTML length: {len(problem.html_string)} characters")
        print()
    
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        import json
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(problems, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(problems)} problems to {args.output}")
    else:
        print("Generated problems:")
        print("=" * 50)
        import json
        print(json.dumps(problems, indent=2, ensure_ascii=False)) 