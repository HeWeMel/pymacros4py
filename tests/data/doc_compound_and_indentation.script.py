for i in range(2):
    insert("print('Code from the text section, variable i is ")
    insert(i)
    insert(".')\n")
    # The macro code of this section is locally indented to this level,
    # but not the content of the following text literal
    more_text = """\
print('This first line is not indented.')
print('This second line is not indented.')
"""
    # We continue at the base indention, it is here
    insert(more_text)
    insert('\n')
