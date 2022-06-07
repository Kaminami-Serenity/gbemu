from pathlib import Path
import sys
from hypothesis import given
import hypothesis.strategies as st

from cartridge.header import get_cartridge_header

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
    metadata = get_cartridge_header(data)
    print(metadata.title)
    print(read(0x134, 14))
    assert metadata.title == read(0x134, 15), 'Metadata of title not matching saved metdata and freshly read'
    checksum = read(0x14E, 2)
    assert metadata.global_checksum == int.from_bytes(checksum, sys.byteorder) , 'global checksum data not the same is freshly read checksum (This not an actual checksum test)'
    

test_read_random_header_data()

# Test function with snake.gb to assert against known values
def test_header_with_gb_module(path: str):
    print(get_cartridge_header(Path(path).read_bytes()))