insert('def example_function() -> int:\n')
i = 3
insert_from("tests/data/file_with_output_macro.py")
insert('    return ')
insert(i)
insert('\n')
