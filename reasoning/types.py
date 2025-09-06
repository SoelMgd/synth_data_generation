from typing import List, Any
from pydantic import BaseModel, Field, validator

class CodeProblem(BaseModel):
    """Represents a code generation problem with short and long target sequences."""
    
    sequence_short: List[Any] = Field(..., description="Short sequence (10 elements) shown to LLM")
    sequence_long: List[Any] = Field(..., description="Long sequence (20 elements) for verification")
    description: str = Field(..., description="Human-readable description of the pattern")
    
    @validator('sequence_short')
    def validate_sequence_short_not_empty(cls, v):
        if not v:
            raise ValueError("Short sequence is empty")
        return v
    
    @validator('sequence_long')
    def validate_sequence_long_not_empty(cls, v):
        if not v:
            raise ValueError("Long sequence is empty")
        return v
