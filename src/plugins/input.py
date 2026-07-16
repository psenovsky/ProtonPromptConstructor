from src.models import Option, Group, GroupType


def get_options() -> list[Option | Group]:
    return [
        Group(
            name="input",
            label="Input",
            type=GroupType.CARD,
            children=[
                Option(
                    key="sdlinput",
                    label="Use SDL input instead of HIDRAW/Steam Input",
                    env_key="PROTON_USE_SDL",
                ),
                Option(
                    key="xalia",
                    label="Enable Xalia gamepad UI for keyboard/mouse interfaces",
                    tooltip="Default: dynamically enabled based on window contents.",
                    env_key="PROTON_USE_XALIA",
                ),
            ],
        )
    ]
