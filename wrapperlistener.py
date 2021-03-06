# utf-8

def to_obj(attrs):
    class X:
        pass

    x = X()
    x.__dict__.update(attrs)

    return x


class WrapperListener:

    def __init__(self, wrapped):
        self._wrapped = wrapped
        self._suiteCount = 0

    def start_suite(self, name, attrs):
        self._suiteCount += 1
        try:
            self._wrapped.start_suite(to_obj(attrs))
        except Exception as e:
            print(repr(e))
            raise e

    def end_suite(self, name, attrs):
        self._suiteCount -= 1
        try:
            self._wrapped.end_suite(to_obj(attrs))
        except Exception as e:
            print(repr(e))
            raise e

    def start_test(self, name, attrs):
        if not self._suiteCount:
            return
        try:
            self._wrapped.start_test(to_obj(attrs))
        except Exception as e:
            print(repr(e))
            raise e

    def end_test(self, name, attrs):
        if not self._suiteCount:
            return
        try:
            self._wrapped.end_test(to_obj(attrs))
        except Exception as e:
            print(repr(e))
            raise e

    def start_keyword(self, name, attrs):
        if not self._suiteCount:
            return
        try:
            self._wrapped.start_keyword(to_obj(attrs))
        except Exception as e:
            print(repr(e))
            raise e

    def end_keyword(self, name, attrs):
        if not self._suiteCount:
            return
        try:
            self._wrapped.end_keyword(to_obj(attrs))
        except Exception as e:
            print(repr(e))
            raise e
