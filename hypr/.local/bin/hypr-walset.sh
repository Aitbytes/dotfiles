#!/usr/bin/env bash

# Default wallpaper directory - can be overridden by WALLPAPER_DIR env variable
WALLPAPER_DIR=${WALLPAPER_DIR:-"$HOME/Pictures/Wallpapers"}
HYPRPAPER_CONFIG="$HOME/.config/hypr/hyprpaper.conf"

selected_wallpaper=""

# Default to 'select' if no argument is provided
mode=${1:-select}

case "$mode" in
    "random")
        selected_wallpaper=$(find "$WALLPAPER_DIR" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" -o -name "*.gif" \) | shuf -n 1)
        ;;
    "select")
        selected_wallpaper=$(find "$WALLPAPER_DIR" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" -o -name "*.gif" \) | wofi --dmenu -p "Select Wallpaper")
        ;;
    *)
        echo "Invalid argument: $1"
        echo "Usage: $0 [select|random]"
        exit 1
        ;;
esac

if [ -z "$selected_wallpaper" ]; then
    echo "No wallpaper selected."
    exit 0 # Exit gracefully if user cancels selection
fi

# Kill existing hyprpaper instance if running
if pgrep -x "hyprpaper" > /dev/null; then
    pkill hyprpaper
fi

# Update hyprpaper configuration
sed -i "s|preload = .*|preload = $selected_wallpaper|" "$HYPRPAPER_CONFIG"
sed -i "s|wallpaper = .*|wallpaper = ,$selected_wallpaper|" "$HYPRPAPER_CONFIG"

# Start hyprpaper in the background
hyprpaper &

# Apply colors with wallust
wallust run "$selected_wallpaper"

echo "Wallpaper set to $selected_wallpaper"
