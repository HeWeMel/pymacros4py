|PyPI version| |PyPI status| |PyPI pyversions| |PyPI license| |CI| |CodeCov| |Code style| |GitHub issues|

.. |PyPI version| image:: https://badge.fury.io/py/pymacros4py.svg
   :target: https://pypi.python.org/pypi/pymacros4py/

.. |PyPI status| image:: https://img.shields.io/pypi/status/pymacros4py.svg
   :target: https://pypi.python.org/pypi/pymacros4py/

.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/pymacros4py.svg
   :target: https://pypi.python.org/pypi/pymacros4py/

.. |PyPy versions| image:: https://img.shields.io/badge/PyPy-3.11-blue
   :target: https://pypi.python.org/pypi/pymacros4py/

.. |PyPI license| image:: https://img.shields.io/pypi/l/pymacros4py.svg
   :target: https://github.com/HeWeMel/pymacros4py/blob/main/LICENSE

.. |CI| image:: https://github.com/HeWeMel/pymacros4py/actions/workflows/main.yml/badge.svg?branch=main
   :target: https://github.com/HeWeMel/pymacros4py/actions/workflows/main.yml

.. |CodeCov| image:: https://img.shields.io/codecov/c/gh/HeWeMel/pymacros4py/main
   :target: https://codecov.io/gh/HeWeMel/pymacros4py

.. |Code style| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

.. |GitHub issues| image:: https://img.shields.io/github/issues/HeWeMel/pymacros4py.svg
   :target: https://GitHub.com/HeWeMel/pymacros4py/issues/


pymacros4py
===========

Brief description
-----------------

pymacros4py is a templating system for Python code. It is based on a source-level macro
preprocessor. Expressions, statements, and functions in the macro domain are also
written in Python.


Why and when?
-------------

Typical Python software is developed without using macros. And that for good reasons:
Macros are not necessary. And they have serious disadvantages.

But in some cases, you might want to write code that generates or manipulates
code. Then, using a template system might be a good alternative.

Here are some examples:

- You maintain a common code base for two different platforms, e.g., CPython and
  Cython. There are places in your code where you want to differentiate
  between the platforms already on the source level, e.g., in order to hide code
  for one platform from users of the other platform.

- There is this function that is called in performance critical code, and you
  want to inline it - but without spreading its implementation all over the project, and
  without larger modifications of your project, e.g., like switching to PyPy.

- You need to automatically generate parts of the content of some
  configuration file, and you want to make this process more explicit than using some
  generator script hidden somewhere in your project.

You need a templating system for Python code? Welcome to pymacros4py!

(Note: pymacros4py expands macros at the source-level. For extending
the language Python itself, in order to get a programming language with
additional capabilities, macro expansion
on the level of the abstract syntax tree, in the build phase of the
interpretation process, is better suited. See, e.g., the language lab
`mcpyrate <https://pypi.org/project/mcpyrate/>`_.)


Properties
----------

*pymacros4py* is a templating system with the following characteristics:

- It is **made for templates for Python files**, e.g., macro-generated code
  respects indentation.

- **Statements, functions, and expressions of the macro domain**
  **are defined as Python code** -
  You do not need to learn a special macro language.
  And you can directly use all the capabilities of Python.

- The preprocessor works **on the source level** - You see the resulting code before
  any bytecode generation / compilation / interpretation is done. And no dependency on
  external code, libraries or executables is introduced in these execution phases.

- Macro variables and functions
  **can be defined directly in the files where they are used**, or
  in separate files.

- Macro expansion can be **multi-level**, e.g., when macro code includes templates 
  that contain macro code. Expansion results are cached in order to avoid unnecessary
  computations.

- **No replacements outside explicitly marked macro sections take place** -
  This avoids the problem that a macro definition may automatically apply to future
  code added by other maintainers who do not know about the macro, with unexpected
  results.

*pymacros4py* is implemented as **pure Python code, with a really tiny code base**.
It could be an acceptable pre-build dependency for your project, even if you aim at
avoiding dependencies. And if it is not acceptable, just copy its code directly into
your project.

The code of *pymacros4py* is tested with 100% code coverage.
All examples in this README, except for a single line (excluded for
technical reasons), are covered by tests.

