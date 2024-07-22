import sys
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QVBoxLayout, QWidget
from keyboard import Keyboard


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self._init_ui()

    def _init_ui(self) -> None:
        self.kb = Keyboard(self)
        self.focused_input = None

        self.line_edit: QLineEdit = QLineEdit()
        self.line_edit.mousePressEvent = self.handle_mouse_press

        layout = QVBoxLayout()
        layout.addWidget(self.line_edit)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def handle_mouse_press(self, e):
        self.focused_input = self.line_edit
        self.kb.exec_()

    def on_key(self, keys):
        if self.focused_input is not None:
            self.focused_input.setText(keys)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    m_window = MainWindow()
    m_window.show()
    app.exec_()
