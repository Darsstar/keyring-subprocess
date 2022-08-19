from io import BytesIO


class LocalFileHeader:

    @classmethod
    def parse(cls, file: BytesIO) -> "LocalFileHeader":
        return LocalFileHeader(file)

    def __init__(self, file: BytesIO):
        offset = file.tell()

        self.signature = int.from_bytes(file.read(4), byteorder="little")
        self.version_needed = int.from_bytes(file.read(2), byteorder="little")
        self.GP_bit_flag = int.from_bytes(file.read(2), byteorder="little")
        self.compression = int.from_bytes(file.read(2), byteorder="little")
        self.mod_time = int.from_bytes(file.read(2), byteorder="little")
        self.mod_date = int.from_bytes(file.read(2), byteorder="little")
        self.crc = int.from_bytes(file.read(4), byteorder="little")
        self.compressed = int.from_bytes(file.read(4), byteorder="little")
        self.uncompressed = int.from_bytes(file.read(4), byteorder="little")
        self.filename_length = int.from_bytes(file.read(2), byteorder="little")
        self.extra_length = int.from_bytes(file.read(2), byteorder="little")

        assert file.tell() - offset == self.min_size()

        self.filename = file.read(self.filename_length)
        self.extra = file.read(self.extra_length)

    @staticmethod
    def min_size():
        return 30

    def size(self):
        return self.min_size() + self.filename_length + self.extra_length
