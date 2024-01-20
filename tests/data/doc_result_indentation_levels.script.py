insert('v = True\n')
# Macro expansion result will be indented to this level
insert(f'print({1+1})\n')
insert('if v:\n')
# Macro expansion result will be indended to this higher level
insert(f'print({2+2})\n')