So far, *SemVer* is not used, and the package is marked as *beta*. The reason is
not a lack of quality, but the practical experience is not sufficient to guarantee
stability of the API.


Usage
-----


Installation
............

You can get and install *pymacros4py* as follows by using *pip*:

.. code-block:: shell

   pip install pymacros4py


Calling pymacros4py
...................

The preprocessor can be accessed in a Python script as follows:

.. code-block:: python

    >>> from pymacros4py import PreProcessor
    >>> pp = PreProcessor()

Then, the macros in a template file can be expanded as follows:

.. code-block:: python

    pp.expand_file_to_file('my_code.template.py', 'my_code.py')

Warning: When *pymacros4py* expands macros, it executes the expressions, statements
and functions of your macro code. You might want to apply it only to files that you
have fully under your control. If you write macro code that includes unsafe file
content, you can disable macro expansion for this content.

The method *expand_file_to_file* offers the following keyword parameter:

- *diffs_to_result_file*: bool = False. True means that the result is not written to
  the output file, but compared to the content of the file, and the result
  of the comparison is returned.
 

.. code-block:: python

    >>> pp.expand_file_to_file('tpl/README.rst', 'README.rst', diffs_to_result_file=True)
    ''

If you need specific arguments for the *encoding*, *errors*, or *newlines*
parameters used for opening files (see Python function *open*), you can set these
as attributes of the global object *file_options*:

.. code-block:: python

    >>> from pymacros4py import file_options
    >>> file_options.encoding = "utf-8"


Templates and template expansion
--------------------------------

A *template* consists of macro sections and text sections. A single line
of a template can already contain several such sections.

- A macro section contains Python code intended to be executed during the macro
  expansion.

- A text section can be anything. In case of a template for a Python file,
  it is normal Python code. It is used as-is (except for a possible adaptation
  of the indentation).

For expanding the macros in a template, *pymacros4py* separates the macro and the
text sections. Then, it generates and executes a so-called *template script*
as follows:

- **Code of macro sections of the template is directly taken into the**
  **template script. When this code is executed, it can insert text into the output**
  **of the macro expansion by calling function** *insert()*.

- **For text sections, a statement that inserts the text into the results**
  **is automatically appended to the template script.**


**Example:** The following template for application code contains a full-line macro
section (the first line) and a macro section embedded in a line of the application
code

.. code-block:: python

    # $$ v = 2 * 3
    x = '$$ insert(v) $$'

From this template, pymacros4py generates a template script that looks roughly as
follows:

.. code-block:: python

    v = 2 * 3
    insert('x = ')
    insert(v)
    insert('\n')

This template script will be executed by pymacros4py. It generates the following
application code as result:

.. code-block:: python

    x = 6

Application code written in Python and macro code written in Python can
be mixed like this, and the macro code extends and manipulates the application code.

This explanation and example already gives a good impression of how templates
can be written. Further details are described in the following sections.


Quoted macro code in templates
..............................

One way to mark macro code in a template looks similar to a
**string starting and ending with two dollar characters**.
Single or double quotes, or triple single or double quotes can be used.

**Example:** The following lines each show a macro section with 'v = 0' as
macro code within the macro section.

.. code-block:: python

    '$$ v = 0 $$'
    "$$ v = 0 $$"
    '''$$ v = 0 $$'''
    """$$ v = 0 $$"""

**Start and end of macro code is identified only by the special combination**
**of quoting and dollar characters**.
Thus, both the quotes and the dollars can be freely used in macro code
and in application code, as long as they do not occur together. This makes the
macro recognition quite robust.

**Example:** Some dollar characters and quotes in application code and in macro
sections, but not combined in the special syntax that starts or ends a macro section

.. code-block:: python

    print('This is application code with $$ characters and quotes')
    '$$ v = 'This is a quoted string within macro code' $$'

A **macro section** spans quoting, dollars and code together.

If before and after the quotes, there are only space or tab characters,
the macro section is a *block macro section* (otherwise: an *inline macro section*)
and spans the whole line(s), including a trailing line break if present.

**Example:** Macro section that spans the whole line, including the trailing line break.

.. code-block:: python

    # This is a comment in application code
    '$$ v = 0  # This macro section spans the whole line $$'
    # This is a second comment in application code

Macro code can span several lines. All four possible quoting types can be used for
this, but triple quotes are more pythonic here.

