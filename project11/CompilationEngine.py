from JackTokenizer import JackTokenizer, INT_CONST, STR_CONST
from SymbolTable import SymbolTable
from VMWriter import VMWriter

# constants:
NEG_INT = '-'
ADD = "add"
THAT = "that"
LOCAL = "local"
MEMORY_ALLOC = "Memory.alloc"
THIS = "this"
POINTER = "pointer"
WHILE_NOT_LABEL = "WHILE_NOT_%s"
WHILE_LABEL = "WHILE_%s"
NEG = "not"
CONST = "constant"
IF_LABEL = "IF_DOES_%s"
IF_NOT_LABEL = "IF_NOT_%s"
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
TEMP = "temp"
KEYWORD_CONSTANT_SET = {"true", "false", "this", "null"}
CLASS_VAR_DEC = {"static", "field"}
CLASS_SUB_DEC = {"method", "function", "constructor"}
SPECIAL_OPERATORS = {'*', '/'}


class CompilationEngine:
    """
    The CompilationEngine class which compiles each type of token by the jack grammar
    """

    def __init__(self, input_file, output_file):
        """
        Constructor of the CompilationEngine class
        :param input_file: the file the JackTokenizer returns
        :param output_file: xml file
        """
        self.input = input_file
        self.output = output_file
        self.tokenizer = JackTokenizer(input_file)
        self.symbol_table = SymbolTable()
        self.vm_writer = VMWriter(output_file)
        self.class_name = ""
        self.label_index = 0

    def advance_token(self):
        """
        Advances the current token if there are more tokens
        :return: None
        """
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()

    def compile_class(self):
        """
        Compiles a class from the file by the class grammar rules
        :return: None
        """
        self.advance_token()
        self.class_name = self.tokenizer.current
        self.advance_token()
        self.advance_token()
        while self.tokenizer.current in CLASS_VAR_DEC:  # compiles the class variants
            self.compile_class_var_dec()
        while self.tokenizer.current in CLASS_SUB_DEC:  # compiles the class subroutines
            self.compile_subroutine()
        self.advance_token()

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
        sub_kind = self.tokenizer.current
        self.symbol_table.start_subroutine()
        self.advance_token()
        self.advance_token()
        name = self.tokenizer.current
        self.advance_token()
        self.advance_token()
        self.compile_parameter_list(sub_kind)
        self.advance_token()
        self.advance_token()
        while self.tokenizer.current == VAR:
            self.compile_var_dec()
        self.vm_writer.write_function(self.class_name + DOT + name, self.symbol_table.indexes[SymbolTable.VAR])
        if sub_kind == SymbolTable.METHOD:
            self.vm_writer.write_push(SymbolTable.ARG, 0)
            self.vm_writer.write_pop(POINTER, 0)
        elif sub_kind == SymbolTable.CONS:
            self.vm_writer.write_push(CONST, self.symbol_table.indexes.get(SymbolTable.FIELD))
            self.vm_writer.write_call(MEMORY_ALLOC, 1)
            self.vm_writer.write_pop(POINTER, 0)
        self.compile_statements()
        self.advance_token()

    def compile_call_subroutine(self, is_do):
        """
        Compiles the call for a subroutine by the call subroutine grammar rules
        :return: None
        """
        current = self.tokenizer.current
        num_of_args = 0
        current, num_of_args = self.compile_var_subroutine(current, num_of_args)
        self.advance_token()
        is_method = True
        if self.tokenizer.current == DOT:
            self.advance_token()
            is_method = False
            current += (DOT + self.tokenizer.current)
            self.advance_token()
        self.advance_token()
        if is_method:
            self.vm_writer.write_push(POINTER, 0)
            num_of_args += 1
        if self.tokenizer.current != CLOSE_TERM:
            num_of_args += 1
            self.compile_expression()
        while self.tokenizer.current == HAS_MORE:
            self.advance_token()
            num_of_args += 1
            self.compile_expression()
        if DOT not in current:
            current = (self.class_name + DOT + current)
        self.vm_writer.write_call(current, num_of_args)
        self.advance_token()

    def compile_var_subroutine(self, current, num_of_args):
        """
        Compiling the call subroutine if it is a var.
        :param current: the name of the var.
        :param num_of_args: the number of args in the function.
        :return: the new var for the call subroutine, and the num_of_args
        """
        if current in self.symbol_table.subroutine_table:
            self.vm_writer.write_push(LOCAL, self.symbol_table.subroutine_table[current][2])
            current = self.symbol_table.subroutine_table[current][0]
            num_of_args += 1
        elif current in self.symbol_table.class_table:
            self.vm_writer.write_push(THIS, int(self.symbol_table.class_table[current][2]))
            num_of_args += 1
            current = self.symbol_table.class_table[current][0]
        return current, num_of_args

    def compile_parameter_list(self, subroutine_type):
        """
        Compiles the parameter list of a new subroutine by the parameter list grammar rules
        :return: None
        """
        if subroutine_type == SymbolTable.METHOD:
            self.symbol_table.define(THIS, self.class_name, SymbolTable.ARG)
        while self.tokenizer.current != CLOSE_TERM:
            arg_type = self.tokenizer.current
            self.advance_token()
            self.symbol_table.define(self.tokenizer.current, arg_type, SymbolTable.ARG)
            self.advance_token()
            if self.tokenizer.current == HAS_MORE:
                self.advance_token()

    def compile_var_dec(self):
        """
        Compiles the variants deceleration of a class or a subroutine by the variants deceleration grammar rules
        :return: None
        """
        kind = self.tokenizer.current
        if kind == VAR:
            kind = LOCAL
        elif kind == SymbolTable.FIELD:
            kind = THIS
        self.advance_token()
        var_type = self.tokenizer.current
        self.advance_token()
        name = self.tokenizer.current
        self.symbol_table.define(name, var_type, kind)
        self.advance_token()
        while self.tokenizer.current == HAS_MORE:
            self.advance_token()
            name = self.tokenizer.current
            self.symbol_table.define(name, var_type, kind)
            self.advance_token()
        self.advance_token()

    def compile_statements(self):
        """
        Compiles statements by the type of each statement
        :return: None
        """
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

    def compile_do(self):
        """
        Compiles do statement by the do statement grammar rules
        :return: None
        """
        self.advance_token()
        self.compile_call_subroutine(True)
        self.vm_writer.write_pop(TEMP, 0)
        self.advance_token()

    def compile_array(self, curr_array):
        """
        Compiles an array access
        :param curr_array: the name of the current array
        :return: None
        """
        self.vm_writer.write_push(self.symbol_table.kind_of(curr_array), self.symbol_table.index_of(curr_array))
        self.compile_expression()
        self.vm_writer.write_arithmetic(ADD)
        self.advance_token()
        self.advance_token()
        self.compile_expression()
        self.vm_writer.write_pop(TEMP, 0)
        self.vm_writer.write_pop(POINTER, 1)
        self.vm_writer.write_push(TEMP, 0)
        self.vm_writer.write_pop(THAT, 0)

    def compile_array_call(self, curr_array):
        """
        Compiles the call to a specific value in an array
        :param curr_array: the array
        :return: None
        """
        self.vm_writer.write_push(self.symbol_table.kind_of(curr_array), self.symbol_table.index_of(curr_array))
        self.compile_expression()
        self.vm_writer.write_arithmetic(ADD)
        self.vm_writer.write_pop(POINTER, 1)
        self.vm_writer.write_push(THAT, 0)
        self.advance_token()

    def compile_let(self):
        """
        Compiles let statement by the let statement grammar rules
        :return: None
        """
        self.advance_token()
        current = self.tokenizer.current
        self.advance_token()
        if self.tokenizer.current == OPEN_ARRAY:
            self.advance_token()
            self.compile_array(current)
        else:
            self.advance_token()
            self.compile_expression()
            self.vm_writer.write_pop(self.symbol_table.kind_of(current), self.symbol_table.index_of(current))
        self.advance_token()

    def compile_while(self):
        """
        Compiles the while statement by the while statement grammar rules
        :return: None
        """
        self.vm_writer.write_label(WHILE_LABEL % self.label_index)
        first_label = self.label_index
        self.advance_token()
        self.advance_token()
        self.label_index += 1
        self.compile_expression()
        self.vm_writer.write_arithmetic(NEG)
        self.vm_writer.write_if(WHILE_NOT_LABEL % first_label)
        self.advance_token()
        self.advance_token()
        self.compile_statements()
        self.advance_token()
        self.vm_writer.write_goto(WHILE_LABEL % first_label)
        self.vm_writer.write_label(WHILE_NOT_LABEL % first_label)

    def compile_return(self):
        """
        Compiles the return statement by the return statement grammar rules
        :return: None
        """
        self.advance_token()
        current = self.tokenizer.current
        if current == END_OF_LINE:
            self.vm_writer.write_push(CONST, 0)
        else:  # in case the subroutine returns a value
            self.compile_expression()
        self.vm_writer.write_return()
        self.advance_token()

    def compile_if(self):
        """
        Compiles the if statement by the if statement grammar rules
        :return: None
        """
        self.advance_token()
        self.advance_token()
        self.compile_expression()
        self.vm_writer.write_arithmetic(NEG)
        self.vm_writer.write_if(IF_NOT_LABEL % self.label_index)
        first_label = self.label_index
        self.label_index += 1
        self.advance_token()
        self.advance_token()
        self.compile_statements()
        self.vm_writer.write_goto(IF_LABEL % first_label)
        self.vm_writer.write_label(IF_NOT_LABEL % first_label)
        self.advance_token()
        if self.tokenizer.current == "else":
            self.advance_token()
            self.advance_token()
            self.compile_statements()
            self.advance_token()
        self.vm_writer.write_label(IF_LABEL % first_label)

    def compile_expression(self):
        """
        Compiles a single expression by the expression grammar rules
        :return: None
        """
        self.compile_term()
        while self.tokenizer.current in JackTokenizer.op_set:
            operator = self.tokenizer.current
            self.advance_token()
            self.compile_term()
            if operator in SPECIAL_OPERATORS:
                self.vm_writer.write_call(JackTokenizer.symbol_dict[operator], 2)
            else:
                self.vm_writer.write_arithmetic(JackTokenizer.symbol_dict[operator])

    def compile_expression_list(self):
        """
        Compiles an expression list by the expression list grammar rules
        :return: None
        """
        if self.tokenizer.current != CLOSE_TERM:
            self.compile_expression()
        while self.tokenizer.current == HAS_MORE:
            self.compile_expression()

    def compile_string_const(self, string_const):
        """
        Compiles a string constant
        :param string_const: the string constant to compile
        :return: None
        """
        self.vm_writer.write_push(CONST, len(string_const))
        self.vm_writer.write_call("String.new", 1)
        for i in range(len(string_const)):
            self.vm_writer.write_push(CONST, ord(string_const[i]))
            self.vm_writer.write_call("String.appendChar", 2)

    def compile_term(self):
        """
        Compiles a term by the term grammar rules
        :return: None
        """
        current = self.tokenizer.current
        if current in KEYWORD_CONSTANT_SET:
            self.vm_writer.write_push_keyword(current)
            self.advance_token()
        elif self.tokenizer.token_type() == INT_CONST:
            self.vm_writer.write_push(CONST, current)
            self.advance_token()
        elif self.tokenizer.token_type() == STR_CONST:
            self.compile_string_const(self.tokenizer.string_val())
            self.advance_token()
        elif current == OPEN_TERM:
            self.advance_token()
            self.compile_expression()
            self.advance_token()
        elif current in JackTokenizer.unary_ops:
            operator = self.tokenizer.current
            self.advance_token()
            self.compile_term()
            self.vm_writer.write_arithmetic(JackTokenizer.unary_ops[operator])
        else:  # in case the term is a variant or a subroutine
            self.advance_token()
            if self.tokenizer.current == OPEN_TERM or self.tokenizer.current == DOT:  # the term is a subroutine
                self.tokenizer.go_back()
                self.compile_call_subroutine(False)
            else:  # the term is a variant
                self.tokenizer.go_back()
                current = self.tokenizer.current
                self.advance_token()
                if self.tokenizer.current == OPEN_ARRAY:
                    self.advance_token()
                    self.compile_array_call(current)
                else:
                    self.vm_writer.write_push(self.symbol_table.kind_of(current), self.symbol_table.index_of(current))

    def close_output_file(self):
        """
        Writes the final lines into the output file
        :return: None
        """
        self.vm_writer.close_output()
