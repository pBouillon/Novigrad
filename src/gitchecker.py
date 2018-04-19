# -*- coding: utf-8 -*-
# author: pBouillon - https://github.com/pBouillon

import json
from time import sleep

import requests

from sqlitedb import SqliteDB

"""Integer: seconds to wait before the next request"""
HOLD = 60 * 31


class GitChecker:
    """Reference Git_Checker

    Get and check github repositories
    If the API is unavailable, wait 35mn for the refresh

    Attributes:
        _base_url : base url for the github api
        _db       : database connection
    """

    def __init__(self):
        self._base_url = "https://api.github.com/repos/"
        self._db = SqliteDB()

    @staticmethod
    def __exec_request(req):
        """Returns the result of the request

        Verify that the API is reachable
        Otherwise wait for the refresh
        Then return the result
        """
        r = requests.get("https://api.github.com/rate_limit")

        if int(
                json.loads(
                    r.text or r.content
                )["rate"]["remaining"]) == 0:
            sleep(HOLD)

        return requests.get(req)

    def __r_get_last_commit(self, name):
        """Returns the last commit

        Get the name of the repo and its owner
        Then build the request
        Then get the commit as a 7 digits string

        Returns:
            String containing the commit
            "Missing" on failure
        """
        owner = self._db.get_repo_owner(name)

        r = self.__exec_request(
            self._base_url +
            owner +
            "/" +
            name +
            "/commits"
        )

        if r.ok:
            for item in json.loads(r.text or r.content):
                return item["sha"][:7]

        return "Missing"

    def __r_get_last_release(self, name):
        """Returns the name of the last release

        Get the name of the repo and its owner
        Then build the request
        Then gather its name

        Returns:
            A String containing the version
            "Missing" on failure
        """
        owner = self._db.get_repo_owner(name)

        r = self.__exec_request(
            self._base_url +
            owner +
            "/" +
            name +
            "/releases/latest"
        )

        if r.ok:
            return json.loads(r.text or r.content)["tag_name"]

        return "Missing"

    def close_db(self):
        """Close the checker's database
        """
        self._db.close_db()

    def get_all_releases(self) -> dict:
        """Gather the latest releases for all repos

        Check each repository and its latest release

        Returns:
            A dict as :
                {
                    repo: [
                            latest_release,
                            latest_commit
                          ],
                    ...
                }
        """
        release = {}
        repo = []
        used_versions = self._db.get_used_versions()

        for elem in used_versions:
            repo.append(elem)

        for repository in repo:
            newest_info = [
                self.__r_get_last_release(repository),
                self.__r_get_last_commit(repository)]

            release[repository] = newest_info

        return release
