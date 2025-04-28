#!/usr/bin/env bash

# Default wallpaper directory - can be overridden by WALLPAPER_DIR env variable
WALLPAPER_DIR=${WALLPAPER_DIR:-"$HOME/Pictures/Wallpapers"}
HYPRPAPER_CONFIG="$HOME/.config/hypr/hyprpaper.conf"

# Check if hyprpaper is running and kill it if it is
if pgrep -x "hyprpaper" > /dev/null; then
    killall hyprpaper
fi

# Use sxiv to select wallpaper
selected_wallpaper=$(sxiv -t -o "$WALLPAPER_DIR")

# Check if user selected a wallpaper
if [ -n "$selected_wallpaper" ]; then
    # Update hyprpaper config
    sed -i "s|preload = .*|preload = $selected_wallpaper|" "$HYPRPAPER_CONFIG"
    sed -i "s|wallpaper = .*|wallpaper = ,$selected_wallpaper|" "$HYPRPAPER_CONFIG"
    
    # Start hyprpaper
    hyprpaper &
else
    echo "No wallpaper selected"
    exit 1
fi

