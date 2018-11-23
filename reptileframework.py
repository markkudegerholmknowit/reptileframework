#!/usr/bin/env python3

import sys
import random
import time
import argparse
import importlib
import importlib.util
import rfw_state
from robot.output.xmllogger import XmlLogger
from wrapperlistener import WrapperListener

class Config(object):

    def error(self, msg):
        sys.stderr.write(msg + '\n')
        sys.exit(1)


    def usage():
        #print"%s [-i include_tags] [-e exclude_tags] [-o out.xml] [-c config.py] [--] file.py" % \
        #    sys.argv[0]
        #print "     test_module args..."
        pass

    def __init__(self, argv):
        parser = argparse.ArgumentParser(description='Test Runner')
        parser.add_argument('-i', dest='included_tags', action='append',
                            default=None,
                            help='Include a test with given tag.' +
                                 'If no tags are given,' +
                                 ' then all tests are included unless excluded.')
        parser.add_argument('-e', dest='excluded_tags', action='append',
                            default=None,
                            help='Exclude a test with given tag. ' +
                                 ' Note: exclusions have' +
                                 ' higher priority than inclusions.')
        parser.add_argument('-o', dest='output_file', action='store',
                            default='out.xml',
                            help='Name of the output XML file')
        parser.add_argument('rest', nargs=argparse.REMAINDER)
        self._args = parser.parse_args()

        if self._args.rest:
            self._rest = self._args.rest
        else:
            self._rest = []

        print('Included tags: ' + str(self.get_included_tags()))
        print('Excluded tags: ' + str(self.get_excluded_tags()))
        print('Output file:   ' + self.get_output_file())

    def get_included_tags(self):
        """ Return list of tags to explicitly include. """
        return self._args.included_tags or []

    def get_excluded_tags(self):
        """ Return list of tags to explicitly exclude. """
        return self._args.excluded_tags or []

    def get_output_file(self):
        """ Return test log output file name (XML). """
        return self._args.output_file

    def get_sut_list(self):
        """ Return list of python SUT files to run """
        return self._rest or []

def to_time(t):
    # fixme copy-paste from decorators.py
    utctime = time.gmtime(t)    # fixme localtime needed
    return time.strftime("%Y%m%d %H:%M:%S.", utctime) + str(int(t * 1000))


def run_test_suite(test_obj):
    """ Runs test cases within given test class.
        """

    listener = rfw_state.get_listener()

    def get_name():
        doclines = test_obj.__doc__.split('\n')
        if doclines:
            hdr = doclines[0]
            if len(hdr) > 0:
                return hdr  # todo escapes / sanity check
        return str(test_obj.__class__)

    suite_id = str(test_obj.__class__)
    start = time.time()
    listener_args = {
        "id": suite_id,
        "name": get_name(),
        "doc": test_obj.__doc__,
        "metadata": None,
        "source": None, #tbd
        "suites": None,       #tbd
        "tests": None,       #tbd
        "totaltests": 0,   #tbd
        "starttime": to_time(start)
    }
    listener.start_suite(suite_id, listener_args)

    listener_args["status"] = "PASS"
    listener_args["message"] = ""

    for name in dir(test_obj):
        if name.startswith('test'):
            fun = eval('test_obj.' + name)
            if callable(fun):
                try:
                    fun()

                except AssertionError as e:
                    listener_args["status"] = "FAIL"
                    listener_args["message"] = repr(e)
                    break

    end = time.time()

    listener_args["endtime"] = to_time(end)
    listener_args["elapsedtime"] = int((end - start) * 1000)
    listener_args["timeout"] = 0    # todo
    listener.end_suite(suite_id, listener_args)


def main():

    config = Config(sys.argv)
    logger = XmlLogger(config.get_output_file())
    listener = WrapperListener(logger)
    state = rfw_state.State(config, listener)

    rfw_state.set_state(state)
    rfw_state.get_state()

    sutlist = config.get_sut_list()

    if not sutlist:
        print('No test modules given!')
        return 1

    for sut in config.get_sut_list():

        if not sut.endswith(".py"):
            print('Ignoring invalid SUT file: ' + sut)
            continue

        name = 'sut'
        spec = importlib.util.spec_from_file_location(name, sut)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        test_obj = module.test_factory()
        run_test_suite(test_obj)

    logger.close()

    print('Logfile generated: ' + config.get_output_file())
    print('  Use rebot to generate log and report files!')

    return 0


if __name__ == '__main__':
    sys.exit(main())
