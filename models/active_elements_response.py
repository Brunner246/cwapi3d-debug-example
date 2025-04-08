from typing import List

from pydantic import BaseModel, Field

class ActiveElementsResponse(BaseModel):
    count: int = Field(description="Number of active elements")
    element_ids: List[int] = Field(description="List of active element IDs")
    success: bool = Field(default=True, description="Operation success status")