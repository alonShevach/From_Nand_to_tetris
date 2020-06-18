# Consts:
DOT = "."
POINTER_BEGIN = 3
TEMP_BEGIN = 5
ONE_VAL_PREFIX = "@SP\nA=M-1\n"
TWO_VALS_PREFIX = ONE_VAL_PREFIX + "D=M\n@SP\nA=M-1\nA=A-1\n"
TWO_VALS_SUFFIX = "@SP\nM=M-1\n"
COMPARE_SUFFIX = "(TRUE%s)\n@SP\nA=M-1\nA=A-1\n" \
                "M=-1\n@END%s\n0;JMP\n(FALSE%s)\n@SP\nA=M-1\nA=A-1" \
                 "\nM=0\n@END%s\n0;JMP\n(END%s)\n" + TWO_VALS_SUFFIX
ADD = "M=D+M\n"
SUB = "M=M-D\n"
NEG = "M=-M\n"
EQ = "D=M-D\n@TRUE%s\nD;JEQ\n@FALSE%s\n0;JMP\n"
GT = "@SP\nA=M-1\nD=M\n@Y_GREATER%s\nD;JGE\n@Y_SMALLER%s\n0;JMP\n(" \
     "Y_GREATER%s)\n@SP\nA=M-1\nA=A-1\nD=M\n@COMPARE%s\nD;JGE\n@FALSE%s\n0;JMP\n(" \
     "COMPARE%s)\n@SP\nA=M-1\nA=A-1\nD=M\n@SP\nA=M-1\nD=D-M\n@TRUE%s\nD;JGT\n@FALSE%s\n0;JMP\n(" \
     "FALSE%s)\n@SP\nA=M-1\nA=A-1\nM=0\n@END%s\n0;JMP\n(TRUE%s)\n@SP\nA=M-1\nA=A-1\nM=-1\n@END%s\n0;JMP\n(" \
     "Y_SMALLER%s)\n@SP\nA=M-1\nA=A-1\nD=M\n@TRUE%s\nD;JGE\n@COMPARE%s\n0;JMP\n(END%s)\n "
LT = "@SP\nA=M-1\nD=M\n@Y_GREATER%s\nD;JGE\n@Y_SMALLER%s\n0;JMP\n(" \
     "Y_GREATER%s)\n@SP\nA=M-1\nA=A-1\nD=M\n@COMPARE%s\nD;JGE\n@TRUE%s\n0;JMP\n(" \
     "COMPARE%s)\n@SP\nA=M-1\nA=A-1\nD=M\n@SP\nA=M-1\nD=D-M\n@TRUE%s\nD;JLT\n@FALSE%s\n0;JMP\n(" \
     "FALSE%s)\n@SP\nA=M-1\nA=A-1\nM=0\n@END%s\n0;JMP\n(TRUE%s)\n@SP\nA=M-1\nA=A-1\nM=-1\n@END%s\n0;JMP\n(" \
     "Y_SMALLER%s)\n@SP\nA=M-1\nA=A-1\nD=M\n@FALSE%s\nD;JGE\n@COMPARE%s\n0;JMP\n(END%s)\n "
