from ctypes import *

from pynfc.nfc import _G_fpos_t
from pynfc.nfc import _G_fpos64_t
from pynfc.nfc import _IO_jump_t
from pynfc.nfc import _IO_marker
from pynfc.nfc import __codecvt_result
from pynfc.nfc import _IO_FILE
from pynfc.nfc import _IO_FILE_plus
from pynfc.nfc import __io_read_fn
from pynfc.nfc import __io_write_fn
from pynfc.nfc import __io_seek_fn
from pynfc.nfc import __io_close_fn
from pynfc.nfc import cookie_read_function_t
from pynfc.nfc import cookie_write_function_t
from pynfc.nfc import cookie_seek_function_t
from pynfc.nfc import cookie_close_function_t
from pynfc.nfc import _IO_cookie_io_functions_t
from pynfc.nfc import cookie_io_functions_t
from pynfc.nfc import _IO_cookie_file
from pynfc.nfc import nfc_context
from pynfc.nfc import nfc_context
from pynfc.nfc import nfc_device
from pynfc.nfc import nfc_device
from pynfc.nfc import nfc_driver
from pynfc.nfc import nfc_driver
from pynfc.nfc import nfc_connstring
from pynfc.nfc import nfc_property
from pynfc.nfc import nfc_dep_mode
from pynfc.nfc import nfc_dep_info
from pynfc.nfc import nfc_iso14443a_info
from pynfc.nfc import nfc_felica_info
from pynfc.nfc import nfc_iso14443b_info
from pynfc.nfc import nfc_iso14443bi_info
from pynfc.nfc import nfc_iso14443b2sr_info
from pynfc.nfc import nfc_iso14443b2ct_info
from pynfc.nfc import nfc_jewel_info
from pynfc.nfc import nfc_target_info
from pynfc.nfc import nfc_baud_rate
from pynfc.nfc import nfc_modulation_type
from pynfc.nfc import nfc_mode
from pynfc.nfc import nfc_modulation
from pynfc.nfc import nfc_target
from pynfc.nfc import int8_t
from pynfc.nfc import int16_t
from pynfc.nfc import int32_t
from pynfc.nfc import int64_t
from pynfc.nfc import uint8_t
from pynfc.nfc import uint16_t
from pynfc.nfc import uint32_t
from pynfc.nfc import uint64_t
from pynfc.nfc import int_least8_t
from pynfc.nfc import int_least16_t
from pynfc.nfc import int_least32_t
from pynfc.nfc import int_least64_t
from pynfc.nfc import uint_least8_t
from pynfc.nfc import uint_least16_t
from pynfc.nfc import uint_least32_t
from pynfc.nfc import uint_least64_t
from pynfc.nfc import int_fast8_t
from pynfc.nfc import int_fast16_t
from pynfc.nfc import int_fast32_t
from pynfc.nfc import int_fast64_t
from pynfc.nfc import uint_fast8_t
from pynfc.nfc import uint_fast16_t
from pynfc.nfc import uint_fast32_t
from pynfc.nfc import uint_fast64_t
from pynfc.nfc import intptr_t
from pynfc.nfc import uintptr_t
from pynfc.nfc import intmax_t
from pynfc.nfc import uintmax_t
from pynfc.nfc import FILE
from pynfc.nfc import __FILE
from pynfc.nfc import va_list
from pynfc.nfc import off_t
from pynfc.nfc import off64_t
from pynfc.nfc import ssize_t
from pynfc.nfc import fpos_t
from pynfc.nfc import fpos64_t
from pynfc.nfc import obstack
from pynfc.nfc import __mbstate_t
from pynfc.nfc import __u_char
from pynfc.nfc import __u_short
from pynfc.nfc import __u_int
from pynfc.nfc import __u_long
from pynfc.nfc import __int8_t
from pynfc.nfc import __uint8_t
from pynfc.nfc import __int16_t
from pynfc.nfc import __uint16_t
from pynfc.nfc import __int32_t
from pynfc.nfc import __uint32_t
from pynfc.nfc import __int64_t
from pynfc.nfc import __uint64_t
from pynfc.nfc import __quad_t
from pynfc.nfc import __u_quad_t
from pynfc.nfc import __dev_t
from pynfc.nfc import __uid_t
from pynfc.nfc import __gid_t
from pynfc.nfc import __ino_t
from pynfc.nfc import __ino64_t
from pynfc.nfc import __mode_t
from pynfc.nfc import __nlink_t
from pynfc.nfc import __off_t
from pynfc.nfc import __off64_t
from pynfc.nfc import __pid_t
from pynfc.nfc import __fsid_t
from pynfc.nfc import __clock_t
from pynfc.nfc import __rlim_t
from pynfc.nfc import __rlim64_t
from pynfc.nfc import __id_t
from pynfc.nfc import __time_t
from pynfc.nfc import __useconds_t
from pynfc.nfc import __suseconds_t
from pynfc.nfc import __daddr_t
from pynfc.nfc import __key_t
from pynfc.nfc import __clockid_t
from pynfc.nfc import __timer_t
from pynfc.nfc import __blksize_t
from pynfc.nfc import __blkcnt_t
from pynfc.nfc import __blkcnt64_t
from pynfc.nfc import __fsblkcnt_t
from pynfc.nfc import __fsblkcnt64_t
from pynfc.nfc import __fsfilcnt_t
from pynfc.nfc import __fsfilcnt64_t
from pynfc.nfc import __fsword_t
from pynfc.nfc import __ssize_t
from pynfc.nfc import __syscall_slong_t
from pynfc.nfc import __syscall_ulong_t
from pynfc.nfc import __loff_t
from pynfc.nfc import __qaddr_t
from pynfc.nfc import __caddr_t
from pynfc.nfc import __intptr_t
from pynfc.nfc import __socklen_t
from pynfc.nfc import __gnuc_va_list
from pynfc.nfc import ptrdiff_t
from pynfc.nfc import size_t
from pynfc.nfc import __va_list_tag


