from array import ArrayType
from dataclasses import dataclass
from multiprocessing.sharedctypes import Array
from typing import Literal

@dataclass(frozen=True)
class Operand:

    immediate: bool
    name: str
    bytes: int
    value: int | None
    adjust: Literal["+", "-"] | None

    # create is meant to be run at runtime as a kind of pseuda update for this one instance?!
    def create(self, value):
        return Operand(
            immediate = self.immediate,
            name = self.name,
            bytes= self.bytes,
            value = value,
            adjust = self.adjust
        )

    def pretty_string(self):
        return "Name: " + self.name + " Value: " + self.value + "\n" + "Immediate: " + str(self.immediate) + " Bytes: " + self.bytes + " Adjust: " + self.adjust

@dataclass(frozen=True, eq=True)
class Flags:

    z: Literal["+", "-"]
    n: Literal["+", "-"]
    h: Literal["+", "-"]
    c: Literal["+", "-"]

    def pretty_string(self):
        return "Z: [" + self.z + "] N: [" + self.n + "] H: [" + self.h + "] C: [" + self.c + "]"

@dataclass(frozen=True, eq=True)
class Instruction:

    opcode: int
    immediate: bool
    bytes: int
    mnemonic: str
    operands: list[Operand] 
    cycles: list[int]
    flags: Flags
    comment: str = ""

    # create is meant to be run at runtime as a kind of pseuda update for this one instance with actual operand values? 
    def create(self, operands):
        return Instruction(
            opcode = self.opcode,
            immediate = self.immediate,
            operands = operands,
            cycles = self.cycles,
            bytes = self.bytes,
            mnemonic = self.mnemonic,
            flags = self.flags
        )

    def pretty_string(self):

        operand_string = ""

        #for op in self.operands:

            #operand_string += op.__repr__ + "\n"

        return "Mnemonic: " + self.mnemonic + " - " + "Opcode: " + self.opcode + "\n" + operand_string + "Immediate: " + str(self.immediate )+ "Cycles: " + str(self.cycles)[1:-1] #+ " Bytes: " + bytes + "\n" + "Flags: " + self.flags.pretty_string() + "\n" + "Comments: " + self.comments + "\n"