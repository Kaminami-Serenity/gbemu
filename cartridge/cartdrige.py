from collections import namedtuple
import struct

# A representation format for the cartridge header 
# containing field name and byte length 
FIELDS = [
    (None, "="),                 # Native Endian
    (None, 'xxxx'),              # 0x100 - 0x103 (entry point)
    (None, '48x'),               # 0x104 - 0x133 (Nintendo Logo)
    ("title", '15s'),            # 0x134 - 0x143 (cartridge title)
    ("cgb", 'B'),                # 0x134 (cbg flag)
    ("new_license_code", 'H'),   # 0x144 - 0x145 (new license code)
    ("sgb", 'B'),                # 0x146 (sgb flag)
    ("cartridge_type", 'B'),     # 0x147 (cartridge type)
    ("rom_size", 'B'),           # 0x148 (ROM size)
    ("ram_size", 'B'),           # 0x149 (RAM size)
    ("destination_code", "B"),   # 0x14A (destination code)
    ("old_license_code", 'B'),   # 0x14B (old license code)
    ("mask_rom_version", 'B'),   # 0x14C (mask rom version)
    ("header_checksum", 'B'),    # 0x14D (header checksum)
    ("global_checksum", 'H')     # 0x14E (global checksum)
]

# reads the cartridge metadata byte range from a byte buffer (the gameboy game) and returns it as a named tuple 
# exmple: CartridgeMetadata(title=b"Yvar's GB Snake", cgb=128, new_license_code=0, sgb=0, cartridge_type=0, rom_size=0, ram_size=0, destination_code=1, old_license_code=11520, mask_rom_version=66, header_checksum=222, global_checksum=199)
def read_cartridge_metadata(buffer, offset: int = 0x100):
    
    # Prepare the byte read format for struct.unpack_from. This tells the functions how to break up the read bytes in pieces
    CARTRIDGE_HEADER = "".join(format_type for _, format_type in FIELDS)

    # Unpacks the cartridge metadata from 'buffer' at 'offset' and r
    data = struct.unpack_from(CARTRIDGE_HEADER, buffer, offset=offset)

    # Prepare the named tuple with field names
    CARTRIDGE_METADATA = namedtuple("CartridgeMetadata", [field_name for field_name, _ in FIELDS if field_name is not None])

    # insert the read metadata bytes in the prepared named tuple set
    metadata = CARTRIDGE_METADATA._make(data)

    # returns a Cartridge Metadata object
    return metadata
