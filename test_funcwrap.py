from funcwrap import wraps

import pytest

import functools
from sys import version_info as python


skipif = pytest.mark.skipif


def test_no_args():
    """Test function without arguments."""
    def wrapped():
        pass
    f = wraps(wrapped, called)
    assert f() == ((), {})
    pytest.raises(TypeError, f, 0)
    pytest.raises(TypeError, f, a=0)


def test_decorator_usage():
    """Test that wraps(func) can be used as decorator."""
    def wrapped(a, b=-1):
        pass
    f = wraps(wrapped)(called)
    assert f(0) == f(a=0) == ((0, -1), {})
    assert f(0, 1) == f(0, b=1) == f(a=0, b=1) == ((0, 1), {})
    pytest.raises(TypeError, f)
    pytest.raises(TypeError, f, b=0)


def test_positional_arguments():
    """Test function with only positional arguments."""
    f = wraps(lambda a, b=-1: None, called)
    assert f(0) == ((0, -1), {})
    assert f(a=0) == ((0, -1), {})
    assert f(0, 1) == ((0, 1), {})
    assert f(0, b=1) == ((0, 1), {})
    assert f(a=0, b=1) == ((0, 1), {})
    pytest.raises(TypeError, f)
    pytest.raises(TypeError, f, b=1)
    pytest.raises(TypeError, f, a=0, b=1, c=2)
    pytest.raises(TypeError, f, 0, 1, 2)


def test_varargs():
    """Test function with only variable length positional arguments."""
    f = wraps(lambda *args: None, called)
    assert f() == ((), {})
    assert f(0) == ((0,), {})
    assert f(0, 1) == ((0, 1), {})
    assert f(0, 1, 2) == ((0, 1, 2), {})
    pytest.raises(TypeError, f, a=0)
    pytest.raises(TypeError, f, 0, b=1)


def test_kwargs():
    """Test function with only variable length keyword arguments."""
    f = wraps(lambda **kwargs: None, called)
    assert f() == ((), {})
    assert f(a=0) == ((), {'a': 0})
    assert f(a=0, b=1) == ((), {'a': 0, 'b': 1})
    assert f(a=0, b=1, c=2) == ((), {'a': 0, 'b': 1, 'c': 2})
    pytest.raises(TypeError, f, 0)
    pytest.raises(TypeError, f, 0, 1)


def test_all_argument_kinds():
    """Test function with all kinds of arguments (except positional-only)."""
    f = wraps(lambda a, b=-1, *args, c, d=-1, **kwargs: None, called)
    assert f(0, c=1) == ((0, -1), {'c': 1, 'd': -1})
    assert f(a=0, c=1) == ((0, -1), {'c': 1, 'd': -1})
    assert f(0, 1, c=2) == ((0, 1), {'c': 2, 'd': -1})
    assert f(0, b=1, c=2) == ((0, 1), {'c': 2, 'd': -1})
    assert f(0, 1, 2, 3, c=4) == ((0, 1, 2, 3), {'c': 4, 'd': -1})
    assert f(0, c=1, d=2) == ((0, -1), {'c': 1, 'd': 2})
    assert f(0, c=1, d=2, e=3) == ((0, -1), {'c': 1, 'd': 2, 'e': 3})
    assert f(0, 1, 2, 3, c=4, d=5, e=6) == (
        (0, 1, 2, 3), {'c': 4, 'd': 5, 'e': 6})
    pytest.raises(TypeError, f, )
    pytest.raises(TypeError, f, 0)
    pytest.raises(TypeError, f, c=4)
    pytest.raises(TypeError, f, a=0)
    pytest.raises(TypeError, f, 0, 4)
    pytest.raises(TypeError, f, 0, 4, b=1)


def test_default_value_identity():
    """Check that object identity is conserved for default values."""
    x = object()
    y = object()
    f = wraps(lambda a=x: None, called)
    assert f() == ((x,), {})
    assert f(y) != ((x,), {})
    assert f(y) == ((y,), {})


def test_lambda():
    """Test that wrapping works also on a lambda."""
    f = wraps(lambda a, b=-1, *args, **kwargs: None, called)
    assert f(0) == ((0, -1), {})
    assert f(0, 1) == ((0, 1), {})
    assert f(0, 1, 2) == ((0, 1, 2), {})
    assert f(a=0) == ((0, -1), {})
    assert f(a=0, b=1) == ((0, 1), {})
    assert f(a=0, b=1, c=2) == ((0, 1), {'c': 2})
    assert f(0, 1, 2, d=3) == ((0, 1, 2), {'d': 3})
    pytest.raises(TypeError, f, b=1)
    pytest.raises(TypeError, f, b=1, c=1)


