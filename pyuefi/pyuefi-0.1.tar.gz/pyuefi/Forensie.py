# Imports
from re import sub, findall
import string
import json

# Globals
F_DEBUG = False
HEXBIN_TRANS = {'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', '7': '0111',
                '8': '1000', '9': '1001', 'a': '1010', 'b': '1011', 'c': '1100', 'd': '1101', 'e': '1110', 'f': '1111',
                'A': '1010', 'B': '1011', 'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'}


class Forensie:
    # Custom Exceptions
    class FormatError(Exception):
        pass

    # Class Methods
    def __init__(self, instr):
        self.origStr = self.inputStr = instr
        self.RemoveDelimiters()
        self.endian = 'little'
        with open('partition_types_mbr.json') as fin:
            self.PType = json.load(fin)
        self.supported_commands = ('hex', 'mbr', 'fat-vbr', 'date', 'time', 'datetime', 'little-endian', 'big-endian')
        self.command_descriptions = {
            'hex': 'The default interpretation mode. Presents the input in a fixed-width font along with its ASCII '
                   'decoding. All other commands fall back to this interpretation if an error occurs.',
            'mbr': 'Analyzes the given input as a Master Boot Record.',
            'fat-vbr': 'Analyzes the given input as a Boot Sector for an FAT volume.',
            'date': 'Analyzes the given input as an FAT date value.',
            'time': 'Analyzes the given input as an FAT time value.',
            'datetime': 'Analyzes the given input as FAT date and time values.',
            'little-endian': 'A sub-command, to be used with one of the other commands above. Tells Forensie to '
                             'process the input for little endian format.',
            'big-endian': 'A sub-command, to be used with one of the other commands above. Tells Forensie to process '
                          'the input for big endian format.'}

    def RemoveDelimiters(self):
        """Removes standard delimiting characters from the input text. No
        return value. Instead, self.inputStr is changed directly.
        """
        badchars = ' -|\n'
        try:
            self.inputStr = str(self.inputStr).translate(None,
                                                         badchars)  # Removes all spaces and pipes from input string
        except(TypeError):  # Python 2.5 doesn't support None translation tables...
            self.inputStr = str(self.inputStr).translate(string.maketrans('', ''), badchars)

    def ProcessInput(self, repeatOnFail=0):
        """Processes the text provided to the constructor. This method is the
        flagship of Forensie. All processing of text springboards from this
        point. First the type of the input is determined, hex, binary, or
        other. Binary text is converted to hex before futher processing. If
        neither binary nor hex text is found, the first line is parsed for
        commands and the rest of the lines are reprocessed for binary or
        hex text in a recursive manner. All commands are kept cummulatively
        and are processed in the order they were discovered.

        Returns a tuple in the form (printable results, 'success' or 'fail',
        type of processing done to input).
        """
        # Check input format
        self.CheckBinary()
        self.bytes = []

        if self.format[:3] == 'bad' or self.format != 'hex':
            if type(repeatOnFail) == int:
                line = 2 + repeatOnFail  # Blip always starts with '\n'; don't want to count that line
                # print "Trying to split the lines...",
                tmp = self.origStr.split('\n', line)
                try:
                    self.inputStr = StrFlatten(tmp[line:])
                except IndexError:  # No more lines to take off
                    print
                    "Failed on try %d" % repeatOnFail
                    return ('Parsed all lines unsuccessfully.', 'fail', None)
                else:
                    # print 'Bad input format: %s\nTrying again, #%d' % (self.format, repeatOnFail+1)
                    self.GetCommand(tmp[:line])
                    self.RemoveDelimiters()
                    return self.ProcessInput(repeatOnFail + 1)
            else:
                return ('', 'fail', None)

        # Text is in an acceptable format. Process according to a command or process as hex text.
        try:
            return self.ExecuteCommand()
        except self.FormatError as m:
            if F_DEBUG:
                print(m)
            return ('%s%s' % (m, self.DecodeHex()), 'success', 'hex')

    def ExecuteCommand(self):
        """Processes the input text according to the stored command(s). Calls
        the method corresponding to the first command given. Raises a
        FormatError if no valid command is found. If called from
        ProcessInput(), this will cause the text to be processed as plain
        hex.

        Returns the value returned from whichever method is called.
        """
        # Process according to first given command
        try:
            com = self.commands[0]
        except IndexError:  # No command found
            raise self.FormatError('No command found.')
        except AttributeError:  # No command found
            raise self.FormatError('No command found.')

        if 'little-endian' in self.commands:
            self.endian = 'little'
        elif 'big-endian' in self.commands:
            self.endian = 'big'

        if com == 'mbr':
            return self.MBRdetector()

        elif self.commands[0] == 'fat-vbr':
            return self.FATVBRdetector()

        elif com == 'date':
            # if 'fat' in self.commands:
            return self.DateDetector()

        elif com == 'time':
            return self.TimeDetector()

        elif com == 'datetime':
            return self.DateTimeDetector()

        elif com == 'hex':
            return (self.DecodeHex(), 'success', 'hex')

        else:
            raise self.FormatError('An unsupported command passed through: %s' % com)

    def MBRdetector(self):
        """Entry point for interpreting the input as an MBR. Begins processing
        the input text and determines if the length and boot signature are
        valid before proceeding. Splits the four primary partition tables
        and sends them each to GetPartInfo(). The information from these
        four entries together make up the bulk of the valuable information
        in an MBR, so it is sent directly to FormatPartInfo().

        Returns a regular success tuple (see ProcessInput()).
        """
        self.bytes = ChopHexStr(self.inputStr)

        # Check length of string
        if len(self.bytes) != 512:
            raise self.FormatError('MBR is of improper length: %d, expected 512' % len(self.bytes))

        # Determine Endian
        if [self.bytes[-2], self.bytes[-1].upper()] == ['55', 'AA']:
            # Little Endian
            self.endian = 'little'
        elif [self.bytes[-2].upper(), self.bytes[-1]] == ['AA', '55']:
            # Big Endian
            self.endian = 'big'
        else:
            # print 'MBR does not have a valid signature'
            raise self.FormatError('MBR does not have a valid signature.')

        partitionsInfo = []
        for n in range(4):
            offset = 446 + 16 * n  # Boot code length + offset of the partitions already parsed
            partEntry = self.bytes[offset:offset + 16]
            partitionsInfo += [self.GetPartInfo(partEntry)]

        return (self.FormatPartInfo(partitionsInfo), 'success', 'mbr')

    def DateDetector(self, alt=None, raw=False):
        """Detects and interprets an FAT date value. Alternate text can be
        passed to alt if the calling code needs text other than the input
        string to be processed. Also, if raw is True, the processing
        results are not put into a string or the success tuple before being
        returned.

        Returns a regular success tuple (see ProcessInput()).
        """
        if alt == None: alt = self.inputStr
        if len(alt) != 4: raise self.FormatError('Date value has improper length of %d, expected 4' % len(alt))
        result = self.GetDate(Hex2Dec(alt, self.endian))
        if raw: return result  # Unformatted (raw) results requested
        return ('Date Value: %d %s, %d\nProcessed for %s endian format' % (result + (self.endian,)), 'success', 'date')

    def GetDate(self, dateNum):
        """Performs the calculation necessary for converting a given dateNum
        value to a tuple in the format (day, month name, year). Raises
        self.FormatError on any invalid values.
        """
        if type(dateNum) != int:
            raise self.FormatError(
                "While converting a date value, received unexpected input type: %s, expected 'int'" % type(dateNum))
        day = dateNum & int('11111', 2)
        month = (dateNum & int('111100000', 2)) >> 5
        year = (dateNum >> 9) + 1980
        months = [None, 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                  'October', 'November', 'December']

        if not (day and month):
            raise self.FormatError('Invalid day or month value of 0 in number: %d' % dateNum)

        try:
            return (day, months[month], year)
        except IndexError:  # Indexed a month > 12
            raise self.FormatError('Month value in date number %d is greater than 12: %d' % (dateNum, month))

    def TimeDetector(self, alt=None, raw=False):
        """Detects and interprets an FAT time value. Alternate text can be
        passed to alt if the calling code needs text other than the input
        string to be processed. Also, if raw is True, the processing
        results are not put into a string or the success tuple before being
        returned. If the time value includes 100ths of seconds, these are
        added to the values sent to GetTime().

        Returns a regular success tuple (see ProcessInput()).
        """
        if alt == None: alt = self.inputStr
        msec = 0.0
        off = 0
        if len(alt) == 6:  # Time includes microsecond units
            msec = Hex2Dec(alt[:2], self.endian) / 100.0
            off = 2
        elif len(alt) != 4:
            raise self.FormatError('Time value has improper length of %d, expected 4 or 6' % len(alt))

        result = self.GetTime(Hex2Dec(alt[off:], self.endian), msec)
        if raw: return result  # Unformatted (raw) results requested
        return (
            'Time Value: %02d:%02d:%05.2f\nProcessed for %s endian format' % (result + (self.endian,)), 'success',
            'time')

    def GetTime(self, timeNum, msec=0.0):
        """Performs the calculation necessary for converting a given timeNum
        value to a tuple in the format (hour, minutes, seconds). Raises
        self.FormatError on any invalid values.
        """
        if type(timeNum) != int:
            raise self.FormatError('While converting a time value, received unexpected input type: %s' % type(timeNum))
        seconds = timeNum & int('11111', 2)  # First 5 LSBs
        minutes = (timeNum & int('11111100000', 2)) >> 5  # Next 6 bits minus first 5 LSBs
        hour = timeNum >> 11  # Last 5 bits minus the first 11 LSBs

        if hour > 23 or minutes > 59 or seconds > 29:
            raise self.FormatError('Time value %d has an improper hour, minute, or second value: ' % timeNum)

        return (hour, minutes, (2 * seconds) + msec)

    def DateTimeDetector(self):
        """Detects and interprets an FAT date and time value by calling
        DateDetector() and TimeDetector() with the raw option set to True.

        Returns a regular success tuple (see ProcessInput()).
        """
        # Acceptable length for this kind of processing is either 8 or 10
        if len(self.inputStr) not in (8, 10): raise self.FormatError(
            'Datetime value has improper length of %d, expected 8 or 10' % len(self.inputStr))

        date = self.DateDetector(self.inputStr[-4:], True)
        time = self.TimeDetector(self.inputStr[:-4], True)
        return ('Time & Date Value: %02d:%02d:%05.2f, %d %s, %d\nProcessed for %s endian format' % (
            time + date + (self.endian,)), 'success', 'datetime')

    def GetCommand(self, lines):
        """Searches lines for supported commands which are then stored in the
        self.commands list. Any words that are not commands are simply
        ignored.

        No return value.
        """
        coms = []
        for line in lines:
            # print line
            if ">>" == line[:2]:
                for x in line[2:].split():
                    if x.strip() == '':
                        continue
                    elif x.lower() in self.supported_commands:
                        # print "Command found: %s" % x.lower()
                        coms += [x.lower()]
        self.commands = coms

    def GetPartInfo(self, entry):
        """Retrieves a single primary partition's information from entry,
        stores it in a dictionary, and returns the dictionary. The entry
        must be in standard IBM compatible partition table format.
        """
        if self.endian == 'little':
            order = -1
        else:
            order = 1

        info = {}
        if entry[0] == '00':
            info['State'] = 'Inactive'
        elif entry[0] == '80':
            info['State'] = 'Active'
        else:
            info['State'] = 'Invalid value'

        info['CHS Address'] = 'Head: %d; Cylinder: %d; Sector: %d' % self.GetCHS(entry)

        try:
            info['Partition Type'] = self.PType[entry[4]]
        except KeyError:  # Invalid entry, may be VBR instead of MBR
            info['Partition Type'] = "Unknown - Input may be VBR instead of MBR"
        # l = []
        # for x in xrange(256):
        # l.append('%02x' % x)

        info['End CHS Address'] = 'Head: %d; Cylinder: %d; Sector: %d' % self.GetCHS(entry, True)

        # LBA of first sector and Number of blocks: Not always used
        lbaVals = []
        if order == -1:
            lbaVals = entry[11:7:-1]
        elif order == 1:
            lbaVals = entry[8:12]
        lbaStr = ''
        for x in lbaVals:
            lbaStr += x
        info['LBA of First Sector'] = int(lbaStr, 16)

        blocksVals = []
        if order == -1:
            blocksVals = entry[15:11:-1]
        elif order == 1:
            blocksVals = entry[12:16]
        blocksStr = ''
        for x in blocksVals:
            blocksStr += x
        info['Number of Blocks'] = int(blocksStr, 16)

        return info

    def FATVBRdetector(self):
        """Entry point for interpreting the input as an FAT VBR. Begins
        processing the input text and determines if the length and boot
        signature are valid before proceeding. If the input text passes
        these tests, it is passed on to GetFATInfo().

        Returns a regular success tuple (see ProcessInput()).
        """
        # Check size, signature, much like MBR
        self.bytes = ChopHexStr(self.inputStr)

        # Check length of string
        if len(self.bytes) != 512:
            raise self.FormatError('FAT VBR is of improper length: %d, expected 512' % len(self.bytes))

        # Determine Endian
        if [self.bytes[-2], self.bytes[-1].upper()] == ['55', 'AA']:
            # Little Endian
            self.endian = 'little'
        elif [self.bytes[-2].upper(), self.bytes[-1]] == ['AA', '55']:
            # Big Endian
            self.endian = 'big'
        else:
            raise self.FormatError('FAT VBR does not have a valid signature.')

        return (self.FormatFATInfo(self.GetFATInfo()), 'success', 'fat-mbr')

    def GetFATInfo(self):
        """Interprets the information from the FAT boot sector and returns a
        dictionary with it. Works with FAT12/16/32.
        """
        # Copy byte information
        byt = self.bytes
        fatInfo = {}
        fatdata = (('OEM Name', 3, 8, 'ascii'),
                   ('Bytes per Sector', 11, 2, 'num'),
                   ('Sectors per Cluster', 13, 1, 'num'),
                   ('Reserved Sector Count', 14, 2, 'num'),
                   ('Number of FATs', 16, 1, 'num'),
                   ('Sectors per track', 24, 2, 'num'),
                   ('Number of Heads', 26, 2, 'num'),
                   ('Hidden Sectors Preceeding', 28, 4, 'num'))
        for w, x, y, z in fatdata:
            self.AddFATInfo(fatInfo, byt, w, x, y, z)

        # Total Sectors Calculation
        ttlSectors = Hex2Dec(StrFlatten(byt[19:19 + 2]), self.endian)
        if not ttlSectors:
            ttlSectors = Hex2Dec(StrFlatten(byt[32:32 + 4]), self.endian)
        fatInfo['Total Sectors'] = ttlSectors

        # Media Descriptor Code Interpretation
        medDesc = Hex2Dec(byt[21], self.endian)
        if medDesc == 240:
            fatInfo[
                'Media Descriptor'] = '3.5" Double Sided, 80 tracks per side, 18 or 36 sectors per track (1.44MB or 2.88MB). 5.25" Double Sided, 80 tracks per side, 15 sectors per track (1.2MB). Used also for other media types.'
        elif medDesc == 248:
            fatInfo['Media Descriptor'] = 'Fixed disk (i.e. Hard disk).'
        elif medDesc == 249:
            fatInfo[
                'Media Descriptor'] = '3.5" Double sided, 80 tracks per side, 9 sectors per track (720K). 5.25" Double sided, 80 tracks per side, 15 sectors per track (1.2MB)'
        elif medDesc == 250:
            fatInfo['Media Descriptor'] = '5.25" Single sided, 80 tracks per side, 8 sectors per track (320K)'
        elif medDesc == 251:
            fatInfo['Media Descriptor'] = '3.5" Double sided, 80 tracks per side, 8 sectors per track (640K)'
        elif medDesc == 252:
            fatInfo['Media Descriptor'] = '5.25" Single sided, 40 tracks per side, 9 sectors per track (180K)'
        elif medDesc == 253:
            fatInfo[
                'Media Descriptor'] = '5.25" Double sided, 40 tracks per side, 9 sectors per track (360K). Also used for 8".'
        elif medDesc == 254:
            fatInfo[
                'Media Descriptor'] = '5.25" Single sided, 40 tracks per side, 8 sectors per track (160K). Also used for 8".'
        elif medDesc == 255:
            fatInfo[
                'Media Descriptor'] = '5.25" Single sided, 40 tracks per side, 8 sectors per track (160K). Also used for 8".'
        else:
            fatInfo['Media Descriptor'] = 'Invalid Value'

        # For remaining bytes, determine if FAT 12, 16, or 32
        if byt[17] == 0:
            # FAT32
            fat32data = (('Sectors per FAT', 36, 4, 'num'),
                         ('Version', 42, 2, 'num'),
                         ('Cluster # of Root Dir', 44, 4, 'num'),
                         ('Sector # of FS Information', 48, 2, 'num'))

            backupSec = Hex2Dec(StrFlatten(byt[50:50 + 2]), self.endian)
            if backupSec:
                fatInfo['Sector # of Boot Sector Backup'] = backupSec
            if byt[64] == '00':
                fatInfo['Drive Type'] = 'Removable Media'
            elif byt[64] == '80':
                fatInfo['Drive Type'] = 'Hard Disk'

            if byt[66] == '29':  # Extended boot signature is valid
                fat32data = fat32data + (('Serial Number', 67, 4, 'num'),
                                         ('Volume Label', 71, 11, 'ascii'),
                                         ('File System Type', 82, 8, 'ascii'))

            for w, x, y, z in fat32data:
                self.AddFATInfo(fatInfo, byt, w, x, y, z)

        else:
            # Process FAT12 and FAT16 the same way
            fat16data = (('Max Root Directories', 17, 2, 'num'), ('Sectors per FAT', 22, 2, 'num'))

            if byt[36] == '00':
                fatInfo['Drive Type'] = 'Removable Media'
            elif byt[36] == '80':
                fatInfo['Drive Type'] = 'Hard Disk'

            if byt[38] == '29':  # Extended boot signature is valid
                fat16data = fat16data + (('Serial Number', 39, 4, 'num'),
                                         ('Volume Label', 43, 11, 'ascii'),
                                         ('File System Type', 54, 8, 'ascii'))
                for w, x, y, z in fat16data:
                    self.AddFATInfo(fatInfo, byt, w, x, y, z)
        return fatInfo

    def AddFATInfo(self, obj, byt, label, off, olen, dtype):
        """To simplify the commands in GetFATInfo(), this method accepts a
        dictionary object, the bytes from the VBR, the string to be the
        dictionary key, the byte offset of the data, the length of the data,
        and the data type which should be either 'ascii' or 'num'. No
        return value because the dictionary is added to directly.
        """
        if dtype == 'ascii':
            obj[label] = self.DecodeHex(StrFlatten(byt[off:off + olen]), float('inf'), False)
        elif dtype == 'num':
            obj[label] = Hex2Dec(StrFlatten(byt[off:off + olen]), self.endian)
        else:
            raise self.FormatError("Invalid data type passed to AddFATInfo: %s, expected 'ascii' or 'num'" % dtype)

    def FormatFATInfo(self, info):
        """Puts all the data from the dictionary info into a string for
        printing. The categories are defined in a local tuple and looped
        through. All categories that do not exist in info are skipped.

        Returns the string for printing.
        """
        cats = ('OEM Name', 'Volume Label', 'Drive Type', 'Media Descriptor', 'File System Type', 'Bytes per Sector',
                'Sectors per Cluster', 'Sectors per track', 'Number of Heads', 'Total Sectors',
                'Hidden Sectors Preceeding', 'Reserved Sector Count', 'Sectors per FAT', 'Number of FATs',
                'Cluster # of Root Dir', 'Max Root Directories', 'Sector # of FS Information',
                'Sector # of Boot Sector Backup', 'Version')
        end = 'Translation of FAT VBR:\n\n'

        for cat in cats:
            try:
                end += '%s: %s\n' % (cat, info[cat])
            except KeyError:
                continue
        return end

    def GetCHS(self, entry, end=False):
        """Retrieves the Cylinder Head Sector address from an MBR partition
        table entry. Since both the start CHS and end CHS are calculated
        the same way, if end is True, the offset will be changed so the
        proper values are put into the calculation.

        Returns a tuple in the form (head, cylinder, sector).
        """
        if not end:
            h, c, s = 1, 2, 3
        else:
            h, c, s = 5, 6, 7
        cyl = int(entry[c], 16) & 0xc0 * 4 + int(entry[s], 16)
        sec = int(entry[s], 16) & 0x3f
        return (int(entry[h], 16), cyl, sec)

    def GetBytes(self, row, width, hexstr=None):
        """Returns a string of the hex bytes from the input string for the
        given row and width. Separates the bytes with a space.
        """
        if hexstr == None:
            self.bytes = ChopHexStr(self.inputStr)  # Make sure we have the input string parsed into bytes
        else:
            self.bytes = ChopHexStr(hexstr)
        end = ''
        for byte in self.bytes[row * width:(row + 1) * width]:
            end += '%s ' % byte
        return end[:-1].ljust(width * 3 - 1)  # Take off last space before returning, make same width as other rows

    def DecodeHex(self, numstr=None, width=16, pretty=True):
        """Returns the decoded hex string of numstr with newlines after width
        characters. Replaces any non-printing characters with a period. If
        width is infinity, no newline characters are inserted. If pretty is
        True (default), the hex byte offset is printed in a column to the
        left, the hex bytes are printed in a center column, the ASCII
        decoding is in a column on the right, and a header with labels for
        the first two columns are all added to the string.
        """
        from math import ceil, log

        if numstr == None: numstr = self.inputStr
        tmp = ''
        for ch in numstr.decode('hex'):
            tmp2 = sub(r'\\x..', '.', repr(ch)[1:-1])
            if len(tmp2) == 1:
                tmp += tmp2
            else:
                tmp += '.'

        if pretty:  # Does a 'pretty print' of the decoded values
            strLength = len(tmp)
            offsetWidth = max(int(ceil(log(strLength, width))), 4)  # At least 4, otherwise log

            byteOffs = ''
            for x in xrange(width):
                byteOffs += ('%02x' % x).upper()

            end = '\n\n%s  %s\n%s %s %s\n' % (
                'Offset'.center(offsetWidth + 2), self.GetBytes(0, width, byteOffs), '-' * (offsetWidth + 2),
                '-' * (width * 3 + 1), '-' * (width + 1))
            for x in xrange(int(ceil(float(strLength) / width))):
                offset = ('%x' % (x * width)).rjust(offsetWidth, '0')
                end += ' %s | %s | %s\n' % (offset, self.GetBytes(x, width), tmp[x * width:(x + 1) * width])
            return end
        elif width == float('inf'):
            return tmp
        else:
            return '\n'.join(findall('.{1,%d}' % width, tmp))  # Inserts a newline after width characters

    def CheckHex(self):
        """Determines if the input string has only valid hex characters.
        Usually this method is called from CheckBinary(), which calls this
        method when its test for binary characters fails.

        No return value. Instead self.format is set to 'hex' or 'bad'.
        """
        mbr = self.inputStr  # Make a copy of the MBR string
        for ch in mbr:
            if ch not in string.hexdigits:
                self.format = "bad: contains '%s'" % ch
                return
        self.format = 'hex'

    def CheckBinary(self):
        """Determines if the input string has only valid binary characters. If
        the test fails, this method calls CheckHex(). If the test passes,
        the text is sent to be converted to hex before further processing,
        which simplifies the writing of all other methods which process the
        input text. This method is the first before CheckHex() because it
        will fail earlier on non-binary character strings given that the
        set of valid characters = {'1', '0'}.

        No return value. Instead self.format is set to 'hex'.
        """
        mbr = self.inputStr  # Make a copy of the MBR string
        for ch in mbr:
            if ch not in '01':
                return self.CheckHex()
        self.inputStr = Bin2Hex(mbr)  # MBR string is in binary, convert to hex
        self.format = 'hex'

    def FormatPartInfo(self, info):
        """Accepts a list (info) that has the information for the four
        partitions in the disk and formats them for being printed. Uses the
        sector counts to determine if any unallocated spaces exist between
        the partitions and inserts a notice at the top of the printed
        results if any are found.

        Returns the string.
        """
        cats = ('State', 'CHS Address', 'Partition Type', 'End CHS Address', 'LBA of First Sector', 'Number of Blocks')
        end = 'Translation of MBR:\n\n'

        # Look for empty spaces inbetween partitions
        lba = 'LBA of First Sector'
        num = 'Number of Blocks'
        ilen = len(info)
        info.append({lba: '0', num: '1'})
        for n in xrange(ilen):
            diff = int(info[n][lba]) - (int(info[n - 1][lba]) + int(info[n - 1][num]))
            if diff > 0:
                end += '--NOTICE--\n%d sectors are unallocated in between partitions %d and %d\n\n' % (diff, n, n + 1)
        info.pop()

        for n in xrange(len(info)):  # Loop through the 4 partitions
            end += "Partition %d\n\n" % (n + 1)
            for cat in cats:
                end += "%s: %s\n" % (cat, info[n][cat])
            end += "\n"
        return end

    def GetCommandDescriptions(self):
        """Returns a string with all supported commands in the format: \n\ncommand: description\ncommand: description\n...
        """
        end = ''
        for k in self.supported_commands:
            end += '\n%s: %s' % (k, self.command_descriptions[k])
        return end


