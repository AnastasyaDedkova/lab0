import unittest
from rtbot import *


class BotTestCase(unittest.TestCase):
    def test_clean(self):
        self.assertEqual(clean("Я же коUГда-нибудь, ...научусь писать/ без ошибокprkm2058???"), "я же когданибудь научусь писать без ошибок")
    def test_req(self):
        self.assertEqual(req(   'https://habr.com/ru/articles/'), 'habr.com/ru/articles')


if __name__ == '__main__':
    unittest.main()
