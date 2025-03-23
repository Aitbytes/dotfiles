#!bash

# Check if the argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path_to_wallpapers>"
    exit 1
fi

WALLPAPERS_PATH="$1"
VAULT_PATH="$HOME/My_second_brain"
POLYBAR_SCRIPTS_PATH="$HOME/.config/polybar/cuts/scripts"
LIB="$HOME/.local/lib"

function resize_fill() {
  local image_path="$1"
  local image_name=$(basename "$image_path")
  local output_path="/tmp/${image_name%.*}-resized.${image_name##*.}"
  local height=1080
  local width=1920
  local background_color="black"

  # Check if the image file exists
  if [[ ! -f "$image_path" ]]; then
    echo "Error: File not found at '$image_path'"
    return  1
  fi

  # Use convert to resize the image to the calculated dimensions and fill with the background color
  convert "$image_path" -resize "${width}x${height}" -background "$background_color" -gravity center -extent "${width}x${height}" "$output_path"

  echo "$output_path"
}


# Display the path for debugging purposes (can be removed if not needed)
echo "Using wallpapers from: $WALLPAPERS_PATH"

# select the image 
image_path=$(find "$WALLPAPERS_PATH" | shuf | head -n 1)

resized_path=$(resize_fill "$image_path")

# Set the wallpaper and update related configurations
wal -n -i "$resized_path" \
&& pywalfox update \
&& Glawal.sh \
&& "$LIB/pywal-obsidianmd/pywal-obsidianmd.sh" "$VAULT_PATH" \
&& "$POLYBAR_SCRIPTS_PATH/pywal.sh" "$image_path"\
#&& sleep 0.05 \
#&& polybar-msg cmd hide

feh --bg-max --no-fehbg "$resized_path"

rm "$resized_path"