def StrFlatten(mylist):
    """Takes a list of strings, mylist, and makes one string from it. Returns
    the string.
    """
    if mylist == []: raise IndexError
    s = ''
    for x in mylist:
        s += '%s' % x
    return s


def Bin2Hex(numstr):
    """Converts the given binary numstr (string) to a hex string. Returns the
    string.
    """
    result = ''
    while len(numstr):
        bstr = numstr[:8]
        numstr = numstr[8:]
        tmpval = 0
        for x in bstr:
            tmpval *= 2
            tmpval += int(x)
        result += '%x' % tmpval
    return result


def Hex2Dec(numstr, endian='little'):
    """Takes a hex number string and converts it to a decimal number. Returns
    the number.
    """
    count, num = 0, 0

    # Convert Little Endian number before processing
    if endian == 'little':
        newstr = ''
        while len(numstr):
            newstr = numstr[:2] + newstr
            numstr = numstr[2:]
        numstr = newstr
    # print "Converted Little Endian number to %s" % numstr

    for n in numstr[::-1]:
        num += string.hexdigits.index(n.lower()) * 16 ** count
        count += 1
    return num


def ChopHexStr(hexstr):
    """Takes a hex string and divides it into strings of length 2 (each
    representing a byte) and places them in a list. Returns the list.
    """
    tmp = hexstr  # Make a copy of the input string
    bytes = []
    # Break hexstr into bytes and put each byte in the 'bytes' list
    while tmp:
        bytes += [(tmp[:2])]
        tmp = tmp[2:]
    return bytes


