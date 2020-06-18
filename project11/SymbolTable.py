class SymbolTable:
    """
    This class represents the symbol tables that are relevant to the current
    subroutine and the class
    """

    FIELD = "field"
    STATIC = "static"
    ARG = "argument"
    VAR = "var"
    CONS = "constructor"
    METHOD = "method"
    THIS = "this"
    LOCAL = "local"

    class_dict = {THIS, STATIC}

    def __init__(self):
        """
        The SymbolTable constructor
        """
        self.class_table = dict()
        self.subroutine_table = dict()
        self.indexes = {self.FIELD: 0, self.STATIC: 0, self.ARG: 0, self.VAR: 0}

    def start_subroutine(self):
        """
        Initializes the subroutine symbol table when accessing a new subroutine
        :return: None
        """
        self.subroutine_table = dict()
        self.indexes[self.ARG] = 0
        self.indexes[self.VAR] = 0

    def define(self, s_name, s_type, s_kind):
        """
        Defines a new symbol and adds it to the relevant table
        :param s_name: the name of the symbol - String
        :param s_type: the type of the symbol
        :param s_kind: the kind of the symbol - field, static. var, arg
        :return: None
        """
        if s_kind in self.class_dict:
            if s_kind == self.THIS:
                self.class_table[s_name] = (s_type, s_kind, self.indexes[self.FIELD])
                self.indexes[self.FIELD] += 1
            else:
                self.class_table[s_name] = (s_type, s_kind, self.indexes[s_kind])
                self.indexes[s_kind] += 1
        else:
            if s_kind == self.LOCAL:
                self.subroutine_table[s_name] = (s_type, s_kind, self.indexes[self.VAR])
                self.indexes[self.VAR] += 1
            else:
                self.subroutine_table[s_name] = (s_type, s_kind, self.indexes[s_kind])
                self.indexes[s_kind] += 1

    def var_count(self, s_kind):
        """
        Returns the number of symbols of the given kind in the current scope
        :param s_kind: field, static. var, arg
        :return: the number of symbols of the given kind in the current scope
        """
        return self.indexes[s_kind]

    def get_by_name(self, s_name, i):
        """
        Returns the relevant information about the given symbol
        :param s_name: the name of the symbol
        :param i: the information wanted
        :return: the type if i = 0, the kind if i = 1 and the index if i = 2
        """
        if s_name in self.subroutine_table:
            return self.subroutine_table[s_name][i]
        elif s_name in self.class_table:
            return self.class_table[s_name][i]
        return None

    def type_of(self, s_name):
        """
        Returns the type of the given symbol
        :param s_name: the name of the symbol
        :return: the type of the given symbol
        """
        return self.get_by_name(s_name, 0)

    def kind_of(self, s_name):
        """
        Returns the kind of the given symbol
        :param s_name: the name of the symbol
        :return: the kind of the given symbol
        """
        return self.get_by_name(s_name, 1)

    def index_of(self, s_name):
        """
        Returns the index of the given symbol
        :param s_name: the name of the symbol
        :return: the index of the given symbol
        """
        return self.get_by_name(s_name, 2)
