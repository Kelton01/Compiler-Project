import pandas as pd
import math


class LexicalAnalyzer:
    
	def __init__(self, scanning_table, token_table, source_code):
		self.scanning_table = pd.read_csv(scanning_table)
		self.token_table = pd.read_csv(token_table)
		self.source_code = source_code
		
	def scan_source_code(self):
		'''
	    This function will scan through every char in the source code file until it finds
	    potential final states
		'''
		sc = open(self.source_code, 'r')
		curr_state = 0
		curr_token = ""
		while 1:
			char = sc.read(1)
			if not char:
			    break
			if char == '\n':
			    char = '\\n'
			elif char == '\t':
			    char = '\\t'
			if self.get_state(curr_state, char) == 0:
				if curr_state == 0:
					continue
				else:
					self.print_final_state(curr_state, curr_token)
					curr_state = 0
					curr_token = ""
			curr_state = self.get_state(curr_state, char)
			if char != '\\n' and char != '\\t':
				curr_token += char
		if curr_state != 0:
			self.print_final_state(curr_state, curr_token)
		sc.close()
		
		
	def get_state(self, state, char):
		'''
	    This function will find the next available state using the old state and new char.
	    If there is no state (as in an empty box) the function will return 0
		'''
		state = self.scanning_table.at[state,char]
		if math.isnan(state) == True:
			return 0;
		else:
			return int(float(state))

	def print_final_state(self, state, token):
		'''
	    this function will check the input state to see if it is a valid final state using
	    the token table and print out the token type and lexeme
		'''
		df = self.token_table.loc[self.token_table['Accepting State'] == state]
		if state in df.values:
			token_name = df.head()['token'].iloc[0]
			print ("token: " + token_name + " | Lexeme: " + token)
		else:
			print ("INVALID TOKEN | Lexeme: " + token)
	    