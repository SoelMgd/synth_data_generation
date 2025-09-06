"""
Data models for PII masking problems using Pydantic.
"""

from typing import Dict, List
from pydantic import BaseModel, Field, validator

class PII(BaseModel):
    """
    Represents PII entities as a dictionary mapping entity types to lists of values.
    
    Example:
        {
            "FIRSTNAME": ["Jean", "Marie"],
            "LASTNAME": ["Dupont"],
            "EMAIL": ["jean.dupont@example.com", "marie.dupont@gmail.com"],
            "PHONE": ["01 23 45 67 89"]
        }
    """
    entities: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Dictionary mapping PII entity types to lists of their values"
    )
    
    @validator('entities')
    def validate_entities_structure(cls, v):
        """Validate that all values in the dictionary are lists of strings."""
        if not isinstance(v, dict):
            raise ValueError("entities must be a dictionary")
        
        for entity_type, values in v.items():
            if not isinstance(entity_type, str):
                raise ValueError(f"Entity type must be string, got {type(entity_type)}")
            if not isinstance(values, list):
                raise ValueError(f"Values for {entity_type} must be a list, got {type(values)}")
            if not all(isinstance(val, str) for val in values):
                raise ValueError(f"All values for {entity_type} must be strings")
        
        return v
    
    def add_entity(self, entity_type: str, value: str) -> None:
        """Add a PII entity value to the collection."""
        if entity_type not in self.entities:
            self.entities[entity_type] = []
        if value not in self.entities[entity_type]:  # Avoid duplicates
            self.entities[entity_type].append(value)
    
    def get_entity_types(self) -> List[str]:
        """Get all entity types present in this PII collection."""
        return list(self.entities.keys())
    
    def get_all_values(self) -> List[str]:
        """Get all PII values as a flat list."""
        all_values = []
        for values in self.entities.values():
            all_values.extend(values)
        return all_values
    
    def has_name(self) -> bool:
        """Check if the PII contains both FIRSTNAME and LASTNAME."""
        return "FIRSTNAME" in self.entities and "LASTNAME" in self.entities
    
    def count_total_entities(self) -> int:
        """Count the total number of PII values across all types."""
        return sum(len(values) for values in self.entities.values())

class PIIProblem(BaseModel):
    """
    Represents a complete PII masking problem with text and ground truth PII.
    
    This is used for both training data generation and evaluation.
    The 'text' field contains the document text with PII embedded.
    The 'pii' field contains the ground truth PII that should be extracted.
    """
    text: str = Field(
        ...,
        description="The document text containing embedded PII information"
    )
    pii: PII = Field(
        ...,
        description="Ground truth PII entities that should be extracted from the text"
    )
    document_type: str = Field(
        default="unknown",
        description="Type of document (e.g., 'letter', 'medical', 'financial')"
    )
    
    @validator('text')
    def validate_text_not_empty(cls, v):
        """Ensure text is not empty."""
        if not v or not v.strip():
            raise ValueError("Text cannot be empty")
        return v.strip()
    
    @validator('pii')
    def validate_pii_constraints(cls, v):
        """Validate PII constraints (must have both FIRSTNAME and LASTNAME, 2-10 total entities)."""
        if not v.has_name():
            raise ValueError("PII must contain both FIRSTNAME and LASTNAME")
        
        total_entities = v.count_total_entities()
        if total_entities < 2 or total_entities > 10:
            raise ValueError(f"PII must contain between 2 and 10 entities, got {total_entities}")
        
        return v
    
    def get_pii_summary(self) -> str:
        """Get a human-readable summary of the PII in this sample."""
        summary_parts = []
        for entity_type, values in self.pii.entities.items():
            if len(values) == 1:
                summary_parts.append(f"{entity_type}: {values[0]}")
            else:
                summary_parts.append(f"{entity_type}: {', '.join(values)}")
        return "; ".join(summary_parts)
    
    def verify_pii_in_text(self) -> Dict[str, List[str]]:
        """
        Verify which PII values are actually present in the text.
        Returns a dictionary of entity_type -> list of found values.
        """
        found_pii = {}
        text_lower = self.text.lower()
        
        for entity_type, values in self.pii.entities.items():
            found_values = []
            for value in values:
                if value.lower() in text_lower:
                    found_values.append(value)
            if found_values:
                found_pii[entity_type] = found_values
        
        return found_pii
    
    def get_missing_pii(self) -> Dict[str, List[str]]:
        """
        Get PII values that are supposed to be in the text but are missing.
        Returns a dictionary of entity_type -> list of missing values.
        """
        found_pii = self.verify_pii_in_text()
        missing_pii = {}
        
        for entity_type, expected_values in self.pii.entities.items():
            found_values = found_pii.get(entity_type, [])
            missing_values = [val for val in expected_values if val not in found_values]
            if missing_values:
                missing_pii[entity_type] = missing_values
        
        return missing_pii 