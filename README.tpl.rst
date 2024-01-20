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

- *diff*: bool = False. True means that the result is not written to the
  output file, but compared to the content of the file, and the result
  of the comparison is printed to *stdout*.
 
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

    # $$ insert_content("tests/data/doc_templ_and_templ_exp.tpl.py")

From this template, pymacros4py generates a template script that looks roughly as
follows:

.. code-block:: python

    # $$ insert_content("tests/data/doc_templ_and_templ_exp.script.py")

This template script will be executed by pymacros4py. It generates the following
application code as result:

.. code-block:: python

    # $$ insert_content("tests/data/doc_templ_and_templ_exp.py")

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

    # $$ insert_content("tests/data/doc_four_quoted_formats.tpl.py")

**Start and end of macro code is identified only by the special combination**
**of quoting and dollar characters**.
Thus, both the quotes and the dollars can be freely used in macro code
and in application code, as long as they do not occur together. This makes the
macro recognition quite robust.

**Example:** Some dollar characters and quotes in application code and in macro
sections, but not combined in the special syntax that starts or ends a macro section

.. code-block:: python

    # $$ insert_content("tests/data/doc_robust_syntax.tpl.py")

A **macro section** spans quoting, dollars and code together.

If before and after the quotes, there are only space or tab characters,
the macro section is a *block macro section* (otherwise: an *inline macro section*)
and spans the whole line(s), including a trailing line break if present.

**Example:** Macro section that spans the whole line, including the trailing line break.

.. code-block:: python

    # $$ insert_content("tests/data/doc_block_macro_section.tpl.py")

Macro code can span several lines. All four possible quoting types can be used for
this, but triple quotes are more pythonic here.

**Example:** Macro section that spans several lines

.. code-block:: python

    # $$ insert_content("tests/data/doc_multi_line_block_macro_section.tpl.py")

Whitespace and line breaks in the macro section before and after the macro code
are ignored.

Example: Identical macro code ('v = 0'), surrounded by different whitespace and/or
line breaks.
  
.. code-block:: python

    # $$ insert_content("tests/data/doc_whitespace_around_macro_code.tpl.py")


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

    # $$ insert_content("tests/data/doc_code_own_line_indentation.tpl.py")

**Example:** Macro code starts in the first line of the macro section. 
All indentation is done by space characters.
The number of characters left to the 'v' determines
the base indentation that the second line follows.
The third line is locally indented, relative to this base indentation.

.. code-block:: python

    # $$ insert_content("tests/data/doc_code_inline_indentation.tpl.py")

**Example:** Multi-line string with non-indented content

.. code-block:: python

    # $$ insert_content("tests/data/doc_code_multiline_indentation.tpl.py")


Macro code in a comment
.......................

A second option to mark macro code in a template has the **form of a comment,**
**starting with a hash character**, optionally
followed by spaces or tabs, **and two dollar characters**. The macro code ends with
the line. If there are only space and/or tab characters before the hash,
the macro section spans the whole line, including a trailing line break.

.. code-block:: python

    # $$ insert_content("tests/data/doc_comment_format.tpl.py")


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

    # $$ insert_content("tests/data/doc_function_generates_code.tpl.py")

The template script derived from this template generates the following result:

.. code-block:: python

    # $$ insert_content("tests/data/doc_function_generates_code.py")

**Example:** Macro code inserting a computation result

.. code-block:: python

    # $$ insert_content("tests/data/doc_inserting_computation_result.tpl.py")

It evaluates to:

.. code-block:: python
  
    # $$ insert_content("tests/data/doc_inserting_computation_result.py")


Indentation of macro results
............................

**The results of the expansion of a macro section**,
e.g., the output of calls of function *insert*, **are indented relative to the**
**indentation of the first non-whitespace character of the macro section** (i.e.,
the hash character for macro code in a comment, resp., the first quote in quoted
macro code).

**Example:** Macro sections with different indentation levels

.. code-block:: python

    # $$ insert_content("tests/data/doc_result_indentation_levels.tpl.py")
        
This template is evaluated to the following result:

.. code-block:: python

    # $$ insert_content("tests/data/doc_result_indentation_levels.py")

**For inline macro sections, the first line of the results is inserted without**
**adding indentation.** For block macro sections, each line is (re-) indented.

**Example:** An inline macro section and a block macro section, both with multi-line
results

.. code-block:: python

    # $$ insert_content("tests/data/doc_result_indentation_cases.tpl.py")
        
This template is evaluated to the following result:

.. code-block:: python

    # $$ insert_content("tests/data/doc_result_indentation_cases.py")

In the first case, the inline macro section, the expansion result (starting with the
opening bracket) is inserted directly after the application code 'y = 1 + ', without
indentation.

In the second case, the block macro section, the expansion result (starting with the
'3') is inserted with indentation.


**If the library detects zero indentation in macro output, this zero indentation**
**is preserved, i.e., no re-indentation happens.**

**Example:** Recognizable zero indentation in macro output is preserved.

.. code-block:: python

    # $$ insert_content("tests/data/doc_result_zero_indentation_preserved.tpl.py")
        
This template is evaluated to the following result:

.. code-block:: python

    # $$ insert_content("tests/data/doc_result_zero_indentation_preserved.py")

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

