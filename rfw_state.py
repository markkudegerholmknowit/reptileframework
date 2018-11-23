#!/usr/bin/env python3

DEFAULT_STATE = None


class Context(object):

    def __init__(self, parent=None):
        self._parent = parent
        self._depth = parent.depth() + 1 if parent else 0

    def depth(self):
        return self._depth

    def get_parent(self):
        return self._parent


class State(object):

    def __init__(self, config, listener):
        self._cur_ctx = self._root_ctx = Context()
        self._included_tags = config.get_included_tags()
        self._excluded_tags = config.get_excluded_tags
        self._config = config
        self._listener = listener

    def set_tags(self, included, excluded):
        self._included_tags = included
        self._excluded_tags = excluded

    def get_listener(self):
        return self._listener

    def check_tags(self, tags):
        """ Returns true if any of the given tags is in list of included tags,
            and none is in the list of excluded tags.
            If list of included tags is empty, then any tag will be accepted """
        is_included = not len(self._include_tags)
        for t in tags:
            if not is_included and t in self._included_tags:
                is_included = True
            if t in self._excluded_tags:
                return False

        return is_included

    def get_current_ctx(self):
        return self._cur_ctx

    def push(self):
        self._cur_ctx = Context(self._cur_ctx)
        return self._cur_ctx

    def pop(self):
        self._cur_ctx = self._cur_ctx.get_parent()
        return self._cur_ctx

    def get_indent(self):
        depth = self.get_current_ctx().depth()
        return "".ljust(depth * 4)


def set_state(state):
    global DEFAULT_STATE
    DEFAULT_STATE = state


def get_state():

    global DEFAULT_STATE
    state = DEFAULT_STATE
    assert state, "State is NULL"
    return state


def get_listener():
    s = get_state()
    listener = s.get_listener()
    assert listener
    return listener
