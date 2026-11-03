# This script takes a macros file (.txt) with macros of the form '\nc{\A}{\mathbf{A}}' and returns a snippet file (.txt) to be pasted in the (.json) snippet file in vscode
from pathlib import Path
import re

possible_prefixes_string = ['nc', 'renc', 'newcommand', 'renewcommand']   # add your own used prefixes to define new commands !
possible_prefixes_compiled = [re.compile('\\\\'+p+'\\{\\\\([a-zA-Z]*)\\}') for p in possible_prefixes_string]
macros = Path(__file__).with_name('macros.txt')
snippets = Path(__file__).with_name('snippets.txt')

with macros.open('r') as f:
    macros_lines = f.readlines()

with snippets.open('w') as f:
    for L in macros_lines:
        if (L[0] != '%') and (L[0] != '\n'):
            for prefix_unknown in possible_prefixes_compiled:
                searched = prefix_unknown.search(L)
                if searched != None:
                    name = searched.group(1)
                    f.writelines('\t"'+name+'": {\n')
                    f.writelines('\t\t"prefix": "'+name+'",\n')
                    f.writelines('\t\t"body": "\\\\'+name+'"\n')
                    f.writelines('\t},\n')
                    f.writelines('\n')












#extract_command = re.compile('\\{\\\\'+name+'\\}\\{([\w,\W]*)\\}')
#command_test = (extract_command.search(L))
#if command_test == None:
#    print(name)
#else:
#    command_latex = command_test.group(1)                            # latex command to execute. Need to double the '\' for json.
#    command = ''
#    for c in command_latex:
#        if c=='\\':
#            command += '\\\\'
#        else:
#            command += c