def test_instance():
    class Wrapped(object):
        def __call__(self, a, b=-1, *args, **kwargs):
            pass
    w = Wrapped()
    f = wraps(w, called)
    assert f(w, 0) == ((w, 0, -1), {})
    assert f(w, 0, 1) == ((w, 0, 1), {})
    assert f(w, 0, 1, 2) == ((w, 0, 1, 2), {})
    assert f(w, a=0) == ((w, 0, -1), {})
    assert f(w, a=0, b=1) == ((w, 0, 1), {})
    assert f(w, a=0, b=1, c=2) == ((w, 0, 1), {'c': 2})
    assert f(w, 0, 1, 2, d=3) == ((w, 0, 1, 2), {'d': 3})
    pytest.raises(TypeError, f, b=1)
    pytest.raises(TypeError, f, b=1, c=1)


def test_partial_0():
    def wrapped(a, b, c, *args, **kwargs):
        pass
    p = functools.partial(wrapped, a=-1, b=-2)
    f = wraps(p, called)
    assert f(c=0, d=1) == ((), {'a': -1, 'b': -2, 'c': 0, 'd': 1})
    assert f(a=0, b=1, c=2) == ((), {'a': 0, 'b': 1, 'c': 2})
    pytest.raises(TypeError, f)
    pytest.raises(TypeError, f, a=1)
    pytest.raises(TypeError, f, b=1)


def test_partial_1():
    def wrapped(a, b, c, *args, **kwargs):
        pass
    p = functools.partial(wrapped, -1, -2)
    f = wraps(p, called)

    assert f(0) == ((0,), {})
    assert f(c=0) == ((0,), {})
    assert f(0, 1, d=2) == ((0, 1), {'d': 2})
    pytest.raises(TypeError, f)
    pytest.raises(TypeError, f, 0, c=1)


def test_annotations_identity():
    """Check that annatotions object identity is preserved."""
    _a, _b, _c, _d, _va, _kw, _ret = [], [], [], [], [], [], []

    def wrapped(
            a: _a,
            b: _b = -1,
            *va: _va,
            c: _c,
            d: _d = -1,
            **kw: _kw) -> _ret:
        pass

    f = wraps(wrapped, called)
    a = f.__annotations__

    assert a['a'] is _a
    assert a['b'] is _b
    assert a['c'] is _c
    assert a['d'] is _d
    assert a['va'] is _va
    assert a['kw'] is _kw
    assert a['return'] is _ret


def test_kwonly_arguments():
    """Test function with only keyword-only arguments."""
    f = wraps(lambda *, c, d=-1: None, called)
    assert f(c=0) == ((), {'c': 0, 'd': -1})
    assert f(c=0, d=1) == ((), {'c': 0, 'd': 1})
    pytest.raises(TypeError, f)
    pytest.raises(TypeError, f, 0)
    pytest.raises(TypeError, f, 0, 1)
    pytest.raises(TypeError, f, d=1)


@skipif(python < (3, 8), reason='posonly arguments require python 3.8')
def test_posonly_arguments_0():
    wrapped = eval('lambda a, b=-1, /: None')
    f = wraps(wrapped, called)
    assert f(0) == ((0, -1), {})
    assert f(0, 1) == ((0, 1), {})
    pytest.raises(TypeError, f)
    pytest.raises(TypeError, f, a=0)
    pytest.raises(TypeError, f, 0, b=1)
    pytest.raises(TypeError, f, 0, 1, c=2)


@skipif(python < (3, 8), reason='posonly arguments require python 3.8')
def test_posonly_arguments_1():
    wrapped = eval('lambda a, b=-1, /, c=-1, *args, d, **kwargs: None')
    f = wraps(wrapped, called)
    assert f(0, d=1) == ((0, -1, -1), {'d': 1})
    assert f(0, 1, d=2) == ((0, 1, -1), {'d': 2})
    assert f(0, 1, 2, d=3) == ((0, 1, 2), {'d': 3})
    assert f(0, 1, 2, 3, d=4) == ((0, 1, 2, 3), {'d': 4})
    assert f(0, c=1, d=2) == ((0, -1, 1), {'d': 2})
    assert f(0, d=1, e=2) == ((0, -1, -1), {'d': 1, 'e': 2})
    pytest.raises(TypeError, f)
    pytest.raises(TypeError, f, 0)
    pytest.raises(TypeError, f, 0, 1)
    pytest.raises(TypeError, f, d=1)


def test_special_argument_names():
    f = wraps(lambda __call__=-1: None, called)
    assert f() == ((-1,), {})
    assert f(0) == ((0,), {})
    assert f(__call__=0) == ((0,), {})


def called(*args, **kwargs):
    return (args, kwargs)
