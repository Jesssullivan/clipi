#!/usr/bin/env python3
"""
clipi:
Emulate, organize, burn, manage a variety of sbc distributions for Raspberry Pi
Written by Jess Sullivan
@ https://github.com/Jesssullivan/clipi
@ https://transscendsurvival.org/
"""

from common import *

"""
qemu.py:
controls various qemu-system functions
"""


class qemu(object):

    @classmethod
    def construct_arm1176_execute(cls,
                                  qcow=''):
        xargs = all_args()
        cmd = str("qemu-system-aarch64 -kernel " +
                  xargs['bin'] +
                  " -cpu " +
                  xargs['cpu32'] +
                  " -m " +
                  xargs['mem_vers'] +
                  " -M versatilepb -dtb bin/versatile-pb.dtb -no-reboot -serial stdio -append " +
                  '"root=/dev/sda2 panic=1 rootfsrtype=ext4 rw" -hda ' +
                  qcow)
        return cmd

    @classmethod
    def construct_arm64_execute(cls,
                                xargs=all_args(),
                                qcow=''):
        cmd = str("qemu-system-aarch64 -M virt -m " +
                  xargs['mem_64'] +
                  " -cpu " +
                  xargs['cpu64'] +
                  " -kernel bin/installer-linux -initrd bin/installer-initrd.gz " +
                  "-no-reboot -serial stdio -append " +
                  '"root=/dev/sda2 panic=1 rootfsrtype=ext4 rw" -hda ' +
                  qcow)
        return cmd

    @classmethod
    def construct_qemu_convert(cls, img, qcow):
        cmd = str("qemu-img convert -f raw -O qcow2 " + img +
                  " " + qcow)
        return cmd

    @classmethod
    def do_qemu_expand(cls,
                       qcow=''):
        xargs = all_args()
        cmd = str("qemu-img resize " + qcow + " " + xargs['qcow_size'])
        subprocess.Popen(cmd, shell=True).wait()
        sleep(.1)
        return 0

    @classmethod
    def ensure_img(cls, image):

        for x in range(10):

            if os.path.isfile(names.src_qcow(image)):
                return names.src_qcow(image)

            if not os.path.exists(names.src_dir(image)):
                os.mkdir(names.src_dir(image))

            if not os.path.exists(names.src_dir(image)):
                os.mkdir(names.src_dir(image))

            if not os.path.isfile(image):
                subprocess.Popen(str('wget -O ' + names.src_local(image) + ' ' + image),
                                 shell=True).wait()
                sleep(.25)

            if os.path.isfile(names.src_img(image)):
                subprocess.Popen(cls.construct_qemu_convert(img=names.src_img(image),
                                                            qcow=names.src_qcow(image)),
                                 shell=True).wait()
                sleep(.25)
                cls.do_qemu_expand(names.src_qcow(image))

            if os.path.isfile(names.src_zip(image)):
                unzip(names.src_zip(image), names.src_dir(image))

            if os.path.isfile(names.src_7z(image)):
                print('unzipping')
                unzip(names.src_7z(image), names.src_dir(image))

        return names.src_qcow(image)

    @classmethod
    def launch(cls, image, xargs=all_args()):
        main_install()
        ensure_dir()
        ensure_bins()
        # "launch_qcow" is returned a .qcow2 after it has been verified to exist-
        # this way we can call to launch an image that we don't actually have yet,
        # letting qemu.ensure_img() go fetch & prepare a fresh one
        launch_qcow = cls.ensure_img(image)
        print(launch_qcow)

        if arg_true(dic=xargs, arg='use64'):
            subprocess.Popen(cls.construct_arm64_execute(qcow=launch_qcow),
                                 shell=True).wait()
        else:
            subprocess.Popen(cls.construct_arm1176_execute(qcow=launch_qcow),
                             shell=True).wait()


