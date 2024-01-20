import datetime
d = datetime.date.today()
if d > datetime.date(2024, 1, 1):
    code_block = 1
    insert('# This comes from the first macro code block, number ')
    insert(code_block)
    insert("\nprint('January 1st, 2024, or later')\n")
else:
    insert('# This comes from the second macro code block, number ')
    insert(code_block)
    insert("\nprint('Earlier than January 1st, 2024')\n")
