#!/bin/bash

mkdir -p movie

#ffmpeg -framerate 24 -i ./img/yz_cross/re5pe1/density/density_%03d.png -pix_fmt yuv420p ./movie/density_yz_re5pe1.mp4

# If file names are not continuous
# https://video.stackexchange.com/questions/7300/how-to-get-ffmpeg-to-join-non-sequential-image-files-skip-by-3s

# Re=5 case
ffmpeg -framerate 24 -pattern_type glob -i './img/yz_cross/re5pe1/density/density_*.png' -pix_fmt yuv420p ./movie/density_yzcross_re5pe1.mp4
ffmpeg -framerate 24 -pattern_type glob -i './img/yz_cross/re5pe1/uz/uz_*.png' -pix_fmt yuv420p ./movie/uz_yzcross_re5pe1.mp4

# Re=10case
ffmpeg -framerate 24 -pattern_type glob -i './img/yz_cross/re10pe1/density/density_*.png' -pix_fmt yuv420p ./movie/density_yzcross_re10pe1.mp4
ffmpeg -framerate 24 -pattern_type glob -i './img/yz_cross/re10pe1/uz/uz_*.png' -pix_fmt yuv420p ./movie/uz_yzcross_re10pe1.mp4
