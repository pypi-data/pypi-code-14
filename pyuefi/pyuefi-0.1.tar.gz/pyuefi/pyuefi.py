#!/usr/bin/env python3
# *-* coding=utf8 *-*
"""
Usage: pyuefi [options] TARGET

 TARGET          The disk to be analyzed
 -s SECTOR_SIZE  Specify an alternate sector size [default: 512]
"""

import os
import re
import struct
import subprocess
from uuid import UUID

from docopt import docopt
from six import *

from .partition_types import uefi_part_types

SECTOR_SIZE = 512
UUID_ZERO = str(UUID(int=0))


def ints_to_int_be(*args):
    """
    Combine a set of 8-bit integers into a single integer. (Big Endian)

    The main purpose of this function is to get around the limitation Python
    has of specifying structures with integers that have unusual byte sizes.

    :param args: List or tuple of 8-bit integers
    :type args: list|tuple
    :return: int
    :rtype: int
    """
    num = 0
    for _int in args:
        num <<= 8
        num = num | _int
    return num


class PyUEFI(object):
    """

    """
    # Partition Table Entry Structure (Offset in MBR: 446 bytes)
    # [0] Status                     1-byte   integer
    # [1:4] CHS start address        3-bytes  don't care
    # [4] Partition type             1-byte   integer
    # [5:8] CHS end address          3-bytes  don't care
    # [8] LBA start address          4-bytes  integer (little-endian)
    # [9] LBA length                 4-bytes  integer (little-endian)
    pte_struct = struct.Struct('<B3BB3BII')

    # UEFI Header Structure
    # [0] Signature                  8-bytes  string
    # [1] Revision                   4-bytes  integer (00h 00h 01h 00h)
    # [2] Header size                4-bytes  integer (little-endian)
    # [3] CRC32 of header            4-bytes  integer
    # [4] Reserved - Zeros           4-bytes  integer
    # [5] Current LBA                8-bytes  integer
    # [6] Backup LBA                 8-bytes  integer
    # [7] First usable LBA           8-bytes  integer
    # [8] Last usable LBA            8-bytes  integer
    # [9:25] Disk GUID              16-bytes  integer (big-endian)
    # [25] Partition entries LBA     8-bytes  integer
    # [26] Number of entries         4-bytes  integer
    # [27] Entry size                4-bytes  integer (usually 128)
    # [28] CRC32 of all entries      4-bytes  integer
    uefi_struct = struct.Struct('<8s4I4Q16BQ3I')

    # GUID Partition Table Entry Structure
    # [0:16] Partition type GUID     16-bytes  integer (big-endian)
    # [16:32] Unique partition GUID  16-bytes  integer (big-endian)
    # [32] First LBA                 8-bytes  integer
    # [33] Last LBA                  8-bytes  integer (inclusive)
    # [34] Attributes                8-bytes  integer
    # [35] Partition name           72-bytes  string
    part_struct = struct.Struct('<16B16B3Q72s')

    def __init__(self, dev):
        """
        General flow:
        1. Make sure the device/file is valid
        2. Open the device
        3. Read/store the MBR, get the LBA of UEFI header
        4. Read/store UEFI header, get LBA and length of entries
        5. Read/store entries

        :param dev: Path to device or file to read.
        :type dev: str
        :return: None
        """
        assert isinstance(dev, str)
        self.dev = dev

        self.mbr_parts = []
        self.uefi_header = dict()
        self.partitions = dict()

        # Before opening the drive, we need to make sure we have the proper
        # permissions
        euid = os.geteuid()
        if euid != 0:
            # Will raise a PermissionError unless the saved user ID is 0
            os.seteuid(0)

        with open(self.dev, 'rb') as _dev:
            self._get_mbr_entries(_dev)

            # Get the location of UEFI header
            lba_start = None
            for p in self.mbr_parts:
                if p.get('type') == 0xee:
                    lba_start = p.get('lba_start')
                    break
            if lba_start is None:
                err = "Couldn't find location of UEFI header."
                raise ValueError(err)

            # Extract header information
            self._get_uefi_header(_dev, lba_start)

            # Read in the UEFI partition entries
            self._get_uefi_entries(_dev)

        # Set our permissions to what they were before
        os.seteuid(euid)

    def _get_mbr_entries(self, dev):
        """
        Get the MBR partition table entries, store in self.mbr_parts.

        :param dev: The open device/file we're reading from.
        :type dev: six.BytesIO
        :return: None
        """
        # First make sure the device is open
        try:
            if dev.closed():
                raise OSError('Target device was not open. Make sure it isn\'t closed before passing it.')
        except AttributeError:
            raise OSError('Unreadable target. Make sure to specify a device or file.')

        dev.seek(446)  # Size of boot code in MBR
        for i in range(4):
            entry = self.pte_struct.unpack(dev.read(16))
            part = dict(status=entry[0],
                        chs_start=ints_to_int_be(*entry[1:4]),
                        type=entry[4],
                        chs_end=ints_to_int_be(*entry[5:8]),
                        lba_start=entry[8],
                        lba_length=entry[9])
            self.mbr_parts.append(part)

    def _get_uefi_header(self, dev, lba_start):
        """
        Get the UEFI header information, store in self.uefi_header.

        :param dev: The open device/file we're reading from.
        :type dev: six.BytesIO
        :param lba_start: LBA of the UEFI header
        :type lba_start: int
        :return: None
        """
        # First make sure the device is open
        try:
            if dev.closed():
                raise OSError('Target device was not open. Make sure it isn\'t closed before passing it.')
        except AttributeError:
            raise OSError('Unreadable target. Make sure to specify a device or file.')

        dev.seek(lba_start*SECTOR_SIZE)
        header = self.uefi_struct.unpack(dev.read(92))
        disk_guid = str(UUID(bytes_le=bytes(header[9:25])))
        self.uefi_header = dict(signature=header[0],
                                revision=header[1],
                                size=header[2],
                                crc1=header[3],
                                zeros=header[4],
                                lba_this=header[5],
                                lba_backup=header[6],
                                lba_usable_start=header[7],
                                lba_usable_end=header[8],
                                disk_guid=disk_guid,
                                lba_entries_start=header[25],
                                num_entries=header[26],
                                entry_size=header[27],  # Bytes
                                crc2=header[28])

    def _get_uefi_entries(self, dev):
        """
        Get the UEFI partition table entries, store in self.partitions.

        :param dev:The open device/file we're reading from.
        :type dev: six.BytesIO
        :return: None
        """
        # First make sure the device is open
        try:
            if dev.closed():
                raise OSError('Target device was not open. Make sure it isn\'t closed before passing it.')
        except AttributeError:
            raise OSError('Unreadable target. Make sure to specify a device or file.')

        # Seek to the first entry
        entry_start = self.uefi_header['lba_entries_start']*SECTOR_SIZE
        dev.seek(entry_start)
        entry_size = self.uefi_header['entry_size']  # Bytes

        # Get the device paths for all the partitions
        # TODO: Only do this for Linux
        labels = subprocess.check_output('ls -l /dev/disk/by-partlabel/', shell=True).splitlines()
        dev_path = {}
        label_pat = re.compile(b'\d\d:\d\d (.*?) -> (.*)$')
        for l in labels:
            m = re.search(label_pat, l)
            if m:
                name = str(m.group(1))[2:-1]
                _path = str(m.group(2))[2:-1].split('/')[-1]
                dev_path[name] = '/dev/' + _path

        # Store each
        for i in range(self.uefi_header['num_entries']):
            entry = self.part_struct.unpack(dev.read(entry_size))

            # Get the GUID values
            part_type_id = str(UUID(bytes_le=bytes(entry[0:16])))
            if part_type_id == UUID_ZERO:
                # Partition is unused, no need to process it
                break
            part_guid = str(UUID(bytes_le=bytes(entry[16:32])))
            try:
                part_type = uefi_part_types[part_type_id.upper()]['Type']
            except KeyError:
                part_type = "Unknown"

            # Decode and trim the partition name
            part_name = entry[35].decode('utf-16-le').strip('\x00')

            # Get the partition's device path
            try:
                part_path = dev_path[part_name]
            except KeyError:
                part_path = None

            self.partitions[part_guid] = dict(type=part_type,
                                              type_id=part_type_id,
                                              guid=part_guid,
                                              lba_start=entry[32],
                                              lba_end=entry[33],
                                              attributes=entry[34],
                                              name=part_name,
                                              dev_path=part_path)
        # Remove the "empty" entry
        self.partitions.pop(UUID_ZERO)

    def get_all_part_info(self):
        """
        Get all the partitions' information.

        :return: A dictionary with all the partitions' info, keyed by the
            partition's GUID.
        :rtype: dict
        """
        # TODO: Change this function to a property
        return self.partitions

    def get_part_by_name(self, part_name):
        """
        Return a dict of the partition's info, using its name to find it.

        :param part_name: The name of the partition to retrieve.
        :type part_name: str
        :return: A dictionary with all the partition's info. None if it
            doesn't exist.
        :rtype: dict|None
        """
        for p in self.partitions:
            if self.partitions[p]['name'] == part_name:
                return self.partitions[p]

    def get_part_names(self):
        """
        Get a list of the names of all the partitions.

        :return: A list with all the partition names.
        :rtype: list
        """
        names = []
        for p in self.partitions:
            names.append(self.partitions[p]['name'])
        return names

    def print_part_info(self):
        raise NotImplementedError


if __name__ == "__main__":
    _args = docopt(__doc__)
    uefi = PyUEFI(_args['TARGET'])

    # TODO: If the user runs this directly, nicely print the results with
    # uefi.print_part_info()
    for _p in uefi.partitions.values():
        print_(_p)
