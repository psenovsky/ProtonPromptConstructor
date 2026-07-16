from src.models import Option, Group, GroupType


def get_options() -> list[Option | Group]:
    return [
        Group(
            name="misc_compatibility",
            label="Compatibility & Overlay",
            type=GroupType.CARD,
            children=[
                Option(
                    key="mangohud",
                    label="Enable MangoHud overlay",
                    tooltip="Requires MangoHud to be installed on the system.",
                    prefix="mangohud",
                ),
                Option(
                    key="forcelgadd",
                    label="Force LARGE_ADDRESS_AWARE",
                    tooltip="Force Wine to enable the LARGE_ADDRESS_AWARE flag for all executables.",
                    env_key="PROTON_FORCE_LARGE_ADDRESS_AWARE",
                ),
                Option(
                    key="heapdelayfree",
                    label="Delay freeing memory",
                    tooltip="Delay freeing some memory, to work around application use-after-free bugs.",
                    env_key="PROTON_HEAP_DELAY_FREE",
                ),
                Option(
                    key="oldglstr",
                    label="Limit GL extension string length",
                    tooltip="Set some driver overrides to limit the length of the GL extension string, for old games that crash on very long extension strings.",
                    env_key="PROTON_OLD_GL_STRING",
                ),
                Option(
                    key="seccomp",
                    label="Enable seccomp-bpf filter for DRM",
                    tooltip="Enable seccomp-bpf filter to emulate native syscalls, required for some DRM protections to work.",
                    env_key="PROTON_USE_SECCOMP",
                ),
                Option(
                    key="nowritewatch",
                    label="Disable memory write watches",
                    tooltip="Disable support for memory write watches in ntdll. This can improve performance for some very specific games.",
                    env_key="PROTON_NO_WRITE_WATCH",
                ),
                Option(
                    key="wow64",
                    label="Enable WoW64 support",
                    env_key="PROTON_USE_WOW64",
                ),
            ],
        ),
        Group(
            name="misc_video",
            label="Video & Media",
            type=GroupType.CARD,
            children=[
                Option(
                    key="dxgi_device_manager",
                    label="Disable DXGI device manager",
                    tooltip="Required for video playback in some games to not be miscolored (usually tinted pink).",
                    env_key="WINE_DO_NOT_CREATE_DXGI_DEVICE_MANAGER",
                ),
                Option(
                    key="mediaconv",
                    label="Enable media converter",
                    tooltip="Enable media converter for winegstreamer. Not needed for winedmo.",
                    env_key="PROTON_ENABLE_MEDIACONV",
                ),
                Option(
                    key="copyprefix",
                    label="Copy prefix and shader cache",
                    tooltip="If -steamdeck is used on steam (or SteamDeck=1 is set), copies the game's prefix and shader cache from the game partition to the local steam steamapps folder.",
                    env_key="COPYPREFIX",
                ),
            ],
        ),
        Group(
            name="misc_troubleshooting",
            label="Troubleshooting",
            type=GroupType.CARD,
            children=[
                Option(
                    key="proton_log",
                    label="Dump debug log",
                    tooltip="Convenience method for dumping a useful debug log to $HOME/steam-$APPID.log.",
                    env_key="PROTON_LOG",
                ),
            ],
        ),
        Group(
            name="misc_locale",
            label="Locale",
            type=GroupType.CARD,
            children=[
                Option(
                    key="host_lc_all",
                    label="Locale override",
                    tooltip="Set value to a locale to override all other system locale settings for a game. This variable should be used instead of LC_ALL.",
                    type="str",
                    env_key="HOST_LC_ALL",
                    placeholder="e.g. en_US.UTF-8",
                ),
            ],
        ),
        Group(
            name="misc_arguments",
            label="Extra Arguments",
            type=GroupType.CARD,
            children=[
                Option(
                    key="cmdlineappend",
                    label="Command-line arguments",
                    tooltip="Append the string as an argument to the game command. May be specified more than once. Separate multiple arguments with commas.",
                    type="str",
                    cmdlineappend=True,
                    placeholder="e.g. --some-flag,--other-flag",
                ),
            ],
        ),
    ]
