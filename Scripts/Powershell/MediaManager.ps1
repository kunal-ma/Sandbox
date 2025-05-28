# Task: Reference for Media Processing tools
# Description: A comprehensive list of commonly used commands for various media processing tools.

# Permissions: None
# Dependencies: Required tools (e.g., FFmpeg, yt-dlp) installed and available in PATH.

# WARNING: DO NOT EXECUTE AS-IS. Review each command carefully before running to ensure it matches your intended operation.

# --------------------------------------------------

# FFMPEG : Batch operation for files in current folder
mkdir output
Get-ChildItem -Filter "*.mp4" | ForEach-Object {`
    $inputFile = $_.FullName`
    $outputFile = "output\$($_.Name)"`
    ffmpeg -i "$inputFile" <Operations> "$outputFile"`
}

# --------------------------------------------------

# YT-DLP : List all options for downloading
yt-dlp -F https://www.youtube.com/watch?v=oBpaB2YzX8s

# YT-DLP : Download video at 480p resolution
yt-dlp -f "bestvideo[height<=480]+bestaudio/best[height<=480]" --merge-output-format mp4 <URL>

# --------------------------------------------------

# YT-DLP : Download best audio available
yt-dlp -f "bestaudio" <URL>

# FFMPEG : Convert WebM audio to OPUS
ffmpeg -i input.webm -vn -acodec copy output.opus

# FFMPEG : Convert OPUS to MP3 losslessly
ffmpeg -i input.opus -c:a libmp3lame -q:a 0 output.mp3

# --------------------------------------------------

# FFMPEG : Rotate video by an angle losslessly
ffmpeg -i input.mp4 -display_rotation:v:0 -90.0 -c copy output.mp4

# FFMPEG : Calculate cropped resolution for videos with black border
ffplay -i input.mp4 -vf cropdetect

# FFMPEG : Test video with cropped resolution
# The elements in the crop are : Width:Height:X:Y
ffplay -i input.mp4 -vf “crop=720:528:0:376"

# FFMPEG : Crop video to remove black borders (almost lossless)
# If video has been rotated using the command provided above, 
# add -noautorotate after ffmpeg to avoid errors of Invalid too big
ffmpeg -i input.mp4 -vf “crop=720:528:0:376” -c:v libx264 -preset slow -crf 22 -c:a copy output.mp4

# --------------------------------------------------
