from dataclasses import dataclass
from typing import Literal

@dataclass()
class Operand:

    name: str
    immediate: bool
    bytes: int = 0
    value: int | None = None
    adjust: Literal["+", "-"] | None = None

    def __init__(self, name: str, immediate: bool, bytes: int = 0, increment: bool = False, decrement: bool = False):
        self.name = name
        self.immediate = immediate
        self.bytes = bytes
        if(increment):
            self.adjust = '+'
        if(decrement):
            self.adjust = '-'
    

    def set_value(self, value):
        value = value

    # create is meant to be run at runtime as a kind of pseuda update for this one instance?!
    def create(self, new_value):
        return Operand(
            immediate = self.immediate,
            name = self.name,
            bytes= self.bytes,
            value = new_value,
            adjust = self.adjust
        )

    def pretty_string(self):
        return "Name: " + self.name + " Value: " + str(self.value) + "\n" + "Immediate: " + str(self.immediate) + " Bytes: " + str(self.bytes) + " Adjust: " + str(self.adjust)

@dataclass(frozen=True, eq=True)
class Flags:

    # "-": flag will not be set
    # "0": reset after the instruction 
    # "1": flag is set 
    # "Z","N", "H", "C": effected as expected by it's function 
    Z: Literal["Z", "-", "0", "1"]
    N: Literal["N", "-", "0", "1"]
    H: Literal["H", "-", "0", "1"]
    C: Literal["C", "-", "0", "1"]

    def pretty_string(self):
        return "Z: [" + self.Z + "] N: [" + self.N + "] H: [" + self.H + "] C: [" + self.C + "]"

@dataclass()
class Instruction:

    opcode: int
    immediate: bool
    bytes: int
    mnemonic: str
    operands: list[Operand] 
    cycles: list[int]
    flags: Flags
    comment: str = ""

    # update the flags and Operands to actually become the class and not the initialized dictionary - might not work with frozen...
    def __post_init__(self):
        # parse the flags string as argument into the Flags dc and resign it to self
        self.flags = Flags(**self.flags)
        
        # temporary list for the newly created operands
        tmp_operands: list[Operand] = []
        # read each Operand string and parse it into an Operand dc
        for operand in self.operands:
            # print(operand)
            # print("\n")
            tmp_operands.append(Operand(**operand))
        # reassign the self operands
        self.operands = tmp_operands

    def update_operands(self, operands):
        operands = operands,


    # create is meant to be run at runtime as a kind of pseuda update for this one instance with actual operand values? 
    def create(self, operands):
        return Instruction(
            opcode = self.opcode,
            immediate = self.immediate,
            operands = operands,
            cycles = self.cycles,
            bytes = self.bytes,
            mnemonic = self.mnemonic,
            flags = self.flags,
            comment = self.comment
        )

    def pretty_string(self):

        operand_string = ""

        for op in self.operands:

            operand_string += op.pretty_string() + "\n"

        return "Mnemonic: " + self.mnemonic + " - " + "Opcode: " + self.opcode + "\n" + operand_string + "Immediate: " + str(self.immediate )+ " - Cycles: " + str(self.cycles)[1:-1] + " Bytes: " + str(self.bytes) + "\n" + "Flags: " + self.flags.pretty_string() + "\n" + "Comments: " + self.comment + "\n"