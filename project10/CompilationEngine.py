from JackTokenizer import JackTokenizer, INT_CONST, STR_CONST

# constants:
WRITE = "w"
CLOSE_ARRAY = ']'
VAR = "var"
OPEN_ARRAY = '['
DOT = '.'
HAS_MORE = ','
CLOSE_TOKEN = '}'
OPEN_TOKEN = '{'
CLOSE_TERM = ')'
OPEN_TERM = '('
EQUAL = '='
END_OF_LINE = ';'
TAB = "  "
KEYWORD_CONSTANT_SET = {"true", "false", "this", "null"}
CLASS_VAR_DEC = {"static", "field"}
CLASS_SUB_DEC = {"method", "function", "constructor"}


class CompilationEngine:
    """
    The CompilationEngine class which compiles each type of token by the jack grammar
    """

    # class constants:
    OPEN_STATEMENT = "<%sStatement>\n"
    CLOSE_STATEMENT = "</%sStatement>\n"
    OPEN = "<%s> "
    CLOSE = " </%s>\n"
    CLOSE_TYPE = "</%s>\n"
    OPEN_TYPE = "<%s>\n"

    def __init__(self, input_file, output_file):
        """
        Constructor of the CompilationEngine class
        :param input_file: the file the JackTokenizer returns
        :param output_file: xml file
        """
        self.input = input_file
        self.output = output_file
        self.tokenizer = JackTokenizer(input_file)
        self.lines = ""
        self.num_of_tabs = 0

    @staticmethod
    def doError():
        """
        A static function which exists the program whenever there is an error
        :return: None
        """
        exit()

    def is_expected(self, expected_val):
        """
        Exists the program if the current token does not equals to the expected token
        :param expected_val: the expected values
        :return: None
        """
        if not self.tokenizer.current == expected_val:
            self.doError()

    def advance_token(self):
        """
        Advances the current token if there are more tokens
        :return: None
        """
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()

    def write_tag(self, val):
        """
        Writes the tag of the current token
        :param val: the values of the current token
        :return: None
        """
        self.lines += TAB * self.num_of_tabs
        self.lines += val

    def write_line(self, tag, val):
        """
        Writes the current tag of a given value with a given tag and advances the current token
        :param tag: the tag of the current value
        :param val: the current token
        :return: None
        """
        self.lines += TAB * self.num_of_tabs
        self.lines += CompilationEngine.OPEN % tag
        self.lines += val
        self.lines += CompilationEngine.CLOSE % tag
        self.advance_token()

    def compile_class(self):
        """
        Compiles a class from the file by the class grammar rules
        :return: None
        """
        token_type = "class"
        self.write_tag(CompilationEngine.OPEN_TYPE % token_type)
        self.num_of_tabs += 1
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes the class
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes the name of the class
        self.is_expected(OPEN_TOKEN)
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes {
        while self.tokenizer.current in CLASS_VAR_DEC:  # compiles the class variants
            self.compile_class_var_dec()
        while self.tokenizer.current in CLASS_SUB_DEC:  # compiles the class subroutines
            self.compile_subroutine()
        self.is_expected(CLOSE_TOKEN)
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes }
        self.num_of_tabs -= 1
        self.write_tag(CompilationEngine.CLOSE_TYPE % token_type)

    def compile_class_var_dec(self):
        """
        Compiles the class variants deceleration by the class variants deceleration grammar rules
        :return: None
        """
        self.compile_var_dec()

    def compile_subroutine(self):
        """
        Compiles the deceleration of function/method/constructor by the subroutine deceleration grammar rules
        :return: None
        """
        out_token_type = "subroutineDec"
        in_token_type = "subroutineBody"
        self.write_tag(CompilationEngine.OPEN_TYPE % out_token_type)
        self.num_of_tabs += 1
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes the type of the subroutine
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes the return type
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes the name of the subroutine
        self.is_expected(OPEN_TERM)
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes (
        self.compile_parameter_list()
        self.is_expected(CLOSE_TERM)
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes )
        self.write_tag(CompilationEngine.OPEN_TYPE % in_token_type)
        self.num_of_tabs += 1
        self.is_expected(OPEN_TOKEN)
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes {
        while self.tokenizer.current == VAR:
            self.compile_var_dec()
        self.compile_statements()
        self.is_expected(CLOSE_TOKEN)
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes }
        self.num_of_tabs -= 1
        self.write_tag(CompilationEngine.CLOSE_TYPE % in_token_type)
        self.num_of_tabs -= 1
        self.write_tag(CompilationEngine.CLOSE_TYPE % out_token_type)

    def compile_call_subroutine(self):
        """
        Compiles the call for a subroutine by the call subroutine grammar rules
        :return: None
        """
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes the name of the subroutine
        if self.tokenizer.current == DOT:
            self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes .
            self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes the name of the subroutine
        self.is_expected(OPEN_TERM)
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes (
        self.compile_expression_list()
        self.is_expected(CLOSE_TERM)
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes )

    def compile_parameter_list(self):
        """
        Compiles the parameter list of a new subroutine by the parameter list grammar rules
        :return: None
        """
        token_type = "parameterList"
        self.write_tag(CompilationEngine.OPEN_TYPE % token_type)
        self.num_of_tabs += 1
        while self.tokenizer.current != CLOSE_TERM:
            self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes the type of the parameter
            self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes the name of the parameter
            if self.tokenizer.current == HAS_MORE:
                self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes ,
        self.num_of_tabs -= 1
        self.write_tag(CompilationEngine.CLOSE_TYPE % token_type)

    def compile_var_dec(self):
        """
        Compiles the variants deceleration of a class or a subroutine by the variants deceleration grammar rules
        :return: None
        """
        token_type = "varDec"
        if not self.tokenizer.current == VAR:
            token_type = "classVarDec"
        self.write_tag(CompilationEngine.OPEN_TYPE % token_type)
        self.num_of_tabs += 1
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes var
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes the type of the var
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes the name of the var
        while self.tokenizer.current == HAS_MORE:
            self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes ,
            self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes the name of the next var
        self.is_expected(END_OF_LINE)
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes ;
        self.num_of_tabs -= 1
        self.write_tag(CompilationEngine.CLOSE_TYPE % token_type)

    def compile_statements(self):
        """
        Compiles statements by the type of each statement
        :return: None
        """
        token_type = "statements"
        self.write_tag(CompilationEngine.OPEN_TYPE % token_type)
        self.num_of_tabs += 1
        while self.tokenizer.current != CLOSE_TOKEN:
            if self.tokenizer.current == "do":
                self.compile_do()
            elif self.tokenizer.current == "let":
                self.compile_let()
            elif self.tokenizer.current == "while":
                self.compile_while()
            elif self.tokenizer.current == "if":
                self.compile_if()
            else:
                self.compile_return()
        self.num_of_tabs -= 1
        self.write_tag(CompilationEngine.CLOSE_TYPE % token_type)

    def compile_do(self):
        """
        Compiles do statement by the do statement grammar rules
        :return: None
        """
        statement_type = self.tokenizer.current
        self.write_tag(CompilationEngine.OPEN_STATEMENT % statement_type)
        self.num_of_tabs += 1
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes do
        self.compile_call_subroutine()
        self.is_expected(END_OF_LINE)
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes ;
        self.num_of_tabs -= 1
        self.write_tag(CompilationEngine.CLOSE_STATEMENT % statement_type)

    def compile_let(self):
        """
        Compiles let statement by the let statement grammar rules
        :return: None
        """
        statement_type = self.tokenizer.current
        self.write_tag(CompilationEngine.OPEN_STATEMENT % statement_type)
        self.num_of_tabs += 1
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes let
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes the first var
        if self.tokenizer.current == OPEN_ARRAY:
            self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes [
            self.compile_expression()
            self.is_expected(CLOSE_ARRAY)
            self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes ]
        self.is_expected(EQUAL)
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes =
        self.compile_expression()
        self.is_expected(END_OF_LINE)
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes ;
        self.num_of_tabs -= 1
        self.write_tag(CompilationEngine.CLOSE_STATEMENT % statement_type)

    def compile_while_if(self, statement_type):
        """
        Compiles the if and while statements (except from the "else" part)
        :param statement_type: if/while
        :return: None
        """
        self.write_tag(CompilationEngine.OPEN_STATEMENT % statement_type)
        self.num_of_tabs += 1
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes the statement type
        self.is_expected(OPEN_TERM)
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes (
        self.compile_expression()
        self.is_expected(CLOSE_TERM)
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes )
        self.is_expected(OPEN_TOKEN)
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes {
        self.compile_statements()
        self.is_expected(CLOSE_TOKEN)
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes }

    def compile_while(self):
        """
        Compiles the while statement by the while statement grammar rules
        :return: None
        """
        statement_type = self.tokenizer.current
        self.compile_while_if(statement_type)
        self.num_of_tabs -= 1
        self.write_tag(CompilationEngine.CLOSE_STATEMENT % statement_type)

    def compile_return(self):
        """
        Compiles the return statement by the return statement grammar rules
        :return: None
        """
        statement_type = self.tokenizer.current
        self.write_tag(CompilationEngine.OPEN_STATEMENT % statement_type)
        self.num_of_tabs += 1
        self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes return
        if self.tokenizer.current == END_OF_LINE:
            self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes ;
        else:  # in case the subroutine returns a value
            self.compile_expression()
            self.is_expected(END_OF_LINE)
            self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes ;
        self.num_of_tabs -= 1
        self.write_tag(CompilationEngine.CLOSE_STATEMENT % statement_type)

    def compile_if(self):
        """
        Compiles the if statement by the if statement grammar rules
        :return: None
        """
        statement_type = self.tokenizer.current
        self.compile_while_if(statement_type)
        if self.tokenizer.current == "else":
            self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes else
            self.is_expected(OPEN_TOKEN)
            self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes {
            self.compile_statements()
            self.is_expected(CLOSE_TOKEN)
            self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes }
        self.num_of_tabs -= 1
        self.write_tag(CompilationEngine.CLOSE_STATEMENT % statement_type)

    def compile_expression(self):
        """
        Compiles a single expression by the expression grammar rules
        :return: None
        """
        statement_type = "expression"
        self.write_tag(CompilationEngine.OPEN_TYPE % statement_type)
        self.num_of_tabs += 1
        self.compile_term()  # compiles a single term
        while self.tokenizer.current in JackTokenizer.op_set:  # in case there is an operator in the expression
            self.write_line(self.tokenizer.token_type(), JackTokenizer.symbol_dict[self.tokenizer.current])
            self.compile_term()  # compiles the next term
        self.num_of_tabs -= 1
        self.write_tag(CompilationEngine.CLOSE_TYPE % statement_type)

    def compile_expression_list(self):
        """
        Compiles an expression list by the expression list grammar rules
        :return: None
        """
        statement_type = "expressionList"
        self.write_tag(CompilationEngine.OPEN_TYPE % statement_type)
        self.num_of_tabs += 1
        if self.tokenizer.current != CLOSE_TERM:
            self.compile_expression()
        while self.tokenizer.current == HAS_MORE:
            self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes ,
            self.compile_expression()
        self.num_of_tabs -= 1
        self.write_tag(CompilationEngine.CLOSE_TYPE % statement_type)

    def compile_term(self):
        """
        Compiles a term by the term grammar rules
        :return: None
        """
        statement_type = "term"
        self.write_tag(CompilationEngine.OPEN_TYPE % statement_type)
        self.num_of_tabs += 1
        if self.tokenizer.current in KEYWORD_CONSTANT_SET or self.tokenizer.token_type() == INT_CONST:
            self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes the term
        elif self.tokenizer.token_type() == STR_CONST:
            self.write_line(self.tokenizer.token_type(), self.tokenizer.string_val())  # writes the term
        elif self.tokenizer.current == OPEN_TERM:
            self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes (
            self.compile_expression()
            self.is_expected(CLOSE_TERM)
            self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes )
        elif self.tokenizer.current in JackTokenizer.unary_ops:
            self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes the unary operator
            self.compile_term()
        else:  # in case the term is a variant or a subroutine
            self.advance_token()
            if self.tokenizer.current == OPEN_TERM or self.tokenizer.current == DOT:  # the term is a subroutine
                self.tokenizer.go_back()
                self.compile_call_subroutine()
            else:  # the term is a variant
                self.tokenizer.go_back()
                self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes the name of the variable
                if self.tokenizer.current == OPEN_ARRAY:
                    self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes [
                    self.compile_expression()
                    self.is_expected(CLOSE_ARRAY)
                    self.write_line(self.tokenizer.token_type(), self.tokenizer.current)  # writes ]
        self.num_of_tabs -= 1
        self.write_tag(CompilationEngine.CLOSE_TYPE % statement_type)

    def write_output_file(self):
        """
        Writes the final lines into the output file
        :return: None
        """
        f = open(self.output, WRITE)
        f.write(self.lines)
        f.close()
