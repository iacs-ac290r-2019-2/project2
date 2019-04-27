#!/bin/bash

mkdir -p movie

#ffmpeg -framerate 24 -i ./img/yz_cross/re5pe1/density/density_%03d.png -pix_fmt yuv420p ./movie/density_yz_re5pe1.mp4

# If file names are not continuous
# https://video.stackexchange.com/questions/7300/how-to-get-ffmpeg-to-join-non-sequential-image-files-skip-by-3s

if false; then

echo 'making movie for blood field'
sleep 1

# Re=5 case
ffmpeg -framerate 24 -pattern_type glob -i './img/yz_cross/re5pe1/density/density_*.png' -pix_fmt yuv420p ./movie/density_yzcross_re5pe1.mp4
ffmpeg -framerate 24 -pattern_type glob -i './img/yz_cross/re5pe1/uz/uz_*.png' -pix_fmt yuv420p ./movie/uz_yzcross_re5pe1.mp4

# Re=10case
ffmpeg -framerate 24 -pattern_type glob -i './img/yz_cross/re10pe1/density/density_*.png' -pix_fmt yuv420p ./movie/density_yzcross_re10pe1.mp4
ffmpeg -framerate 24 -pattern_type glob -i './img/yz_cross/re10pe1/uz/uz_*.png' -pix_fmt yuv420p ./movie/uz_yzcross_re10pe1.mp4

fi


if true; then

    echo 'making movie for blood field'
    sleep 1

# Re=5 Pe=1 case
ffmpeg -framerate 24 -pattern_type glob -i './img/yz_cross/re5pe1/drug/large_vrange/drug_*.png' -pix_fmt yuv420p ./movie/drug_yzcross_largev_re5pe1.mp4
ffmpeg -framerate 24 -pattern_type glob -i './img/yz_cross/re5pe1/drug/small_vrange/drug_*.png' -pix_fmt yuv420p ./movie/drug_yzcross_smallv_re5pe1.mp4

# Re=5 Pe=3 case
ffmpeg -framerate 24 -pattern_type glob -i './img/yz_cross/re5pe3/drug/large_vrange/drug_*.png' -pix_fmt yuv420p ./movie/drug_yzcross_largev_re5pe3.mp4
ffmpeg -framerate 24 -pattern_type glob -i './img/yz_cross/re5pe3/drug/small_vrange/drug_*.png' -pix_fmt yuv420p ./movie/drug_yzcross_smallv_re5pe3.mp4

# Re=10 Pe=1 case
ffmpeg -framerate 24 -pattern_type glob -i './img/yz_cross/re10pe1/drug/large_vrange/drug_*.png' -pix_fmt yuv420p ./movie/drug_yzcross_largev_re10pe1.mp4

fi
