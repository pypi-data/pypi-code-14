# Copyright 2016 Neverware Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Enumerate Legacy Plug and Play devices.

PNP specification:

    ftp://download.intel.com/support/motherboards/desktop/sb/pnpbiosspecificationv10a.pdf

PNP device product identifier:

    This field is an EISA ID, which is a seven character ASCII
    representation of the product identifier compressed into a
    32-bit identifier. The seven character ID consists of a three
    character manufacturer code, a three character hexadecimal
    product identifier, and a one character hexadecimal revision
    number.

PNP manufacturer codes:

    http://www.uefi.org/pnp_id_list

Related kernel sources:

    git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/tree/drivers/acpi/acpi_pnp.c

"""

from glob import glob

import attr


@attr.s
class Vendor(object):
    """Vendor metadata.

             name: company name (UTF-8)

           pnp_id: three-digit vendor code (ASCII). Always stored as
                   upper case for comparison purposes.

    approval_date: datetime.date object containing the date the vendor
                   received their PNP ID.

    """
    name = attr.ib()
    pnp_id = attr.ib()
    approval_date = attr.ib()


@attr.s(repr=False)
class DeviceId(object):
    """Plug and Play device ID.

    vendor_id: three-digit vendor code (ASCII). Always stored as upper
               case for comparison purposes.

      product: numeric product ID

     revision: numeric revision ID

    """
    vendor = attr.ib(convert=lambda string: string.upper())
    product = attr.ib()
    revision = attr.ib()

    def __repr__(self):
        return 'DeviceId(vendor={}, product={:#05x}, revision={:#x})'.format(
            self.vendor, self.product, self.revision)

    def __str__(self):
        return '{}{:03x}{:x}'.format(self.vendor, self.product, self.revision)


@attr.s
class Device(object):
    """Plug 'n Play device.

    ids: list of PnpDeviceIds.
    """
    ids = attr.ib()

    def __str__(self):
        # pylint: disable=not-an-iterable
        string_ids = (str(device_id) for device_id in self.ids)
        return 'Device({})'.format(', '.join(string_ids))


def split_n(seq, num):
    """Split |seq| in twain with the first part having length |num|."""
    if len(seq) < num:
        raise ValueError('sequence too short: seq={}, num={}'.format(seq, num))
    else:
        return seq[:num], seq[num:]


def parse_hex(string):
    """Parse a string as a hexadecimal value."""
    return int(string, 16)


def parse_device_id(device_id):
    """Parse a 7-character device_id string into a |PnpDevice|."""
    vendor_length = 3
    product_length = 3
    revision_length = 1
    total_length = (vendor_length + product_length + revision_length)

    if len(device_id) == total_length:
        vendor, rest = split_n(device_id, vendor_length)
        product, revision = split_n(rest, product_length)

        return DeviceId(vendor=vendor,
                        product=parse_hex(product),
                        revision=parse_hex(revision))
    else:
        raise ValueError('invalid device_id: {}'.format(device_id))


def parse_sysfs_pnp_id_file(id_file):
    """Create a PnpDevice from an ID file in sysfs.

    The PNP device ID files contain line-separated device IDs.
    """
    ids = []
    for line in id_file.readlines():
        ids.append(parse_device_id(line.strip()))
    return Device(ids=ids)


def get_all_pnp_devices_from_sysfs():
    """Enumerate all PnpDevices via sysfs."""
    for path in glob('/sys/bus/pnp/devices/*/id'):
        with open(path) as id_file:
            yield parse_sysfs_pnp_id_file(id_file)
