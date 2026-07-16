from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto


class OptionType(Enum):
    BOOL = auto()
    TEXT = auto()
    INT = auto()
    SLIDER = auto()


@dataclass
class Option:
    name: str
    env_var: str
    description: str
    option_type: OptionType = OptionType.BOOL
    compat_config: str = ""
    default_value: str | int | None = None
    min_value: int | None = None
    max_value: int | None = None
    requires: list[str] = field(default_factory=list)
    info: str = ""


@dataclass
class MutuallyExclusiveGroup:
    group_name: str
    options: list[str] = field(default_factory=list)


ALL_OPTIONS: dict[str, Option] = {}

MUTUALLY_EXCLUSIVE_GROUPS: list[MutuallyExclusiveGroup] = []


def _register(option: Option) -> Option:
    ALL_OPTIONS[option.name] = option
    return option


# ── Display / HDR / Wayland ──────────────────────────────────────────────

HDR = _register(Option(
    name="hdr",
    env_var="PROTON_ENABLE_HDR",
    description="Enable HDR support",
    compat_config="",
    info="Requires a compositor, game, and monitor with HDR support. "
         "Enabling HDR auto-enables the Wayland driver.",
))

WAYLAND = _register(Option(
    name="wayland",
    env_var="PROTON_USE_WAYLAND",
    description="Enable the Wayland driver",
    info="Steam overlay does not work with Wayland.",
))

WAYLAND_MONITOR = _register(Option(
    name="wayland_monitor",
    env_var="WAYLANDDRV_PRIMARY_MONITOR",
    description="Primary monitor (e.g. eDP-1)",
    option_type=OptionType.TEXT,
    requires=["wayland"],
))

WAYLAND_RAWINPUT = _register(Option(
    name="wayland_rawinput",
    env_var="WAYLANDDRV_RAWINPUT",
    description="Raw input sensitivity (0 = disabled, 0.5 = default)",
    option_type=OptionType.SLIDER,
    min_value=0,
    max_value=2,
    default_value=0,
    requires=["wayland"],
))

# ── Sync ──────────────────────────────────────────────────────────────────

NOESYNC = _register(Option(
    name="noesync",
    env_var="PROTON_NO_ESYNC",
    description="Disable esync",
    compat_config="noesync",
))

NOFSYNC = _register(Option(
    name="nofsync",
    env_var="PROTON_NO_FSYNC",
    description="Disable fsync",
    compat_config="nofsync",
    info="Automatically disabled on systems without FUTEX_WAIT_MULTIPLE support.",
))

NONTSYNC = _register(Option(
    name="nontsync",
    env_var="PROTON_NO_NTSYNC",
    description="Disable ntsync",
    compat_config="nontsync",
    info="Requires kernel 6.14+ with CONFIG_NTSYNC=y or =m.",
))

MUTUALLY_EXCLUSIVE_GROUPS.append(MutuallyExclusiveGroup(
    group_name="sync",
    options=["noesync", "nofsync", "nontsync"],
))

# ── Rendering ─────────────────────────────────────────────────────────────

WINED3D = _register(Option(
    name="wined3d",
    env_var="PROTON_USE_WINED3D",
    description="Use OpenGL-based wined3d instead of Vulkan-based DXVK",
    compat_config="wined3d",
))

NOD3D9 = _register(Option(
    name="nod3d9",
    env_var="PROTON_NO_D3D9",
    description="Disable DX9",
    compat_config="nod3d9",
))

NOD3D10 = _register(Option(
    name="nod3d10",
    env_var="PROTON_NO_D3D10",
    description="Disable DX10",
    compat_config="nod3d10",
))

NOD3D11 = _register(Option(
    name="nod3d11",
    env_var="PROTON_NO_D3D11",
    description="Disable DX11",
    compat_config="nod3d11",
))

NOD3D12 = _register(Option(
    name="nod3d12",
    env_var="PROTON_NO_D3D12",
    description="Disable DX12",
    compat_config="nod3d12",
))

# ── Upscaling — FSR ──────────────────────────────────────────────────────

FSR = _register(Option(
    name="fsr",
    env_var="WINE_FULLSCREEN_FSR",
    description="Enable AMD FidelityFX Super Resolution (FSR)",
    info="Only works in Vulkan games (DXVK and VKD3D-Proton).",
))

FSR_STRENGTH = _register(Option(
    name="fsr_strength",
    env_var="WINE_FULLSCREEN_FSR_STRENGTH",
    description="FSR sharpening strength (0 = max sharpness, 5 = least)",
    option_type=OptionType.SLIDER,
    min_value=0,
    max_value=5,
    default_value=2,
    requires=["fsr"],
))

FSR_CUSTOM_MODE = _register(Option(
    name="fsr_custom_mode",
    env_var="WINE_FULLSCREEN_FSR_CUSTOM_MODE",
    description="Custom resolution (WIDTHxHEIGHT, e.g. 1280x720)",
    option_type=OptionType.TEXT,
    requires=["fsr"],
))

FSR3 = _register(Option(
    name="fsr3",
    env_var="PROTON_FSR3_UPGRADE",
    description="Enable FSR 3 upgrade",
    requires=["fsr"],
))

