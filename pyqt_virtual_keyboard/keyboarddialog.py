import os
from typing import Optional
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from .languagekeyboard import LanguageKeyboard


class KeyboardDialog(QDialog):
    """
    Class with virtual keyboard.
    """

    def __init__(self, callback=None, font_size: Optional[int] = None) -> None:
        """
        :param callback:
        :param font_size: new font size for keyboard.
        """

        super().__init__()
        self._callback = callback
        self._english: bool = True
        self._text: Optional[str] = None
        self._init_keyboards(font_size)
        self._change_size()

    @property
    def text(self) -> str:
        """
        :return: keyboard final text.
        """

        if self._text is None:
            return ""

        return self._text

    @pyqtSlot(bool, bool)
    def _change_language(self, english: bool, upper: bool) -> None:
        """
        :param english: if True, then you need to show the keyboard with English letters;
        :param upper: if True, then the keyboard should be in uppercase.
        """

        self._english = english
        visible_keyboard = self._keyboard_en if self._english else self._keyboard_ru
        visible_keyboard.change_upper_state(upper)
        position = self.line_edit_text.cursorPosition()
        self._show_correct_language()
        self.line_edit_text.deselect()
        self.line_edit_text.setFocus()
        self.line_edit_text.setCursorPosition(position)

    def _change_size(self) -> None:
        new_width = 400
        new_height = 250
        self.resize(new_width, new_height)

    @pyqtSlot()
    def _handle_ok(self) -> None:
        self._text = self.line_edit_text.text()
        self.close()

    def _init_keyboards(self, font_size: Optional[int]) -> None:
        """
        :param font_size: new font size for keyboard.
        """

        loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)), "keyboarddialog.ui"), self)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)

        self.btn_cancel.clicked.connect(self.close)

        self._keyboard_en: LanguageKeyboard = LanguageKeyboard(self.line_edit_text, self._callback, True,
                                                               font_size)
        self._keyboard_en.language_changed.connect(self._change_language)
        self._keyboard_en.ok_signal.connect(self._handle_ok)
        self._keyboard_ru: LanguageKeyboard = LanguageKeyboard(self.line_edit_text, self._callback, False,
                                                               font_size)
        self._keyboard_ru.language_changed.connect(self._change_language)
        self._keyboard_ru.ok_signal.connect(self._handle_ok)

        self.vertical_layout.setStretch(0, 10)
        self.vertical_layout.addWidget(self._keyboard_en, 50)
        self.vertical_layout.addWidget(self._keyboard_ru, 50)

    def _show_correct_language(self) -> None:
        self._keyboard_en.setVisible(self._english)
        self._keyboard_ru.setVisible(not self._english)

    def exec_(self, text: Optional[str] = None) -> int:
        """
        :param text: initial text.
        :return: result code.
        """

        self._text = None
        self.line_edit_text.setText("" or text)
        self._show_correct_language()
        return super().exec_()

    def show(self) -> None:
        self._show_correct_language()
        super().show()
