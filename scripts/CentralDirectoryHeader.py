

class CentralDirectoryHeader:
    @staticmethod
    def parse(file: bytes, offset: int):
        buf = bytes(file[offset:])
        self = CentralDirectoryHeader()
        self._signature = int.from_bytes(buf[0:4], byteorder="little")
        self._version_created = int.from_bytes(buf[4:6], byteorder="little")
        self._version_needed = int.from_bytes(buf[6:8], byteorder="little")
        self._GP_bit_flag = int.from_bytes(buf[8:10], byteorder="little")
        self._compression = int.from_bytes(buf[10:12], byteorder="little")
        self._mod_time = int.from_bytes(buf[12:14], byteorder="little")
        self._mod_date = int.from_bytes(buf[14:16], byteorder="little")
        self._crc = int.from_bytes(buf[16:20], byteorder="little")
        self._compressed = int.from_bytes(buf[20:24], byteorder="little")
        self._uncompressed = int.from_bytes(buf[24:28], byteorder="little")
        self._filename_length = int.from_bytes(buf[28:30], byteorder="little")
        self._extra_length = int.from_bytes(buf[30:32], byteorder="little")
        self._comment_length = int.from_bytes(buf[32:34], byteorder="little")
        self._disk_start = int.from_bytes(buf[34:36], byteorder="little")
        self._internal_file_attrs = int.from_bytes(buf[36:38], byteorder="little")
        self._external_file_attrs = int.from_bytes(buf[38:42], byteorder="little")
        self._rel_local_header_offset = int.from_bytes(buf[42:46], byteorder="little")
        filename_end = 46 + self._filename_length
        self._filename = buf[46:filename_end]
        extra_end = filename_end + self._extra_length
        self._extra = buf[filename_end:extra_end]
        comment_end = extra_end + self._comment_length
        self._comment = buf[extra_end:comment_end]

        assert self._signature == 0x02014b50
        assert self._disk_start == 0, "Cannot handle split archive"

        return self, offset + comment_end
