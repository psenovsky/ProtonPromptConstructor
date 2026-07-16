from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QClipboard
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from .config import load_defaults, save_defaults
from .models import ALL_OPTIONS, MUTUALLY_EXCLUSIVE_GROUPS
from .prompt_builder import PromptState, build_prompt
from .tabs.display_tab import DisplayTab
from .tabs.input_tab import InputTab
from .tabs.misc_tab import MiscTab
from .tabs.rendering_tab import RenderingTab
from .tabs.sync_tab import SyncTab
from .tabs.upscaling_tab import UpscalingTab


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Proton Prompt Constructor")
        self.setMinimumSize(600, 500)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        self._tabs = QTabWidget()
        main_layout.addWidget(self._tabs)

        self._display_tab = DisplayTab()
        self._sync_tab = SyncTab()
        self._rendering_tab = RenderingTab()
        self._upscaling_tab = UpscalingTab()
        self._input_tab = InputTab()
        self._misc_tab = MiscTab()

        self._all_tabs = [
            self._display_tab,
            self._sync_tab,
            self._rendering_tab,
            self._upscaling_tab,
            self._input_tab,
            self._misc_tab,
        ]

        self._tabs.addTab(self._display_tab, "Display / HDR")
        self._tabs.addTab(self._sync_tab, "Sync")
        self._tabs.addTab(self._rendering_tab, "Rendering")
        self._tabs.addTab(self._upscaling_tab, "Upscaling")
        self._tabs.addTab(self._input_tab, "Input")
        self._tabs.addTab(self._misc_tab, "Misc")

        for tab in self._all_tabs:
            tab.state_changed.connect(self._update_prompt)

        defaults_bar = QHBoxLayout()
        defaults_label = QLabel("Defaults:")
        defaults_label.setStyleSheet("font-weight: bold;")
        defaults_bar.addWidget(defaults_label)

        self._save_defaults_btn = QPushButton("Save as Default")
        self._save_defaults_btn.clicked.connect(self._save_defaults)
        defaults_bar.addWidget(self._save_defaults_btn)

        self._load_defaults_btn = QPushButton("Load Defaults")
        self._load_defaults_btn.clicked.connect(self._load_defaults)
        defaults_bar.addWidget(self._load_defaults_btn)

        self._reset_btn = QPushButton("Reset All")
        self._reset_btn.clicked.connect(self._reset_all)
        defaults_bar.addWidget(self._reset_btn)

        defaults_bar.addStretch()
        main_layout.addLayout(defaults_bar)

        prompt_group = QVBoxLayout()

        prompt_header = QHBoxLayout()
        prompt_label = QLabel("Generated Prompt:")
        prompt_label.setStyleSheet("font-weight: bold;")
        prompt_header.addWidget(prompt_label)
        prompt_header.addStretch()

        copy_btn = QPushButton("Copy to Clipboard")
        copy_btn.clicked.connect(self._copy_to_clipboard)
        prompt_header.addWidget(copy_btn)

        prompt_group.addLayout(prompt_header)

        self._prompt_display = QTextEdit()
        self._prompt_display.setReadOnly(True)
        font = self._prompt_display.font()
        font.setFamily("Menlo")
        font.setPointSize(12)
        self._prompt_display.setFont(font)
        self._prompt_display.setStyleSheet(
            "background-color: #1e1e1e; color: #d4d4d4; padding: 8px;"
        )
        self._prompt_display.setMinimumHeight(60)
        self._prompt_display.setMaximumHeight(100)
        prompt_group.addWidget(self._prompt_display)

        main_layout.addLayout(prompt_group)

        self._update_prompt()
        self._auto_load_defaults()

    def _collect_state(self) -> PromptState:
        state = PromptState()
        for tab in self._all_tabs:
            tab_state = tab.get_state()
            for key, value in tab_state.items():
                if isinstance(value, bool):
                    state.bool_options[key] = value
                elif isinstance(value, (int, float)):
                    state.slider_options[key] = float(value)
                elif isinstance(value, str):
                    state.text_options[key] = value
        return state

    def _update_prompt(self) -> None:
        state = self._collect_state()
        prompt = build_prompt(state, ALL_OPTIONS, MUTUALLY_EXCLUSIVE_GROUPS)
        self._prompt_display.setPlainText(prompt)

    def _copy_to_clipboard(self) -> None:
        clipboard = QApplication.clipboard()
        if clipboard is not None:
            clipboard.setText(self._prompt_display.toPlainText())

    def _collect_flat_state(self) -> dict:
        flat: dict = {}
        for tab in self._all_tabs:
            flat.update(tab.get_state())
        return flat

    def _apply_state(self, state: dict) -> None:
        for tab in self._all_tabs:
            tab.set_state(state)
        self._update_prompt()

    def _save_defaults(self) -> None:
        save_defaults(self._collect_flat_state())

    def _load_defaults(self) -> None:
        defaults = load_defaults()
        if defaults is not None:
            self._apply_state(defaults)

    def _auto_load_defaults(self) -> None:
        defaults = load_defaults()
        if defaults is not None:
            self._apply_state(defaults)

    def _reset_all(self) -> None:
        self._apply_state({})
