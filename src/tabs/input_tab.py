from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from ..models import SDL_INPUT, XALIA


class InputTab(QWidget):
    state_changed = pyqtSignal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        group = QGroupBox("Input Settings")
        group_layout = QVBoxLayout()

        self._sdl = QCheckBox(SDL_INPUT.description)
        self._sdl.setToolTip("Uses SDL input instead of HIDRAW/Steam Input.")
        self._sdl.toggled.connect(lambda: self.state_changed.emit())
        group_layout.addWidget(self._sdl)

        self._xalia = QCheckBox(XALIA.description)
        self._xalia.setToolTip(XALIA.info)
        self._xalia.toggled.connect(lambda: self.state_changed.emit())
        group_layout.addWidget(self._xalia)

        group.setLayout(group_layout)
        layout.addWidget(group)
        layout.addStretch()

    def get_state(self) -> dict:
        return {
            SDL_INPUT.name: self._sdl.isChecked(),
            XALIA.name: self._xalia.isChecked(),
        }
