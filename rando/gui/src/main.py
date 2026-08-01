import sys

from PyQt6.QtWidgets import QApplication, QTabWidget
from patcher_ui import Ui_TabWidget


class MainWindow(QTabWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_TabWidget()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
