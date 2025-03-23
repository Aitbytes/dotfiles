#!/bin/bash

CONFIG_FILE_LOCATION="$HOME/.config/rclone/rclone.conf"
REMOTES_DIRS_LOCATION="$HOME/mnt/"

mountRemote() {
  while read -r data; do
    mkdir -p "$REMOTES_DIRS_LOCATION$data"
    rclone mount --daemon $data: "$REMOTES_DIRS_LOCATION$data"  
  done
  # rclone mount --daemon $1
  
}

deleteMounts(){
  while read -r data; do
    fusermount -uz "$REMOTES_DIRS_LOCATION$data"
    rm -r "$REMOTES_DIRS_LOCATION$data"
  done
}



if [[ $1 = "-mount" ]]; then
  echo mount
  grep "\[.*\]" "$CONFIG_FILE_LOCATION" | sed --regexp-extended "s/\[(.*)\]/\1/g" | mountRemote 
  
elif [[ $1 = "-unmount" ]]; then
  echo unmount
  grep "\[.*\]" "$CONFIG_FILE_LOCATION" | sed --regexp-extended "s/\[(.*)\]/\1/g" | deleteMounts 
elif [[ $1 = "-list" ]]; then
  grep "\[.*\]" "$CONFIG_FILE_LOCATION" | sed --regexp-extended "s/\[(.*)\]/\1/g"  
else 
  echo "bad parameter"
fi

