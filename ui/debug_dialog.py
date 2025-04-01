import sys
import platform
from PyQt5.QtWidgets import QDialog, QWidget, QMainWindow
from PyQt5.sip import voidptr

from ui_debug_dialog import Ui_DebugDialog


class DebugDialog(QDialog):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.ui : Ui_DebugDialog | None = None
        self.setup_ui()
        self.connect_buttons_to_slot_functions()

        self.is_wireframe = False

    def setup_ui(self):
        self.ui = Ui_DebugDialog()
        self.ui.setupUi(self)

    def connect_buttons_to_slot_functions(self):
        self.ui.printElementsButton.clicked.connect(self.print_elements)
        self.ui.toggleViewButton.clicked.connect(self.toggle_view_mode)
        self.ui.systemInfoButton.clicked.connect(self.show_system_info)
        self.ui.closeButton.clicked.connect(self.accept)


    def print_elements(self):
        print("Fetching elements...")
        import element_controller as ec
        elements = ec.get_all_identifiable_element_ids()
        print(f"Found {len(elements)} elements")
        for element in elements[:5]:
            print(f"Element ID: {element}")


    def toggle_view_mode(self):
        import visualization_controller as vc
        if not self.is_wireframe:
            vc.show_view_wireframe()
            self.is_wireframe = True
        else:
            vc.show_view_shaded2()
            self.is_wireframe = False


    def show_system_info(self):
        print(f"Python version: {platform.python_version()}")
        print(f"System: {platform.system()} {platform.release()}")
        print(f"Platform: {platform.platform()}")
        print(f"Path: {sys.path}")


def get_cadwork_main_widget():
    import utility_controller as uc

    parent_window_hwnd = uc.get_3d_hwnd()
    widget = QWidget.find(voidptr(parent_window_hwnd))
    cadwork_main_widget = widget if isinstance(widget, QMainWindow) else None
    return cadwork_main_widget

