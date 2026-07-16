# ProtonPromtConstructor

## Introduction to the project

This is a program written in Python, using PyQt6 for GUI. 

Its main goal is to provide the user GUI for constructing game launch prompt in Steam in Linux. Proton GE has many different toggles, settings etc. which the user has to to know, learn before setting his gamest. We are changing that by providing easy to navigate GUI, which will allow the user with small or no knowledge of Proton GE settings to set up the prompt.

So the outcome will be a lene of text, which the user will copy/paste into the steam for his game.

## Plan

We are implementing always only one phase of the plan.

- [ ] phase 1: Basic GUI
- [ ] phase 2: poolishing up the GUI
- [ ] phase 3: setting additional external tools

### phase 1: Basic GUI

At present time Proton GE supports following options

#### Enable HDR

It should work if you have:

- A compositor with HDR support
- A game with HDR support.
- A monitor with HDR support.

```bash
PROTON_ENABLE_HDR=1 %command%
```

> [!NOTE]
> Enabling HDR auto-enables the wine-wayland driver as it is a requirement.
> As of right now, in-game Steam overlay WILL NOT work with Wayland enabled.
> Please also note that Steam Input also does not work properly with the wine-wayland driver due to the overlay being broken.

##### Enabling NTSync
For NTSync to work, your kernel must be version 6.14 or newer and built with `CONFIG_NTSYNC=y` or `CONFIG_NTSYNC=m`. On non-systemd systems, you must also have a `ulimit -Hn` of 524288 or higher.
If using `CONFIG_NTSYNC=m`, a module loading configuration is required followed by a reboot:

/etc/modules-load.d/ntsync.conf
```
ntsync
```
You can also manually enable the module without reboot, just keep in mind the above configuration is needed for it to persist after reboots:
```
sudo modprobe ntsync
```
If on a non-systemd system with an inadequate `ulimit -Hn`, adjusting limits is required followed by a reboot:

/etc/security/limits.d/26-steam-nofile.conf
```
*               hard    nofile             524288
```

Environment variable options:

