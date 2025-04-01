from typing import List
import cadwork


def create_surface(surface_vertices: List[cadwork.point_3d]) -> int:
    import element_controller as ec
    return ec.create_surface(surface_vertices)


def adjust_surface_normal(surface_id: int):
    import geometry_controller as gc
    # assume the length axis is not pointing to the surface normal
    # in production code, evaluate the normal direction and adjust accordingly ;)
    gc.rotate_length_axis_90([surface_id])


def create_endtype_on_element(element_id: int, end_type_name: str):
    import endtype_controller as ec
    ec.set_endtype_name_end(element_id, end_type_name)


def create_surface_with_endtype(surface_vertices: List[cadwork.point_3d], end_type_name: str) -> int:
    surface_id = create_surface(surface_vertices)
    adjust_surface_normal(surface_id)
    create_endtype_on_element(surface_id, end_type_name)
    return surface_id
