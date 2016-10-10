import sys

from construct import Adapter, CString, If, IfThenElse, Magic, MetaArray, OneOf, Optional, Padding, PascalString, String, Struct, Switch, UBInt8, ULInt16, Value
from enum import Enum


# ===============================================================================
# /*
#    * Rough structure of a .wsg file:
#    *
#    * === HEADER ===
#    * WoW File
#    *   [junk byte]
#    * Song words
#    *   [0x13 - 0x37 junk bytes]
#    *   [# of blocks in file]
#    *   [0x0 0x0 0x0]
#    *   [0xFF 0xFF]
#    *   [0x3E - 0x41 junk bytes]
#    * CSongDoc::CBlock
#    *   [BLOCKS - see below]
#    *   [Byte count of author]
#    * Author
#    *   [Byte count of copyright]
#    * Copyright
#    *   [LICENSEFLAG]
#    *   [0x0 0x0 0x0]
#    * [EOF]
#    *
#    * === LICENSEFLAG ===
#    * 0 - Covered by CCL
#    * 1 - Author's explicit permission
#    * 2 - Public Domain
#    * 3 - Copyright Expired
#    * 4 - Other
#    * === BLOCKS ===
#    *   [# of lines in block]
#    *   [0x0 0x0 0x0]
#    *   [LINES - see below]
#    *   [BLOCKTYPE]
#    *   [0x0 0x0 0x0]
#    *
#    * Two adjacent blocks will have two bytes of "junk" between them.
#    *
#    * === BLOCKTYPE ===
#    * 0 - verse
#    * 1 - chorus
#    * 2 - bridge
#    *
#    * === LINES ===
#    *   [# of bytes in line] - one byte, or if 0xFF, the following two bytes (little-endian)
#    *   Line text
#    *   [LINETYPE]
#    *
#    * === LINETYPE ===
#    * 0 - normal
#    * 1 - minor words
class LineType(Enum):
    NORMAL = 0
    MINOR = 1


class BlockType(Enum):
    VERSE = 0
    CHORUS = 1
    BRIDGE = 2


class LicenseType(Enum):
    CCL = 0
    AUTHOR_EXPLICIT_PERMISSION = 1
    PUBLIC_DOMAIN = 2
    COPYRIGHT_EXPIRED = 3
    OTHER = 4


class EnumAdapter(Adapter):
    def __init__(self, enumClass, subcon):
        super(Adapter, self).__init__(subcon)
        self.enumClass = enumClass

    def _encode(self, obj, context):
        return obj.value

    def _decode(self, obj, context):
        return self.enumClass(obj)


def valuesOf(enum):
    return map(lambda x: x.value, enum)


def findFormat(ctx):
    if 'format' in ctx:
        return ctx.format
    if '_' in ctx:
        return findFormat(ctx._)
    return 0


Line = Struct(
    "line",
    UBInt8("length"),
    IfThenElse(
        "length",
        lambda ctx: ctx.length == 0xFF,
        ULInt16("length"),
        Value("length", lambda ctx: ctx.length)
    ),
    String("text", length=lambda ctx: ctx.length, encoding="windows-1252"),
    If(
        lambda ctx: findFormat(ctx) == 1,  # 0 = Really old WoW format without minor words
        EnumAdapter(LineType, OneOf(UBInt8("type"), valuesOf(LineType))),
        LineType.NORMAL
    ),
    allow_overwrite=True
)


Block = Struct(
    "block",
    Padding(2),
    UBInt8("linecount"),
    Padding(3),
    MetaArray(lambda ctx: ctx.linecount, Line),
    EnumAdapter(BlockType, OneOf(UBInt8("type"), valuesOf(BlockType))),
    Padding(3)
)

Song = Struct(
    "song",
    UBInt8("blockcount"),
    Padding(9),
    Magic('CSongDoc::CBlo'),  # The 'ck' is considered padding at start of block
    MetaArray(lambda ctx: ctx.blockcount, Block),
    PascalString("author", encoding="windows-1252"),
    PascalString("copyright", encoding="windows-1252"),
    Optional(
        Struct(
            "license",
            EnumAdapter(LicenseType, OneOf(UBInt8("type"), valuesOf(LicenseType))),
            Padding(3)
        )
    )
)

Liturgy = Struct(
    'liturgy',
    UBInt8("linecount"),
    Padding(3),
    MetaArray(lambda ctx: ctx.linecount, Line)
)

RESOURCE_MAPPING = {
    'Song Words': Song,
    'Liturgy': Liturgy
}

Resource = Struct(
    "resource",
    Magic("WoW File\n"),
    OneOf(CString("filetype", encoding="windows-1252", terminators="\x00\n"), RESOURCE_MAPPING.keys()),
    Padding(4),
    UBInt8("format"),
    Padding(31),
    Switch(
        "content",
        lambda ctx: ctx.filetype,
        RESOURCE_MAPPING
    )
)


if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename, "rb") as f:
        print Resource.parse(f.read())
