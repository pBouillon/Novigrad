# -*- coding: utf-8 -*-
# author: pBouillon - https://github.com/pBouillon

from sqlitedb import SqliteDB
import unittest


class TestSqlMethods(unittest.TestCase):
    ''' Database connectivity '''

    def test_databaseCantOpenWrongDataBase_assertFalse(self):
        with self.assertRaises(SystemExit):
            SqliteDB("test/sql/unknown_db.db")

    def test_databaseCanConnectToTheDefaultDataBase_assertTrue(self):
        try:
            db = SqliteDB()
            db.close_db()
        except Exception:
            self.assertEqual(True, False)

    ''' Database requests '''

    def test_databaseExitIfNoRepositoryExists_assertFalse(self):
        db = SqliteDB()
        with self.assertRaises(SystemExit):
            db.get_repo_owner("some_imaginary_repository")

    ''' Database add '''

    def test_databaseExitIfDependencyNameIsEmpty_assertFalse(self):
        db = SqliteDB()
        with self.assertRaises(SystemExit):
            db.add_dependency("", "v0.0.2", "e45d87", "owner")

    def test_databaseExitIfVersionNameIsEmpty_assertFalse(self):
        db = SqliteDB()
        with self.assertRaises(SystemExit):
            db.add_dependency("Some_repo", "", "e45d87", "owner")

    def test_databaseExitIfCommitNameIsEmpty_assertFalse(self):
        db = SqliteDB()
        with self.assertRaises(SystemExit):
            db.add_dependency("Some_repo", "v0.0.2", "", "owner")

    def test_databaseExitIfownerNameIsEmpty_assertFalse(self):
        db = SqliteDB()
        with self.assertRaises(SystemExit):
            db.add_dependency("Some_repo", "v0.0.2", "e45d87", "")

    def test_databaseExitIfDependencyNameIsEmpty_assertFalse(self):
        huge_str = ''
        for i in range(150):
            huge_str += '#'

        db = SqliteDB()
        with self.assertRaises(SystemExit):
            db.add_dependency(huge_str, "v0.0.2", "e45d87", "owner")

    def test_databaseExitIfVersionNameIsEmpty_assertFalse(self):
        huge_str = ''
        for i in range(150):
            huge_str += '#'

        db = SqliteDB()
        with self.assertRaises(SystemExit):
            db.add_dependency("Some_repo", huge_str, "e45d87", "owner")

    def test_databaseExitIfCommitNameIsEmpty_assertFalse(self):
        huge_str = ''
        for i in range(150):
            huge_str += '#'

        db = SqliteDB()
        with self.assertRaises(SystemExit):
            db.add_dependency("Some_repo", "v0.0.2", huge_str, "owner")

    def test_databaseExitIfownerNameIsEmpty_assertFalse(self):
        huge_str = ''
        for i in range(150):
            huge_str += '#'

        db = SqliteDB()
        with self.assertRaises(SystemExit):
            db.add_dependency("Some_repo", "v0.0.2", "e45d87", huge_str)


if __name__ == '__main__':
    unittest.main()
