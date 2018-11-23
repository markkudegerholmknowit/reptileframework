
from decorators import *

@keyword
def expect(x, msg=None):
    assert x, msg or "Expectation failed"

@keyword
def expect_equal(v1, v2, msg=None):
    assert v1 == v2, msg or ("%s not equal to %s" % (repr(v1, v2)))

@keyword
def test_value(x):
    return x

@keyword
def expect_true(x):
    assert x

@keyword
def expect_false(x):
    assert not x
