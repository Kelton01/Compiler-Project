import pandas as pd
import math

from Lexical_Analyzer import LexicalAnalyzer

scanning_table = "scanning new.csv"
token_table = "token table new.csv"
source_code = "source code.txt"
test = LexicalAnalyzer(scanning_table, token_table, source_code)

test.scan_source_code()


