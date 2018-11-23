#!/usr/bin/env python

from decorators import keyword, testcase, string_randomizer, disabled
from asserts import expect_true, expect_false
import requests

@keyword
def testlog(msg):
    pass

class TestGameServer(object):
    """ Game Server Acceptance Tests """

    def __init__(self, url):
        self._url = url

    class Login:

        @keyword
        def __init__(self, url, user, passw):
            self._url = url
            self._user = user
            self._passw = passw

        @keyword
        def try_login(self):
            params = {'user': self._user, 'pass': self._passw}
            r = requests.get(self._url, params=params)

            testlog('http status=%i' % r.status_code)
            if r.status_code == requests.codes.ok:
                j = r.json()
                testlog('result=%s' % j)
                return 'status' in j and j['status'] == 'OK'

            return False

    @testcase
    def test_empty_creds(self):
        login = TestGameServer.Login(self._url + "/login", user="", passw="")
        expect_false(login.try_login())

    @testcase
    def test_valid_creds(self):
        login = TestGameServer.Login(self._url + "/login", "markku", "3l1t3")
        expect_true(login.try_login())

    @disabled
    @string_randomizer(n=3, arg='user', min_len=0, max_len=10)
    @string_randomizer(n=3, arg='passw', min_len=0, max_len=10)
    @testcase
    def test_random_creds(self, user, passw):
        login = TestGameServer.Login(
                    url=self._url + "/login", user=user, passw=passw)
        expect_false(login.try_login())

def test_factory():
    return TestGameServer("http://localhost:5000/game")
