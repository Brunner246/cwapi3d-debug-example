import os
import sys

site_packages_path = os.path.join(os.path.dirname(__file__), '.venv', 'Lib', 'site-packages')
paths = [
    site_packages_path,
    os.path.dirname(__file__),
    os.path.dirname("ui"),
]

os.environ['PYTHONPATH'] = os.pathsep.join([*paths, os.environ.get('PYTHONPATH', '')])
sys.path.extend(paths)

if __name__ == '__main__':

    from debug_manager import DebugManager

    debug = DebugManager()
    debug.debug_enabled = True

    if debug.debug_enabled:
        import pydevd_pycharm
        pydevd_pycharm.settrace('localhost', port=3000, stdoutToServer=True,
                               stderrToServer=True, patch_multiprocessing=False)

    import element_controller as ec

    elements = ec.get_all_identifiable_element_ids()
    print(f"Found {len(elements)} elements")

    [print(f"Element ID: {element}") for element in elements[:5]]

    from ui.debug_dialog import DebugDialog, get_cadwork_main_widget

    debug_dialog = DebugDialog(get_cadwork_main_widget())
    debug_dialog.show()

