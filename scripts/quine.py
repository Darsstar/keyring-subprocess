from io import BytesIO
from pathlib import Path
from EndOfCentralDirectoryRecord import EndOfCentralDirectoryRecord

END_OF_CENTRAL_DIRECTORY_RECORD_SIGNATURE = 0x06054b50.to_bytes(4, byteorder="little")

dist_folder = Path(__file__).parent.parent / "dist"
wheels = list(dist_folder.glob("*.whl"))
assert len(wheels) == 1, f"Expected to find exactly one wheel. Wheels found: {wheels}"
wheel = wheels[0]
del wheels
wheel_bytes = wheel.read_bytes()
wheel_io = BytesIO(wheel_bytes)

end_of_central_directory_record = None
end_of_central_directory_record_offset = len(wheel_bytes)
while end_of_central_directory_record is None:
    print(f"{end_of_central_directory_record_offset}")
    assert end_of_central_directory_record_offset != -1, "End of central directory record signature not found"
    try:
        end_of_central_directory_record = EndOfCentralDirectoryRecord(wheel_io, end_of_central_directory_record_offset)
    except AssertionError:
        end_of_central_directory_record_offset = wheel_bytes.rfind(END_OF_CENTRAL_DIRECTORY_RECORD_SIGNATURE, 0, end_of_central_directory_record_offset)

CDR_headers = list(end_of_central_directory_record.iter(wheel_io))
for CDR_header in CDR_headers:
    wheel_io.seek(CDR_header._rel_local_header_offset)
    local = CDR_header.local_header(wheel_io)
    print(f"{CDR_header._filename=}, {CDR_header._rel_local_header_offset}, {CDR_header.size() + CDR_header._compressed}")

print(f"{end_of_central_directory_record._CDR_offset}")
