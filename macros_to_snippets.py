# This script takes a macros file (.txt) with macros of the form '\nc{\A}{\mathbf{A}}' and returns a snippet file (.txt) to be pasted in the (.json) snippet file in vscode
from pathlib import Path
import re

possible_commands_string = ['nc', 'renc', 'newcommand', 'renewcommand']   # add your own used prefixes to define new commands
possible_environments_string = ['newenv', 'renewenv', 'nenv', 'renenv', 'newenvironment', 'renewenvironment']   # add your own used prefixes to define new environments 

possible_commands_compiled = [re.compile('\\\\'+p+'\\{\\\\([a-zA-Z]*)\\}') for p in possible_commands_string]
possible_environments_compiled = [re.compile('\\\\'+p+'\\{([a-zA-Z]*)\\}') for p in possible_environments_string]
possibilities_compiled = possible_commands_compiled+possible_environments_compiled

variable_count_search = re.compile('\[([\d])\]')

macros = Path(__file__).with_name('macros.txt')
snippets = Path(__file__).with_name('snippets.txt')

with macros.open('r') as f:
    macros_lines = f.readlines()

with snippets.open('w') as f:
    for L in macros_lines:
        if (L[0] == '\\'):
            for prefix in possibilities_compiled:
                searched = prefix.search(L)
                if searched != None:
                    name = searched.group(1)
                    if prefix in possible_commands_compiled:
                        f.writelines('\t"'+name+'": {\n'+'\t\t"prefix": "'+name+'",\n'+'\t\t"body": "\\\\'+name+'"\n'+'\t},\n'+'\n')
                    else:
                        count_search = variable_count_search.search(L)
                        if count_search != None:
                            count = int(count_search.group(1))
                            suffix = ''
                            for i in range(count):
                                suffix += '\\{\\$'+str(i)+'\\}'
                            f.writelines('\t"'+name+'": {\n'+'\t\t"prefix": "'+name+'",\n'+'\t\t"body": "\\\\'+name+suffix+'$0"\n'+'\t},\n'+'\n')
