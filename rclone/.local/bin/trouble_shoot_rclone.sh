#!/bin/bash

# Define your service name and user
SERVICE_USER="a8taleb"
SERVICE_GROUP="users"
REMOTE="Cloud_Dropbox_General_Medangi_ait_161123"
MOUNT_POINT="/home/a8taleb/Remotes/$REMOTE"
SERVICE_NAME="rclone@$REMOTE"

# Check if systemd syntax is correct
echo "Checking systemd syntax..."
systemd-analyze verify /etc/systemd/system/${SERVICE_NAME}.service
if [ $? -ne 0 ]; then
    echo "Systemd syntax has errors."
    exit 1
else
    echo "Systemd syntax is OK."
fi

# Check if user and group exist
echo "Checking if user and group exist..."
if ! id "$SERVICE_USER" &>/dev/null; then
    echo "User $SERVICE_USER does not exist."
    exit 1
else
    echo "User exists."
fi

if ! getent group "$SERVICE_GROUP" &>/dev/null; then
    echo "Group $SERVICE_GROUP does not exist."
    exit 1
else
    echo "Group exists."
fi

# Check if mount point directory exists and writable
echo "Checking if mount point directory exists and is writable..."
if [ ! -d "$MOUNT_POINT" ]; then
    echo "Mount point directory $MOUNT_POINT does not exist."
    exit 1
elif [ ! -w "$MOUNT_POINT" ]; then
    echo "Mount point directory $MOUNT_POINT is not writable."
    exit 1
else
    echo "Mount point directory is OK."
fi

# Check service status
echo "Checking service status..."
systemctl status $SERVICE_NAME
if [ $? -ne 0 ]; then
    echo "Service $SERVICE_NAME has issues."
    exit 1
else
    echo "Service $SERVICE_NAME is running fine."
fi

echo "All checks passed."

