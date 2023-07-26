#!/bin/bash


wallpapers=$1
vault=$HOME/Shared/My_second_brain
Scripts=$HOME/Scripts/wal/Scripts
wal -i $wallpapers && pywalfox update && $Scripts/Glawal.sh && $Scripts/pywal-obsidianmd/pywal-obsidianmd.sh $vault && $HOME/.config/polybar/hack/scripts/pywal.sh

