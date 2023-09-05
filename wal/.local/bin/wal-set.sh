#!/bin/bash

# Check if the argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path_to_wallpapers>"
    exit 1
fi

WALLPAPERS_PATH="$1"
VAULT_PATH="$HOME/Shared/My_second_brain"
POLYBAR_SCRIPTS_PATH="$HOME/.config/polybar/hack/scripts"
LIB="$HOME/.local/lib"

# Display the path for debugging purposes (can be removed if not needed)
echo "Using wallpapers from: $WALLPAPERS_PATH"

# select the image 
image_path=$(find "$WALLPAPERS_PATH" | shuf | head -n 1)

# Set the wallpaper and update related configurations
wal -n -i "$image_path" \
&& pywalfox update \
&& Glawal.sh \
&& "$LIB/pywal-obsidianmd/pywal-obsidianmd.sh" "$VAULT_PATH" \
&& "$POLYBAR_SCRIPTS_PATH/pywal.sh" \
&& sleep 0.05 \
&& polybar-msg cmd hide

feh --bg-max "$image_path"

