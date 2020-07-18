#!/bin/bash
# a WIP by Jess Sullivan
# @ https://github.com/Jesssullivan/clipi
# @ https://transscendsurvival.org/

# launches dhclient, assuming it is a child of python script.
# TODO: make internet connection stay alive while bridge is on

# brctl addbr br0
read CLIPINET <<< $(ip -o link | awk '$2 != "lo:" {print $2}')
echo ${CLIPINET//:}

sudo ip addr flush dev ${IPETH0//:}
sudo brctl addif br0 ${IPETH0//:}

# sep tap0:
sudo tunctl -u $(whoami)
sudo brctl addif br0 tap0
sudo ip link set dev br0 up
sudo ip link set dev tap0 up

# start dhclient:
echo -e "staring dhclient..."
sudo dhclient br0
 sudo ./network/runqemu.sh -hda image/2019-04-08-raspbian-stretch/2019-04-08-raspbian-stretch.qcow2