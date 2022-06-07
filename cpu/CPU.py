from cpu.Memory import Memory
from cpu.instruction.instructionset import load_opcodes


class CPU():

    # Instructionset register ... the dictionary located here?
    # Maybe make a "Register class" and "RAM" class and combine in here on CPU all three + cartdridge ROM
    # CPU will then be mostly dataclass and having functions for execution of Instruction

    instructions: dict
    instructions_cb: dict

    memory: Memory
    # ???
    AF: int # F is flag register -> realized differently in this emulator, AFAIK 'A' is unused on the gameboy 
    
    # Register BC - r/w
    B: int  #Hi
    C: int  #Lo

    # Register DE r/w
    D: int  #Hi
    E: int  #Lo

    # Register HL ??
    H: int 
    L: int 

    # Stackpointer
    SP: int 

    # Processcounter
    PC: int 

    # Flags
    z: int(1, base=2)   # result of operation == 0
    n: int(1, base=2)   # 1 == former instruction was a subtraction
    h: int(1, base=2)   # Half-Carry flag
    c: int(1, base=2)   # Carry flag

    # RAM / Memory / MBC


    def __init__(self, cartridge_path:str):
        self.instructions, self.instructions_cb = load_opcodes()
        
        self.PC = 0
        
        self.B = 0
        self.C = 0

        self.D = 0
        self.E = 0

        self.memory = Memory().init_memory(cartridge_path:str)

        

