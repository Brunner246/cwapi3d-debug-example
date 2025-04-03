# routes.py
from typing import List, Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1")


# Models
class ActiveElementsResponse(BaseModel):
    count: int = Field(description="Number of active elements")
    element_ids: List[int] = Field(description="List of active element IDs")
    success: bool = Field(default=True, description="Operation success status")


class SearchElementsResponse(BaseModel):
    query: str = Field(description="The search query used")
    count: int = Field(description="Number of matching elements")
    element_ids: List[int] = Field(description="List of matching element IDs")
    success: bool = Field(default=True, description="Operation success status")


# Routes
@router.get("/")
async def root():
    return {"message": "Debug API is running"}


@router.get("/debug/status")
async def debug_status():
    # Debug manager will be passed from main application
    from debug_manager import DebugManager
    debug = DebugManager()
    return {"debug_enabled": debug.debug_enabled}


@router.get("/debug/toggle")
async def toggle_debug():
    from debug_manager import DebugManager
    debug = DebugManager()
    debug.debug_enabled = not debug.debug_enabled
    return {"debug_enabled": debug.debug_enabled}


@router.get("/cadwork/active-elements", response_model=ActiveElementsResponse)
async def get_active_elements():
    import element_controller as ec
    active_elements = ec.get_active_identifiable_element_ids()
    if not active_elements:
        return ActiveElementsResponse(
            count=0,
            element_ids=[],
            success=False,
        )
    return ActiveElementsResponse(
        count=len(active_elements),
        element_ids=active_elements
    )


@router.get("/cadwork/search-elements", response_model=SearchElementsResponse)
async def search_elements(name: Optional[str] = None):
    """
    Search active elements by name
    If no name parameter is provided, returns all active elements

    Example: 'http://127.0.0.1:3030/api/v1/cadwork/search-elements?name=beam'
    """
    import element_controller as ec
    import attribute_controller as ac

    active_elements = ec.get_active_identifiable_element_ids()

    if not name:
        return SearchElementsResponse(
            query="no name provided",
            count=len(active_elements),
            element_ids=active_elements
        )

    matching_elements = [element_id for element_id in active_elements if
                         name.lower() == ac.get_name(element_id).lower()]

    return SearchElementsResponse(
        query=name,
        count=len(matching_elements),
        element_ids=matching_elements
    )