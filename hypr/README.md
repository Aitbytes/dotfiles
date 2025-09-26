# Hyprland Configuration

This is a personalized Hyprland configuration that includes custom scripts, themes, and keybindings.

## Overview

This setup is designed for a dual-monitor environment and uses `hyprpaper` for wallpaper management, `waybar` as a status bar, and `wofi` as an application launcher. It features a `dwindle` layout, custom animations, and a script for dynamically changing wallpapers.

## Key Features

### Appearance
- **Layout**: Uses the `dwindle` layout with `pseudotile` enabled.
- **Gaps**: Outer gaps of `20px` and inner gaps of `5px`.
- **Borders**: Active windows have a colorful, gradient border, while inactive windows have a simple grey border.
- **Rounding**: Windows have a `10px` corner radius.
- **Effects**: Blur and shadows are enabled for a modern look.
- **Animations**: Numerous animations are enabled for workspaces, windows, and layers to provide a fluid user experience.

### Keybindings
The main modifier key is `SUPER` (Windows key).

| Keybinding              | Action                                       |
| ----------------------- | -------------------------------------------- |
| `SUPER + Return`        | Open terminal (`alacritty`)                  |
| `SUPER + D`             | Open application menu (`wofi`)               |
| `SUPER + X`             | Close active window                          |
| `SUPER + SHIFT + E`     | Exit Hyprland                                |
| `SUPER + F`             | Toggle fullscreen                            |
| `SUPER + E`             | Toggle split direction in dwindle layout     |
| `SUPER + SHIFT + space` | Toggle floating for the active window        |
| `SUPER + h/j/k/l`       | Move focus                                   |
| `SUPER + [1-9,0]`       | Switch to a different workspace              |
| `SUPER + SHIFT + [1-9,0]`| Move active window to a different workspace  |
| `SUPER + S`             | Toggle the special workspace (scratchpad)    |
| `SUPER + SHIFT + W`     | Change wallpaper using `hypr-walset.sh`      |
| `SUPER + Print`         | Take a screenshot of a window                |
| `Print`                 | Take a screenshot of a monitor               |
| `SHIFT + Print`         | Take a screenshot of a region                |
| `SUPER + SHIFT + X`     | Lock the screen (`hyprlock`)                 |
| `XF86Audio*` keys       | Control volume and media playback (`playerctl`)|
| `XF86MonBrightness*` keys| Adjust screen brightness (`brightnessctl`)   |

### Wallpaper Management

The `hypr-walset.sh` script provides an easy way to change wallpapers.
- It uses `sxiv` to open a thumbnail view of your wallpapers located in `~/Pictures/Wallpapers`.
- After selecting an image, the script automatically updates the `hyprpaper.conf` and restarts `hyprpaper` to apply the new wallpaper.
- This script is bound to `SUPER + SHIFT + W`.

### Monitor and Workspace Configuration
- **`monitors.conf`**: Configures two monitors, `eDP-1` and `HDMI-A-1`, with specific resolutions and positions.
- **`workspaces.conf`**: Sets the default workspace to be on the `HDMI-A-1` monitor.

## File Structure

- `hyprland.conf`: The main configuration file.
- `hyprpaper.conf`: Configuration for `hyprpaper`, defines the wallpaper path.
- `monitors.conf`: Monitor setup.
- `workspaces.conf`: Default workspace rules.
- `.local/bin/hypr-walset.sh`: Script for changing wallpapers.