| Compat config string  | Environment Variable           | Description  |
| :-------------------- | :----------------------------- | :----------- |
|                       | PROTON_LOG            | Convenience method for dumping a useful debug log to `$HOME/steam-$APPID.log`. For more thorough logging, use `user_settings.py`. |
|                       | PROTON_DUMP_DEBUG_COMMANDS | When running a game, Proton will write some useful debug scripts for that game into `$PROTON_DEBUG_DIR/proton_$USER/`. |
|                       | PROTON_DEBUG_DIR      | Root directory for the Proton debug scripts, `/tmp` by default. |
| wined3d      | PROTON_USE_WINED3D    | Use OpenGL-based wined3d instead of Vulkan-based DXVK for d3d11 and d3d10. This used to be called `PROTON_USE_WINED3D11`, which is now an alias for this same option. |
| nod3d12      | PROTON_NO_D3D12       | Disables DX12. |
| nod3d11      | PROTON_NO_D3D11       | Disables DX11. |
| nod3d10      | PROTON_NO_D3D10       | Disables DX10. |
| nod3d9      | PROTON_NO_D3D9        | Disables DX9.  |
| noesync      | PROTON_NO_ESYNC       | Do not use eventfd-based in-process synchronization primitives. |
| nofsync      | PROTON_NO_FSYNC       | Do not use futex-based in-process synchronization primitives. (Automatically disabled on systems with no `FUTEX_WAIT_MULTIPLE` support.) |
| nontsync      | PROTON_NO_NTSYNC       | Do not use the ntsync kernel module for in-process synchronization primitives. |
| forcelgadd   | PROTON_FORCE_LARGE_ADDRESS_AWARE | Force Wine to enable the LARGE_ADDRESS_AWARE flag for all executables. |
| heapdelayfree| PROTON_HEAP_DELAY_FREE| Delay freeing some memory, to work around application use-after-free bugs. |
|                       | HOST_LC_ALL           | Set value to a locale to override all other system locale settings for a game.  This variable should be used instead of `LC_ALL`. |
| enablenvapi  | PROTON_ENABLE_NVAPI   | Enable NVIDIA's NVAPI GPU support library. |
| noforcelgadd |                                | Disable forcelgadd. If both this and `forcelgadd` are set, enabled wins. |
| oldglstr     | PROTON_OLD_GL_STRING  | Set some driver overrides to limit the length of the GL extension string, for old games that crash on very long extension strings. |
| cmdlineappend:|                               | Append the string after the colon as an argument to the game command. May be specified more than once. Escape commas and backslashes with a backslash. |
| xalia or noxalia               | PROTON_USE_XALIA                 | Enable Xalia, a program that can add a gamepad UI for some keyboard/mouse interfaces, or set to 0 to disable. The default is to enable it dynamically based on window contents. |
| seccomp      | PROTON_USE_SECCOMP    | Enable seccomp-bpf filter to emulate native syscalls, required for some DRM protections to work. |
| nowritewatch | PROTON_NO_WRITE_WATCH | Disable support for memory write watches in ntdll. This should only be applied if you have verified that the game can operate without write watches. This can improves performance for some very specific games. |
|                       | WINE_FULLSCREEN_FSR   | Enable AMD FidelityFX Super Resolution (FSR), use in conjunction with `WINE_FULLSCREEN_FSR_STRENGTH`. Only works in Vulkan games (DXVK and VKD3D-Proton included). |
|                       | WINE_FULLSCREEN_FSR_STRENGTH | AMD FidelityFX Super Resolution (FSR) strength, the default sharpening of 5 is enough without needing modification, but can be changed with 0-5 if wanted. 0 is the maximum sharpness, higher values mean less sharpening. 2 is the AMD recommended default and is set by GE-Proton by default. |
|                       | WINE_FULLSCREEN_FSR_CUSTOM_MODE | Set fake resolution of the screen. This can be useful in games that render in native resolution regardless of the selected resolution. Parameter `WIDTHxHEIGHT` |
|                       | WINE_DO_NOT_CREATE_DXGI_DEVICE_MANAGER | Set to 1 to enable. Required for video playback in some games to not be miscolored (usually tinted pink) |
|                       | COPYPREFIX | Set to 1 to enable. If -steamdeck is used on steam (or SteamDeck=1 is set), copies the game's prefix and shader cache from the game partition to the local steam steamapps folder. Logic is reversed if -steamdeck not enabled (or SteamDeck=0) |
| `fsr4`               | `PROTON_FSR4_UPGRADE`          | Automatically download `amdxcffx64.dll` and upgrade games with FSR 3.1 to use FSR 4. Version to download can be specified by supplying it as a value, like so `PROTON_FSR4_UPGRADE="4.0.1"`, instead of `1`. Downloads version `4.0.2` of the required DLL by default. This option also disables AMD Anti-Lag 2 currently due to various issues.                                                                                      |
| `fsr4hud`            | `PROTON_FSR4_INDICATOR`        | Enable the FSR4 watermark at the top left portion of the screen.                                                                                                                                                                                                                                                                                                                                                                      |
| `fsr4rdna3`          | `PROTON_FSR4_RDNA3_UPGRADE`    | Identical to `PROTON_FSR4_UPGRADE` but for RDNA3 GPUs. Enables some required compatibility options and downloads version `4.0.0` of the DLL by default.                                                                                                                                                                                                                                                                               |
| `fsr3`               | `PROTON_FSR3_UPGRADE`          |                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `dlss`               | `PROTON_DLSS_UPGRADE`          | Automatically download and use newer versions of `nvngx_dlss(d\|g).dll` DLLs. Version to download can be specified by supplying it as a value, like so `PROTON_DLSS_UPGRADE="310.2"`, instead of `1`, to download version `310.2.1.0`. This option also sets `DXVK_NVAPI_DRS_SETTINGS` to use the latest preset. If you provide your own config for it through this environment variable, your configuration is going to be applied.. |
| `dlsshud`            | `PROTON_DLSS_INDICATOR`        | Enable the DLSS overlay at the bottom left portion of the screen. This is exactly the same as `FSR4_WATERMARK=1`                                                                                                                                                                                                                                                                                                                      |
| `xess`               | `PROTON_XESS_UPGRADE`          |                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `sdlinput`           | `PROTON_USE_SDL` or `PROTON_PREFER_SDL` | Uses SDL input instead of HIDRAW/Steam Input. |
| `wayland`            | `PROTON_USE_WAYLAND` or `PROTON_ENABLE_WAYLAND` | Enables the Wayland driver. |
| `wow64`              | `PROTON_USE_WOW64`             | Enables wow64. |
|                      | `WAYLANDDRV_PRIMARY_MONITOR`   | Specify primary monitor where the value is something like `eDP-1`. Requires the Wayland driver. |
|                      | `PROTON_ENABLE_MEDIACONV`      | Enable media converter for winegstreamer. This is not needed for winedmo, since the mediaconverter implementation of the codecs doesn't override the underlying implementation. |
|                      | `WAYLANDDRV_RAWINPUT`          | A value of 0 disables unaccelerated input and uses accelerated input. Any positive real number (like 0.5) adjusts the sensitivity of rawinput. Requires the Wayland driver. |

Some optins are mutually exclusive and the GUI needs to reflect that. It would be nice if we were able to detect some system properties to limit available options.

As you can see the problem is relatively complex, so first formulate plan and save its copy into file `PLAN.md`.

### phase 2: poolishing up the GUI

TODO

### phase 3: setting additional external to

TODO