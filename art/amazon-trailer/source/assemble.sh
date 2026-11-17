#!/bin/bash
# Черновик тизера: крушение 5 с → белая вспышка в чёрное → рация → титул 33 DAYS. 13 секунд.
set -e
cd "$(dirname "$0")"
ffmpeg -loglevel error -y -framerate 24 -i ../frames_cut/f_%04d.png -vf "scale=1280:720:flags=lanczos,eq=saturation=1.15:contrast=1.05,format=yuv420p" -c:v libx264 -crf 18 crash.mp4
ffmpeg -loglevel error -y \
  -i crash.mp4 \
  -f lavfi -t 0.4 -i "color=c=white:s=1280x720:r=24" \
  -loop 1 -t 3.2 -framerate 24 -i radio.png \
  -loop 1 -t 4.2 -framerate 24 -i title.png \
  -i sound.wav \
  -filter_complex "
[0]setsar=1,format=yuv420p[a];
[1]fade=t=out:st=0:d=0.4:color=black,setsar=1,format=yuv420p[b];
[2]fade=t=in:st=0:d=0.4,fade=t=out:st=2.8:d=0.4,setsar=1,format=yuv420p[c];
[3]fade=t=in:st=0:d=0.6,fade=t=out:st=3.6:d=0.6,setsar=1,format=yuv420p[d];
[a][b][c][d]concat=n=4:v=1:a=0[v]" \
  -map "[v]" -map 4:a -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart teaser-33days.mp4
echo saved