N_TARGET = 0
MC_AUTH_B = 97
NP_TIMEOUT_ATR = 1
__codecvt_partial = 1
NP_FORCE_SPEED_106 = 14
N_INITIATOR = 1
NP_ACTIVATE_CRYPTO1 = 6
NDM_ACTIVE = 2
NDM_PASSIVE = 1
NP_ACTIVATE_FIELD = 5
NDM_UNDEFINED = 0
NP_TIMEOUT_COMMAND = 0
NMT_FELICA = 7
NBR_847 = 4
NBR_424 = 3
NBR_212 = 2
NBR_106 = 1
NBR_UNDEFINED = 0
NP_AUTO_ISO14443_4 = 10
MC_STORE = 194
MC_INCREMENT = 193
MC_DECREMENT = 192
__codecvt_noconv = 3
MC_AUTH_A = 96
__codecvt_error = 2
__codecvt_ok = 0
NP_FORCE_ISO14443_B = 13
NP_FORCE_ISO14443_A = 12
NP_EASY_FRAMING = 11
NP_ACCEPT_MULTIPLE_FRAMES = 9
NP_ACCEPT_INVALID_FRAMES = 8
NP_INFINITE_SELECT = 7
NP_HANDLE_PARITY = 4
NP_HANDLE_CRC = 3
NP_TIMEOUT_COM = 2
NMT_DEP = 8
NMT_ISO14443B2CT = 6
NMT_ISO14443B2SR = 5
NMT_ISO14443BI = 4
NMT_ISO14443B = 3
NMT_JEWEL = 2
NMT_ISO14443A = 1
MC_TRANSFER = 176
MC_WRITE = 160
MC_READ = 48
_IO_lock_t = None
class N11__mbstate_t3DOT_2E(Union):
    pass
N11__mbstate_t3DOT_2E._fields_ = [
    ('__wch', c_uint),
    ('__wchb', c_char * 4),
]

# values for enumeration 'mifare_cmd'
mifare_cmd = c_int # enum
class mifare_param_auth(Structure):
    pass
mifare_param_auth._fields_ = [
    ('abtKey', uint8_t * 6),
    ('abtAuthUid', uint8_t * 4),
]
class mifare_param_data(Structure):
    pass
mifare_param_data._fields_ = [
    ('abtData', uint8_t * 16),
]
class mifare_param_value(Structure):
    pass
mifare_param_value._fields_ = [
    ('abtValue', uint8_t * 4),
]
class mifare_param(Union):
    pass
