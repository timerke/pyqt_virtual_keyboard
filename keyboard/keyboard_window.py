import os
import re
from typing import List
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton, QWidget


class KeyboardWindow(QWidget):

    canceled: pyqtSignal = pyqtSignal()
    closed: pyqtSignal = pyqtSignal()
    language_changed: pyqtSignal = pyqtSignal(bool, str, bool)

    def __init__(self, callback=None, english: bool = True) -> None:
        super().__init__()
        self._english: bool = english
        lang = "en" if english else "ru"
        uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"keyboard_{lang}.ui"), self)

        self.cb = callback

        self._get_buttons()
        self._setup_listener()
        self._change_size()

    @staticmethod
    def _change_buttons_font(font: QFont, buttons: List[QPushButton]) -> None:
        for button in buttons:
            button.setFont(font)

    def _change_size(self) -> None:
        font_size = 14
        font = QFont()
        font.setPointSize(font_size)
        self._change_buttons_font(font, self._buttons_letters)
        self._change_buttons_font(font, self._buttons_numbers)
        self._change_buttons_font(font, self._buttons)

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

    def _setup_listener(self) -> None:
        for btn in self._buttons_letters:
            btn.clicked.connect(self.print_btn_symbol)

        for btn in self._buttons_numbers:
            btn.clicked.connect(self.print_btn_symbol)

        for btn in self._buttons:
            btn.clicked.connect(self.print_btn_symbol)

        self.btn_backspace.clicked.connect(self.handle_backspace_clicked)
        self.btn_cancel.clicked.connect(self.handle_cancel_clicked)
        self.btn_language.clicked.connect(self.change_language)
        self.btn_ok.clicked.connect(self.handle_ok_clicked)
        self.btn_upper.toggled.connect(self.handle_upper_clicked)

    @pyqtSlot()
    def change_language(self) -> None:
        self.language_changed.emit(not self._english, self.edit_text.text(), self.btn_upper.isChecked())

    def change_upper_state(self, upper: bool) -> None:
        if upper != self.btn_upper.isChecked():
            self.btn_upper.toggle()

    @pyqtSlot()
    def handle_backspace_clicked(self) -> None:
        text = self.edit_text.text()
        position = self.edit_text.cursorPosition()
        if position > 0:
            new_text = text[:position - 1] + text[position:]
            self.edit_text.setText(new_text)
            self.edit_text.setFocus()
            self.edit_text.setCursorPosition(position - 1)
            if self.cb is not None:
                self.cb.on_key(new_text)
        else:
            self.edit_text.setFocus()
            self.edit_text.setCursorPosition(0)

    @pyqtSlot()
    def handle_cancel_clicked(self) -> None:
        self.canceled.emit()
        self.closed.emit()

    @pyqtSlot()
    def handle_ok_clicked(self) -> None:
        self.closed.emit()

    @pyqtSlot(bool)
    def handle_upper_clicked(self, state: bool) -> None:
        if state:
            for btn in self._buttons_letters:
                btn.setText(btn.text().upper())
        else:
            for btn in self._buttons_letters:
                btn.setText(btn.text().lower())

    @pyqtSlot()
    def print_btn_symbol(self) -> None:
        self.reflect_keys(self.sender().text())

    def reflect_keys(self, key: str) -> None:
        text = self.edit_text.text()
        position = self.edit_text.cursorPosition()
        new_text = text[:position] + key + text[position:]
        self.edit_text.setText(new_text)
        self.edit_text.setFocus()
        self.edit_text.setCursorPosition(position + 1)

        if self.cb is not None:
            self.cb.on_key(new_text)

    def set_text(self, text: str) -> None:
        self.edit_text.setText(text)
