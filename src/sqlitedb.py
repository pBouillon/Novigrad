# -*- coding: utf-8 -*-
# author: pBouillon - https://github.com/pBouillon

import csv
import sqlite3
from sqlite3 import Error, connect


class SqliteDB:
    """Reference SqliteDB

    Handle the sqlite database of the project
    
    Attributes:
        _database   : database name, by default novigrad_db 
        _connection : connection to the sqlite database
        _cursor     : cursor for the sqlite database
    """

    def __init__(self, database_name=":memory:"):
        self._database = database_name
        self._connection = None
        self._cursor = None
        self.connect_db()
        self.__init_database()

    def __init_database(self) -> None:
        """initialize the database

        Get the content of the sql source file and run it
        If the database already exists, doesn't override anything
        """
        try:
            sql = """
                create table if not exists DEPENDENCIES(
                    ID               integer       primary key   autoincrement,
                    DEPENDENCY_NAME  varchar(100),
                    DEPENDENCY_VERS  varchar(11),
                    DEPENDENCY_COMM  varchar(50),
                    REPOSITORY_OWNER varchar(100)
                ) ;
            """
            self._connection.execute(sql)
            self._connection.commit()

        except sqlite3.OperationalError:
            self.close_db()
            exit("An error occurred while initializing to the database")

        try:
            with open("etc/dependencies.csv", "r") as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    if row[0] != "Dependency_name":
                        self.add_dependency(
                            row[0],
                            row[1],
                            row[2],
                            row[3]
                        )
        except IOError:
            self.close_db()
            exit("dependencies.csv missing")

    def add_dependency(
            self,
            dep_name: str,
            dep_version: str,
            dep_version_commit: str,
            repo_owner: str
    ) -> None:
        """Add the dependence inside the database

        Get the dependency and its version
        Then add it into the database if variables are correct
        """
        if 1 < len(dep_name) < 100 \
                and 1 < len(dep_version) < 11 \
                and 1 < len(dep_version_commit) < 50 \
                and 1 < len(repo_owner) < 100:
            sql = """
                insert into
                DEPENDENCIES(DEPENDENCY_NAME, DEPENDENCY_VERS,
                DEPENDENCY_COMM, REPOSITORY_OWNER)
                values (?,?,?,?)
            """
            record = [
                dep_name,
                dep_version,
                dep_version_commit,
                repo_owner
            ]
            self._cursor.execute(sql, record)
            self._connection.commit()
        else:
            self.close_db()
            exit("Unhandled args length")

    def close_db(self) -> None:
        """Close the connection to the database

        Close the cursor if open
        Then close the connection
        """
        if self._connection:
            self._cursor.close()
            self._connection.close()

    def connect_db(self) -> None:
        """Connect the database

        Connect to the sqlite database
        Then initialize _connection and _cursor
        """
        if self._connection:
            return
        try:
            self._connection = connect(self._database)
            self._cursor = self._connection.cursor()
        except Error:
            self.close_db()
            exit("An error occurred while connecting to the database")

    def get_repo_owner(self, repo: str) -> str:
        """Get the name of the owner

        Returns the name of the owner of 'repo'

        Returns:   
            String - owner of the repository
        """
        sql = """
            SELECT REPOSITORY_OWNER
            FROM DEPENDENCIES
            WHERE DEPENDENCY_NAME=?;
        """
        self._cursor.execute(sql, [repo])

        row = self._cursor.fetchone()

        if row is None:
            exit("Error looking for " + repo + " owner in sqlite")
        return row[0]

    def get_used_versions(self) -> list:
        """Get all dependencies

        Get all dependencies and their used versions from the owner

        Returns:
            content: a list[
                            dependency_name, 
                            dependencies_version,
                            dep_version_commit,
                            repo_owner
                        ]
        """
        content = {}
        self._cursor.execute("SELECT * FROM DEPENDENCIES ;")

        while True:
            row = self._cursor.fetchone()
            if row is None:
                break
            content[str(row[1])] = [
                str(row[2]),
                str(row[3]),
                str(row[4])
            ]

        self._connection.commit()
        return content
