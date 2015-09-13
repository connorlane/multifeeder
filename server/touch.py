#!/usr/bin/env python

import struct
import time
import math
import glob
import uinput
import pyudev
import os

# Wait and find devices
def read_and_emulate_mouse(deviceFound):
    with open(deviceFound, 'rb') as f:
        print("Read buffer")

        device = uinput.Device([
            uinput.BTN_LEFT,
            uinput.BTN_RIGHT,
            uinput.ABS_X,
            uinput.ABS_Y,
        ])

        clicked = False

        while True:
            b = f.read(25)
            (tag, btnLeft, x, y) = struct.unpack_from('>c?HH', b)
            (x, y) = (480 - y, max(x - 10, 0))
            time.sleep(0.01) 

            if btnLeft:
                device.emit(uinput.ABS_X, x, True)
                device.emit(uinput.ABS_Y, y, True)

                if not clicked:
                    device.emit(uinput.BTN_LEFT, 1)
                    clicked = True

            else:
                clicked = False
                device.emit(uinput.BTN_LEFT, 0)


if __name__ == "__main__":
    os.system("modprobe uinput")
    os.system("chmod 666 /dev/hidraw*")
    os.system("chmod 666 /dev/uinput*")

    while True:
        # try:
        print("Waiting device")
        hidrawDevices = glob.glob("/dev/hidraw*")

        context = pyudev.Context()

        deviceFound = None
        for hid in hidrawDevices:
            device = pyudev.Device.from_device_file(context, hid)
            if "0EEF:0005" in device.device_path:
                deviceFound = hid

        if deviceFound:
            print("Device found", deviceFound)
            read_and_emulate_mouse(deviceFound)
            # except:
            #     print("Error:", sys.exc_info())
            #     pass
            # finally:
            #     time.sleep(1)
