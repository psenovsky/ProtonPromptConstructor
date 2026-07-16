from src.models import Option, Group, GroupType


def get_options() -> list[Option | Group]:
    return [
        Group(
            name="upscaling",
            label="Upscaling",
            type=GroupType.CARD,
            exclusive_children=True,
            children=[
                Option(
                    key="fsr",
                    label="Enable AMD FSR (FidelityFX Super Resolution)",
                    tooltip="Only works in Vulkan games (DXVK and VKD3D-Proton).",
                    env_key="WINE_FULLSCREEN_FSR",
                    mutually_exclusive_with=["dlss", "xess"],
                    exclusive_children=True,
                    children=[
                        Option(
                            key="fsr3",
                            label="FSR 3 upgrade",
                            env_key="PROTON_FSR3_UPGRADE",
                            mutually_exclusive_with=["fsr4", "fsr4rdna3"],
                        ),
                        Option(
                            key="fsr4",
                            label="FSR 4 upgrade",
                            tooltip="Downloads amdxcffx64.dll. Disables AMD Anti-Lag 2. Optionally specify version.",
                            env_key="PROTON_FSR4_UPGRADE",
                            mutually_exclusive_with=["fsr3", "fsr4rdna3"],
                        ),
                        Option(
                            key="fsr4rdna3",
                            label="FSR 4 RDNA3 upgrade",
                            tooltip="For RDNA3 GPUs. Downloads version 4.0.0 of the DLL by default.",
                            env_key="PROTON_FSR4_RDNA3_UPGRADE",
                            mutually_exclusive_with=["fsr3", "fsr4"],
                        ),
                        Option(
                            key="fsr4hud",
                            label="FSR4 watermark overlay",
                            env_key="PROTON_FSR4_INDICATOR",
                        ),
                        Option(
                            key="fsr_strength",
                            label="Sharpening strength",
                            tooltip="0 = max sharpness, 5 = least sharpness. Default: 2.",
                            type="int",
                            env_key="WINE_FULLSCREEN_FSR_STRENGTH",
                            default=2,
                            min_val=0,
                            max_val=5,
                        ),
                        Option(
                            key="fsr_custom_mode",
                            label="Custom resolution",
                            tooltip="Set fake resolution (WIDTHxHEIGHT). Useful for games that ignore resolution selection.",
                            type="str",
                            env_key="WINE_FULLSCREEN_FSR_CUSTOM_MODE",
                            items=["1280x720", "1600x900", "1920x1080", "2560x1440", "3840x2160", "1024x768", "1680x1050", "2560x1600"],
                            editable=True,
                        ),
                    ],
                ),
                Option(
                    key="dlss",
                    label="Enable NVIDIA DLSS",
                    tooltip="Automatically downloads newer nvngx_dlss(d|g).dll DLLs.",
                    env_key="PROTON_DLSS_UPGRADE",
                    mutually_exclusive_with=["fsr", "xess"],
                    children=[
                        Option(
                            key="dlsshud",
                            label="DLSS overlay indicator",
                            env_key="PROTON_DLSS_INDICATOR",
                        ),
                    ],
                ),
                Option(
                    key="xess",
                    label="Enable Intel XeSS",
                    tooltip="Automatically downloads XeSS DLLs.",
                    env_key="PROTON_XESS_UPGRADE",
                    mutually_exclusive_with=["fsr", "dlss"],
                ),
            ],
        )
    ]
