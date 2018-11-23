#!/usr/bin/env python3

import random
import time
import rfw_state
import traceback

def conv_args(args):
    return [repr(x) for x in args]


def conv_kwargs(kwargs):
    return [("%s=%s") % (repr(x), repr(y)) for x, y in kwargs.items()]


def to_time(t):
    utctime = time.gmtime(t)    # fixme localtime needed
    return time.strftime("%Y%m%d %H:%M:%S.", utctime) + str(int(t * 1000))


def keyword(fun):
    def decorator(*args, **kwargs):
        listener = rfw_state.get_listener()
        name = fun.__name__
        print(args)
        print(kwargs)
        all_args = conv_args(args) + conv_kwargs(kwargs)
        start = time.time()
        listener_args = {
            "type": "kw",
            "kwname": name,
            "libname": "",
            "doc": fun.__doc__,
            "args": all_args,
            "assign": None,
            "tags": [],
            "starttime": to_time(start)
        }

        listener.start_keyword(name, listener_args)

        ret = None

        try:
            ret = fun(*args, **kwargs)

            listener_args["status"] = "PASS"
            listener_args["message"] = ""
        except Exception as e:
            listener_args["status"] = "FAIL"
            listener_args["message"] = repr(e)
            raise
        finally:
            end = time.time()

            listener_args["endtime"] = to_time(end)
            listener_args["elapsedtime"] = str(int((end - start) * 1000))

            listener_args["assign"] = {"ret": repr(ret)}
            listener_args["timeout"] = 0    # todo
            listener.end_keyword(name, listener_args)

        # todo: log return value somehow...

        return ret

    return decorator


def testcase(fun):
    def decorator(*args, **kwargs):
        listener = rfw_state.get_listener()
        name = fun.__name__
        all_args = conv_args(args[1:]) + conv_kwargs(kwargs)

        start = time.time()
        listener_args = {
            "id": name,
            "name": name,
            "longname": name,   # tbd
            "doc": fun.__doc__,
            "args": all_args,
            "assign": None,
            "tags": [],         # tbd
            "critical": True,   # tbd
            "template": None,
            "starttime": to_time(start)
        }
        listener.start_test(name, listener_args)

        try:
            fun(*args, **kwargs)

            listener_args["status"] = "PASS"
            listener_args["message"] = ""
        except AssertionError as e:
            listener_args["status"] = "FAIL"
            listener_args["message"] = repr(e)
        except Exception as e:
            listener_args["status"] = "FAIL"
            listener_args["message"] = repr(e)
            traceback.print_exc()
        finally:

            end = time.time()

            listener_args["endtime"] = to_time(end)
            listener_args["elapsedtime"] = str(int((end - start) * 1000))
            listener_args["timeout"] = 0    # todo
            listener.end_test(name, listener_args)

    return decorator


def string_randomizer(n, arg, min_len=0, max_len=None):
    def decorator(fun):
        def inner_decorator(*args, **kwargs):
            state = rfw_state.get_state()

            for i in range(n):
                slen = random.randint(min_len, max_len or 255)
                chars = ["%c" % (int(random.randint(0, 255)))
                         for x in range(slen)]
                value = "".join(chars)
                kwargs[arg] = value
                state.push()
                fun(*args, **kwargs)
                state.pop()
        return inner_decorator
    return decorator


def tags(**tags):
    """ A decorator to tag a testcase, which can be used to limit which
        testcases get run.
        Example:
        @tags("not-ready")
        def test_xxx:
            pass

        @tags("arm", "powerpc"")
        def test_yyy:
            ...

        UNTESTED.

        """
    def decorator(fun):
        state = rfw_state.get_state()

        if state.check_tags(tags):
            return fun()
        else:
            return None


def noncritical(fun):
    """ Same as @tags("non-critical") """
    return tags(fun, "noncritical")

def disabled(fun):
    """ A decorator to disable a test. """
    def decorator(*args, **kwargs):
        pass

    return decorator
