from typing import List

from pydantic import BaseModel, Field

class SearchElementsResponse(BaseModel):
    query: str = Field(description="The search query used")
    count: int = Field(description="Number of matching elements")
    element_ids: List[int] = Field(description="List of matching element IDs")
    success: bool = Field(default=True, description="Operation success status")
