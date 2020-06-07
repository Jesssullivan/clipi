#!/usr/bin/env python3
"""
clipi:
Emulate, organize, burn, manage a variety of sbc distributions for Raspberry Pi
Written by Jess Sullivan
@ https://github.com/Jesssullivan/clipi
@ https://transscendsurvival.org/
"""

from common import *
from qemu import qemu

"""
dd.py:
control dd utility to write raw out to disk / sd card.  
"""


class dd(object):

    @classmethod
    def what_disk(cls):
            # prompt following image selection for target disk
            target = {
                'type': 'input',
                'name': 'target',
                'message': "please type the target disk's system name, such as `sdb` or sdc`",
                'default': "sdc"
            }
            response = prompt(target)
            return response['target']

    @classmethod
    def dd_output_convert(cls, qcow):
        print('converting qcow disk image to burnable raw....')
        cmd = str("qemu-img convert " + qcow + " -O raw " + names.src_output(qcow))
        subprocess.Popen(cmd, shell=True).wait()
        return names.src_output(qcow)


    @classmethod
    def dd_write(cls, sd_disk, image):
        main_install()
        ensure_dir()
        qemu.ensure_img(image=image)
        print('preparing to write out image, unmount target....')
        umount_cmd = str('umount /dev/' + sd_disk + ' 2>/dev/null || true')
        subprocess.Popen(umount_cmd, shell=True).wait()
        for x in range(3):
            print('writing ' + image + ' to target....')
            sleep(.1)
        dd_cmd = str('sudo dd if=' + image + ' of=/dev/' + sd_disk + ' bs=1048576')
        print('writing to target....')
        subprocess.Popen(dd_cmd, shell=True).wait()
        sleep(.1)
        print('completed write, syncing....')
        subprocess.Popen('sync ', shell=True).wait()
        print('finished xD \n ' +
              'to pre-enable wifi and ssh, reinsert sd_disk, then ' +
              'copy file `ssh` and a configured `wpa_supplicant.conf` to /boot :)')