**Example:** Macro section that spans several lines

.. code-block:: python

    '''$$ # This comment belongs to the macro code
          v = 'a string'
    $$'''

Whitespace and line breaks in the macro section before and after the macro code
are ignored.

Example: Identical macro code ('v = 0'), surrounded by different whitespace and/or
line breaks.
  
.. code-block:: python

    '''$$      v = 0       $$'''
    '''$$
          v = 0
    $$'''


Indentation in macro code
.........................

Macro code in a macro section can be indented to an arbitrary local level, independently
of other macro sections and surrounding application code. Locally, indentation needs
to follow Python syntax. Globally, *pymacros4py* will establish a valid indentation when
combining code of several macro sections, and code generated by *mymacros4py* itself. 

**The first (non-whitespace) character of the macro code** in a macro section
**defines the base indentation** of the code. Subsequent lines of the macro code need to
be indented accordingly: equally indented (by literally the same characters, but
with each non-whitespace character replaced by a space character),
or with additional indentation characters (following the base indentation), or not
indented at all. When *pymacros4py* re-indents code, it changes only the base
indentation, and it keeps non-indented lines non-indented.

Note: This concept supports indentation by space characters, by tabs, and even
mixed forms, and does not require fixing the amount of indentation resulting from a tab.
But there is one limitation:
**If macro code is indented by tabs, it needs to start in its own line.**

**Example:** Macro code starts in its own line.
Indentation is done by space and/or tab characters.
The indentation of the first
non-whitespace character (here: 'v') defines the base indentation of the
macro section, and subsequent lines are indented equally (by an identical indentation
string). The third line is locally indented, relative to this base indentation.

.. code-block:: python

    '''$$
            v1 = 0
            for i in range(3):
                v1 += i
    $$'''

**Example:** Macro code starts in the first line of the macro section. 
All indentation is done by space characters.
The number of characters left to the 'v' determines
the base indentation that the second line follows.
The third line is locally indented, relative to this base indentation.

.. code-block:: python

    '''$       v1 = 0
               for i in range(3):
                   v1 += i
    $$'''

**Example:** Multi-line string with non-indented content

.. code-block:: python

    '''$$
        if True:  # enforce indentation
            v1 = """
        First line of string. No indentation. This will be preserved.
        Second line of string. No indentation. This will be preserved.
        """
            # We continue the indented suite of the if statement
            v2 = 0
    $$'''


Macro code in a comment
.......................

A second option to mark macro code in a template has the **form of a comment,**
**starting with a hash character**, optionally
followed by spaces or tabs, **and two dollar characters**. The macro code ends with
the line. If there are only space and/or tab characters before the hash,
the macro section spans the whole line, including a trailing line break.

.. code-block:: python

    # $$ v = 0


Arbitrary Python code as macro code
...................................

**Macro code is regular Python code**. A call to the predefined
**function**
*insert*
**inserts the results of applying the function**
*str*
**to the arguments of**
*insert*
**at the place of the macro section**.

**Example:** Macro code defining a function that generates code

.. code-block:: python

    def a_function_of_our_application():
        '''$$
        # Here, we define a function in macro code
        def return_print_n_times(n, s):
            statement = f'print("{s}")\n'
            return statement * n
        # Now, we call it
        insert(return_print_n_times(3, "Yep."))
        $$'''

The template script derived from this template generates the following result:

.. code-block:: python

    def a_function_of_our_application():
        print("Yep.")
        print("Yep.")
        print("Yep.")

**Example:** Macro code inserting a computation result

.. code-block:: python

    def example_function(i: int) -> int:
        # $$ v = 2 * 2
        return '$$ insert(v) $$'

It evaluates to:

.. code-block:: python
  
    def example_function(i: int) -> int:
        return 4


Indentation of macro results
............................

**The results of the expansion of a macro section**,
e.g., the output of calls of function *insert*, **are indented relative to the**
**indentation of the first non-whitespace character of the macro section** (i.e.,
the hash character for macro code in a comment, resp., the first quote in quoted
macro code).

**Example:** Macro sections with different indentation levels

.. code-block:: python

    v = True
    # $$ # Macro expansion result will be indented to this level
    # $$ insert(f'print({1+1})\n')
    if v:
        # $$ # Macro expansion result will be indended to this higher level
        # $$ insert(f'print({2+2})\n')
        
