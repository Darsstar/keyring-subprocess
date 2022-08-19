from io import BytesIO

from LocalFileHeader import LocalFileHeader


class CentralDirectoryHeader:
    @staticmethod
    def parse(file: BytesIO):
        return CentralDirectoryHeader(file)

    def __init__(self, bio: BytesIO):
        offset = bio.tell()

        self._signature = int.from_bytes(bio.read(4), byteorder="little")
        self._version_created = int.from_bytes(bio.read(2), byteorder="little")
        self._version_needed = int.from_bytes(bio.read(2), byteorder="little")
        self._GP_bit_flag = int.from_bytes(bio.read(2), byteorder="little")
        self._compression = int.from_bytes(bio.read(2), byteorder="little")
        self._mod_time = int.from_bytes(bio.read(2), byteorder="little")
        self._mod_date = int.from_bytes(bio.read(2), byteorder="little")
        self._crc = int.from_bytes(bio.read(4), byteorder="little")
        self._compressed = int.from_bytes(bio.read(4), byteorder="little")
        self._uncompressed = int.from_bytes(bio.read(4), byteorder="little")
        self._filename_length = int.from_bytes(bio.read(2), byteorder="little")
        self._extra_length = int.from_bytes(bio.read(2), byteorder="little")
        self._comment_length = int.from_bytes(bio.read(2), byteorder="little")
        self._disk_start = int.from_bytes(bio.read(2), byteorder="little")
        self._internal_file_attrs = int.from_bytes(bio.read(2), byteorder="little")
        self._external_file_attrs = int.from_bytes(bio.read(4), byteorder="little")
        self._rel_local_header_offset = int.from_bytes(bio.read(4), byteorder="little")

        assert bio.tell() - offset == self.min_size()

        self._filename = bio.read(self._filename_length)
        self._extra = bio.read(self._extra_length)
        self._comment = bio.read(self._comment_length)

        assert self._signature == 0x02014b50
        assert self._disk_start == 0, "Cannot handle split archive"

    @staticmethod
    def min_size() -> int:
        return 46

    def size(self) -> int:
        return self.min_size() + self._filename_length

    def local_header(self, file: BytesIO) -> LocalFileHeader:
        local_header = LocalFileHeader.parse(file)

        assert local_header.filename_length == self._filename_length, f"{local_header.filename_length} != {self._filename_length}"
        assert local_header.filename == self._filename, f"{local_header.filename} != {self._filename}"
        assert local_header.extra == self._extra
        assert local_header.GP_bit_flag == self._GP_bit_flag
        assert local_header.compressed == self._compressed
        assert local_header.uncompressed == self._uncompressed
        assert local_header.mod_time == self._mod_time
        assert local_header.mod_date == self._mod_date
        assert local_header.crc == self._crc

        return local_header
