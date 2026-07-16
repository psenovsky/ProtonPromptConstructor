from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QLabel,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from ..models import (
    WINED3D,
    NOD3D9,
    NOD3D10,
    NOD3D11,
    NOD3D12,
)


class RenderingTab(QWidget):
    state_changed = pyqtSignal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        renderer_group = QGroupBox("Graphics Renderer")
        renderer_layout = QVBoxLayout()

        self._wined3d = QRadioButton(WINED3D.description)
        self._wined3d.setToolTip(
            "Use OpenGL-based wined3d instead of Vulkan-based DXVK. "
            "This affects DX11 and DX10 rendering."
        )
        self._wined3d.toggled.connect(self._on_renderer_changed)
        renderer_layout.addWidget(self._wined3d)

        self._dxvk = QRadioButton("Use Vulkan-based DXVK (default)")
        self._dxvk.setChecked(True)
        self._dxvk.toggled.connect(self._on_renderer_changed)
        renderer_layout.addWidget(self._dxvk)

        renderer_group.setLayout(renderer_layout)
        layout.addWidget(renderer_group)

        dx_group = QGroupBox("Disable DirectX Versions")
        dx_layout = QVBoxLayout()

        dx_info = QLabel(
            "Only applicable when using DXVK (Vulkan) renderer."
        )
        dx_info.setWordWrap(True)
        dx_info.setStyleSheet("color: #888; font-style: italic;")
        dx_layout.addWidget(dx_info)

        self._nod3d9 = QCheckBox(NOD3D9.description)
        self._nod3d9.toggled.connect(lambda: self.state_changed.emit())
        dx_layout.addWidget(self._nod3d9)

        self._nod3d10 = QCheckBox(NOD3D10.description)
        self._nod3d10.toggled.connect(lambda: self.state_changed.emit())
        dx_layout.addWidget(self._nod3d10)

        self._nod3d11 = QCheckBox(NOD3D11.description)
        self._nod3d11.toggled.connect(lambda: self.state_changed.emit())
        dx_layout.addWidget(self._nod3d11)

        self._nod3d12 = QCheckBox(NOD3D12.description)
        self._nod3d12.toggled.connect(lambda: self.state_changed.emit())
        dx_layout.addWidget(self._nod3d12)

        dx_group.setLayout(dx_layout)
        self._dx_group = dx_group
        layout.addWidget(dx_group)
        layout.addStretch()

    def _on_renderer_changed(self) -> None:
        use_wined3d = self._wined3d.isChecked()
        self._dx_group.setEnabled(not use_wined3d)
        self.state_changed.emit()

    def get_state(self) -> dict:
        use_wined3d = self._wined3d.isChecked()
        return {
            WINED3D.name: use_wined3d,
            NOD3D9.name: False if use_wined3d else self._nod3d9.isChecked(),
            NOD3D10.name: False if use_wined3d else self._nod3d10.isChecked(),
            NOD3D11.name: False if use_wined3d else self._nod3d11.isChecked(),
            NOD3D12.name: False if use_wined3d else self._nod3d12.isChecked(),
        }

    def set_state(self, state: dict) -> None:
        self.blockSignals(True)
        wined3d = state.get(WINED3D.name, False)
        self._wined3d.setChecked(wined3d)
        self._dxvk.setChecked(not wined3d)
        self._nod3d9.setChecked(state.get(NOD3D9.name, False))
        self._nod3d10.setChecked(state.get(NOD3D10.name, False))
        self._nod3d11.setChecked(state.get(NOD3D11.name, False))
        self._nod3d12.setChecked(state.get(NOD3D12.name, False))
        self._dx_group.setEnabled(not wined3d)
        self.blockSignals(False)