def Hex2BinStr(hexstr, endian='little'):
    """
    Accepts a hex text string and translates it into a binary text string.
    Returns the binary text string.
    """
    binstr = ''
    dir = 1
    # if endian == 'little':
    # dir = -1
    for ch in hexstr[::dir]:
        binstr += HEXBIN_TRANS[ch]
    return binstr


if __name__ == '__main__':
    mbr = '33 C0 8E D0 BC 00 7C FB 50 07 50 1F FC BE 1B 7C BF 1B 06 50 57 B9 E5 01 F3 A4 CB BD BE 07 B1 04 38 6E 00 7C 09 75 13 83 C5 10 E2 F4 CD 18 8B F5 83 C6 10 49 74 19 38 2C 74 F6 A0 B5 07 B4 07 8B F0 AC 3C 00 74 FC BB 07 00 B4 0E CD 10 EB F2 88 4E 10 E8 46 00 73 2A FE 46 10 80 7E 04 0B 74 0B 80 7E 04 0C 74 05 A0 B6 07 75 D2 80 46 02 06 83 46 08 06 83 56 0A 00 E8 21 00 73 05 A0 B6 07 EB BC 81 3E FE 7D 55 AA 74 0B 80 7E 10 00 74 C8 A0 B7 07 EB A9 8B FC 1E 57 8B F5 CB BF 05 00 8A 56 00 B4 08 CD 13 72 23 8A C1 24 3F 98 8A DE 8A FC 43 F7 E3 8B D1 86 D6 B1 06 D2 EE 42 F7 E2 39 56 0A 77 23 72 05 39 46 08 73 1C B8 01 02 BB 00 7C 8B 4E 02 8B 56 00 CD 13 73 51 4F 74 4E 32 E4 8A 56 00 CD 13 EB E4 8A 56 00 60 BB AA 55 B4 41 CD 13 72 36 81 FB 55 AA 75 30 F6 C1 01 74 2B 61 60 6A 00 6A 00 FF 76 0A FF 76 08 6A 00 68 00 7C 6A 01 6A 10 B4 42 8B F4 CD 13 61 61 73 0E 4F 74 0B 32 E4 8A 56 00 CD 13 EB D6 61 F9 C3 49 6E 76 61 6C 69 64 20 70 61 72 74 69 74 69 6F 6E 20 74 61 62 6C 65 00 45 72 72 6F 72 20 6C 6F 61 64 69 6E 67 20 6F 70 65 72 61 74 69 6E 67 20 73 79 73 74 65 6D 00 4D 69 73 73 69 6E 67 20 6F 70 65 72 61 74 69 6E 67 20 73 79 73 74 65 6D 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 2C 44 63 8F D5 32 82 00 00 00 01 01 00 DE FE 3F 08 3F 00 00 00 8A 34 02 00 80 00 01 09 07 FE FF FF C9 34 02 00 B0 1A 18 1D 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 55 AA'
    foren = Forensie(mbr)
    print
    foren.ProcessInput()