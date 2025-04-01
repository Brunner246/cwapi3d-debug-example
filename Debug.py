import os
import sys
from typing import List

site_packages_path = os.path.join(os.path.dirname(__file__), '.venv', 'Lib', 'site-packages')
paths = [
    site_packages_path,
    os.path.dirname(__file__),
    os.path.dirname("ui"),
]

os.environ['PYTHONPATH'] = os.pathsep.join([*paths, os.environ.get('PYTHONPATH', '')])
sys.path.extend(paths)

from endtype_surface import create_surface_with_endtype

if __name__ == '__main__':

    from debug_manager import DebugManager

    debug = DebugManager()
    debug.debug_enabled = False

    if debug.debug_enabled:
        import pydevd_pycharm

        pydevd_pycharm.settrace('localhost', port=3000, stdoutToServer=True,
                                stderrToServer=True, patch_multiprocessing=False)

    import cadwork
    import element_controller as ec
    import endtype_controller as end_type


    elements = ec.get_all_identifiable_element_ids()
    print(f"Found {len(elements)} elements")

    for element in elements[:5]:
        print(f"Element ID: {element}")

    surface_points: List[cadwork.point_3d] = [cadwork.point_3d(0, 0, 0),
                                              cadwork.point_3d(100, 0, 0),
                                              cadwork.point_3d(100, 100, 0),
                                              cadwork.point_3d(0, 100, 0)]
    tenon_ids = end_type.get_existing_tenon_ids()
    if tenon_ids:
        end_type_name: str = end_type.get_endtype_name(tenon_ids[0])
        surface_id: int = create_surface_with_endtype(surface_points, end_type_name)
        print(f"Created surface with ID: {surface_id}")

    from ui.debug_dialog import DebugDialog, get_cadwork_main_widget

    debug_dialog = DebugDialog(get_cadwork_main_widget())
    debug_dialog.show()
