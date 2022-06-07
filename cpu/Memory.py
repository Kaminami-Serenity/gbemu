from collections import namedtuple
from pathlib import Path
from core.Cartridge import get_cartridge_header


class Memory:

    # Cartridge parsed header
    header: namedtuple


    # Cache MBC-Type for write queries
    mbc_type: int 
    # Cartridge rom as memory banks
    rom_banks: dict[int, bytes]
    # index of currently chosen rom bank
    rom_bank_pointer: int 

    # RAM on Cartridge - Always maximum possible ram provided, even if not needed, as adressing should work anyhow
    ext_ram: dict[int, bytearray]  = {}
    # index of currently chosen ram block
    ram_block_pointer: int 
    # Boolean switch wether I/O to Ram is currently active TODO: Necessary to be emulated?
    ram_access_on: bool = False       # If writing 0xXA to addressspace 0x0000 - 0x1FFF: switch RAM access mode on 
    
    # Tracks wether the GB is on ROM or RAM mode TODO: Necessary to actually track in Emulator?
    mbc_rom_ram_mode: int = 0     # On MBC1 there are two modes: 16Mb ROM / 8 KB RAM or 4MB ROM / 32KB RAM The game is able to switch between these on the fly # 0 == ROM Mode / 1 == RAM Mode


    int_ram: bytearray = bytearray(8192)  # 0xE000 - 0xFE00 or C000 - DF00 as Echo :  8 kiB Address range data - type RAM
                   
    
    
    def init_memory(self, cartridge_path:str):

        # Read cartridge data
        cartridge_as_bytes = Path(cartridge_path).read_bytes()
        # print("Size of loaded cartdridge is: ", cartridge_as_bytes.__len__(),"bytes")

        # Parse header
        header = get_cartridge_header(cartridge_as_bytes)
        # print(header)

        # Create ROM-Banks and fill with cartridge data
        mb_count = get_memory_bank_count(header.rom_size)
        # print("ROM Bank count: ", mb_count, "mbc mode:", header.mbc_type)
        self.rom_banks = slice_cartridge_into_mbc(cartridge_as_bytes, mb_count)

        # Create RAM 16 blocks of 8kib
        for ram_block in range(16):
            self.ext_ram[ram_block] = bytearray(8192)

        self.mbc_type = get_mbc_settings(header.mbc_type)

        return self



    def read(self, address):

        # Address range $0000 - $3FFF - Default bank 0
        if(int('0x0000', base=16) <= address <= int('0x3FFF', base=16)):
            return self.rom_banks.get(0)[address : address +1]

        # Address range $4000 - $7FFF - Default bank 1
        elif(int('0x4000', base=16) <= address <= int('0x7FFF', base=16)):
            return self.rom_banks.get(self.rom_bank_pointer)[address : address +1]

        # Address range $A000 - $BFFF - Default external RAM
        elif(int('0xA000', base=16) <= address <= int('0xBFFF', base=16)):
            return self.ext_ram.get(self.ram_block_pointer)[address : address +1]

        # Read from internal ram | Write to internal ram (echo)
        elif(int('0E0000', base=16) <= address <= int('0xFE00', base=16) | int('0C0000', base=16) <= address <= int('0xDF00', base=16)):
            return self.int_ram[address : address +1]


    # Write needs to check a lot of stuff
    def write(self, address: int, content: bytes):

        # MBC 5 specific write instructions
        if(self.mbc_type == 5):
            
            # Write try to rom -> set rom bank pointer (lower)
            if(int('0x2000', base=16) <= address <= int('0x2FFF', base=16)):
                rom_bank_pointer = int(content)
            
            # Write try to rom -> set rom bank pointer (upper bit)
            elif(int('0x2000', base=16) <= address <= int('0x2FFF', base=16)):
                content = content << 7
                content = content >> 7
                if(content == 0b1):
                    rom_bank_pointer * rom_bank_pointer * 2
                # rom_bank_pointer = int(bytes) -> take lowest bit and add to rom_bank_pointer as 9. th bit

            # Write try to rom -> set ram block pointer (upper bit)
            elif(int('0x4000', base=16) <= address <= int('0x5FFF', base=16)):
                # ram_block_pointer = (bytes) lower 4 bits to int, upper bits ignore -> to mask to zero
                content = content << 4
                content = content >> 4
                ram_block_pointer = int(content)

            # Write to internal ram | Write to internal ram (echo)
            elif(int('0E0000', base=16) <= address <= int('0xFE00', base=16) | int('0C0000', base=16) <= address <= int('0xDF00', base=16)):
                pass

            # Write to external RAM
            elif(int('0A0000', base=16) <= address <= int('0xBFFF', base=16)):
                pass







        ##########################################################################
        # Check if intercept is necessary:
            # If Address is between $0xxx - $1xxx and content: $xA -> enable RAM access
            # If Address is between $0xxx - $1xxx and content is not: $xA -> disable RAM access
        if(0 <= address <= int('0x1FFF', base=16) ):
            
            if(content.hex().endswith('A')):
                self.ram_access_mode = True
            else:
                self.ram_access_mode = False


        # Switch rom bank (lower bits)
        if(int('0x2000', base=16) <= address <= int('0x3FFF', base=16) ):
            # choosing the lower five bits of rom bank number 
            # writing $00, $20, $40, $60 will be switched to $01, $21, $41, and $61
            # this makes the ranges 20, 40, 60 unaccessable
            pass

        # Switch rom bank (upper bits)
        if(int('0x4000', base=16) <= address <= int('0x5FFF', base=16) ):
            # effects ROM and RAM Modes. First two bits of content are used
            # IF ROM Mode (0) -> Two bits specify upper two bank number. Only RAM bank $00 can be used
            # If RAM Mode (1) -> specifies which RAM banks are loaded to $A000 - $BFFF. Only ROM bank $00 - $1F can be used
            pass

        # Switch variable ROM/RAM mode
        if(int('0x6000', base=16) <= address <= int('0x7FFF', base=16) ):
            
            # Writing $00 (ROM) or $01 (RAM) will select the ROM/RAM mode
            if(content == bytes.fromhex("0x00")):
                rom_ram_mode = 0
            elif(content == bytes.fromhex("0x01")):
                rom_ram_mode = 1


