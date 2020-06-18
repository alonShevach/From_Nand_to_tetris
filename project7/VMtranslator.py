import os
import sys
import Parser
import CodeWriter

NEWLINE = "\n"
WRONG_NUM_OF_ARGS = "Wrong number of arguments"
NUM_OF_ARGS = 2
SUFFIX = ".vm"
FILE_SEPARATOR = "/"
HACK_ENDING = ".asm"
WRITE = "w"


def write_output_file(path, instructions):
    """
    A function that gets a list of instruction and writes to an output
    file according to the commands.
    :param path: the current file's path.
    :param instructions: the instructions in the given file
    """
    final = ""
    head, file_name = os.path.split(path)
    file_name, vm, tail = file_name.partition(SUFFIX)
    for i in range(len(instructions)):
        if instructions[i][0] == CodeWriter.C_PUSH:
            final += CodeWriter.push(file_name, instructions[i])
        elif instructions[i][0] == CodeWriter.C_POP:
            final += CodeWriter.pop(file_name, instructions[i])
        elif instructions[i][0] in CodeWriter.ARITHMETIC_DICT:
            final += CodeWriter.arithmetic(instructions[i])
        elif instructions[i][0] in CodeWriter.COMPARE_DICT:
            final += CodeWriter.compare_arithmetic(instructions[i], i)
    output_file = open(path[:-3] + HACK_ENDING, WRITE)
    output_file.write(final)
    output_file.close()


def create_single_file(path):
    """
    A function that creates a single file and writes to it
    according to the instructions.
    :param path: the current file's path.
    """
    instructions = []
    Parser.read_file(path, instructions)
    write_output_file(path, instructions)


def main():
    if len(sys.argv) != NUM_OF_ARGS:
        sys.exit(WRONG_NUM_OF_ARGS)
    else:
        path = sys.argv[1]
    if os.path.isdir(path):
        for file_name in os.listdir(path):
            if file_name.endswith(SUFFIX):
                create_single_file(path + FILE_SEPARATOR + file_name)
    elif os.path.isfile(path):
        create_single_file(path)


if __name__ == "__main__":
    main()