Macro code can access the *PreProcessor* object that executes the current macro
expansion: In the macro scope, it is available as attribute *pp*.

Its methods are:

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

    # $$ insert_content("tests/data/doc_insert_from.tpl.py")

with the following content of the file:

.. code-block:: python

    # $$ insert_content("tests/data/file_with_output_macro.py")

evaluates to:

.. code-block:: python
    
    # $$ insert_content("tests/data/doc_insert_from.py")

The output of the *include* statement is added to the results,
but the content of the global namespace (here: the value of variable *i*) is not
changed.

**Example for import_from:**

The following template:

.. code-block:: python

    # $$ insert_content("tests/data/doc_import_from.tpl.py")

with the following content of the file:

.. code-block:: python

    # $$ insert_content("tests/data/file_with_definition_macro.py")

evaluates to:

.. code-block:: python
    
    # $$ insert_content("tests/data/doc_import_from.py")

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

    # $$ insert_content("tests/data/doc_section_ends_suite.tpl.py")

Result:

.. code-block:: python

    # $$ insert_content("tests/data/doc_section_ends_suite.py")

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
    
    # $$ insert_content("tests/data/doc_compound_if.tpl.py")

The template script generated from this template looks roughly as follows:
    
.. code-block:: python
    
    # $$ insert_content("tests/data/doc_compound_if.script.py")

Note that *pymacros4py* automatically indents the *insert* statements and the
statements *code_block = ...* when generating the template script, because in
Python, suites of compound statements need to be indented.

This template script evaluates to:
          
.. code-block:: python
    
    # $$ insert_content("tests/data/doc_compound_if.py")

**Examples for loops over text blocks:**

.. code-block:: python
    
    # $$ insert_content("tests/data/doc_compound_for.tpl.py")
    
This template evaluates to:
          
.. code-block:: python
    
    # $$ insert_content("tests/data/doc_compound_for.py")

**Example for a multi-section suite containing**
**both indented and non-indented macro code:**

.. code-block:: python
    
    # $$ insert_content("tests/data/doc_compound_and_indentation.tpl.py")

The template script generated from this template looks roughly as follows:
    
.. code-block:: python
    
    # $$ insert_content("tests/data/doc_compound_and_indentation.script.py")

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

    # $$ insert_content("tests/data/doc_compound_and_indentation.py")
 

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

    # $$ insert_content("tests/data/doc_compound_def.tpl.py")

This template evaluates to:
          
.. code-block:: python

    # $$ insert_content("tests/data/doc_compound_def.py")

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

    # $$ insert_content("tests/data/error_wrong_indentation_in_macro.tpl.py")

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

    # $$ insert_content("tests/data/error_macro_section_not_ended.tpl.py")

This template leads to the following exception:

.. code-block:: python

    >>> pp.expand_file_to_file("tests/data/error_macro_section_not_ended.tpl.py", "out.py"
    ... )   # doctest: +NORMALIZE_WHITESPACE
    # $$ insert_content("tests/data/error_macro_section_not_ended.msg.py")


**Example: Nesting of multi-section suites of compound statements wrong,**
**unexpected suite end**

.. code-block:: python

    # $$ insert_content("tests/data/error_unexpected_end.tpl.py")

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

    # $$ insert_content("tests/data/error_end_missing.tpl.py")

This template leads to the following exception:

.. code-block:: python

    >>> pp.expand_file_to_file("tests/data/error_end_missing.tpl.py", "out.py"
    ... )   # doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
    RuntimeError: Syntax error: block nesting (indentation) not correct,
    is :end somewhere missing?

**Example: Wrong indentation of expansion results**

.. code-block:: python

    # $$ insert_content("tests/data/error_result_indentation_inconsistent.tpl.py")

This template leads to the following exception: 

.. code-block:: python

    >>> pp.expand_file_to_file("tests/data/error_result_indentation_inconsistent.tpl.py", "out.py"
    ... )   # doctest: +NORMALIZE_WHITESPACE, +ELLIPSIS
    Traceback (most recent call last):
    RuntimeError: Error when executing template script ...

In this example output, the name of the template file is left out, because it
is not constant. Also omitted is the first half of the error message,
because Python doctests cannot handle sequences of exceptions (to my knowledge).
Here it is:

.. code-block:: python

    RuntimeError: File "tests/data/error_result_indentation_inconsistent.tpl.py", line 2:
    Output syntax error: indentation of the following line of the results of
    the template script from the above given template line is not an extension
    of the base indentation of these results:
    >  # Second line indented, but less than the first<
    (Start of line shown enclosed by characters '>' and '<')

Comparing results
.................

Method *expand_file_to_file* offers an option *diffs_to_result_file* that shows
the differences between the results of the macro expansion and the current content
of the result file.

**Example:** Showing results of a change in a template

In the following template, we changed the expression with respect to the example of
section *Templates and template expansion*.

.. code-block:: python

    # $$ insert_content("tests/data/diff_templ_and_templ_exp.tpl.py")

Now, we compare against the result we have gotten there:

.. code-block:: python

    >>> pp.expand_file_to_file("tests/data/diff_templ_and_templ_exp.tpl.py",
    ...                        "tests/data/doc_templ_and_templ_exp.py",
    ...                        diffs_to_result_file = True)
    - x = 6
    ?     ^
    + x = 9
    ?     ^
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
