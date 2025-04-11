def signature_fragment():
    insert(f"increment: bool = True\n")

def code_fragment(v):
    insert(f'''\
"""If *increment* is True, return one more than *{v}*,
and otherwise, one less than *{v}*.
"""
return {v + 1} if increment else {v - 1}
''')
insert('def increment_or_decrement_1(\n')
signature_fragment()
insert(') -> int:\n')
code_fragment(1)
insert('\ndef increment_or_decrement_2(\n')
signature_fragment()
insert(') -> int:\n')
code_fragment(2)
