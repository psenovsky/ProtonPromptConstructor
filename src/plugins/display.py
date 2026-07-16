from src.models import Option, Group, GroupType


def get_options() -> list[Option | Group]:
    return [
        Group(
            name="display",
            label="Display / HDR",
            type=GroupType.CARD,
            children=[
                Option(
                    key="hdr",
                    label="Enable HDR support",
                    tooltip=(
                        "Requires a compositor, game, and monitor with HDR support. "
                        "Auto-enables the wine-wayland driver. Note: Steam overlay and "
                        "Steam Input do not work with Wayland."
                    ),
                    env_key="PROTON_ENABLE_HDR",
                    mutually_exclusive_with=["wayland"],
                    conflicts=["wayland"],
                ),
                Option(
                    key="wayland",
                    label="Enable the Wayland driver",
                    tooltip="Enables the wine-wayland driver for Wayland compositors.",
                    env_key="PROTON_USE_WAYLAND",
                    mutually_exclusive_with=["hdr"],
                ),
                Option(
                    key="wayland_monitor",
                    label="Primary monitor",
                    tooltip="Specify primary monitor, e.g. eDP-1. Requires the Wayland driver.",
                    type="str",
                    env_key="WAYLANDDRV_PRIMARY_MONITOR",
                    requires=["wayland"],
                    placeholder="e.g. eDP-1",
                ),
                Option(
                    key="wayland_rawinput",
                    label="Raw input sensitivity",
                    tooltip=(
                        "0 disables unaccelerated input and uses accelerated input. "
                        "Any positive real number adjusts sensitivity. Requires Wayland."
                    ),
                    type="int",
                    env_key="WAYLANDDRV_RAWINPUT",
                    default=0,
                    min_val=0,
                    max_val=20,
                    step=1,
                    scale=0.1,
                    requires=["wayland"],
                ),
            ],
        )
    ]
