from pathlib import Path

import pytest

from cpu.decoding.decoder import Decoder
from cpu.instruction.instructionclasses import Instruction


#@pytest.fixture
def make_decoder(data: bytes, address: int = 0):
    
    return Decoder.create(data = data, address = address)
            


def test_decoder_nop_instruction(make_decoder):
    decoder = make_decoder(data = bytes.fromhex('00'))
    new_address, instruction = decoder.decode(0x0)
    assert new_address == 0x1, 'Address wrong after decode'
    assert instruction == Instruction()


