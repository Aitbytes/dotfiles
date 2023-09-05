#!/bin/bash
#
layout="$HOME/.config/i3/layouts/workspace-2.json"
i3-msg "workspace 2; append_layout $layout"

(alacritty -e zsh -c tmux &)
(alacritty -e zsh -c htop &)
(alacritty -e zsh -c "neofetch ; zsh") &
