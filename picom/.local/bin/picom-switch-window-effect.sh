#!/bin/bash

# Get the current focused window's ID
window_id=$(xdotool getactivewindow)

# Extract the window's class name
class_name=$(xprop -id $window_id | grep "WM_CLASS(STRING)" | awk -F '"' '{print $4}')

# Define the configuration file path
config_file="$HOME/.config/picom/picom.conf"

# Check the current state of the window
state_file="$HOME/.cache/window_states/window_state_$class_name"
if [ ! -f $state_file ]; then
  echo "0" > $state_file
fi
state=$(cat $state_file)

# Toggle between states
case $state in
  0)
    # Set opacity to 95
    sed -i "/opacity-rule = \[/a\  \"95:class_g = '$class_name'\"," $config_file
    echo "1" > $state_file
    ;;
  1)
    #Set opacity to 85
    sed -i "/opacity-rule = \[/{:a;N;/\];/!ba;s/  \"95:class_g = '$class_name'\",\n//}" $config_file
    sed -i "/opacity-rule = \[/a\  \"85:class_g = '$class_name'\"," $config_file
    echo "2" > $state_file
    ;;
  2)
    # Exclude from blurring
    # sed -i "/opacity-rule = \[/{:a;N;/\];/!ba;s/  \"85:class_g = '$class_name'\",\n//}" $config_file
    sed -i "/blur-background-exclude = \[/a\  \"class_g = '$class_name'\"," $config_file
    echo "3" > $state_file
    ;;
  3)
    # Reset to initial state
    sed -i "/opacity-rule = \[/{:a;N;/\];/!ba;s/  \"85:class_g = '$class_name'\",\n//}" $config_file
    sed -i "/blur-background-exclude = \[/{:a;N;/\];/!ba;s/  \"class_g = '$class_name'\",\n//}" $config_file
    rm $state_file
    ;;
esac
 

# Reload picom to apply the changes
# pkill -USR1 picom

