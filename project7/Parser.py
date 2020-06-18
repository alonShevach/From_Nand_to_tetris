SPACE = " "
COMMENT = "//"
NEW_LINE = "\n"
NEW_LINE_W = "\r"
READ = "r"


def read_file(filename, instructions):
    """
    Parses the file by sections - reads each line, and if it is not a comment line
    or an empty line it splits it into sections and appends it to the instructions list
    :param instructions: a list which holds the separated instructions
    :param filename: the name of the file
    """
    f = open(filename, READ)
    lines = f.readlines()
    for line in lines:
        line, sep, leftover = line.partition(COMMENT)
        line, sep, leftover = line.partition(NEW_LINE)
        line, sep, leftover = line.partition(NEW_LINE_W)
        line = line.strip()
        if len(line) > 0:
            instructions.append(line.split(SPACE))
    f.close()

""
