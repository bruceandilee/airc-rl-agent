#!/bin/bash

# Enable the Learning Racer container.
# Usage: ./enable.sh /home/jetbot

JETBOT_CAMERA=${2:-opencv_gst_camera}

L4T_VERSION_STRING=$(head -n 1 /etc/nv_tegra_release)
L4T_RELEASE=$(echo "$L4T_VERSION_STRING" | cut -f 2 -d ' ' | grep -Po '(?<=R)[^;]+')
L4T_REVISION=$(echo "$L4T_VERSION_STRING" | cut -f 2 -d ',' | grep -Po '(?<=REVISION: )[^;]+')
#export L4T_VERSION="$L4T_RELEASE.$L4T_REVISION"
export L4T_VERSION=32.5.0
# set default swap limit as unlimited

if [ -z "$JETBOT_LEARNING_RACER_MEMORY_SWAP" ];
then
        export JETBOT_LEARNING_RACER_MEMORY_SWAP=-1
fi

if [ -z "$JETBOT_LEARNING_RACER_MEMORY" ];
then
  export JETBOT_LEARNING_RACER_MEMORY=2500m
fi

sudo docker run --gpus all -it -d \
      --restart always \
      --runtime nvidia \
      --network host \
      --privileged \
#     --device /dev/video* \
      --volume /dev/bus/usb:/dev/bus/usb \
      --volume /tmp/argus_socket:/tmp/argus_socket \
      -p 8888:8888 \
      -v ~/:/workspace \
      --workdir /workspace \
      --name=learning_racer \
      --memory="$JETBOT_LEARNING_RACER_MEMORY" \
      --memory-swap="$JETBOT_LEARNING_RACER_MEMORY_SWAP" \
#      --env JETBOT_DEFAULT_CAMERA="$JETBOT_CAMERA" \
      learning_racer:"$L4T_VERSION"
