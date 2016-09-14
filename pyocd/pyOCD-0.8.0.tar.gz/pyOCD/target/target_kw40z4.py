"""
 mbed CMSIS-DAP debugger
 Copyright (c) 2006-2013 ARM Limited

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

from target_kinetis import Kinetis
from .memory_map import (FlashRegion, RamRegion, MemoryMap)
from .coresight_target import SVDFile
import logging


class KW40Z4(Kinetis):

    memoryMap = MemoryMap(
        FlashRegion(    start=0,           length=0x28000,      blocksize=0x400, isBootMemory=True),
        RamRegion(      start=0x1ffff000,  length=0x5000)
        )

    def __init__(self, transport):
        super(KW40Z4, self).__init__(transport, self.memoryMap)
        self.mdm_idr = 0x001c0020
        self._svd_location = SVDFile(vendor="Freescale", filename="MKW40Z4.svd")