mifare_param._fields_ = [
    ('mpa', mifare_param_auth),
    ('mpd', mifare_param_data),
    ('mpv', mifare_param_value),
]
class mifare_classic_block_manufacturer(Structure):
    pass
mifare_classic_block_manufacturer._fields_ = [
    ('abtUID', uint8_t * 4),
    ('btBCC', uint8_t),
    ('btSAK', uint8_t),
    ('abtATQA', uint8_t * 2),
    ('abtManufacturer', uint8_t * 8),
]
class mifare_classic_block_data(Structure):
    pass
mifare_classic_block_data._fields_ = [
    ('abtData', uint8_t * 16),
]
class mifare_classic_block_trailer(Structure):
    pass
mifare_classic_block_trailer._fields_ = [
    ('abtKeyA', uint8_t * 6),
    ('abtAccessBits', uint8_t * 4),
    ('abtKeyB', uint8_t * 6),
]
class mifare_classic_block(Union):
    pass
mifare_classic_block._fields_ = [
    ('mbm', mifare_classic_block_manufacturer),
    ('mbd', mifare_classic_block_data),
    ('mbt', mifare_classic_block_trailer),
]
class mifare_classic_tag(Structure):
    pass
mifare_classic_tag._fields_ = [
    ('amb', mifare_classic_block * 256),
]
class mifareul_block_manufacturer(Structure):
    pass
mifareul_block_manufacturer._fields_ = [
    ('sn0', uint8_t * 3),
    ('btBCC0', uint8_t),
    ('sn1', uint8_t * 4),
    ('btBCC1', uint8_t),
    ('internal', uint8_t),
    ('lock', uint8_t * 2),
    ('otp', uint8_t * 4),
]
class mifareul_block_data(Structure):
    pass
mifareul_block_data._fields_ = [
    ('abtData', uint8_t * 16),
]
class mifareul_block(Union):
    pass
mifareul_block._fields_ = [
    ('mbm', mifareul_block_manufacturer),
    ('mbd', mifareul_block_data),
]
class mifareul_tag(Structure):
    pass
mifareul_tag._fields_ = [
    ('amb', mifareul_block * 4),
]
__all__ = ['NMT_ISO14443A', 'NMT_ISO14443B', 'NMT_FELICA',
           'mifare_param_value', 'NBR_UNDEFINED',
           'NP_FORCE_ISO14443_B', '__codecvt_ok',
           'NP_ACCEPT_INVALID_FRAMES', 'MC_AUTH_A',
           'mifareul_block_data', 'NP_ACTIVATE_FIELD', 'NBR_847',
           'NP_ACCEPT_MULTIPLE_FRAMES', 'NP_HANDLE_CRC',
           'MC_INCREMENT', 'NBR_106', 'mifare_param',
           'mifare_classic_block', 'NP_FORCE_SPEED_106', 'NMT_DEP',
           'NMT_ISO14443BI', 'N11__mbstate_t3DOT_2E',
           'NP_FORCE_ISO14443_A', 'MC_STORE', 'NP_TIMEOUT_COMMAND',
           'NP_AUTO_ISO14443_4', 'NMT_JEWEL', 'NMT_ISO14443B2CT',
           'mifare_classic_block_manufacturer', 'N_INITIATOR',
           'mifare_param_auth', 'MC_AUTH_B', '__codecvt_partial',
           'N_TARGET', 'MC_TRANSFER', 'mifare_classic_tag', 'MC_READ',
           'mifare_param_data', 'mifareul_block_manufacturer',
           'mifare_classic_block_trailer', '__codecvt_error',
           'NP_INFINITE_SELECT', 'NBR_424', '_IO_lock_t',
           'MC_DECREMENT', 'mifareul_block', 'NP_ACTIVATE_CRYPTO1',
           'mifare_cmd', 'NDM_PASSIVE', 'NDM_UNDEFINED',
           'NP_HANDLE_PARITY', 'NP_EASY_FRAMING', 'NMT_ISO14443B2SR',
           'mifareul_tag', 'mifare_classic_block_data', 'MC_WRITE',
           'NDM_ACTIVE', 'NBR_212', '__codecvt_noconv',
           'NP_TIMEOUT_ATR', 'NP_TIMEOUT_COM']
