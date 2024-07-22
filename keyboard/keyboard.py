import os
from typing import Optional
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout
from .keyboard_window import KeyboardWindow


class Keyboard(QDialog):

    def __init__(self, callback=None) -> None:
        super().__init__()
        self._callback = callback
        self._english: bool = True
        self._text: Optional[str] = None
        self._init_keyboards()
        self._change_size()

    @property
    def text(self) -> str:
        """
        :return: keyboard final text.
        """

        if self._text is None:
            return ""

        return self._text

    def _change_size(self) -> None:
        new_width = 400
        new_height = 250
        self.resize(new_width, new_height)

    def _init_keyboards(self) -> None:
        self.setWindowTitle("Keyboard")
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(os.path.abspath(__file__)), "keyboard.png")))
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)

        self._keyboard_en: KeyboardWindow = KeyboardWindow(self._callback, True)
        self._keyboard_en.cancel_signal.connect(self.close)
        self._keyboard_en.ok_signal.connect(self.handle_ok)
        self._keyboard_en.language_changed.connect(self.change_language)
        self._keyboard_ru: KeyboardWindow = KeyboardWindow(self._callback, False)
        self._keyboard_ru.cancel_signal.connect(self.close)
        self._keyboard_ru.ok_signal.connect(self.handle_ok)
        self._keyboard_ru.language_changed.connect(self.change_language)

        layout = QVBoxLayout()
        layout.setContentsMargins(1, 1, 1, 1)
        layout.addWidget(self._keyboard_en)
        layout.addWidget(self._keyboard_ru)
        self.setLayout(layout)

    def _show_correct_board(self) -> None:
        self._keyboard_en.setVisible(self._english)
        self._keyboard_ru.setVisible(not self._english)

    @pyqtSlot(bool, str, bool)
    def change_language(self, english: bool, text: str, upper: bool) -> None:
        self._english = english
        new_board = self._keyboard_en if self._english else self._keyboard_ru
        new_board.set_text(text)
        new_board.change_upper_state(upper)
        self._show_correct_board()

    def exec_(self) -> int:
        self._text = None
        for keyboard in (self._keyboard_en, self._keyboard_ru):
            keyboard.set_text("")
        self._show_correct_board()
        return super().exec_()

    @pyqtSlot(str)
    def handle_ok(self, text: str) -> None:
        """
        :param text: final text.
        """

        self._text = text
        self.close()

    def show(self) -> None:
        self._show_correct_board()
        super().show()
