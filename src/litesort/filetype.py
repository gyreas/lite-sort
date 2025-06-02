from enum import IntEnum

class FileType(IntEnum):
    ARCHIVE    = 1
    AUDIO      = 2
    DOCUMENT   = 3
    EXECUTABLE = 4
    IMAGE      = 5
    RAW_DATA   = 6
    TEXT       = 7
    VIDEO      = 8
    UNKNOWN    = -1

    def __str__(self) -> str:
        return self.name
