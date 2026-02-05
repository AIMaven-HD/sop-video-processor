@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

if not exist "ffmpeg.exe" (
    echo Missing ffmpeg.exe!
    echo Please copy ffmpeg.exe into this folder and try again.
    pause
    exit /b 1
)

echo Processing all MP4 and MOV files...
set "found=0"
for %%F in (*.mp4 *.mov) do (
    if exist "%%F" (
        set "found=1"
        if /I not "%%~nF"=="output" (
            echo Processing: %%F
            ffmpeg.exe -y -i "%%F" -vf scale=-2:720 -c:v libx264 -crf 23 -preset veryfast -c:a aac -b:a 128k -f segment -segment_time 900 -reset_timestamps 1 "%%~nF_part%%03d.mp4"
        )
    )
)

if "!found!"=="0" (
    echo No .mp4 or .mov files found in this folder.
)

echo DONE!
pause
