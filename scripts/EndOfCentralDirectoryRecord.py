

class EndOfCentralDirectoryRecord:
    """
    https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT section 4.3.16
    """
    def __init__(self, file: bytes, offset: int):
        buf = bytes(file[offset:])
        self._signature = buf[0:4]
        self._number_of_this_disk = buf[4:6]
        self._number_of_the_disk_with_the_start_of_the_central_directory = buf[6:8]
        self._total_number_of_entries_in_the_central_directory_on_this_disk = buf[8:10]
        self._total_number_of_entries_in_the_central_directory = buf[10:12]
        self._size_of_the_central_directory = buf[12:16]
        self._offset_of_start_of_central_directory_with_respect_to_the_starting_disk_number = buf[16:20]
        self._ZIP_file_comment_length = buf[20:22]
        self._ZIP_file_comment = buf[22:]

        comment_length = int.from_bytes(self._ZIP_file_comment_length, byteorder="little")
        assert comment_length == len(self._ZIP_file_comment)

        size_of_central_directory = int.from_bytes(self._size_of_the_central_directory, byteorder="little")
        central_directory_offset = int.from_bytes(self._offset_of_start_of_central_directory_with_respect_to_the_starting_disk_number,
                                    byteorder="little")
        assert size_of_central_directory == len(file[central_directory_offset:offset])

    # def __repr__(self):
    #     return (
    #         "EndOfCentralDirectoryRecord("
    #         f"signature={self._signature}"
    #         f"number_of_this_disk={self._number_of_this_disk}"
    #     )