This template is evaluated to the following result:

.. code-block:: python

    v = True
    print(2)
    if v:
        print(4)

**For inline macro sections, the first line of the results is inserted without**
**adding indentation.** For block macro sections, each line is (re-) indented.

**Example:** An inline macro section and a block macro section, both with multi-line
results

.. code-block:: python

    # $$ v = 2
    y = 1 + '$$ insert("(\n", v, "\n* w\n)") $$'
    z = 11 + (
             '''$$ insert(v+1, "\n*w\n") $$'''
             )
        
This template is evaluated to the following result:

.. code-block:: python

    y = 1 + (
            2
            * w
            )
    z = 11 + (
             3
             *w
             )

In the first case, the inline macro section, the expansion result (starting with the
opening bracket) is inserted directly after the application code 'y = 1 + ', without
indentation.

In the second case, the block macro section, the expansion result (starting with the
'3') is inserted with indentation.


**If the library detects zero indentation in macro output, this zero indentation**
**is preserved, i.e., no re-indentation happens.**

**Example:** Recognizable zero indentation in macro output is preserved.

.. code-block:: python

    if True:
        """$$
            insert("    v = '''\ntext\n'''\n")
        $$"""
        
This template is evaluated to the following result:

.. code-block:: python

    if True:
        v = '''
    text
    '''

The macro section of the example starts in an indented suite, here, of an *if*
statement. Thus, macro output of the following macro code will be re-indented
to this level - except for the case that zero indentation of output is explicitly
demanded. So, we can check in the results, if this exception works.

Then, in the macro code, we start with inserting output at a non-zero base
indentation, as reference (the spaces before the assignment). So, the library
can detect that the subsequent lines require zero-indentation (the text of
the string literal is given with zero indentation).

In the expansion result, we see that the macro output starts indented to the
level of the start of the macro section: re-indentation happened here. But then,
the zero indentation of the lines of the string literal is detected and thus
preserved.


Including and importing files
-----------------------------

Macro code can insert expansion results or import attributes, e.g.,
function definitions, from other template files. pymacros4py offers the following
functions for this:

- **insert_from(self, template_file: str, globals_dict: Optional[dict]=None) -> None:**

  Perform a macro expansion of *template_file* within a new namespace, and
  **insert the results** into the results of the current macro expansion.
  *globals* can be given to initialize the namespace like in a call of *eval()*.

  When called a second time with an identical argument for *file*,
  and *globals* is *None* in both calls, re-use the output of the previous run.

  (If *globals* is not *None*, and you want to re-use results in cases of
  equivalent content of *globals*, this has to be implemented manually.)

- **import_from(self, template_file: str) -> None:**

  Perform a macro expansion of *template_file*
  **in the namespace of the current macro expansion**
  (attributes that have already been set can be used by macro code in
  *template_file*,
  and attributes set by such code can be used in macro code following
  the call).

  Discard the output of the expansion run.

  When called a second time with an identical argument for *template_file*,
  ignore the call.

**Example for insert_from:**

The following call of *insert_from*:

.. code-block:: python

    def example_function() -> int:
        # $$ i = 3
        # $$ insert_from("tests/data/file_with_output_macro.py")
        return "$$ insert(i) $$"

with the following content of the file:

.. code-block:: python

    # $$ i = 2
    print('some text')

evaluates to:

.. code-block:: python
    
    def example_function() -> int:
        print('some text')
        return 3

The output of the *include* statement is added to the results,
but the content of the global namespace (here: the value of variable *i*) is not
changed.

**Example for import_from:**

The following template:

.. code-block:: python

    # $$ import_from("tests/data/file_with_definition_macro.py")
    # $$ insert(return_print_n_times(3, "Yep."))

with the following content of the file:

.. code-block:: python

    '''$$
        def return_print_n_times(n, s):
            statement = f'print("{s}")\n'
            return statement * n
    $$'''
    print("Text not important")

evaluates to:

.. code-block:: python
    
    print("Yep.")
    print("Yep.")
    print("Yep.")

The content of the global namespace is extended by function *return_print_n_times*,
but the output of the imported template is ignored.


Macro statement suites spanning multiple sections
-------------------------------------------------

