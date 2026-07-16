from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from src.models import Group, GroupType, Option


class OptionWidget(QWidget):
    state_changed = pyqtSignal()

    def __init__(
        self,
        option: Option,
        state: dict[str, object],
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self.option = option
        self.state = state
        self.widgets: list[QWidget] = []

        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        if self.option.tooltip:
            self.widgets.append(self._create_tooltip_label(self.option.tooltip))

        if self.option.type == "int":
            self._create_slider_widget(layout)
        elif self.option.items:
            self._create_combo_widget(layout)
        elif self.option.type == "str":
            self._create_text_widget(layout)
        elif self.option.env_key or self.option.prefix:
            self._create_bool_widget(layout)

        for w in self.widgets:
            layout.addWidget(w)

    def _create_tooltip_label(self, text: str) -> QLabel:
        label = QLabel(f"  {text}")
        label.setWordWrap(True)
        label.setStyleSheet("color: #888; font-style: italic;")
        return label

    def _create_bool_widget(self, layout: QVBoxLayout) -> None:
        if self.option.mutually_exclusive_with:
            widget = QRadioButton(self.option.label)
        else:
            widget = QCheckBox(self.option.label)

        widget.setToolTip(self.option.tooltip)

        def on_toggled(checked: bool) -> None:
            self.state[self.option.key] = checked
            self.state_changed.emit()

        widget.toggled.connect(on_toggled)

        if self.option.mutually_exclusive_with:
            self.state_changed.connect(lambda: self._update_checked(widget))
        self.widgets.append(widget)

    def _create_slider_widget(self, layout: QVBoxLayout) -> None:
        self.widgets.append(QLabel(self.option.label))

        slider_layout = QHBoxLayout()
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(self.option.min_val)
        slider.setMaximum(self.option.max_val)
        slider.setSingleStep(self.option.step)
        slider.setValue(self.option.default)

        value_label = QLabel(self._format_slider_value(self.option.default))

        def on_slider_changed(value: int) -> None:
            actual_value = value * self.option.scale
            self.state[self.option.key] = actual_value
            value_label.setText(self._format_slider_value(value))
            self.state_changed.emit()

        slider.valueChanged.connect(on_slider_changed)
        slider_layout.addWidget(slider)
        slider_layout.addWidget(value_label)

        slider_container = QWidget()
        slider_container.setLayout(slider_layout)
        self.widgets.append(slider_container)

    def _format_slider_value(self, value: int) -> str:
        actual = value * self.option.scale
        if self.option.scale < 1:
            return f"{actual:.1f}"
        return str(actual)

    def _create_text_widget(self, layout: QVBoxLayout) -> None:
        self.widgets.append(QLabel(self.option.label))
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(self.option.placeholder)

        def on_text_changed(text: str) -> None:
            self.state[self.option.key] = text
            self.state_changed.emit()

        line_edit.textChanged.connect(on_text_changed)
        self.widgets.append(line_edit)

    def _create_combo_widget(self, layout: QVBoxLayout) -> None:
        self.widgets.append(QLabel(self.option.label))
        combo = QComboBox()
        combo.setEditable(self.option.editable)
        combo.addItems(self.option.items)

        def on_current_text_changed(text: str) -> None:
            self.state[self.option.key] = text
            self.state_changed.emit()

        combo.currentTextChanged.connect(on_current_text_changed)
        self.widgets.append(combo)

    def _update_checked(self, widget: QWidget) -> None:
        if isinstance(widget, (QRadioButton, QCheckBox)):
            current_value = self.state.get(self.option.key, False)
            if widget.isChecked() != current_value:
                widget.setChecked(current_value)

    def get_state(self) -> dict[str, object]:
        return self.state

    def set_state(self, new_state: dict[str, object]) -> None:
        self.state.update(new_state)
        self._sync_ui()

    def _sync_ui(self) -> None:
        value = self.state.get(self.option.key, self.option.default)

        for widget in self.widgets:
            if isinstance(widget, (QRadioButton, QCheckBox)):
                widget.setChecked(bool(value))
            elif isinstance(widget, QSlider):
                slider_value = int(value / self.option.scale) if self.option.scale < 1 else int(value)
                widget.setValue(slider_value)
            elif isinstance(widget, QLineEdit):
                widget.setText(str(value))
            elif isinstance(widget, QComboBox):
                widget.setCurrentText(str(value))


class PluginTab(QWidget):
    state_changed = pyqtSignal()

    def __init__(
        self,
        group: Group,
        state: dict[str, object],
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self.group = group
        self.state = state
        self.option_widgets: list[OptionWidget] = []

        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        for child in self.group.children:
            if isinstance(child, Option):
                widget = OptionWidget(child, self.state)
                widget.state_changed.connect(self._on_child_changed)
                self.option_widgets.append(widget)
                scroll_layout.addWidget(widget)
            elif isinstance(child, Group):
                self._add_group(child, scroll_layout)

        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

    def _add_group(self, group: Group, parent_layout: QVBoxLayout) -> None:
        if group.type == GroupType.CARD:
            group_box = QGroupBox(group.label)
            group_layout = QVBoxLayout()
            group_box.setLayout(group_layout)
            parent_layout.addWidget(group_box)
            target_layout = group_layout
        else:
            target_layout = parent_layout

        for child in group.children:
            if isinstance(child, Option):
                widget = OptionWidget(child, self.state)
                widget.state_changed.connect(self._on_child_changed)
                self.option_widgets.append(widget)
                target_layout.addWidget(widget)
            elif isinstance(child, Group):
                self._add_group(child, target_layout)

    def _on_child_changed(self) -> None:
        self._update_conditions()
        self.state_changed.emit()

    def _update_conditions(self) -> None:
        for widget in self.option_widgets:
            option = widget.option
            if option.condition:
                visible = option.condition(self.state)
                widget.setVisible(visible)

            requires_met = all(self.state.get(req, False) for req in option.requires)
            widget.setEnabled(requires_met)

    def get_state(self) -> dict[str, object]:
        result = {}
        for widget in self.option_widgets:
            result.update(widget.get_state())
        return result

    def set_state(self, new_state: dict[str, object]) -> None:
        for widget in self.option_widgets:
            widget.set_state(new_state)
        self._update_conditions()
