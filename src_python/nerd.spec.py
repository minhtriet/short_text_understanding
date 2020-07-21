import unittest

from nerd import NERD

class NERDTest(unittest.TestCase):
    def test_apple(self):
        n = NERD('apple')
        assert False

if __name__ == '__main__':
    unittest.main()
