# Magic Cutter Portable Folders

This repo now includes ready-to-copy folder templates for both platforms:

- `Magic_Cutter_Win/CLICK_ME.bat`
- `Magic_Cutter_Mac/CLICK_ME.command`

## Windows setup
1. Copy the `Magic_Cutter_Win` folder to your Windows machine.
2. Download FFmpeg (e.g., from gyan.dev), unzip it, and copy `ffmpeg.exe` from the `bin` folder into `Magic_Cutter_Win`.
3. Put your `.mp4` and `.mov` files in the same folder.
4. Double-click `CLICK_ME.bat`.

## Mac setup
1. Copy the `Magic_Cutter_Mac` folder to your Mac.
2. Download FFmpeg (e.g., from evermeet.cx), and place the `ffmpeg` binary into `Magic_Cutter_Mac`.
3. Put your `.mp4` and `.mov` files in the same folder.
4. Double-click `CLICK_ME.command`.

## What the scripts do
- Convert input videos to 720p.
- Encode with H.264 video + AAC audio.
- Split each input into 15-minute chunks (`900` seconds).
- Produce files like `filename_part000.mp4`, `filename_part001.mp4`, etc.

## Create ZIPs for sharing
Zip each folder separately:
- `Magic_Cutter_Win.zip`
- `Magic_Cutter_Mac.zip`
