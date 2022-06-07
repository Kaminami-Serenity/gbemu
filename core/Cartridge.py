from collections import namedtuple
import struct

# A mapping of the header byte positions used to create a formatted header object. 
HEADER_FIELDS = [
    (None, "="),                 # Native Endian
    (None, 'xxxx'),              # 0x100 - 0x103 (entry point)
    (None, '48x'),               # 0x104 - 0x133 (Nintendo Logo)
    ("title", '15s'),            # 0x134 - 0x143 (cartridge title)
    ("cgb", 'B'),                # 0x134 - (color bg flag)
    ("new_license_code", 'H'),   # 0x144 - 0x145 (new license code)
    ("sgb", 'B'),                # 0x146 - (super gb flag)
    ("mbc_type", 'B'),           # 0x147 - (cartridge type) -> MBC type
    ("rom_size", 'B'),           # 0x148 - (ROM size) -> Memory Bank count can be calculated
    ("ram_size", 'B'),           # 0x149 - (RAM size)
    ("destination_code", "B"),   # 0x14A - (destination code)
    ("old_license_code", 'B'),   # 0x14B - (old license code)
    ("mask_rom_version", 'B'),   # 0x14C - (mask rom version)
    ("header_checksum", 'B'),    # 0x14D - (header checksum)
    ("global_checksum", 'H')     # 0x14E - (global checksum)
]

# reads the cartridge metadata byte range from a byte buffer (the gameboy game) and returns it as a named tuple of 'field_name' : 'content_as_bytes'
def get_cartridge_header(cartridge_rom_as_bytestream, read_offset: int = 0x100):
    
    # Creates a string with instruction for 'struct.unpack_from' on how to slice the bytes into an array
    CARTRIDGE_HEADER_SLICE_MAP = "".join(format_type for _, format_type in HEADER_FIELDS)

    # Unpacks the cartridge metadata from 'buffer' at 'offset' and r
    byte_representation = struct.unpack_from(CARTRIDGE_HEADER_SLICE_MAP, cartridge_rom_as_bytestream, offset=read_offset)

    # Prepare the named tuple with field names
    CARTRIDGE_METADATA_MAP = namedtuple("CartridgeMetadata", [field_name for field_name, _ in HEADER_FIELDS if field_name is not None])

    # insert the read metadata bytes in the prepared named tuple set
    metadata = CARTRIDGE_METADATA_MAP._make(byte_representation)

    # returns a Cartridge Metadata object
    return metadata