FSR4 = _register(Option(
    name="fsr4",
    env_var="PROTON_FSR4_UPGRADE",
    description="Enable FSR 4 upgrade (downloads amdxcffx64.dll)",
    requires=["fsr"],
    info="Disables AMD Anti-Lag 2. Optionally specify version (e.g. 4.0.1).",
))

FSR4_RDNA3 = _register(Option(
    name="fsr4rdna3",
    env_var="PROTON_FSR4_RDNA3_UPGRADE",
    description="Enable FSR 4 upgrade for RDNA3 GPUs",
    requires=["fsr"],
    info="Downloads version 4.0.0 of the DLL by default.",
))

FSR4_HUD = _register(Option(
    name="fsr4hud",
    env_var="PROTON_FSR4_INDICATOR",
    description="Enable FSR4 watermark overlay",
    requires=["fsr"],
))

MUTUALLY_EXCLUSIVE_GROUPS.append(MutuallyExclusiveGroup(
    group_name="fsr_version",
    options=["fsr3", "fsr4", "fsr4rdna3"],
))

# ── Upscaling — DLSS ─────────────────────────────────────────────────────

DLSS = _register(Option(
    name="dlss",
    env_var="PROTON_DLSS_UPGRADE",
    description="Enable DLSS upgrade (downloads nvngx_dlss.dll)",
    info="Optionally specify version (e.g. 310.2).",
))

DLSS_HUD = _register(Option(
    name="dlsshud",
    env_var="PROTON_DLSS_INDICATOR",
    description="Enable DLSS overlay indicator",
    requires=["dlss"],
))

# ── Upscaling — XeSS ─────────────────────────────────────────────────────

XESS = _register(Option(
    name="xess",
    env_var="PROTON_XESS_UPGRADE",
    description="Enable XeSS upgrade",
))

# ── Upscaling vendor group (mutually exclusive) ──────────────────────────

MUTUALLY_EXCLUSIVE_GROUPS.append(MutuallyExclusiveGroup(
    group_name="upscaling_vendor",
    options=["fsr", "dlss", "xess"],
))

# ── Input ─────────────────────────────────────────────────────────────────

SDL_INPUT = _register(Option(
    name="sdlinput",
    env_var="PROTON_USE_SDL",
    description="Use SDL input instead of HIDRAW/Steam Input",
    compat_config="sdlinput",
))

XALIA = _register(Option(
    name="xalia",
    env_var="PROTON_USE_XALIA",
    description="Enable Xalia gamepad UI for keyboard/mouse interfaces",
    info="Default: dynamically enabled based on window contents.",
))

# ── Misc ──────────────────────────────────────────────────────────────────

FORCELGADD = _register(Option(
    name="forcelgadd",
    env_var="PROTON_FORCE_LARGE_ADDRESS_AWARE",
    description="Force LARGE_ADDRESS_AWARE flag for all executables",
    compat_config="forcelgadd",
))

HEAP_DELAY_FREE = _register(Option(
    name="heapdelayfree",
    env_var="PROTON_HEAP_DELAY_FREE",
    description="Delay freeing memory (workaround for use-after-free bugs)",
    compat_config="heapdelayfree",
))

OLD_GL_STRING = _register(Option(
    name="oldglstr",
    env_var="PROTON_OLD_GL_STRING",
    description="Limit GL extension string length (for old games)",
    compat_config="oldglstr",
))

SECCOMP = _register(Option(
    name="seccomp",
    env_var="PROTON_USE_SECCOMP",
    description="Enable seccomp-bpf filter for DRM support",
    compat_config="seccomp",
))

NOWRITEWATCH = _register(Option(
    name="nowritewatch",
    env_var="PROTON_NO_WRITE_WATCH",
    description="Disable memory write watches (performance for specific games)",
    compat_config="nowritewatch",
))

WOW64 = _register(Option(
    name="wow64",
    env_var="PROTON_USE_WOW64",
    description="Enable WoW64 support",
    compat_config="wow64",
))

DXGI_DEVICE_MANAGER = _register(Option(
    name="dxgi_device_manager",
    env_var="WINE_DO_NOT_CREATE_DXGI_DEVICE_MANAGER",
    description="Disable DXGI device manager (fix video playback color issues)",
))

COPY_PREFIX = _register(Option(
    name="copyprefix",
    env_var="COPYPREFIX",
    description="Copy prefix and shader cache to local steamapps folder",
))

MEDIA_CONV = _register(Option(
    name="mediaconv",
    env_var="PROTON_ENABLE_MEDIACONV",
    description="Enable media converter for winegstreamer",
))

HOST_LC_ALL = _register(Option(
    name="host_lc_all",
    env_var="HOST_LC_ALL",
    description="Override system locale for the game",
    option_type=OptionType.TEXT,
))

PROTON_LOG = _register(Option(
    name="proton_log",
    env_var="PROTON_LOG",
    description="Dump debug log to ~/steam-$APPID.log",
))

CMDLINE_APPEND = _register(Option(
    name="cmdlineappend",
    env_var="cmdlineappend",
    description="Extra arguments appended to the game command",
    option_type=OptionType.TEXT,
    info="Separate multiple arguments with commas. Escape with backslash.",
))
