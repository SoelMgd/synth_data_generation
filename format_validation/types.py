from typing import Any
from pydantic import BaseModel, Field

class HTMLValidationProblem(BaseModel):
    """Represents an HTML validation problem with an HTML string and its validity."""
    
    html_string: str = Field(..., description="The HTML string to validate")
    is_valid: bool = Field(..., description="Whether the HTML string is syntactically valid")
    
    class Config:
        json_encoders = {
            str: lambda v: v
        } 