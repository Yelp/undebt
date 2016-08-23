# Undebt

Undebt is a fast, straightforward, reliable tool for performing massive, automated code refactoring used [@Yelp](https://github.com/Yelp). Undebt lets you define complex find-and-replace rules using standard, straightforward Python that can be applied quickly to an entire code base with a simple command.

To learn about what Undebt is and why we created it, check out our [post on the Yelp Engineering Blog](http://engineeringblog.yelp.com/2016/08/undebt-how-we-refactored-3-million-lines-of-code.html).

## Get Started

To get started using Undebt, install with
```bash
pip install undebt
```
then head over to our **[documentation](http://undebt.readthedocs.io/en/latest/)** for more information.

## Example

While the [full list of examples](http://undebt.readthedocs.io/en/latest/examples.html) can be found in the documentation, to show you how it's done we'll go in-depth into one example in particular, [`class_inherit_object.py`](https://github.com/Yelp/undebt/blob/master/undebt/examples/class_inherit_object.py). Like most of the examples, this pattern is built for Python, but in theory Undebt could be used with any language. The idea of this pattern is to convert any usage of [old-style classes to new-style classes](https://docs.python.org/2/reference/datamodel.html#newstyle) by making all classes that don't inherit from anything else inherit from `object`. The code for this pattern is incredibly simple—a mere four lines not counting imports:
```python
grammar = INDENT + Keyword("class").suppress() + NAME + (Optional(LPAREN + RPAREN) + COLON).suppress()

@tokens_as_list(assert_len=2)
def replace(tokens):
    return tokens[0] + "class " + tokens[1] + "(object):"
```

What's going on here? The basic idea is that `grammar` defines what to look for, and `replace` defines how to change it. Undebt scans your files looking for `grammar`, tokenizes the matching text, passes the tokens to `replace`, and replaces the original text with the return value. _For a more in-depth explanation of how to use `grammar` and `replace` in a pattern file, see the [pattern files documentation](http://undebt.readthedocs.io/en/latest/patterns.html)._

In this particular case, `grammar` is defined to match an indent (`INDENT`), followed by a class definition (`+ Keyword("class") + NAME`) that doesn't inherit from anything (`+ Optional(LPAREN + RPAREN) + COLON`). Along the way, all the tokens except for the indent and the class name are suppressed, that way `replace` only gets those two tokens, which it reassembles into a class definition that inherits from `object`. _For a full specification of all of the helper objects used here, see the [pattern utilities documentation](http://undebt.readthedocs.io/en/latest/util.html)._

To run this pattern on your code:

**(1)** Install Undebt by entering into your command line
```bash
pip install undebt
```
**(2)** Create a new file `my_class_inherit_object.py` containing
```python
from undebt.examples.class_inherit_object import grammar, replace
```
**(3)** Run `undebt` with `my_class_inherit_object.py` as the pattern
```bash
undebt --pattern ./my_class_inherit_object.py --input <directory or file to undebt>
```
If you are undebting a directory, you will also need to pass `-e py` to tell `undebt` to search for Python files in that directory. _For a complete command line example and the full command line help, see the [command line documentation](http://undebt.readthedocs.io/en/latest/cli.html)._
