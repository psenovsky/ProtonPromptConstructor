from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QGroupBox,
    QLabel,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from ..models import NOESYNC, NOFSYNC, NONTSYNC


class SyncTab(QWidget):
    state_changed = pyqtSignal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        group_box = QGroupBox("Synchronization Primitives")
        group_layout = QVBoxLayout()

        info = QLabel(
            "These options control how Proton handles in-process synchronization. "
            "Disabling any of these may affect performance."
        )
        info.setWordWrap(True)
        info.setStyleSheet("color: #888; font-style: italic;")
        group_layout.addWidget(info)

        self._noesync = QRadioButton(NOESYNC.description)
        self._noesync.setToolTip(NOESYNC.description)
        self._noesync.toggled.connect(lambda: self.state_changed.emit())
        group_layout.addWidget(self._noesync)

        self._nofsync = QRadioButton(NOFSYNC.description)
        self._nofsync.setToolTip(NOFSYNC.info)
        self._nofsync.toggled.connect(lambda: self.state_changed.emit())
        group_layout.addWidget(self._nofsync)

        self._nontsync = QRadioButton(NONTSYNC.description)
        self._nontsync.setToolTip(NONTSYNC.info)
        self._nontsync.toggled.connect(lambda: self.state_changed.emit())
        group_layout.addWidget(self._nontsync)

        ntsync_note = QLabel(
            "  Note: NTSync requires kernel 6.14+ with CONFIG_NTSYNC=y or =m."
        )
        ntsync_note.setWordWrap(True)
        ntsync_note.setStyleSheet("color: #888; font-style: italic;")
        group_layout.addWidget(ntsync_note)

        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
        layout.addStretch()

    def get_state(self) -> dict:
        return {
            NOESYNC.name: self._noesync.isChecked(),
            NOFSYNC.name: self._nofsync.isChecked(),
            NONTSYNC.name: self._nontsync.isChecked(),
        }

    def set_state(self, state: dict) -> None:
        self.blockSignals(True)
        self._noesync.setChecked(state.get(NOESYNC.name, False))
        self._nofsync.setChecked(state.get(NOFSYNC.name, False))
        self._nontsync.setChecked(state.get(NONTSYNC.name, False))
        self.blockSignals(False)
