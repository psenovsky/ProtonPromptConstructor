# ProtonPromptConstructor

A GUI application for constructing Proton GE game launch prompts in Steam on Linux.

## Purpose

Proton GE supports many different toggles and settings that users need to learn before configuring their games. This tool provides an easy-to-navigate GUI that allows users with small or no knowledge of Proton GE settings to set up launch prompts.

The outcome is a command line that you copy and paste into Steam's launch options for your game.

## Features

### Display / HDR

- Enable HDR support (auto-enables the Wayland driver as it is a requirement)
- Enable the Wayland driver independently (be carefull, you will not be able to use Steam while it is enabled)
- Set primary monitor name for Wayland
- Adjust raw input sensitivity for Wayland

### Sync

- Disable esync, fsync, or ntsync (mutually exclusive — only one can be active)

### Rendering

- Switch between Vulkan-based DXVK (default) and OpenGL-based wined3d
- Individually disable DX9, DX10, DX11, and DX12 (only available when using DXVK)

### Upscaling

- **AMD FSR:** Enable FSR with sharpening strength slider (0–5), custom resolution mode, and choice of FSR 3, FSR 4, or FSR 4 RDNA3 upgrades, plus a watermark overlay toggle
- **NVIDIA DLSS:** Enable DLSS upgrade with overlay indicator toggle
- **Intel XeSS:** Enable XeSS upgrade
- Vendor selection is mutually exclusive

### Input

- Use SDL input instead of HIDRAW/Steam Input
- Enable Xalia gamepad UI for keyboard/mouse interfaces

### Misc / Compatibility

- MangoHud overlay (prepended as a command prefix)
- Force LARGE_ADDRESS_AWARE
- Delay freeing memory (use-after-free workaround)
- Limit GL extension string length (for old games)
- Enable seccomp-bpf filter (required for some DRM)
- Disable memory write watches
- Enable WoW64 support
- Disable DXGI device manager (fixes pink-tinted video in some games)
- Enable media converter for winegstreamer
- Copy prefix and shader cache to local steamapps folder
- Dump debug log
- Locale override
- Custom extra command-line arguments (appended as `cmdlineappend:` entries)

### Smart UI Behavior

- **HDR forces Wayland on** — selecting HDR locks the Wayland driver to enabled
- **Wined3d disables DX options** — the DirectX version checkboxes are grayed out when using OpenGL
- **Sub-panels show/hide** — FSR and DLSS options are only visible when their vendor is selected
- **Dependency enforcement** — options that require another (e.g. FSR strength requires FSR enabled) are silently omitted from the prompt if the prerequisite is not active
- **Mutual exclusion in output** — conflicting options (sync modes, FSR versions, upscaling vendors) cannot appear together in the generated prompt
- **Slider defaults suppressed** — values at their default are not emitted, keeping the prompt clean

### Persistence

- Save all current settings to `defaults.json`
- Load saved defaults on startup or manually
- Reset all options to their off/empty state

## Requirements

- Linux
- Python 3.10+
- uv package manager

## Installation

```bash
git clone https://github.com/your-username/ProtonPromptConstructor.git
cd ProtonPromptConstructor
uv sync
```

## Usage

```bash
uv run python main.py
```

## License

GPL
