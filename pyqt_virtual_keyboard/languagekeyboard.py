import os
import re
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit, QWidget


class LanguageKeyboard(QWidget):
    """
    Widget with language keyboard (Russian or English).
    """

    cancel_signal: pyqtSignal = pyqtSignal()
    language_changed: pyqtSignal = pyqtSignal(bool, bool)
    ok_signal: pyqtSignal = pyqtSignal()

    def __init__(self, line_edit: QLineEdit, callback=None, english: bool = True) -> None:
        """
        :param line_edit: line edit widget of keyboard;
        :param callback:
        :param english: if True, then you need to create the keyboard with English letters.
        """

        super().__init__()
        self._english: bool = english
        lang = "en" if english else "ru"
        self._dir_path: str = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(self._dir_path, f"keyboard_{lang}.ui"), self)

        self._line_edit: QLineEdit = line_edit
        self.cb = callback

        self._get_buttons()
        self._setup_listener()

    @pyqtSlot()
    def _change_language(self) -> None:
        self.language_changed.emit(not self._english, self.btn_upper.isChecked())

    def _display_key(self, key: str) -> None:
        """
        :param key: symbol of the key to be displayed.
        """

        text = self._line_edit.text()
        position = self._line_edit.cursorPosition()
        new_text = text[:position] + key + text[position:]
        self._line_edit.setText(new_text)
        self._line_edit.setFocus()
        self._line_edit.setCursorPosition(position + 1)

        if self.cb is not None:
            self.cb.on_key(new_text)

    def _get_buttons(self) -> None:
        self._buttons_special = [self.btn_backspace, self.btn_cancel, self.btn_language, self.btn_ok, self.btn_upper]
        self._buttons = []
        self._buttons_letters = []
        self._buttons_numbers = []
        for attr_name in dir(self):
            if re.match(r"btn_\d", attr_name):
                self._buttons_numbers.append(getattr(self, attr_name))
            elif re.match(r"btn_lt_\d{1,2}", attr_name):
                self._buttons_letters.append(getattr(self, attr_name))
            elif re.match(r"btn_.*", attr_name) and getattr(self, attr_name) not in self._buttons_special:
                self._buttons.append(getattr(self, attr_name))
        self.btn_space.setText(" ")

    @pyqtSlot()
    def _handle_backspace_clicked(self) -> None:
        text = self._line_edit.text()
        position = self._line_edit.cursorPosition()
        if position > 0:
            new_text = text[:position - 1] + text[position:]
            self._line_edit.setText(new_text)
            self._line_edit.setFocus()
            self._line_edit.setCursorPosition(position - 1)
            if self.cb is not None:
                self.cb.on_key(new_text)
        else:
            self._line_edit.setFocus()
            self._line_edit.setCursorPosition(0)

    @pyqtSlot()
    def _handle_cancel_clicked(self) -> None:
        self.cancel_signal.emit()

    @pyqtSlot()
    def _handle_ok_clicked(self) -> None:
        self.ok_signal.emit()

    @pyqtSlot(bool)
    def _handle_upper_clicked(self, upper: bool) -> None:
        """
        :param upper: if True, then you need to switch the keyboard to uppercase.
        """

        if upper:
            icon_name = "up-arrow-black.png"
            for btn in self._buttons_letters:
                btn.setText(btn.text().upper())
        else:
            icon_name = "up-arrow.png"
            for btn in self._buttons_letters:
                btn.setText(btn.text().lower())
        self.btn_upper.setIcon(QIcon(os.path.join(self._dir_path, icon_name)))
        self._line_edit.setFocus()

    @pyqtSlot()
    def _print_btn_symbol(self) -> None:
        self._display_key(self.sender().text())

    def _setup_listener(self) -> None:
        for btn in self._buttons_letters:
            btn.clicked.connect(self._print_btn_symbol)

        for btn in self._buttons_numbers:
            btn.clicked.connect(self._print_btn_symbol)

        for btn in self._buttons:
            btn.clicked.connect(self._print_btn_symbol)

        self.btn_backspace.clicked.connect(self._handle_backspace_clicked)
        self.btn_cancel.clicked.connect(self._handle_cancel_clicked)
        self.btn_language.clicked.connect(self._change_language)
        self.btn_ok.clicked.connect(self._handle_ok_clicked)
        self.btn_upper.toggled.connect(self._handle_upper_clicked)

    def change_upper_state(self, upper: bool) -> None:
        """
        :param upper: if True, then you need to switch the keyboard to uppercase.
        """

        if upper != self.btn_upper.isChecked():
            self.btn_upper.toggle()
