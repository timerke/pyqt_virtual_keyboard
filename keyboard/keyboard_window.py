import os
import re
from typing import List
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QPushButton


LOWER = "QPushButton\n""{\n" \
            "    background-color: qlineargradient(spread:pad, x1:0.521, y1:0.8925, x2:0.504, y2:0.244227, stop:0.00847458 rgba(238, 235, 232, 255), stop:1 rgba(255, 255, 255, 255));\n"" \
            ""    border: 1px solid gray;\n" \
            "    border-radius: 2px;\n" \
            "}\n" \
            "\n" \
            "QPushButton:pressed \n" \
            "{    \n" \
            "    background-color: rgb(140, 223, 255);\n" \
            " }"

UPPER = "QPushButton\n""{\n" \
            "    background-color: rgb(0, 162, 255);\n"" \
            ""    border: 1px solid gray;\n" \
            "    border-radius: 2px;\n" \
            "}\n" \
            "\n" \
            "QPushButton:pressed \n" \
            "{    \n" \
            "    background-color: rgb(140, 223, 255);\n" \
            " }"


class KeyboardWindow(QMainWindow):

    language_changed: pyqtSignal = pyqtSignal(bool, str)

    def __init__(self, callback=None, english: bool = True) -> None:
        super().__init__()
        self._english: bool = english
        lang: str = "en" if english else "ru"
        uic.loadUi(os.path.join("keyboard", f"window_keyboard_{lang}.ui"), self)

        # self.setFixedSize(self.size())
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)

        self.cb = callback
        self.upper: bool = False

        self._get_buttons()
        self._setup_listener()
        self._change_size()

    @staticmethod
    def _change_buttons_font(font: QFont, buttons: List[QPushButton]) -> None:
        for button in buttons:
            button.setFont(font)

    def _change_size(self) -> None:
        new_width = 400
        new_height = 250
        self.resize(new_width, new_height)

        font_size = 14
        font = QFont()
        font.setPointSize(font_size)
        self._change_buttons_font(font, self._buttons_letters)
        self._change_buttons_font(font, self._buttons_numbers)
        self._change_buttons_font(font, self._buttons)

    def _get_buttons(self) -> None:
        self._buttons_letters = []
        self._buttons_numbers = []
        for attr_name in dir(self):
            if re.match(r"btn_\d", attr_name):
                self._buttons_numbers.append(getattr(self, attr_name))
            elif re.match(r"btn_lt_\d{1,2}", attr_name):
                self._buttons_letters.append(getattr(self, attr_name))
        self._buttons = [self.btn_upper, self.btn_underscore, self.btn_at, self.btn_space, self.btn_period,
                         self.btn_backspace, self.btn_ok]

    def _setup_listener(self):
        for btn in self._buttons_letters:
            btn.clicked.connect(self.print_btn_symbol)

        for btn in self._buttons_numbers:
            btn.clicked.connect(self.print_btn_symbol)

        self.btn_at.clicked.connect(self.print_btn_symbol)
        self.btn_space.clicked.connect(self.print_btn_symbol)
        self.btn_period.clicked.connect(self.print_btn_symbol)
        self.btn_underscore.clicked.connect(self.print_btn_symbol)

        self.btn_upper.clicked.connect(self.handle_upper_clicked)
        self.btn_backspace.clicked.connect(self.handle_backspace_clicked)
        self.btn_ok.clicked.connect(self.handle_ok_clicked)
        self.btn_language.clicked.connect(self.change_language)

    @pyqtSlot()
    def change_language(self) -> None:
        self.hide()
        self.language_changed.emit(not self._english, self.edit_text.text())

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
    def handle_ok_clicked(self) -> None:
        self.hide()

    @pyqtSlot()
    def handle_upper_clicked(self) -> None:
        self.upper = not self.upper

        if self.upper:
            self.btn_upper.setStyleSheet(UPPER)

            for btn in self._buttons_letters:
                btn.setText(btn.text().upper())
        else:
            self.btn_upper.setStyleSheet(LOWER)

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
