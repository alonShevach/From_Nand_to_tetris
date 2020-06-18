class VMWriter:
    """
    This class responsible for the translation to the vm language
    """

    WRITE = "w"
    KEYWORD_DICT = {"true", "false", "null"}

    def __init__(self, output_stream):
        """
        The constructor od the VMWriter class
        :param output_stream: the path of the output stream
        """
        self.output = open(output_stream, self.WRITE)

    def write_push(self, segment, index):
        """
        Writes the push command into the output file
        :param segment: the segment to push the value from
        :param index: the index of the value in the given segment
        :return: None
        """
        self.output.write("push %s %s\n" % (segment, str(index)))

    def write_pop(self, segment, index):
        """
        Writes the pop command into the output file
        :param segment: the segment to pop the value to
        :param index: the index of the value in the given segment
        :return: None
        """
        self.output.write("pop %s %s\n" % (segment, str(index)))

    def write_arithmetic(self, command):
        """
        Writes an arithmetic command to the output file
        :param command: the arithmetic command to write
        :return: None
        """
        self.output.write(command + "\n")

    def write_label(self, label_name):
        """
        Writes a new label to the output file
        :param label_name: the name of the new label
        :return: None
        """
        self.output.write("label %s\n" % label_name)

    def write_goto(self, label_name):
        """
        Writes the goto label command to the output file
        :param label_name: the name of the label to go to
        :return: None
        """
        self.output.write("goto %s\n" % label_name)

    def write_if(self, label_name):
        """
        Writes the if-goto label command to the output file
        :param label_name: the name of the label to go to
        :return: None
        """
        self.output.write("if-goto %s\n" % label_name)

    def write_call(self, func_name, n_args):
        """
        Writes a call to a function command to the output file
        :param func_name: the name of the function
        :param n_args: the number of the arguments of the function
        :return: None
        """
        self.output.write("call %s %s\n" % (func_name, str(n_args)))

    def write_function(self, func_name, n_locals):
        """
        Writes a new function to the output file
        :param func_name: the name of the new function
        :param n_locals: the number of the locals of the function
        :return: None
        """
        self.output.write("function %s %s\n" % (func_name, str(n_locals)))

    def write_return(self):
        """
        Writes the return command to the output file
        :return: None
        """
        self.output.write("return\n")

    def write_push_keyword(self, keyword):
        """
        Writes the push command for a keyword to the output file
        :param keyword: the keyword, String
        :return: None
        """
        if keyword in self.KEYWORD_DICT:
            self.write_push("constant", 0)
            if keyword == "true":
                self.write_arithmetic("not")
        if keyword == "this":
            self.write_push("pointer", 0)

    def close_output(self):
        """
        Closes the output file
        :return: None
        """
        self.output.close()