def get_memory_bank_count(rom_size_value: int):
    # ROM Size and amount of banks

    if(rom_size_value == int('0x00', base = 16)):
        # 32kB (0 banks)
        return 0 

    elif(rom_size_value == int('0x01', base = 16)):
        # 64kB (4 banks)
        return 4 

    elif(rom_size_value == int('0x02', base = 16)):
        # 128kB (8 banks)
        return 8

    elif(rom_size_value == int('0x03', base = 16)):
        # 256kB (16 banks)
        return 16

    elif(rom_size_value == int('0x04', base = 16)):
        # 512kB (32 banks)
        return 32

    elif(rom_size_value == int('0x05', base = 16)):
        # 1MB (64 banks)
        return 64 

    elif(rom_size_value == int('0x06', base = 16)):
        # 2MB (128 banks)
        return 128

    elif(rom_size_value == int('0x07', base = 16)):
        # 4MB (256 banks)
        return 256   

    elif(rom_size_value == int('0x52', base = 16)):
        # 1,1MB (72 banks)
        return 72   

    elif(rom_size_value == int('0x53', base = 16)):
        # 1,2MB (80 banks)
        return 80   

    elif(rom_size_value == int('0x54', base = 16)):
        # 1,5MB (96 banks)
        return 96                       

def slice_cartridge_into_mbc(cartridge: bytes, mb_count: int):

    BANK_SIZE_IN_BYTES = 16384
    rom_banks: dict[int, bytes] = {}

    if(mb_count == 0):
        rom_banks[0] = cartridge[0 : 16384]
        rom_banks[1] = cartridge[16384 : 32768]

    else: 
        for slice in range(mb_count):

            rom_banks[slice] = cartridge[BANK_SIZE_IN_BYTES * slice : BANK_SIZE_IN_BYTES * slice + BANK_SIZE_IN_BYTES]

    return rom_banks

# TODO Implement other MBC Types
def get_mbc_settings(mbc_mode):

        # switch on mbc code
    if(mbc_mode == int('0x00', base = 16)):
        # 32KiB module, no mbc
        return 0, False, False

    elif(mbc_mode == int('0x01', base = 16)):
        # MBC 1
        pass 

    elif(mbc_mode == int('0x02', base = 16)):
        # MBC 1 + RAM
        pass 

    elif(mbc_mode == int('0x03', base = 16)):
        # MBC 1 + RAM + BAT
        pass 

    elif(mbc_mode == int('0x05', base = 16)):
        # MBC 2
        pass 

    elif(mbc_mode == int('0x06', base = 16)):
        # MBC 2 + BAT
        pass   

    elif(mbc_mode == int('0x08', base = 16)):
        # ROM + RAM
        pass  

    elif(mbc_mode == int('0x09', base = 16)):
        # ROM + RAM + BAT
        pass 

    elif(mbc_mode == int('0x0F', base = 16)):
        # MBC 3 + Timer + BAT
        pass 

    elif(mbc_mode == int('0x15', base = 16)):
        # MBC 4
        pass 

    elif(mbc_mode == int('0x16', base = 16)):
        # MBC 4 + RAM 
        pass 
        
    elif(mbc_mode == int('0x17', base = 16)):
        # MBC 4 + RAM + BAT
        pass 

    elif(mbc_mode == int('0x19', base = 16)):
        # MBC 5 
        return 5, False, False

    elif(mbc_mode == int('0x1A', base = 16)):
        # MBC 5 + RAM
        pass 

    elif(mbc_mode == int('0x1B', base = 16)):
        # MBC 5 + RAM + BAT
        pass 
