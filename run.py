from cpu.CPU import CPU

SNAKE_GB_CARTRIDGE = '/home/photon/Workspace/Projects/Git_Repo_GBEmu/local_test_games/snake.gb'
PKM_GB_CARTRIDGE = '/home/photon/Workspace/Projects/Git_Repo_GBEmu/local_test_games/Pokemon - Red Version (USA, Europe).gb'

# There will be no Gameboy bios and ROM check for validity of N-Logo or some such -> streight into action
def start_emulator(path_to_cartridge: str = SNAKE_GB_CARTRIDGE):

# -> Load CPU
    cpu = CPU(**path_to_cartridge)
    # -> TODO: Prepare Instruction set classes
    # -> TODO: Prepare registers
    # -> Done: Load GameBoy cartridge (includes header decode)    
    # -> Done: Prepare MBC and RAM (requires header metadata to identifiy) 


# -> TODO: Graphics, Sound

# -> TODO: Start execution

start_emulator(PKM_GB_CARTRIDGE)

