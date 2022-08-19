from CentralDirectoryHeader import CentralDirectoryHeader
from typing import Generator

class EndOfCentralDirectoryRecord:
    """
    https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT section 4.3.16
    """
    def __init__(self, file: bytes, offset: int):
        buf = bytes(file[offset:])
        self._signature = int.from_bytes(buf[0:4], byteorder="little")
        self._disk_number = int.from_bytes(buf[4:6], byteorder="little")
        self._disk_containing_CDR = int.from_bytes(buf[6:8], byteorder="little")
        self._CDR_entries_on_disk = int.from_bytes(buf[8:10], byteorder="little")
        self._CDR_entries_on_all_disks = int.from_bytes(buf[10:12], byteorder="little")
        self._CDR_size = int.from_bytes(buf[12:16], byteorder="little")
        self._CDR_offset = int.from_bytes(buf[16:20], byteorder="little")
        self._comment_length = int.from_bytes(buf[20:22], byteorder="little")
        self._comment = buf[22:]

        assert self._signature == 0x06054b50
        assert self._comment_length == len(self._comment)
        assert self._CDR_size == len(file[self._CDR_offset:offset])
        assert self._disk_number == 0, "Cannot handle split archive"
        assert self._disk_containing_CDR == 0, "Cannot handle split archive"
        assert self._CDR_entries_on_disk == self._CDR_entries_on_all_disks, "Cannot handle split archive"

    def iter(self, file: bytes) -> Generator[CentralDirectoryHeader, None, None]:
        offset = self._CDR_offset
        for i in range(0, self._CDR_entries_on_all_disks):
            header, offset = CentralDirectoryHeader.parse(file, offset)
            yield header

    # def __repr__(self):
    #     return (
    #         "EndOfCentralDirectoryRecord("
    #         f"signature={self._signature}"
    #         f"number_of_this_disk={self._number_of_this_disk}"
    #     )
