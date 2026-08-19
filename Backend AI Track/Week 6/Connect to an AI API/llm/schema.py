from enum import Enum
from pydantic import BaseModel, Field

class CanonicalTitle(str, Enum):
    software_engineer = "software_engineer"
    senior_software_engineer = "senior_software_engineer"
    staff_engineer = "staff_engineer"
    engineering_manager = "engineering_manager"
    product_manager = "product_manager"
    data_scientist = "data_scientist"
    designer = "designer"
    other = "other"

class NormalizeInput(BaseModel):
    title: str = Field(min_length=1, max_length=100)

class NormalizeOutput(BaseModel):
    canonical_title: CanonicalTitle
    confidence: float = Field(ge=0.0, le=1.0)
    original: str