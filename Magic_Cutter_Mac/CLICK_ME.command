#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -f ./ffmpeg ]; then
    echo "Missing ffmpeg file!"
    echo "Please copy the ffmpeg binary into this folder and try again."
    exit 1
fi

chmod +x ./ffmpeg

echo "Processing all MP4 and MOV files..."
found=0
for f in *.mp4 *.mov; do
    [ -e "$f" ] || continue
    found=1
    ./ffmpeg -y -i "$f" -vf scale=-2:720 -c:v libx264 -crf 23 -preset veryfast -c:a aac -b:a 128k -f segment -segment_time 900 -reset_timestamps 1 "${f%.*}_part%03d.mp4"
done

if [ "$found" -eq 0 ]; then
    echo "No .mp4 or .mov files found in this folder."
fi

echo "DONE! You can close this window."
