#!/usr/bin/python3
#
# $Id: usbblk.py 91 2022-10-04 20:02:57Z olof $
#
# This module defines the classes used for scan and enumerate usb mass store.
# Devices properties are store.
#
# usbblk.py
# Copyright (C) 2020 Olof Söderström <olof.soderstrom@bahnhof.se>
#
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; -*-
# -*- Mode: Python; c-basic-offset: 4; tab-width: 4 -*-
#
# ----------------------------------------------------------------------------
#
# Add demo dir's parent to sys path, so that 'import colorama' always finds
# the local source in preference to any installed version of colorama.
#
# Windows device instance ID
# instance-ID + device-ID (instance-specific-DI) ==> 
#   device-ID\instance-specific-ID
# For example :from PCI\VEN_1000&DEV_0001&SUBSYS_00000000&REV_02\1&08
#
# Device id : VEN_1000&DEV_0001&SUBSYS_00000000&REV_02 and instance id =  1&08 (unique id)
#
# import sys
# from os.path import normpath, dirname, join
# local_colorama_module = normpath(join(dirname(__file__), '..'))
# sys.path.insert(0, local_colorama_module)
#

import os
import json
import pyudev
import usb.core
import usb.util
import fcntl
import struct
import codecs
from collections import namedtuple
from hashlib import sha256
from lib.confutil import Version as Ver  # Version number string
from lib.formatutil import get_human_size  # Size into KB, MB and so on

property_to_attribute = {
        'device':           'DEVNAME',
        'bus':              'ID_BUS',
        'devtype':          'DEVTYPE',
        'type':             'ID_TYPE',
        'driver':           'ID_USB_DRIVER',
        'usbver':           '?',
        'speed':            '?',
        'drive_thumb':      'ID_DRIVE_THUMB',
        'vendor':           'ID_VENDOR',
        'vendor_enc':       'ID_VENDOR_ENC',
        'vendor_str':       '?',
        'model':            'ID_MODEL',
        'model_enc':        'ID_MODEL_ENC',
        'model_str':        '?',
        'revision':         'ID_REVISION',
        'size':             '?',
        'vid':              'ID_VENDOR_ID',
        'pid':              'ID_MODEL_ID',
        'id':               '?',
        'serial':           'ID_SERIAL_SHORT',
        'serial_long':      'ID_SERIAL',
        'interfaces':       'ID_USB_INTERFACES',    # Class SubClass Protocol
        'interface_num':    'ID_USB_INTERFACE_NUM',
        'label':            'ID_FS_LABEL',
        'fs':               'ID_FS_TYPE',
        'devbus':           '?',
        'devaddr':          '?',
        'busaddr':          '?',
        'major':            'MAJOR',
        'minor':            'MINOR',
        'usec':             'USEC_INITIALIZED',
        'chksum':           '?',
        }

all_prop = property_to_attribute.keys()

chksum_prop = ['bus', 'devtype', 'type', 'driver', 'drive_thumb', 'vendor',
               'vendor_enc', 'model', 'model_enc', 'revision', 'size', 'vid',
               'pid', 'serial', 'serial_long', 'interfaces', 'interface_num']

# Verify that the chksum_props list validity
for prop in chksum_prop:
    if prop not in all_prop:
        raise ValueError('Checksum property: "' + prop +
                         '" not part of all properies')


class keyvaluestore:
    """ general attribute store """

    def __init__(self, keys):
        self.store = dict.fromkeys(keys)

    def set(self, key, value):
        if key in self.store:
            self.store[key] = value
        else:
            raise ValueError('Key: "' + key + '" not found in store')

    def get(self, key):
        if key in self.store:
            return self.store[key]
        else:
            raise ValueError('Key: "' + key + '" not found in store')

    def get_all(self):
        return self.store

    def is_populated(self):
        for key in self.store:
            if self.store[key] is None:
                return False
        return True


def get_raw_device_size(device_path):
    """ BLKGETSIZE64, result is bytes as unsigned 64-bit integer (uint64) """

    req = 0x80081272
    buf = ' ' * 8

    try:
        with open(device_path) as dev:
            buf = fcntl.ioctl(dev.fileno(), req, buf)
        bytes = struct.unpack('L', buf)[0]

        return bytes
    except (OSError, PermissionError):
        return 0


def shasum(line):
    """ make sha256 digest of line """
    h = sha256()
    h.update(line.encode())
    return h.hexdigest()


class usbids:
    """ Class that parses usb id list file and provides vid and pid
        to vid string and pid string lookup """

    def __init__(self, localfile='./usb.ids',
                 distrofile='/usr/share/hwdata/usb.ids'):

        self.file = None
        self.vendor = namedtuple("Vendor", ['name', 'devices'])
        self.vendors = dict()
        self.downloaded = False

        # Find USB id list
        if os.path.isfile(localfile):
            self.file = localfile
            self.downloaded = True
        elif os.path.isfile(distrofile):
            self.file = distrofile

        if self.file is not None:
            with codecs.open(self.file, "r", "latin-1") as f:
                for line in f:
                    if not line.strip():
                        continue
                    line = line.rstrip()
                    if line.startswith("#"):
                        continue
                    if line.startswith("# List of known device classes, " +
                                       "subclasses and protocols"):
                        break
                    if not line.startswith("\t"):
                        current_vendor, name = line.split(None, 1)
                        self.vendors[current_vendor] = self.vendor(
                                name=name, devices=dict())
                    if line.startswith("\t"):
                        device_id, desc = line.lstrip().split(None, 1)
                        self.vendors[current_vendor].devices[device_id] = desc

    def file_is_loaded(self):
        """ Return True if USB id file was found """
        return self.file is not None

    def is_downloaded(self):
        """ Return True if USB id file was found and has been downloaded """
        return (self.file is not None) and (self.downloaded)

    def getids(self, vid, pid):
        """ Return string representation of vid and pid """
        vidstr = 'None'
        pidstr = 'None'

        if vid in self.vendors:
            vidstr = self.vendors[vid].name
            if pid in self.vendors[vid].devices:
                pidstr = self.vendors[vid].devices[pid]

        return vidstr, pidstr


