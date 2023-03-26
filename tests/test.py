import sys
sys.path.append("src")

from unittest import TestCase


class Emailesting(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_1(self):
        
