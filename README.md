# ProtonPromptConstructor

A GUI application for constructing Proton GE game launch prompts in Steam on Linux.

## Purpose

Proton GE supports many different toggles and settings that users need to learn before configuring their games. This tool provides an easy-to-navigate GUI that allows users with small or no knowledge of Proton GE settings to set up launch prompts.

The outcome is a command line that you copy and paste into Steam's launch options for your game.

## Features (Planned)

- Enable/disable HDR support
- Configure NTSync
- Set up FSR (FidelityFX Super Resolution)
- Configure DLSS and XeSS upscaling
- Toggle sync primitives (esync, fsync, ntsync)
- Set rendering options (wined3d, DirectX versions)
- Configure Wayland support
- And more...

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
