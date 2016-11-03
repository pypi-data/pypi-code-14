# -*- coding: utf-8 -*-

from ctypes import CDLL, POINTER, Structure, c_int, c_uint, c_ulong


libx11 = CDLL("libX11.so.6")


XkbOD_Success = 0
XkbOD_BadLibraryVersion = 1
XkbOD_ConnectionRefused = 2
XkbOD_NonXkbServer = 3
XkbOD_BadServerVersion = 4

BadAlloc = 11
BadImplementation = 17
BadLength = 16
BadMatch = 8
Success = 0

XkbMajorVersion = 1
XkbMinorVersion = 0

XkbUseCoreKbd = 256

XkbAllControlsMask = 4160757759

XkbSymbolsNameMask = 4
XkbGroupNamesMask = 4096


class _XDisplay(Structure):
    pass
_XDisplay._fields_ = [
    ('ext_data', POINTER(XExtData)),
    ('free_funcs', POINTER(_XFreeFuncs)),
    ('fd', c_int),
    ('conn_checker', c_int),
    ('proto_major_version', c_int),
    ('proto_minor_version', c_int),
    ('vendor', STRING),
    ('resource_base', XID),
    ('resource_mask', XID),
    ('resource_id', XID),
    ('resource_shift', c_int),
    ('resource_alloc', CFUNCTYPE(XID, POINTER(_XDisplay))),
    ('byte_order', c_int),
    ('bitmap_unit', c_int),
    ('bitmap_pad', c_int),
    ('bitmap_bit_order', c_int),
    ('nformats', c_int),
    ('pixmap_format', POINTER(ScreenFormat)),
    ('vnumber', c_int),
    ('release', c_int),
    ('head', POINTER(_XSQEvent)),
    ('tail', POINTER(_XSQEvent)),
    ('qlen', c_int),
    ('last_request_read', c_ulong),
    ('request', c_ulong),
    ('last_req', STRING),
    ('buffer', STRING),
    ('bufptr', STRING),
    ('bufmax', STRING),
    ('max_request_size', c_uint),
    ('db', POINTER(_XrmHashBucketRec)),
    ('synchandler', CFUNCTYPE(c_int, POINTER(_XDisplay))),
    ('display_name', STRING),
    ('default_screen', c_int),
    ('nscreens', c_int),
    ('screens', POINTER(Screen)),
    ('motion_buffer', c_ulong),
    ('flags', c_ulong),
    ('min_keycode', c_int),
    ('max_keycode', c_int),
    ('keysyms', POINTER(KeySym)),
    ('modifiermap', POINTER(XModifierKeymap)),
    ('keysyms_per_keycode', c_int),
    ('xdefaults', STRING),
    ('scratch_buffer', STRING),
    ('scratch_length', c_ulong),
    ('ext_number', c_int),
    ('ext_procs', POINTER(_XExten)),
    ('event_vec', CFUNCTYPE(c_int, POINTER(Display), POINTER(XEvent), POINTER(xEvent)) * 128),
    ('wire_vec', CFUNCTYPE(c_int, POINTER(Display), POINTER(XEvent), POINTER(xEvent)) * 128),
    ('lock_meaning', KeySym),
    ('lock', POINTER(_XLockInfo)),
    ('async_handlers', POINTER(_XInternalAsync)),
    ('bigreq_size', c_ulong),
    ('lock_fns', POINTER(_XLockPtrs)),
    ('idlist_alloc', CFUNCTYPE(None, POINTER(Display), POINTER(XID), c_int)),
    ('key_bindings', POINTER(_XKeytrans)),
    ('cursor_font', Font),
    ('atoms', POINTER(_XDisplayAtoms)),
    ('mode_switch', c_uint),
    ('num_lock', c_uint),
    ('context_db', POINTER(_XContextDB)),
    ('error_vec', CFUNCTYPE(c_int, POINTER(Display), POINTER(XErrorEvent), POINTER(xError))),
    ('cms', N9_XDisplay5DOT_252E),
    ('im_filters', POINTER(_XIMFilter)),
    ('qfree', POINTER(_XSQEvent)),
    ('next_event_serial_num', c_ulong),
    ('flushes', POINTER(_XExten)),
    ('im_fd_info', POINTER(_XConnectionInfo)),
    ('im_fd_length', c_int),
    ('conn_watchers', POINTER(_XConnWatchInfo)),
    ('watcher_count', c_int),
    ('filedes', XPointer),
    ('savedsynchandler', CFUNCTYPE(c_int, POINTER(Display))),
    ('resource_max', XID),
    ('xcmisc_opcode', c_int),
    ('xkb_info', POINTER(_XkbInfoRec)),
    ('trans_conn', POINTER(_XtransConnInfo)),
    ('xcb', POINTER(_X11XCBPrivate)),
    ('next_cookie', c_uint),
    ('generic_event_vec', CFUNCTYPE(c_int, POINTER(Display), POINTER(XGenericEventCookie), POINTER(xEvent)) * 128),
    ('generic_event_copy_vec', CFUNCTYPE(c_int, POINTER(Display), POINTER(XGenericEventCookie), POINTER(XGenericEventCookie)) * 128),
    ('cookiejar', c_void_p),
]
Display = _XDisplay

class _XkbDesc(Structure):
    pass
_XkbDesc._fields_ = [
    ('dpy', POINTER(_XDisplay)),
    ('flags', c_ushort),
    ('device_spec', c_ushort),
    ('min_key_code', KeyCode),
    ('max_key_code', KeyCode),
    ('ctrls', XkbControlsPtr),
    ('server', XkbServerMapPtr),
    ('map', XkbClientMapPtr),
    ('indicators', XkbIndicatorPtr),
    ('names', XkbNamesPtr),
    ('compat', XkbCompatMapPtr),
    ('geom', XkbGeometryPtr),
]
XkbDescRec = _XkbDesc
XkbDescPtr = POINTER(_XkbDesc)


XkbIgnoreExtension = libx11.XkbIgnoreExtension
XkbIgnoreExtension.restype = c_int
XkbIgnoreExtension.argtypes = [c_int]

XkbOpenDisplay = libx11.XkbOpenDisplay
XkbOpenDisplay.restype = POINTER(Display)
XkbOpenDisplay.argtypes = [STRING, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]

XkbGetMap = libx11.XkbGetMap
XkbGetMap.restype = XkbDescPtr
XkbGetMap.argtypes = [POINTER(Display), c_uint, c_uint]

XkbGetControls = libx11.XkbGetControls
XkbGetControls.restype = c_int
XkbGetControls.argtypes = [POINTER(Display), c_ulong, XkbDescPtr]

XkbGetNames = libx11.XkbGetNames
XkbGetNames.restype = c_int
XkbGetNames.argtypes = [POINTER(Display), c_uint, XkbDescPtr]

XkbFreeNames = libx11.XkbFreeNames
XkbFreeNames.restype = None
XkbFreeNames.argtypes = [XkbDescPtr, c_uint, c_int]

XkbFreeControls = libx11.XkbFreeControls
XkbFreeControls.restype = None
XkbFreeControls.argtypes = [XkbDescPtr, c_uint, c_int]

XkbFreeClientMap = libx11.XkbFreeClientMap
XkbFreeClientMap.restype = None
XkbFreeClientMap.argtypes = [XkbDescPtr, c_uint, c_int]

XCloseDisplay = libx11.XCloseDisplay
XCloseDisplay.restype = c_int
XCloseDisplay.argtypes = [POINTER(Display)]


