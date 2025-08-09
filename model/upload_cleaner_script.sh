#!/bin/bash
UPLOAD_DIR="./uploads"
if [ ! -d "$UPLOAD_DIR" ]; then
    mkdir -p "$UPLOAD_DIR"
fi
INTERVAL=150  # 2.5 minutes
AGE_THRESHOLD=3600  # 1 hour
while true; do
    find "$UPLOAD_DIR" -type f -mmin +$((AGE_THRESHOLD / 60)) -exec rm -f {} \;
    sleep $INTERVAL
done