AND = "M=D&M\n"
OR = "M=D|M\n"
NOT = "M=!M\n"
PUSH = "@%s\nD=M\n@%s\nA=D+A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
SPECIAL_PUSH = "@%s\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
CONSTANT_PUSH = "@%s\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
POP = "@%s\nD=M\n@%s\nD=D+A\n@R15\nM=D\n@SP\nA=M-1\nD=M\n@R15\nA=M\nM=D\n" + TWO_VALS_SUFFIX
SPECIAL_POP = "@SP\nA=M-1\nD=M\n@%s\nM=D\n" + TWO_VALS_SUFFIX
COND_JMP = "@SP\nAM=M-1\nD=M\n@%s$%s\nD;JNE\n"
UNCOND_JMP = "@%s$%s\n0;JMP\n"
NEW_LABEL = "(%s$%s)\n"
LCL_UPDATE = "@SP\nD=M\n@LCL\nM=D\n"
ARG_UPDATE = "@SP\nD=M\n@5\nD=D-A\n@%s\nD=D-A\n@ARG\nM=D\n"
FUNC_JMP = "@%s\n0;JMP\n"
INIT_FUNC = "Sys.init"
INIT = "@256\nD=A\n@SP\nM=D\n"
RETURN_JMP = "@R14\nA=M\n0;JMP\n"
SP_TO_ARG = "@ARG\nD=M+1\n@SP\nM=D\n"
REDIRECT_ADDRESS = "@%s\nD=M\n@R13\nM=D\n@%s\nA=D-A\nD=M\n@R14\nM=D\n"
FUNC_LABEL = "(%s)\n"
REFACTOR = "@R13\nAM=M-1\nD=M\n@%s\nM=D\n"

# Commands:
C_ARG = "argument"
C_LOCAL = "local"
C_STATIC = "static"
C_CONST = "constant"
C_THIS = "this"
C_THAT = "that"
C_POINTER = "pointer"
C_TEMP = "temp"
C_ADD = "add"
C_SUB = "sub"
C_NEG = "neg"
C_EQ = "eq"
C_GT = "gt"
C_LT = "lt"
C_AND = "and"
C_OR = "or"
C_NOT = "not"
C_PUSH = "push"
C_POP = "pop"
C_LABEL = "label"
C_GOTO = "goto"
C_IF = "if-goto"
C_FUNCTION = "function"
C_RETURN = "return"
C_CALL = "call"
UNCONDITIONAL_GOTO = "goto"
CONDITIONAL_GOTO = "if-goto"
RETURN_ADDRESS_LABEL = "return-address_%s"

# Pointers:
P_ARG = "ARG"
P_LOCAL = "LCL"
P_THIS = "THIS"
P_THAT = "THAT"

# Dictionaries:
REG_SEGMENT_DICT = {
    C_ARG: P_ARG,
    C_LOCAL: P_LOCAL,
    C_THIS: P_THIS,
    C_THAT: P_THAT
}

ARITHMETIC_DICT = {
    C_ADD: TWO_VALS_PREFIX + ADD + TWO_VALS_SUFFIX,
    C_SUB: TWO_VALS_PREFIX + SUB + TWO_VALS_SUFFIX,
    C_NEG: ONE_VAL_PREFIX + NEG,
    C_AND: TWO_VALS_PREFIX + AND + TWO_VALS_SUFFIX,
    C_OR: TWO_VALS_PREFIX + OR + TWO_VALS_SUFFIX,
    C_NOT: ONE_VAL_PREFIX + NOT
}

COMPARE_DICT = {
    C_GT: GT + TWO_VALS_SUFFIX,
    C_LT: LT + TWO_VALS_SUFFIX,
    C_EQ: TWO_VALS_PREFIX + EQ + COMPARE_SUFFIX
}

GOTO_DICT = {
    UNCONDITIONAL_GOTO: UNCOND_JMP,
    CONDITIONAL_GOTO: ONE_VAL_PREFIX + COND_JMP
}

def push(file_name, instruction):
    """
    A function that is responsible for the push command.
    :param file_name: The name of the file
    :param instruction: the current instruction to push.
    :return: The translated line according to the instruction.
    """
    output_line = ""
    push_command, seg, i = instruction
    if seg in REG_SEGMENT_DICT:
        output_line += PUSH % (REG_SEGMENT_DICT[seg], i)
    elif seg == C_POINTER:
        output_line += SPECIAL_PUSH % str(POINTER_BEGIN + int(i))
    elif seg == C_TEMP:
        output_line += SPECIAL_PUSH % str(TEMP_BEGIN + int(i))
    elif seg == C_STATIC:
        output_line += SPECIAL_PUSH % (file_name + DOT + i)
    else:
        output_line += CONSTANT_PUSH % i
    return output_line


