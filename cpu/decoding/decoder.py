from dataclasses import dataclass
import sys
from cpu.instruction.instructionset import load_opcodes


@dataclass
class Decoder:
    
    
    prefixed_instructions: dict
    unprefixed_instructions: dict
    data: bytes
    address: int

    # Something like a constructor to instantiate the class as an object with actual values
    # @data: this should be the GB cartdridge ROM data
    # @address: the first address to read on the ROM, can also be manipulated in the read function, so 0 is fine to init
    @classmethod
    def create(cls, data:bytes, address: int = 0):
        
        unprefixed_instructions, prefixed_instructions = load_opcodes()

        return cls(
            # TODO: is it necessary to give the class the dictionary after assigning them earlier?
            unprefixed_instructions,
            prefixed_instructions,
            data,
            address
        )

    # Reads a 'count' amount of byte(s) from the data at given address
    # Should only be used by the function decode
    def read(self, address: int, count: int = 1):

        if 0 <= address+count <= len(self.data):
            cache: bytes = self.data[address : address+count]
            return hex(int.from_bytes(cache, sys.byteorder))

        else:
            raise IndexError(f'{address=}+{count=} is out of range')

    # Decodes the next instruction at address. Returns the Instruction with optional operands
    def decode(self, address: int):
        
        opcode = None
        decoded_instruction = None
        new_operands = []

        opcode= self.read(address)
        address += 1

        # Switch on 0xCB Instruction to prefix instruction set
        if opcode == 0xCB:
            opcode = self.read(address)
            address +=1
            instruction = self.prefixed_instructions[opcode]
        else:
            instruction = self.unprefixed_instructions[opcode]

        
        # Now collect operands and read eventual values from ROM
        for operand in instruction.operands:
            if operand.bytes is not None:
                value = self.read(address, operand.bytes)
                address += operand.bytes
                new_operands.append(operand.copy(value))

            else: 
                new_operands.append(operand)

        # Create the complete Instruction with operands and actual values
        decoded_instruction = instruction.copy(operands=new_operands)

        # Return current address pointer value and the Instruction
        return address, decoded_instruction

