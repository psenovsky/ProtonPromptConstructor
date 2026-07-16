from src.models import Option, Group, GroupType


def get_options() -> list[Option | Group]:
    return [
        Group(
            name="sync",
            label="Sync",
            type=GroupType.CARD,
            children=[
                Option(
                    key="noesync",
                    label="Disable esync",
                    tooltip="Do not use eventfd-based in-process synchronization primitives.",
                    env_key="PROTON_NO_ESYNC",
                    mutually_exclusive_with=["nofsync", "nontsync"],
                ),
                Option(
                    key="nofsync",
                    label="Disable fsync",
                    tooltip="Do not use futex-based in-process synchronization primitives. Automatically disabled on systems without FUTEX_WAIT_MULTIPLE support.",
                    env_key="PROTON_NO_FSYNC",
                    mutually_exclusive_with=["noesync", "nontsync"],
                ),
                Option(
                    key="nontsync",
                    label="Disable ntsync",
                    tooltip="Do not use the ntsync kernel module for in-process synchronization primitives. Requires kernel 6.14+ with CONFIG_NTSYNC=y or =m.",
                    env_key="PROTON_NO_NTSYNC",
                    mutually_exclusive_with=["noesync", "nofsync"],
                ),
            ],
            exclusive_children=True,
        )
    ]
