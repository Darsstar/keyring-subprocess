from pathlib import Path
from EndOfCentralDirectoryRecord import EndOfCentralDirectoryRecord

END_OF_CENTRAL_DIRECTORY_RECORD_SIGNATURE = 0x06054b50.to_bytes(4, byteorder="little")

dist_folder = Path(__file__).parent.parent / "dist"
wheels = list(dist_folder.glob("*.whl"))
assert len(wheels) == 1, f"Expected to find exactly one wheel. Wheels found: {wheels}"
wheel = wheels[0]
del wheels
wheel_bytes = wheel.read_bytes()

end_of_central_directory_record_offset = wheel_bytes.rfind(END_OF_CENTRAL_DIRECTORY_RECORD_SIGNATURE)
assert end_of_central_directory_record_offset != -1, "End of central directory record signature not found"
print(f"{end_of_central_directory_record_offset=}/{len(wheel_bytes)}")

end_of_central_directory_record = EndOfCentralDirectoryRecord(wheel_bytes, end_of_central_directory_record_offset)
print(end_of_central_directory_record._comment_length)
