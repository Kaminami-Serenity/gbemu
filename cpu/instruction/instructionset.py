import json
from instructionclasses import Instruction

# Hard path to the json file of opcodes
PATH_OPCODES_JSON = 'Opcodes.json'

# Load opcodes.json file -> Parse into dataclasses -> return two dictionaries, one for unprefixed instructions and one for prefixed instructions
def instantiate_opcodes():

    # Load the opcdoes from json file
    opcodes_json = open(PATH_OPCODES_JSON, 'r')
    opcodes_dict = json.load(opcodes_json)
    # print(opcodes_dict)

    # Split json into unprefixed and prefixed 
    unprefixed_opcodes = opcodes_dict.get("unprefixed")
    prefixed_opcodes_json = opcodes_dict.get("prefixed")
 
    # prepare the two dictionaries that will be returned
    instructions_unprefixed = dict[{str, Instruction}]
    instructions_prefixed = dict[{str, Instruction}]

    # Parse the json data into Instruction class and save in prepared dictionary
    for key in unprefixed_opcodes:

        # add the opcode signature to the value set so it can be included in the Instruction values
        unprefixed_opcodes.get(key).update({'opcode' : key})

        #print(unprefixed_codes.get(key))

        # Instantiate and parse this instruction
        instruction_tmp = Instruction(**unprefixed_opcodes.get(key))
        instructions_unprefixed.update({key : instruction_tmp})
        

        # for k in instructions_unprefixed:
        #     print(instructions_unprefixed.get(k).pretty_string())

        return instructions_unprefixed, instructions_prefixed
