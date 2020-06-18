import os
import sys
import Parser
import CodeWriter

ADD = "a"
NEWLINE = "\n"
WRONG_NUM_OF_ARGS = "Wrong number of arguments"
NUM_OF_ARGS = 2
SUFFIX = ".vm"
FILE_SEPARATOR = "/"
HACK_ENDING = ".asm"
WRITE = "w"


def write_output_file(path, instructions, dir_path, is_first_file, return_index):
    """
    A function that gets a list of instruction and writes to an output
    file according to the commands.
    :param path: the current file's path.
    :param instructions: the instructions in the given file
    :param dir_path: the path of the directory
    :param is_first_file: a boolean value which represents if the file is the first in the directory
    :param return_index: the return index
    :return: the return index
    """
    final = ""
    head, file_name = os.path.split(path)
    file_name, vm, tail = file_name.partition(SUFFIX)
    if is_first_file:
        final += CodeWriter.bootstrap_code()
        return_index += 1
    for i in range(len(instructions)):
        if instructions[i][0] == CodeWriter.C_PUSH:
            final += CodeWriter.push(file_name, instructions[i])
        elif instructions[i][0] == CodeWriter.C_POP:
            final += CodeWriter.pop(file_name, instructions[i])
        elif instructions[i][0] in CodeWriter.ARITHMETIC_DICT:
            final += CodeWriter.arithmetic(instructions[i])
        elif instructions[i][0] in CodeWriter.COMPARE_DICT:
            final += CodeWriter.compare_arithmetic(instructions[i], i)
        elif instructions[i][0] == CodeWriter.C_LABEL or instructions[i][0] == CodeWriter.C_FUNCTION:
            final += CodeWriter.new_label(instructions[i], file_name)
        elif instructions[i][0] in CodeWriter.GOTO_DICT:
            final += CodeWriter.go_to_label(instructions[i], file_name)
        elif instructions[i][0] == CodeWriter.C_CALL:
            final += CodeWriter.call(instructions[i], return_index)
            return_index += 1
        elif instructions[i][0] == CodeWriter.C_RETURN:
            final += CodeWriter.write_return()
    if dir_path is None:
        output_file = open(path[:-3] + HACK_ENDING, WRITE)
    else:
        if is_first_file:
            output_file = open(dir_path + HACK_ENDING, WRITE)
        else:
            output_file = open(dir_path + HACK_ENDING, ADD)
    output_file.write(final)
    output_file.close()
    return return_index

def create_single_file(path, dir_path, is_first_file, return_index):
    """
    A function that creates a single file and writes to it
    according to the instructions.
    :param path: the current file's path.
    :param dir_path: the path of the directory
    :param is_first_file: a boolean value which represents if the file is the first in the directory
    """
    instructions = []
    Parser.read_file(path, instructions)
    return write_output_file(path, instructions, dir_path, is_first_file, return_index)


def main():
    if len(sys.argv) != NUM_OF_ARGS:
        sys.exit(WRONG_NUM_OF_ARGS)
    else:
        path = sys.argv[1]
    if os.path.isdir(path):
        split_path = path.split(FILE_SEPARATOR)
        dir_name = split_path[-1]
        is_first_file = True
        return_index = 0
        for file_name in os.listdir(path):
            if file_name.endswith(SUFFIX):
                return_index += create_single_file(path + FILE_SEPARATOR + file_name, path +
                                                   FILE_SEPARATOR + dir_name, is_first_file, return_index)
                is_first_file = False
    elif os.path.isfile(path):
        create_single_file(path, None, None, 0)


if __name__ == "__main__":
    main()