class usbfs:
    """ Stub for class inspecting file systems """
    def __init__(self):
        pass


class usbdevice(keyvaluestore):

    def _find_devices(vid, pid, serial):
        """ Returns a list of devices with given vid, pid and serial """

        devices = []
        for device in usb.core.find(idVendor=vid, idProduct=pid, find_all=1):
            devices.append(device)

        # If more than one device, locate device with correct serial number
        if len(devices) > 1:
            devices = []
            for device in usb.core.find(idVendor=vid,
                                        idProduct=pid,
                                        find_all=1):
                try:
                    if device.serial_number == serial:
                        devices.append(device)
                except ValueError:
                    # if user not root by pass known bug(?) in usb.core
                    pass

        return devices

    def __init__(self, device, human_readable, usbids):
        super().__init__(all_prop)  # Initiate with all properties
        for prop in all_prop:
            self.set(prop, '?')

        getprop = device.properties.get

        # Get properties from udev
        for key, value in property_to_attribute.items():
            if value != '?':
                self.set(key, str(getprop(value)))

        self.set('size', str(get_raw_device_size(self.get('device'))))
        self.set('id',   self.get('vid') + ':' + self.get('pid'))

        # Get list of devices from USB core package
        devices = usbdevice._find_devices(int(self.get('vid'), 16),
                                          int(self.get('pid'), 16),
                                          self.get('serial'))

        # Get string representation of VID and PID from USB id list
        vidstr, pidstr = usbids.getids(self.get('vid'), self.get('pid'))
        self.set('vendor_str', vidstr)
        self.set('model_str', pidstr)

        """
        Set if one and only one device with specified vid, pid and serial is
        found. Note that some manufacture do not provide device unique serial
        numbers.
        """
        if len(devices) == 1:
            device = devices[0]
            self.set('devbus', str(device.bus))
            self.set('devaddr', str(device.address))
            self.set('busaddr',
                     "{:03d}".format(int(self.get('devbus'))) +
                     ':' +
                     "{:03d}".format(int(self.get('devaddr'))))
            major = f"{(device.bcdUSB & 0xff00)>>8}"
            minor = f"{(device.bcdUSB & 0xf0)>>4}"
            self.set('usbver', f"USB {major}.{minor}")
            self.set('speed', str(device.speed))

        # calculate checksum of static device properties
        chksum_text = ''
        for a in chksum_prop:
            chksum_text += self.get(a)
        self.set('chksum', shasum(chksum_text))

        if human_readable:
            self.set('size', get_human_size(int(self.get('size'))))

        self.label_size = dict.fromkeys(self.store.keys())
        for key in self.label_size:
            self.label_size[key] = len(self.get(key))

    def __str__(self):
        return self.get('device')

    def get_labels(self):
        return self.store.keys()

    def serialise(self, keys=None):
        if keys is None:
            res = json.dumps(self.get_all(), separators=(',', ':'))  # Compact
        else:
            new = {}
            for k in keys:
                new[k] = self.get(k)
            res = json.dumps(new, separators=(',', ':'))  # Compact output

        return res

    def display(self):
        return self.get_all()

    def debug(self):
        print(self.get_all())


class usbblk:

    def __init__(self, human_readable):
        self.context = pyudev.Context()
        self.devices = {}
        self.usbids = usbids()

        for device in self.context.list_devices(subsystem='block'):
            if device.get('ID_BUS') == 'usb':
                if device.get('DEVTYPE') == 'disk':
                    self.devices[device.get('DEVNAME')] = usbdevice(
                            device, human_readable, self.usbids)

    def get(self, name):
        if name in self.devices:
            return self.devices[name]
        else:
            return None

    def get_label_size_of_key(self, key):
        size = len(key)
        for dev in self.devices:
            size = max(size, self.devices[dev].label_size[key])
        return size

    def get_devices(self):
        devices = []
        for dev in sorted(list(self.devices.keys())):
            devices.append(self.devices[dev])
        return devices

    def get_device_list(self):
        return sorted(list(self.devices.keys()))

    def get_all_prop(self):
        return all_prop

    def number_of(self):
        return len(self.devices)

    def is_empty(self):
        return len(self.devices) == 0

    def display(self):
        for device in self.get_device_list():
            self.devices[device].display()

    def serialise(self, properties=None, device=None):
        res = '{'
        if device is not None:
            res += '"' + device + '":'
            res += self.devices[device].serialise(properties)
        else:
            first = True
            for dev in self.get_device_list():
                if first:
                    first = False
                else:
                    res += ','

                res += '"' + str(dev) + '":'
                res += self.devices[dev].serialise(properties)
        res += '}'
        return res

    def debug(self):
        for device in self.devices:
            self.devices[device].debug()
        for device in self.context.list_devices(subsystem='block'):
            if device.get('ID_BUS') == 'usb':
                if device.get('DEVTYPE') == 'disk':
                    print('-' * 20)
                    for prop in device.properties:
                        print(prop + " = " + device.properties.get(prop))


if __name__ == '__main__':

    myusb = usbblk()
    myusb.debug()
