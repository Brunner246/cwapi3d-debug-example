# routes.py
from typing import Optional

from fastapi import APIRouter

from models.active_elements_response import ActiveElementsResponse
from models.search_elements_response import SearchElementsResponse

router = APIRouter(prefix="/api/v1")

# see OPENAPI_DOCS via http://localhost:3030/docs

@router.get("/")
async def root():
    return {"message": "Debug API is running"}


@router.get("/cadwork/toggle-render-mode")
async def toggle_render_mode():
    import visualization_controller as vc
    from models.render_state import RenderState

    render_state = RenderState.get_instance()

    if not render_state.is_wireframe:
        vc.show_view_wireframe()
        render_state.is_wireframe = True
        current_mode = "wireframe"
    else:
        vc.show_view_shaded2()
        render_state.is_wireframe = False
        current_mode = "shaded2"

    return {
        "success": True,
        "current_mode": current_mode
    }


@router.get("/debug/status")
async def debug_status():
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
