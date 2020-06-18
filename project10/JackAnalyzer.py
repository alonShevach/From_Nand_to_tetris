from CompilationEngine import CompilationEngine
import os
import sys

# constants:
NUM_OF_ARGS = 2
FILE_SEPARATOR = "/"
JACK_SUFFIX = ".jack"
WRONG_NUM_OF_ARGS = "Wrong number of arguments"
XML_SUFFIX = ".xml"


def main():
    """
    The main function which runs the entire program
    :return: None
    """
    if len(sys.argv) != NUM_OF_ARGS:
        sys.exit(WRONG_NUM_OF_ARGS)
    else:
        path = sys.argv[1]
    if os.path.isdir(path):  # in case the path is of a directory
        for file_name in os.listdir(path):
            if file_name.endswith(JACK_SUFFIX):
                class_writer = CompilationEngine(path + FILE_SEPARATOR + file_name,
                                                 path + FILE_SEPARATOR + file_name[:-5] + XML_SUFFIX)
                class_writer.compile_class()
                class_writer.write_output_file()
    elif os.path.isfile(path):  # in case the path is of a single file
        class_writer = CompilationEngine(path, path[:-5] + XML_SUFFIX)
        class_writer.compile_class()
        class_writer.write_output_file()


if __name__ == "__main__":
    main()
