from pathlib import Path
import sys
from hypothesis import given
import hypothesis.strategies as st

from gbemu.cartridge.cartdrige import read_cartridge_metadata

# Define parameters for hypothesis to create random test data
HEADER_START = 0x100
HEADER_END = 0x14F

# Header size as measured from the last element to the first + 1 (+1 because its a size of indexes and not a pointing number)
HEADER_SIZE = (HEADER_END - HEADER_START)+1

# Generates random binary data for testing
# The size of bynary array is exactly until HEADER_END +1 so that a header read out can be simulated
@given (data = st.binary(min_size = HEADER_SIZE + HEADER_START, max_size = HEADER_SIZE + HEADER_START))
def test_read_random_header_data(data):

    # read a part of the iven data, default read one byte
    def read(offset, count = 1):

        # hows the stuff in the bracket working?
        # The test itself features read(), a helper function that reads count number of bytes from offset. -> this is wrong I guess, cause index o.o. bound error at last read Note that we need to add +1 because if offset = count = 1 then data[1:1] == ''.
        return data[offset : offset + count]

    # Only tests weather the data was correctly read and parsed into the metadata tuple
    metadata = read_cartridge_metadata(data)
    assert metadata.title == read(0x134, 14)
    checksum = read(0x14E, 2)
    assert metadata.global_checksum == int.from_bytes(checksum, sys.byteorder) 
    

test_read_random_header_data()

# Test function with snake.gb to assert against known values
p = Path('/home/photon/Workspace/Projects/GBEmu/snake.gb')
print(read_cartridge_metadata(p.read_bytes()))