If the code in a macro section ends within a *suite* of a Python *compound statement*
(see https://docs.python.org/3/reference/compound_stmts.html)
e.g., an indented block of statements after statements like *if*, *for*, or *def*,
this suite ends with the macro code:

**Example:**

.. code-block:: python

    '''$$ v = 1
          if v == 0:
              insert("print('v == 0')")
    $$'''
    # $$ insert("print('Always')\n")

Result:

.. code-block:: python

    print('Always')

**But a suite can also span over subsequent template or**
**macro sections**. This case is supported in a limited form (!) as follows:

- **Start of the suite: Macro section with just the introducing statement**

  The header of the compound statement (its introducing statement, ending with
  a colon) needs to be the only content of the macro section. Not even
  a comment is allowed after the colon.

  Reason: The beginning of a suite that is meant to span multiple sections is
  recognized by the colon ending the macro code. The kind of compound statement is
  recognized by the first word of the macro code.
 
- **A suite is ended by a** *:end* **macro section**

  If the code of a macro section just consists of the special statement *:end*,
  the suite that has started most recently, ends. Whitespace is ignored.
 
- **Macro sections** *elif, else, except, finally,* **and** *case*
  **end a suite and start a new one**

  If a macro section starts with one of the listed statements and ends with
  a colon, the suite ends, that has started most recently, the macro code is handled,
  and then a new suite starts.

- **Such suites can be nested.**

**Examples for conditionally discarding or using text sections:**

.. code-block:: python
    
    # $$ import datetime
    # $$ d = datetime.date.today()
    # $$ if d > datetime.date(2024, 1, 1):
    # $$ code_block = 1
    # This comes from the first macro code block, number '$$ insert(code_block) $$'
    print('January 1st, 2024, or later')
    # $$ else:
    # This comes from the second macro code block, number '$$ insert(code_block) $$'
    print('Earlier than January 1st, 2024')
    # $$ :end

The template script generated from this template looks roughly as follows:
    
.. code-block:: python
    
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

Note that *pymacros4py* automatically indents the *insert* statements and the
statements *code_block = ...* when generating the template script, because in
Python, suites of compound statements need to be indented.

This template script evaluates to:
          
.. code-block:: python
    
    # This comes from the first macro code block, number 1
    print('January 1st, 2024, or later')

**Examples for loops over text blocks:**

.. code-block:: python
    
    # $$ for i in range(3):
    print('Yep, i is "$$ insert(i) $$".')
    # $$ :end
    # $$ j = 5
    # $$ while j > 3:
    print('And, yep, j is "$$ insert(j) $$".')
    # $$ j -= 1
    # $$ :end
    
This template evaluates to:
          
.. code-block:: python
    
    print('Yep, i is 0.')
    print('Yep, i is 1.')
    print('Yep, i is 2.')
    print('And, yep, j is 5.')
    print('And, yep, j is 4.')

**Example for a multi-section suite containing**
**both indented and non-indented macro code:**

.. code-block:: python
    
    # $$ for i in range(2):
    print('Code from the text section, variable i is "$$ insert(i) $$".')
    '''$$ # The macro code of this section is locally indented to this level,
          # but not the content of the following text literal
          more_text = """\
    print('This first line is not indented.')
    print('This second line is not indented.')
    """
          # We continue at the base indention, it is here
          insert(more_text)
    $$'''
    
    # $$ :end

The template script generated from this template looks roughly as follows:
    
.. code-block:: python
    
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

This template script shows: The implementation of multi-section suites by
*pymacros4py* meets two requirements:

- In Python, code in suites of compound statements needs to be indented. So,
  *pymacros4py* generates this indentation synthetically (re-indentation) when
  generating the template script.

- It must be possible to define unindented string literals. So, *pymacros4py*
  distinguishes unindented code from indented code, re-indents only the indented
  code, but uses the unindented code as-is.

The template evaluates to:
          
.. code-block:: python

    print('Code from the text section, variable i is 0.')
    print('This first line is not indented.')
    print('This second line is not indented.')
    
    print('Code from the text section, variable i is 1.')
    print('This first line is not indented.')
    print('This second line is not indented.')
    
 

def-statement-suites spanning multiple sections
-----------------------------------------------

If the suite of a *def*-statement spans multiple sections, indentation of
generated results of the macro expansion is special-cased as follows:

- **Macro sections: Generated code is indented as part of the calling macro section**,
  not the defining macro section.

- **Text sections: The content is also indented as part of the generated results**
  (whereas outside the suite of a *def* statement, it is interpreted as literal).
  And the same rules apply: Zero indentation is kept, other indentation is interpreted
  relative to the indentation of the first content character, and the indentation
  is adapted to the indentation of the calling macro section.

**Examples:**

.. code-block:: python

    # $$ def some_inlined_computation(times, acc):
    for macro_var_i in range('$$ insert(times) $$'):
        '$$ insert(acc) $$' = 1
    # $$ :end
    j = k = 0
    # $$ some_inlined_computation(3, "j")
    if True:
        # $$ some_inlined_computation(2, "k")

This template evaluates to:
          
.. code-block:: python

    j = k = 0
    for macro_var_i in range(3):
        j = 1
    if True:
        for macro_var_i in range(2):
            k = 1

Note, that the indentation of the results of the two calls of the function is defined
by the indentation of the calling macro sections, and not the defining macro
section. And this holds both for the macro sections and the text sections within the
suite of the *def* statement. Like that, valid indentation is established.


Debugging
---------

Error messages
..............

In case something goes wrong, *pymacros4py* tries to give helpful error messages.

**Example: Wrong indentation within macro code**

.. code-block:: python

    '''$$
        # first line
      # indentation of second line below base indentation, but not zero
    $$'''

This template leads to the following exception: 

.. code-block:: python

    >>> pp.expand_file_to_file("tests/data/error_wrong_indentation_in_macro.tpl.py", "out.py"
    ... )   # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    RuntimeError: File "tests/data/error_wrong_indentation_in_macro.tpl.py", line 2:
    Syntax error: indentation of line 1 of the macro code is not an
    extension of the base indentation.

**Example: Macro section started, but not ended**

.. code-block:: python

    '''$$

This template leads to the following exception:

.. code-block:: python

    >>> pp.expand_file_to_file("tests/data/error_macro_section_not_ended.tpl.py", "out.py"
    ... )   # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    RuntimeError: --- File "tests/data/error_macro_section_not_ended.tpl.py", line 1:
    Syntax error in macro section, macro started but not ended:
    '''$$
    <BLANKLINE>


**Example: Nesting of multi-section suites of compound statements wrong,**
**unexpected suite end**

.. code-block:: python

    #$$ if True:
    #$$ :end
    #$$ :end

This template leads to the following exception: 

.. code-block:: python

    >>> pp.expand_file_to_file("tests/data/error_unexpected_end.tpl.py", "out.py"
    ... )   # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    RuntimeError: --- File "tests/data/error_unexpected_end.tpl.py", line 3:
    Nesting error in compound statements with suites spanning several sections,
    in macro section:
      :end

**Example: Nesting of multi-section suites of compound statements wrong,**
**suite end missing**

.. code-block:: python

    #$$ if True:

This template leads to the following exception:

.. code-block:: python

    >>> pp.expand_file_to_file("tests/data/error_end_missing.tpl.py", "out.py"
    ... )   # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    RuntimeError: Syntax error: block nesting (indentation) not correct,
    is :end somewhere missing?

**Example: Wrong indentation of expansion results**

.. code-block:: python

    '''$$
      insert("    # First line indented\n")
      insert("  # Second line indented, but less than the first\n")
    $$'''

This template leads to an exception:

.. code-block:: python

    >>> try:
    ...     pp.expand_file_to_file("tests/data/error_result_indentation_inconsistent.tpl.py",
    ...                            "out.py")
    ... except Exception as e:
    ...     print(type(e).__name__)  # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
    RuntimeError

(Depending on the used Python version, the exception contains notes. If there
are notes, the doctest module cannot correctly parse them. And if not, the doctest
cannot handle this version-specific deviation of the results. So, above, we only
check that the expected exception occurs.)


Comparing results
.................

Method *expand_file_to_file* offers an option *diffs_to_result_file* that returns
the differences between the results of the macro expansion and the current content
of the result file. If there are no differences, the empty string is returned.

**Example:** Showing results of a change in a template

In the following template, we changed the expression with respect to the example of
section *Templates and template expansion*.

.. code-block:: python

    # $$ # In the following line, we changed the expression w.r.t. the example of
    # $$ # section Templates and template expansion
    # $$ v = 3 * 3
    x = '$$ insert(v) $$'

Now, we compare against the result we have gotten there:

.. code-block:: python

    >>> print(pp.expand_file_to_file("tests/data/diff_templ_and_templ_exp.tpl.py",
    ...                              "tests/data/doc_templ_and_templ_exp.py",
    ...                              diffs_to_result_file = True))
    --- current content
    +++ expansion result
    @@ -1 +1 @@
    -x = 6
    +x = 9
    <BLANKLINE>


Viewing the template script
...........................

When an exception is raised during the execution of a generated template script,
e.g., if there is an error in your Python macro code, the
script will be automatically stored (as temporary file, with the platform specific
Python mechanisms) and its path will be given in the error message.

Additionally, the method *template_script* of *pymacros4py* can be used to
see the generated template script anytime. 

**Example:** Getting the template script

.. code-block:: python

    >>> print(pp.template_script("tests/data/doc_templ_and_templ_exp.tpl.py")
    ... )   # doctest: +NORMALIZE_WHITESPACE
    _macro_starts(indentation='', embedded=False,
        content_line='File "tests/data/doc_templ_and_templ_exp.tpl.py", line 1')
    v = 2 * 3
    _macro_ends('File "tests/data/doc_templ_and_templ_exp.tpl.py", line 1')
    insert('x = ')
    _macro_starts(indentation='    ', embedded=True,
        content_line='File "tests/data/doc_templ_and_templ_exp.tpl.py", line 2')
    insert(v)
    _macro_ends('File "tests/data/doc_templ_and_templ_exp.tpl.py", line 2')
    insert('\n')
    <BLANKLINE>

Here, we used the template from section *Templates and template expansion*.
As can be seen, the real template script looks like the one shown there, but has some
additional bookkeeping code that marks when macro code starts and ends during
the execution of the template script.


Tracing
.......

*pymacros4py* can write a trace log during parsing of a template and during
execution of a template script: The options *trace_parsing* and *trace_evaluation*
of method *expand_file_to_file* activate this functionality. We demonstrate
this in the following example with method *expand_file*, which returns
the expansion result instead of storing it to a file.

**Example:** Tracing of the parsing process

.. code-block:: python

    >>> r = pp.expand_file("tests/data/doc_templ_and_templ_exp.tpl.py",
    ...                    trace_parsing=True)   # doctest: +NORMALIZE_WHITESPACE
    --- File "tests/data/doc_templ_and_templ_exp.tpl.py", line 1: line_block_macro:
    >v = 2 * 3<
    <BLANKLINE>
    <BLANKLINE>
    --- File "tests/data/doc_templ_and_templ_exp.tpl.py", line 2: text:
    >x = <
    <BLANKLINE>
    <BLANKLINE>
    --- File "tests/data/doc_templ_and_templ_exp.tpl.py", line 2: embedded_macro:
    >insert(v)<
    <BLANKLINE>
    <BLANKLINE>
    --- File "tests/data/doc_templ_and_templ_exp.tpl.py", line 2: text:
    >
    <
    <BLANKLINE>
    <BLANKLINE>

**Example:** Tracing of the evaluation process

.. code-block:: python

    >>> r = pp.expand_file("tests/data/doc_templ_and_templ_exp.tpl.py",
    ...                    trace_evaluation=True)   # doctest: +NORMALIZE_WHITESPACE
    'File "tests/data/doc_templ_and_templ_exp.tpl.py", line 1': line_block_macro
    >v = 2 * 3<
    <BLANKLINE>
    <BLANKLINE>
    'File "tests/data/doc_templ_and_templ_exp.tpl.py", line 2': text
    >x = <
    <BLANKLINE>
    <BLANKLINE>
    'File "tests/data/doc_templ_and_templ_exp.tpl.py", line 2': embedded_macro
    >insert(v)<
    <BLANKLINE>
    <BLANKLINE>
    'File "tests/data/doc_templ_and_templ_exp.tpl.py", line 2': text
    >
    <
    <BLANKLINE>
    <BLANKLINE>


Changelog
.........

**v0.8.1** (2024-02-11)

- Error messages and format of text differences improved
- Source formatted with black default 2024

**v0.8.0** (2024-01-21)

- First published version
