from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QLabel,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ..models import (
    FORCELGADD,
    HEAP_DELAY_FREE,
    OLD_GL_STRING,
    SECCOMP,
    NOWRITEWATCH,
    WOW64,
    DXGI_DEVICE_MANAGER,
    COPY_PREFIX,
    MEDIA_CONV,
    HOST_LC_ALL,
    PROTON_LOG,
    CMDLINE_APPEND,
)


class MiscTab(QWidget):
    state_changed = pyqtSignal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        compat_group = QGroupBox("Compatibility")
        compat_layout = QVBoxLayout()

        self._forcelgadd = QCheckBox(FORCELGADD.description)
        self._forcelgadd.toggled.connect(lambda: self.state_changed.emit())
        compat_layout.addWidget(self._forcelgadd)

        self._heapdelayfree = QCheckBox(HEAP_DELAY_FREE.description)
        self._heapdelayfree.toggled.connect(lambda: self.state_changed.emit())
        compat_layout.addWidget(self._heapdelayfree)

        self._oldglstr = QCheckBox(OLD_GL_STRING.description)
        self._oldglstr.toggled.connect(lambda: self.state_changed.emit())
        compat_layout.addWidget(self._oldglstr)

        self._seccomp = QCheckBox(SECCOMP.description)
        self._seccomp.setToolTip("Required for some DRM protections to work.")
        self._seccomp.toggled.connect(lambda: self.state_changed.emit())
        compat_layout.addWidget(self._seccomp)

        self._nowritewatch = QCheckBox(NOWRITEWATCH.description)
        self._nowritewatch.toggled.connect(lambda: self.state_changed.emit())
        compat_layout.addWidget(self._nowritewatch)

        self._wow64 = QCheckBox(WOW64.description)
        self._wow64.toggled.connect(lambda: self.state_changed.emit())
        compat_layout.addWidget(self._wow64)

        compat_group.setLayout(compat_layout)
        layout.addWidget(compat_group)

        video_group = QGroupBox("Video & Media")
        video_layout = QVBoxLayout()

        self._dxgi = QCheckBox(DXGI_DEVICE_MANAGER.description)
        self._dxgi.setToolTip("Fixes pink-tinted video playback in some games.")
        self._dxgi.toggled.connect(lambda: self.state_changed.emit())
        video_layout.addWidget(self._dxgi)

        self._mediaconv = QCheckBox(MEDIA_CONV.description)
        self._mediaconv.toggled.connect(lambda: self.state_changed.emit())
        video_layout.addWidget(self._mediaconv)

        self._copyprefix = QCheckBox(COPY_PREFIX.description)
        self._copyprefix.toggled.connect(lambda: self.state_changed.emit())
        video_layout.addWidget(self._copyprefix)

        video_group.setLayout(video_layout)
        layout.addWidget(video_group)

        troubleshoot_group = QGroupBox("Troubleshooting")
        troubleshoot_layout = QVBoxLayout()

        self._proton_log = QCheckBox(PROTON_LOG.description)
        self._proton_log.setToolTip(
            "Creates a log file at ~/steam-$APPID.log. "
            "Use this when a game fails to launch or crashes to help diagnose the issue."
        )
        self._proton_log.toggled.connect(lambda: self.state_changed.emit())
        troubleshoot_layout.addWidget(self._proton_log)

        troubleshoot_group.setLayout(troubleshoot_layout)
        layout.addWidget(troubleshoot_group)

        locale_group = QGroupBox("Locale")
        locale_layout = QVBoxLayout()

        lc_all_label = QLabel(f"{HOST_LC_ALL.description}:")
        locale_layout.addWidget(lc_all_label)
        self._lc_all = QLineEdit()
        self._lc_all.setPlaceholderText("e.g. en_US.UTF-8")
        self._lc_all.textChanged.connect(lambda: self.state_changed.emit())
        locale_layout.addWidget(self._lc_all)

        locale_group.setLayout(locale_layout)
        layout.addWidget(locale_group)

        cmdline_group = QGroupBox("Extra Arguments")
        cmdline_layout = QVBoxLayout()

        cmdline_info = QLabel(CMDLINE_APPEND.info)
        cmdline_info.setWordWrap(True)
        cmdline_info.setStyleSheet("color: #888; font-style: italic;")
        cmdline_layout.addWidget(cmdline_info)

        self._cmdline = QTextEdit()
        self._cmdline.setPlaceholderText("Enter arguments, one per line or comma-separated")
        self._cmdline.setMaximumHeight(80)
        self._cmdline.textChanged.connect(lambda: self.state_changed.emit())
        cmdline_layout.addWidget(self._cmdline)

        cmdline_group.setLayout(cmdline_layout)
        layout.addWidget(cmdline_group)
        layout.addStretch()

    def get_state(self) -> dict:
        cmdline_text = self._cmdline.toPlainText().strip()
        cmdline_text = cmdline_text.replace("\n", ",")
        return {
            FORCELGADD.name: self._forcelgadd.isChecked(),
            HEAP_DELAY_FREE.name: self._heapdelayfree.isChecked(),
            OLD_GL_STRING.name: self._oldglstr.isChecked(),
            SECCOMP.name: self._seccomp.isChecked(),
            NOWRITEWATCH.name: self._nowritewatch.isChecked(),
            WOW64.name: self._wow64.isChecked(),
            DXGI_DEVICE_MANAGER.name: self._dxgi.isChecked(),
            COPY_PREFIX.name: self._copyprefix.isChecked(),
            MEDIA_CONV.name: self._mediaconv.isChecked(),
            PROTON_LOG.name: self._proton_log.isChecked(),
            HOST_LC_ALL.name: self._lc_all.text(),
            CMDLINE_APPEND.name: cmdline_text,
        }

    def set_state(self, state: dict) -> None:
        self.blockSignals(True)
        self._forcelgadd.setChecked(state.get(FORCELGADD.name, False))
        self._heapdelayfree.setChecked(state.get(HEAP_DELAY_FREE.name, False))
        self._oldglstr.setChecked(state.get(OLD_GL_STRING.name, False))
        self._seccomp.setChecked(state.get(SECCOMP.name, False))
        self._nowritewatch.setChecked(state.get(NOWRITEWATCH.name, False))
        self._wow64.setChecked(state.get(WOW64.name, False))
        self._dxgi.setChecked(state.get(DXGI_DEVICE_MANAGER.name, False))
        self._mediaconv.setChecked(state.get(MEDIA_CONV.name, False))
        self._copyprefix.setChecked(state.get(COPY_PREFIX.name, False))
        self._proton_log.setChecked(state.get(PROTON_LOG.name, False))
        self._lc_all.setText(state.get(HOST_LC_ALL.name, ""))
        cmdline = state.get(CMDLINE_APPEND.name, "")
        self._cmdline.setPlainText(cmdline.replace(",", "\n"))
        self.blockSignals(False)
