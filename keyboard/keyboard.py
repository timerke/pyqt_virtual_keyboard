from PyQt5.QtCore import pyqtSlot, QObject
from .keyboard_window import KeyboardWindow


class Keyboard(QObject):

    def __init__(self, callback=None) -> None:
        super().__init__()
        self._callback = callback
        self._english: bool = True
        self._init_keyboards()

    def _init_keyboards(self) -> None:
        self._keyboard_en = KeyboardWindow(self._callback, True)
        self._keyboard_en.language_changed.connect(self.change_language)
        self._keyboard_ru = KeyboardWindow(self._callback, False)
        self._keyboard_ru.language_changed.connect(self.change_language)

    @pyqtSlot(bool, str)
    def change_language(self, english: bool, text: str) -> None:
        self._english = english
        old_keyboard, new_board = (self._keyboard_ru, self._keyboard_en) if self._english else\
            (self._keyboard_en, self._keyboard_ru)
        new_board.resize(old_keyboard.size())
        new_board.move(old_keyboard.pos())
        new_board.set_text(text)
        self.show()

    def show(self) -> None:
        if self._english:
            self._keyboard_en.show()
        else:
            self._keyboard_ru.show()
