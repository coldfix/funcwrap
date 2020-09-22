funcwrap
========

|Tests| |Version| |Unlicense|

Simple helper for function wrappers or decorators that makes the wrapper
function look indistinguishable from the original.

This module provides the function ``funcwrap.wraps`` — which is a replacement
for the standard functools.wraps_ function. The difference is that while the
standard function just updates a few properties (such as ``__doc__``,
``__name__``, etc) on the wrapper object, *funcwrap* creates a new function
whose signature is identical to that of the wrapped function on the python
syntax level.

In many cases, it is enough to simply use the standard function. Use this
module if you need access to the default arguments within the wrapper, or need
to preserve the wrapped function's arity on a low level.

**IMPORTANT:** If you're planning to wrap callables other than python
functions or lambdas (e.g. partials, methods, objects), be advised that the
results may be surprising. Make absolutely sure that the wrapper function
behaves as expected before using *funcwrap*!

.. _functools.wraps: https://docs.python.org/3/library/functools.html#functools.wraps


Installation
------------

Using ``pip``::

    pip install funcwrap

Alternatively, you can redistribute the ``funcwrap.py`` module or even just
the ``funcwrap.wraps`` function by itself as part of your code or program
without any license ramifications.


Usage
-----

Use this function to create "perfect" wrapper functions:

.. code-block:: python

    from funcwrap import wraps

    def func(a, /, b='b', *, c='c'):
        """Hello, I'm an interestingly looking function!"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """I'm just a wrapper."""
        return (args, kwargs)

This makes ``wrapper`` a near identical replacement for ``func`` (except of
course function body and object identity). For one, ``help(wrapper)`` should
show up identical to ``help(func)``. But more than that, ``wrapper`` argument
binding is identical to that of ``func``:

.. code-block:: python

    # wrapper has access to func's default arguments:
    assert wrapper('A') == (('A', 'b'), {'c': 'c'})

    # b is passed as positional argument (b is positional on func):
    assert wrapper('A', b='B', c='C') == (('A', 'B'), {'c': 'C'})

    wrapper()           # TypeError: missing 1 required positional argument 'a'
    wrapper('A', d=1)   # TypeError: got an unexpected keyword argument 'd'
    wrapper(a='A')      # TypeError: got some positional-only arguments passed as keyword arguments: 'a'


Example
-------

This function is typically used as part of decorators, e.g.:

.. code-block:: python

    from funcwrap import wraps

    def trace(func):
        """Trace a method call."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('TRACE:', func.__name__, args, kwargs)
            return func(*args, **kwargs)
        return wrapper

The above decorator can be used to mark functions/methods with ``@trace`` in
order to print a notice when they are executed. It is clear that (a) marked
functions should not look different to the outside world in order not to alter
program behaviour, and (b) it is nice to be able to print the argument values
exactly as they will be received by the marked functions, with defaults
arguments inserted.

Assume you use this as part of a PyQt program similar to this:

.. code-block:: python

    class Window(QWidget):

        @trace
        def on_exit_clicked(self):
            pass

    ...

    exit_action.triggered.connect(window.on_exit_clicked)

Using the above trace function without ``funcwrap.wraps`` (or replaced by
``functools.wraps``) will introduce a subtle error. Can you spot it?

Here it goes: For overloaded signals PyQt dispatches the matching signal based
on the function signature of the connected callback (if the signature is not
selected explicitly when connecting). Without ``trace`` PyQt will correctly
detect that the ``on_exit_clicked`` handler doesn't receive an extra argument
and dispatches the plain signal without its optional ``(bool checked)``
argument. However, if you now apply ``@trace`` but using a wrapper that
doesn't perfectly conserve the function arity, PyQt will assume that the
handler can receive more parameters and pass the *checked* argument, which
will result in a ``TypeError``.


Why (not) use decorator_?
-------------------------

*funcwrap* is a lighter alternative to the decorator_ module. There are many
reasons to stick with *decorator* and some for trying *funcwrap*.

Reasons to stick with *decorator*:

- more well tested and empirically proven, mature package
- has a different API that is more directly geared toward writing decorators
- supports generator and coroutine functions
- supports python versions below 3.5
- and probably many more

Reasons to use *funcwrap*:

- support for python 3.8's `positional-only parameters`_
- simpler, shorter code that is easier to understand and modify if you need to
- license: you can redistribute this module as part of your code or program
  without having to retain any license notice
- has a different API that may better fit your needs
  (``@wraps(func)`` vs ``@decorator``)

.. _decorator: https://pypi.python.org/pypi/decorator
.. _positional-only parameters: https://www.python.org/dev/peps/pep-0570/


.. Badges:

.. |Tests| image::      https://github.com/coldfix/funcwrap/workflows/Tests/badge.svg
   :target:             https://github.com/coldfix/funcwrap/actions?query=Tests
   :alt:                GitHub Actions Status

.. |Version| image::    https://img.shields.io/pypi/v/funcwrap.svg
   :target:             https://pypi.python.org/pypi/funcwrap/
   :alt:                Latest Version

.. |Unlicense| image::  https://img.shields.io/pypi/l/funcwrap.svg
   :target:             https://unlicense.org/
   :alt:                Unlicense
