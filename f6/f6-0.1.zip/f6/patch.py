from ctypes import *
from ctypes.wintypes import *

LPBYTE = POINTER(BYTE)

class STARTUPINFOW(Structure):

    _fields_ = [
        ('cb',               DWORD),
        ('lpReserved',       LPWSTR),
        ('lpDesktop',        LPWSTR),
        ("dwX",              DWORD),
        ("dwY",              DWORD),
        ("dwXSize",          DWORD),
        ("dwYSize",          DWORD),
        ("dwXCountChars",    DWORD),
        ("dwYCountChars",    DWORD),
        ("dwFillAtrribute",  DWORD),
        ("dwFlags",          DWORD),
        ("wShowWindow",      WORD),
        ("cbReserved2",      WORD),
        ("lpReserved2",      LPBYTE),
        ("hStdInput",        HANDLE),
        ("hStdOutput",       HANDLE),
        ("hStdError",        HANDLE),
    ]

class PROCESS_INFORMATION(Structure):

    _fields_ = [
               ("hProcess",         HANDLE),
               ("hThread",          HANDLE),
               ("dwProcessId",      DWORD),
               ("dwThreadId",       DWORD),
    ]

CreateProcessW = windll.kernel32.CreateProcessW

startupinfow = STARTUPINFOW()
process_information = PROCESS_INFORMATION()

def systemw(cmd):
    if not isinstance(cmd, unicode):
        cmd = cmd.decode('mbcs')
    return CreateProcessW(
        None,
        cmd,
        None,
        None,
        0,
        None,
        None,
        None,
        byref(startupinfow),
        byref(process_information),
    )

if __name__ == '__main__':
    systemw('calc')
