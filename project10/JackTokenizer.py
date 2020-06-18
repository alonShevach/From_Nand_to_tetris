import re

# constants:
OUT_COMMENT_END = "*/"
COMMENT_SUFFIX = '/'
COMMENT_PREFIX = '*'
QUOT = "\""
EMPTY = ""
READ = "r"
IN_COMMENT = "//"
OUT_COMMENT_BEGIN = "/**"
REGEX = r"\w+|\(|\)|\[|\]|{|}|<|>|-|\+|=|,|;|~|\".*\"|&|\*|\/|\.|\|"
KEY_WORD = "keyword"
SYMBOL = "symbol"
IDENTIFIER = "identifier"
INT_CONST = "integerConstant"
STR_CONST = "stringConstant"


class JackTokenizer:
    """
    The JackTokenizer class which ignores empty lines and comments and separates the file into tokens
    """
    unary_ops = ['~', '-']

    op_set = {'+', '-', '*', '/', '&', '|', '<', '>', '='}

    keyword_set = {'class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean',
                   'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return'}

    symbol_dict = {
        '{': "{", '}': '}', '(': '(', ')': ')', '[': '[', ']': ']', '.': '.', ',': ',', ';': ';', '+': '+',
        '-': '-', '*': '*', '/': '/', '&': '&amp;', '|': '|', '<': '&lt;', '>': "&gt;", '=': '=', '~': '~',
        '"': "&quot;"
    }

    def __init__(self, path):
        """
        Constructor of the JackTokenizer class
        :param path: the path of the jack file
        """
        f = open(path, READ)
        self.lines = f.readlines()
        f.close()
        self.tokens = []
        self.current_index = 0
        self.read_file()
        self.current = self.tokens[0]  # updates the current token to be the first one

    def dispose_comments(self, line_num):
        """
        Responsible for ignoring the outer comments
        :param line_num: the index of the current line
        :return: the line and letter index
        """
        for i in range(line_num, len(self.lines)):
            for j in range(len(self.lines[i]) - 1):
                if self.lines[i][j] == COMMENT_PREFIX and self.lines[i][j + 1] == COMMENT_SUFFIX:
                    return i, j

    def read_file(self):
        """
        Reads the file by line - ignores the empty lines and comments and separates the
        file into tokens
        :return: None
        """
        line_index = None
        inline_index = None
        for i, line in enumerate(self.lines):
            if line_index is not None and inline_index is not None:
                if line_index > i:
                    continue
                if line_index == i:
                    prefix, sep, line = line.partition(OUT_COMMENT_END)
            line, sep, tail = line.partition(IN_COMMENT)
            line, sep, tail = line.partition(OUT_COMMENT_BEGIN)
            line = line.strip()
            if sep == OUT_COMMENT_BEGIN and line == EMPTY:
                line_index, inline_index = self.dispose_comments(i)
            line = line.strip()
            if line == EMPTY:
                continue
            self.tokens += re.findall(REGEX, line)

    def go_back(self):
        """
        Returns to the previous token
        :return: None
        """
        if self.current_index > 0:
            self.current_index -= 1
            self.current = self.tokens[self.current_index]

    def has_more_tokens(self):
        """
        Checks if there is more tokens
        :return: True if there are more tokens, False otherwise
        """
        return self.current_index < len(self.tokens) - 1

    def advance(self):
        """
        Advances the current token if there are more tokens
        :return: the current token
        """
        if self.has_more_tokens():
            self.current_index += 1
            self.current = self.tokens[self.current_index]
            return self.tokens[self.current_index]

    def token_type(self):
        """
        Returns the type of the current token
        :return: the type of the current token
        """
        if self.current in self.keyword_set:
            return KEY_WORD
        elif self.current in self.symbol_dict:
            return SYMBOL
        elif self.current.isdigit():
            return INT_CONST
        elif self.current[0] == QUOT:
            return STR_CONST
        else:
            return IDENTIFIER

    def keyword(self):
        """
        Returns the current token if it is a keyword
        :return: the current token if it is a keyword
        """
        return self.current

    def symbol(self):
        """
        Returns the current token if it is a symbol
        :return: the current token if it is a symbol
        """
        return self.symbol_dict[self.current]

    def identifier(self):
        """
        Returns the current token if it is an identifier
        :return: the current token if it is an identifier
        """
        return self.current

    def int_val(self):
        """
        Returns the current token if it is an integer constant
        :return: the current token if it is an integer constant
        """
        return self.current

    def string_val(self):
        """
        Returns the current token if it is a string constant
        :return: the current token if it is a string constant
        """
        return self.current[1:-1]
