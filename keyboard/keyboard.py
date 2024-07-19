from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout
from .keyboard_window import KeyboardWindow


class Keyboard(QDialog):

    def __init__(self, callback=None) -> None:
        super().__init__()
        self._callback = callback
        self._english: bool = True
        self._init_keyboards()
        self._change_size()

    def _change_size(self) -> None:
        new_width = 400
        new_height = 250
        self.resize(new_width, new_height)

    def _init_keyboards(self) -> None:
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)

        self._keyboard_en: KeyboardWindow = KeyboardWindow(self._callback, True)
        self._keyboard_en.canceled.connect(self.close)
        self._keyboard_en.closed.connect(self.close)
        self._keyboard_en.language_changed.connect(self.change_language)
        self._keyboard_ru: KeyboardWindow = KeyboardWindow(self._callback, False)
        self._keyboard_ru.canceled.connect(self.close)
        self._keyboard_ru.closed.connect(self.close)
        self._keyboard_ru.language_changed.connect(self.change_language)

        layout = QVBoxLayout()
        layout.addWidget(self._keyboard_en)
        layout.addWidget(self._keyboard_ru)
        self.setLayout(layout)

    @pyqtSlot(bool, str, bool)
    def change_language(self, english: bool, text: str, upper: bool) -> None:
        self._english = english
        new_board = self._keyboard_en if self._english else self._keyboard_ru
        new_board.set_text(text)
        new_board.change_upper_state(upper)
        self.show()

    def show(self) -> None:
        self._keyboard_en.setVisible(self._english)
        self._keyboard_ru.setVisible(not self._english)
        super().show()