def pop(file_name, instruction):
    """
    A function that is responsible for the pop command.
    :param file_name: The name of the file
    :param instruction: the current instruction to pop.
    :return: The translated line according to the instruction.
    """
    output_line = ""
    pop_command, seg, i = instruction
    if seg in REG_SEGMENT_DICT:
        output_line += POP % (REG_SEGMENT_DICT[seg], i)
    elif seg == C_POINTER:
        output_line += SPECIAL_POP % str(POINTER_BEGIN + int(i))
    elif seg == C_TEMP:
        output_line += SPECIAL_POP % str(TEMP_BEGIN + int(i))
    else:
        output_line += SPECIAL_POP % (file_name + DOT + i)
    return output_line


def arithmetic(instruction):
    """
    A function that is responsible for the arithmetic commands.
    :param instruction: the current instruction to the arithmetic commands.
    :return: The translated line according to the instruction.
    """
    output_line = ""
    output_line += ARITHMETIC_DICT[instruction[0]]
    return output_line


def compare_arithmetic(instruction, i):
    """
    A function that is responsible for the compare arithmetic commands.
    :param instruction: the current instruction to the compare arithmetic commands.
    :param i: the number of the instruction
    :return: The translated line according to the instruction.
    """
    output_line = ""
    if instruction[0] == C_EQ:
        output_line += COMPARE_DICT[instruction[0]] % (i, i, i, i, i, i, i)
    else:
        output_line += COMPARE_DICT[instruction[0]] % (i, i, i, i, i, i, i, i, i, i, i, i, i, i, i, i)
    return output_line


def new_label(instruction, file_name):
    """
    Creates the line for a new label or a deceleration of a function
    :param instruction: the instruction which declares a new label or function
    :param file_name: the name of the file
    :return: the assembly line
    """
    output_line = ""
    if instruction[0] == C_FUNCTION:
        output_line += FUNC_LABEL % (instruction[1])
        for i in range(int(instruction[2])):
            output_line += CONSTANT_PUSH % 0
    else:
        output_line += NEW_LABEL % (file_name, instruction[1])
    return output_line


def go_to_label(instruction, file_name):
    """
    Responsible to jump in the go-to or if-go-to cases
    :param instruction: the go-to or if-goto instruction
    :param file_name: the name of the file
    :return: The assembley line
    """
    output_line = ""
    output_line += GOTO_DICT[instruction[0]] % (file_name, instruction[1])
    return output_line


def call(instruction, return_index):
    """
    Responsible for the call function instruction
    :param instruction: the instruction to call a function
    :return: the assembly line
    """
    output_line = ""
    output_line += CONSTANT_PUSH % (RETURN_ADDRESS_LABEL % str(return_index))
    output_line += SPECIAL_PUSH % P_LOCAL
    output_line += SPECIAL_PUSH % P_ARG
    output_line += SPECIAL_PUSH % P_THIS
    output_line += SPECIAL_PUSH % P_THAT
    output_line += ARG_UPDATE % instruction[2]
    output_line += LCL_UPDATE
    output_line += FUNC_JMP % (instruction[1])
    output_line += FUNC_LABEL % (RETURN_ADDRESS_LABEL % str(return_index))
    return output_line


def write_return():
    """
    Responsible for return from a function
    :return: the assembly line
    """
    output_line = ""
    output_line += REDIRECT_ADDRESS % (P_LOCAL, str(5))
    output_line += POP % (P_ARG, str(0))
    output_line += SP_TO_ARG
    output_line += REFACTOR % P_THAT
    output_line += REFACTOR % P_THIS
    output_line += REFACTOR % P_ARG
    output_line += REFACTOR % P_LOCAL
    output_line += RETURN_JMP
    return output_line


def bootstrap_code():
    """
    Responsible for the bootstrap code
    :return: the assembly line
    """
    output_line = ""
    output_line += INIT
    init_lst = [C_CALL, INIT_FUNC, 0]
    output_line += call(init_lst, 0)
    return output_line
