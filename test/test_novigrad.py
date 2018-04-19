# -*- coding: utf-8 -*-
# author: pBouillon - https://github.com/pBouillon

import unittest
from subprocess import call


class TestNovigrad(unittest.TestCase):

    def test_progAbortIfBadArgLengthForDependency(self):
        sys_exit = call(["python3", "src/novigrad.py", "-d"])
        self.assertNotEqual(sys_exit, 0)

    def test_progAbortIfBadArgLengthForTime(self):
        sys_exit = call(["python3", "src/novigrad.py", "-t"])
        self.assertNotEqual(sys_exit, 0)

    def test_progAbortIfBadArgLengthForMail(self):
        sys_exit = call(["python3", "src/novigrad.py", "-m"])
        self.assertNotEqual(sys_exit, 0)

    def test_progAbortIfTooMuchArgsForDependency(self):
        sys_exit = call([
            "python3", "src/novigrad.py",
            "-d", "a", "a", "a", "a", "a"
        ])
        self.assertNotEqual(sys_exit, 0)

    def test_progAbortIfTooMuchArgsForTime(self):
        sys_exit = call(["python3", "src/novigrad.py", "-t", "1", "5"])
        self.assertNotEqual(sys_exit, 0)

    def test_progAbortIfTooMuchArgsForMail(self):
        sys_exit = call(["python3", "src/novigrad.py", "-m", "a", "a"])
        self.assertNotEqual(sys_exit, 0)

    def test_progAbortIfBadArgTypeForTime(self):
        sys_exit = call(["python3", "src/novigrad.py", "-t", "'str'"])
        self.assertNotEqual(sys_exit, 0)

    def test_progAbortIfBadArgTypeForMail(self):
        sys_exit = call(["python3", "src/novigrad.py", "-m", "0"])
        self.assertNotEqual(sys_exit, 0)


if __name__ == '__main__':
    unittest.main()
