funcwrap
========

|Tests| |Version| |Unlicense|

Simple helper for function wrappers or decorators that makes the wrapper
function look indistinguishable from the original.


Installation
------------

Using ``pip``::

    pip install funcwrap

Alternatively, you can redistribute the ``funcwrap.py`` module or even the
``funcwrap.wrap`` function by itself as part of your code or program without
any license ramifications.


Usage
-----

``funcwrap.wrap`` is similar to the standard ``functools.wraps`` function.
However, it returns a wrapper that imitates the wrapped function's signature
exactly on the python syntax level.

.. code-block:: python

    >>> from funcwrap import wraps

    >>> def func(a='Hello,', *, b='World!'):
    ...     pass

    >>> @wraps(func)
    ... def wrapper(*args, **kwargs):
    ...     return (args, kwargs)

    >>> wrapper()
    (('Hello,',), {'b': 'World!'})

    >>> wrapper('Bye,', b='Quentin!')
    (('Bye,',), {'b': 'Quentin!'})


**IMPORTANT:** If you're planning to wrap callables other than python
functions or lambdas (e.g. partials, methods, objects), be advised that the
results may be surprising. Make absolutely sure that the wrapper function
behaves as expected before using *funcwrap*!


Why (not) use decorator_?
-------------------------

*funcwrap* is a lighter alternative to the decorator_ module. There are many
reasons to stick with *decorator* and some for trying *funcwrap*.

Reasons to stick with *decorator*:

- more well tested and empirically proven, mature package
- has a different API that is more directly designed toward writing decorators
- supports generator and coroutine functions
- supports python versions below 3.5
- and probably many more

Reasons to use *funcwrap*:

- support for python 3.8's `positional-only parameters`_
- simpler, shorter code that is easier to understand and modify if you need to
- license: you can redistribute this module as part of your code or program
  without having to retain any license notice
- has a different API that fits your needs better
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
