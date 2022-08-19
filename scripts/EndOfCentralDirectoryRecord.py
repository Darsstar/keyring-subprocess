from io import BytesIO

from CentralDirectoryHeader import CentralDirectoryHeader
from typing import Generator


class EndOfCentralDirectoryRecord:
    """
    https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT section 4.3.16
    """

    def __init__(self, file: BytesIO, offset: int):
        file.seek(offset)
        self._signature = int.from_bytes(file.read(4), byteorder="little")
        self._disk_number = int.from_bytes(file.read(2), byteorder="little")
        self._disk_containing_CDR = int.from_bytes(file.read(2), byteorder="little")
        self._CDR_entries_on_disk = int.from_bytes(file.read(2), byteorder="little")
        self._CDR_entries_on_all_disks = int.from_bytes(file.read(2), byteorder="little")
        self._CDR_size = int.from_bytes(file.read(4), byteorder="little")
        self._CDR_offset = int.from_bytes(file.read(4), byteorder="little")
        self._comment_length = int.from_bytes(file.read(2), byteorder="little")
        self._comment = file.read()

        assert file.tell() - offset == self.min_size()

        assert self._signature == 0x06054b50
        assert self._comment_length == len(self._comment)
        assert self._CDR_size == len(file.getbuffer()[self._CDR_offset:offset])
        assert self._disk_number == 0, "Cannot handle split archive"
        assert self._disk_containing_CDR == 0, "Cannot handle split archive"
        assert self._CDR_entries_on_disk == self._CDR_entries_on_all_disks, "Cannot handle split archive"

    @staticmethod
    def min_size() -> int:
        return 22

    def size(self) -> int:
        return self.min_size() + self._comment_length

    def iter(self, file: BytesIO) -> Generator[CentralDirectoryHeader, None, None]:
        file.seek(self._CDR_offset)
        for i in range(0, self._CDR_entries_on_all_disks):
            yield CentralDirectoryHeader.parse(file)
