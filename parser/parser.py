import pandas as pd
import math
#
# CPSC 323 Parser Project
# Authors: Kelton Benson, Mathias Nguyen, and Harrold Ventayen
# Your task is to implement a parser using the default grammar 
# parser csv table generated by the Java program.
#
class Parser:
    """
    This class parses the token stream outputted from the lexical analyzer 
    into a parse tree or produces errors if the program is malformed.
    """
    def __init__(self, token_stream, parse_table_file, grammar):
        """
        Class constructor takes the token stream output from the 
        lexical analyzer as input. Appends $ to the end of the stream.
        """
        self.token_stream = token_stream
        self.parser_table = pd.read_csv(parse_table_file)
        self.grammar = grammar
        # Append the end of file symbol to the end.
        self.token_stream.append(("$", "$"))
        
    
    """
    This function is not needed because we are using Pandas
        
    def __read_parse_table(self, parse_table_file):
        Reads the parse table from a file.
        @param parse_table_file The file path for the parse table csv file.
        @return A dictionary/map (state, symbol) -> action/goto.
        #raise NotImplementedError()
    """

    def __has_next_token(self):
        """
        @return True if the token stream is not empty.
        """
        return len(self.token_stream) != 0

    def __get_next_token(self):
        """
        Fetches and consumes the next token in the input.
        @return tuple (token, type)
        """
        if self.__has_next_token():
            to_return = self.token_stream[0]
            self.token_stream.pop(0)
            return to_return
        return None

    def parse(self):
        stack = []
        prev_token = ""
        # we will use the append function to substitute for push
        stack.append(0)
        # because the token is returned as a tuple with the form (lexeme, token), we take only the second value from i
        i = self.__get_next_token()[1] 
        accept = False
        while accept == False: 
            print("current token: " + i)
            qm = stack[-1]
            print("current stack:")
            print(stack)
            x = str(self.parser_table.at[int(qm),i])
            print("action: " + x)
            print("\n")
            if x == 'nan':
                """
                    If the value inside the box returns "nan" then that means the next token input was
                    invalid. An Error message will be returned and the parsing will end
                """
                print("PARSING ERROR: did not expect " + i + " after " + prev_token)
                break
            if x[0] == 'S' or x[0] == 's':
                """
                    SHIFT ACTION. pushes the token and state onto the stack
                    and then sets i to the next token.
                """
                stack.append(i) # pushes token
                stack.append(x[1:]) # pushes state
                prev_token = i
                i = self.__get_next_token()[1]
            elif x[0] == 'R' or x[0] == 'r':
                """
                    RUDUCE ACTION. this will find the # of RHS symbols, multiply it by 2, then pop that amount from the stack
                    in order to get rid of the handle, then it will push the terminal and state onto the stack.
                """
                symbols = self.grammar[int(x[1:])-1]
                RHS_symbols_count = (len(symbols.split()) - 2) * 2
                for j in range(RHS_symbols_count):
                    stack.pop()
                top = stack[-1]
                stack.append(symbols[0]) # pushes terminal
                stack.append(int(self.parser_table.at[int(top),symbols[0]])) # pushes state
            if x == "ACCT":
                """
                    When the parser reaches an Accept state, accept will become true and the loop
                    will end.
                """
                accept = True
                print("Parsing completed with no errors")
        #raise NotImplementedError()