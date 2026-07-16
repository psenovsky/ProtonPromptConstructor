from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QGroupBox,
    QLabel,
    QLineEdit,
    QRadioButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from ..models import HDR, WAYLAND, WAYLAND_MONITOR, WAYLAND_RAWINPUT, OptionType


class DisplayTab(QWidget):
    state_changed = pyqtSignal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        hdr_group = QGroupBox("HDR")
        hdr_layout = QVBoxLayout()
        self._hdr = QRadioButton(HDR.description)
        self._hdr.setToolTip(HDR.info)
        self._hdr.toggled.connect(self._on_hdr_toggled)
        hdr_layout.addWidget(self._hdr)
        self._hdr_info = QLabel(
            "  Note: Enabling HDR auto-enables the Wayland driver. "
            "Steam overlay will not work with Wayland."
        )
        self._hdr_info.setWordWrap(True)
        self._hdr_info.setStyleSheet("color: #888; font-style: italic;")
        hdr_layout.addWidget(self._hdr_info)
        hdr_group.setLayout(hdr_layout)
        layout.addWidget(hdr_group)

        wayland_group = QGroupBox("Wayland Driver")
        wayland_layout = QVBoxLayout()
        self._wayland = QRadioButton(WAYLAND.description)
        self._wayland.setToolTip(WAYLAND.info)
        self._wayland.toggled.connect(self._on_wayland_toggled)
        wayland_layout.addWidget(self._wayland)

        self._monitor_label = QLabel(f"  {WAYLAND_MONITOR.description}:")
        self._monitor_input = QLineEdit()
        self._monitor_input.setPlaceholderText("e.g. eDP-1")
        self._monitor_input.setEnabled(False)
        self._monitor_input.textChanged.connect(lambda: self.state_changed.emit())
        wayland_layout.addWidget(self._monitor_label)
        wayland_layout.addWidget(self._monitor_input)

        self._rawinput_label = QLabel(f"  {WAYLAND_RAWINPUT.description}:")
        self._rawinput_slider = QSlider()
        self._rawinput_slider.setOrientation(Qt.Orientation.Horizontal)
        self._rawinput_slider.setMinimum(0)
        self._rawinput_slider.setMaximum(20)
        self._rawinput_slider.setValue(0)
        self._rawinput_slider.setEnabled(False)
        self._rawinput_slider.valueChanged.connect(lambda: self.state_changed.emit())
        self._rawinput_value_label = QLabel("0")
        self._rawinput_slider.valueChanged.connect(
            lambda v: self._rawinput_value_label.setText(str(v / 10))
        )
        wayland_layout.addWidget(self._rawinput_label)
        wayland_layout.addWidget(self._rawinput_slider)
        wayland_layout.addWidget(self._rawinput_value_label)

        wayland_group.setLayout(wayland_layout)
        layout.addWidget(wayland_group)
        layout.addStretch()

    def _on_hdr_toggled(self, checked: bool) -> None:
        if checked:
            self._wayland.setChecked(True)
            self._wayland.setEnabled(False)
        else:
            self._wayland.setEnabled(True)
        self._update_wayland_controls()
        self.state_changed.emit()

    def _on_wayland_toggled(self, checked: bool) -> None:
        self._update_wayland_controls()
        self.state_changed.emit()

    def _update_wayland_controls(self) -> None:
        enabled = self._wayland.isChecked()
        self._monitor_input.setEnabled(enabled)
        self._monitor_label.setEnabled(enabled)
        self._rawinput_slider.setEnabled(enabled)
        self._rawinput_label.setEnabled(enabled)
        self._rawinput_value_label.setEnabled(enabled)

    def get_state(self) -> dict:
        return {
            HDR.name: self._hdr.isChecked(),
            WAYLAND.name: self._wayland.isChecked(),
            WAYLAND_MONITOR.name: self._monitor_input.text(),
            WAYLAND_RAWINPUT.name: self._rawinput_slider.value() / 10,
        }

    def set_state(self, state: dict) -> None:
        self.blockSignals(True)
        hdr = state.get(HDR.name, False)
        self._hdr.setChecked(hdr)
        self._on_hdr_toggled(hdr)
        self._wayland.setChecked(state.get(WAYLAND.name, False))
        self._monitor_input.setText(state.get(WAYLAND_MONITOR.name, ""))
        raw = state.get(WAYLAND_RAWINPUT.name, 0)
        self._rawinput_slider.setValue(int(raw * 10))
        self._update_wayland_controls()
        self.blockSignals(False)
