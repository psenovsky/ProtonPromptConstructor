from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QLabel,
    QLineEdit,
    QRadioButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from ..models import (
    FSR,
    FSR_STRENGTH,
    FSR_CUSTOM_MODE,
    FSR3,
    FSR4,
    FSR4_RDNA3,
    FSR4_HUD,
    DLSS,
    DLSS_HUD,
    XESS,
)


class UpscalingTab(QWidget):
    state_changed = pyqtSignal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        vendor_group = QGroupBox("Upscaling Technology")
        vendor_layout = QVBoxLayout()

        self._fsr = QRadioButton("AMD FSR (FidelityFX Super Resolution)")
        self._fsr.toggled.connect(self._on_vendor_changed)
        vendor_layout.addWidget(self._fsr)

        self._dlss = QRadioButton("NVIDIA DLSS")
        self._dlss.toggled.connect(self._on_vendor_changed)
        vendor_layout.addWidget(self._dlss)

        self._xess = QRadioButton("Intel XeSS")
        self._xess.toggled.connect(self._on_vendor_changed)
        vendor_layout.addWidget(self._xess)

        self._none = QRadioButton("None")
        self._none.setChecked(True)
        self._none.toggled.connect(self._on_vendor_changed)
        vendor_layout.addWidget(self._none)

        vendor_group.setLayout(vendor_layout)
        layout.addWidget(vendor_group)

        self._fsr_options = self._build_fsr_options()
        layout.addWidget(self._fsr_options)

        self._dlss_options = self._build_dlss_options()
        layout.addWidget(self._dlss_options)

        self._update_visibility()
        layout.addStretch()

    def _build_fsr_options(self) -> QGroupBox:
        group = QGroupBox("FSR Options")
        glayout = QVBoxLayout()

        info = QLabel(FSR.info)
        info.setWordWrap(True)
        info.setStyleSheet("color: #888; font-style: italic;")
        glayout.addWidget(info)

        fsr_version_label = QLabel("Version upgrade:")
        glayout.addWidget(fsr_version_label)

        self._fsr3 = QRadioButton(FSR3.description)
        self._fsr3.toggled.connect(lambda: self.state_changed.emit())
        glayout.addWidget(self._fsr3)

        self._fsr4 = QRadioButton(FSR4.description)
        self._fsr4.setToolTip(FSR4.info)
        self._fsr4.toggled.connect(lambda: self.state_changed.emit())
        glayout.addWidget(self._fsr4)

        self._fsr4rdna3 = QRadioButton(FSR4_RDNA3.description)
        self._fsr4rdna3.setToolTip(FSR4_RDNA3.info)
        self._fsr4rdna3.toggled.connect(lambda: self.state_changed.emit())
        glayout.addWidget(self._fsr4rdna3)

        self._fsr4_hud = QCheckBox(FSR4_HUD.description)
        self._fsr4_hud.toggled.connect(lambda: self.state_changed.emit())
        glayout.addWidget(self._fsr4_hud)

        strength_label = QLabel(f"Sharpening strength ({FSR_STRENGTH.min_value}-{FSR_STRENGTH.max_value}, "
                                f"default {FSR_STRENGTH.default_value}):")
        glayout.addWidget(strength_label)
        self._fsr_strength = QSlider()
        self._fsr_strength.setOrientation(Qt.Orientation.Horizontal)
        self._fsr_strength.setMinimum(FSR_STRENGTH.min_value)
        self._fsr_strength.setMaximum(FSR_STRENGTH.max_value)
        self._fsr_strength.setValue(FSR_STRENGTH.default_value)
        self._fsr_strength.valueChanged.connect(lambda: self.state_changed.emit())
        self._fsr_strength_value = QLabel(str(FSR_STRENGTH.default_value))
        self._fsr_strength.valueChanged.connect(
            lambda v: self._fsr_strength_value.setText(str(v))
        )
        glayout.addWidget(self._fsr_strength)
        glayout.addWidget(self._fsr_strength_value)

        custom_label = QLabel(f"{FSR_CUSTOM_MODE.description}:")
        glayout.addWidget(custom_label)
        self._fsr_custom = QLineEdit()
        self._fsr_custom.setPlaceholderText("e.g. 1280x720")
        self._fsr_custom.textChanged.connect(lambda: self.state_changed.emit())
        glayout.addWidget(self._fsr_custom)

        group.setLayout(glayout)
        return group

    def _build_dlss_options(self) -> QGroupBox:
        group = QGroupBox("DLSS Options")
        glayout = QVBoxLayout()

        info = QLabel(DLSS.info)
        info.setWordWrap(True)
        info.setStyleSheet("color: #888; font-style: italic;")
        glayout.addWidget(info)

        self._dlss_hud = QCheckBox(DLSS_HUD.description)
        self._dlss_hud.toggled.connect(lambda: self.state_changed.emit())
        glayout.addWidget(self._dlss_hud)

        group.setLayout(glayout)
        return group

    def _on_vendor_changed(self) -> None:
        self._update_visibility()
        self.state_changed.emit()

    def _update_visibility(self) -> None:
        fsr_active = self._fsr.isChecked()
        dlss_active = self._dlss.isChecked()
        self._fsr_options.setVisible(fsr_active)
        self._dlss_options.setVisible(dlss_active)

    def get_state(self) -> dict:
        fsr_active = self._fsr.isChecked()
        dlss_active = self._dlss.isChecked()
        return {
            FSR.name: fsr_active,
            DLSS.name: dlss_active,
            XESS.name: self._xess.isChecked(),
            FSR3.name: fsr_active and self._fsr3.isChecked(),
            FSR4.name: fsr_active and self._fsr4.isChecked(),
            FSR4_RDNA3.name: fsr_active and self._fsr4rdna3.isChecked(),
            FSR4_HUD.name: fsr_active and self._fsr4_hud.isChecked(),
            FSR_STRENGTH.name: self._fsr_strength.value(),
            FSR_CUSTOM_MODE.name: self._fsr_custom.text() if fsr_active else "",
            DLSS_HUD.name: dlss_active and self._dlss_hud.isChecked(),
        }
