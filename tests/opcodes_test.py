from cpu.instruction.instructionset import load_opcodes
from cpu.instruction.instructionclasses import Instruction

# Creat the two dictionaries
def test_instructionset():

    instructionset_unprefixed: dict[str, Instruction]
    instructionset_prefixed: dict[str, Instruction]
    instructionset_unprefixed, instructionset_prefixed = load_opcodes()

    print("Instructionset unprefixed:")
    for code in instructionset_unprefixed:
        print(instructionset_unprefixed[code].pretty_string() + "\n")

    print("Instructionset prefixed:")
    for code in instructionset_prefixed:
        print(instructionset_prefixed[code].pretty_string() + "\n")

    assert instructionset_unprefixed.__len__() + instructionset_prefixed.__len__() == 512

    

