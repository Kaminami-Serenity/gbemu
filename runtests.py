import pathlib

from cairo import Path
from tests.decoder_test import make_decoder, test_decoder_nop_instruction
from tests.header_test import test_header_with_gb_module, test_read_random_header_data
from tests.opcodes_test import test_instructionset


# This file calls all test functions in an orderly fashion

# Test import of Instructionset
test_instructionset()

#Test header metadata reader
test_read_random_header_data()
snake_gb_path = '/home/photon/Workspace/Projects/Git_Repo_GBEmu/local_test_games/snake.gb'
test_header_with_gb_module(snake_gb_path)

# Test instruction decoder
test_decoder_nop_instruction(make_decoder)