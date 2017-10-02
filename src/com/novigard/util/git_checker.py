# -*- coding: utf-8 -*-
# author: pBouillon - https://github.com/pBouillon

import json
import time
from time import sleep

import requests

from src.com.novigard.db.sqlite_db import Sqlite_db

"""Integer: seconds to wait before the next request"""
TEMPORISATION = 60*31

class Git_Checker:
    """Reference Git_Checker

    Get and check github repositories
    If the API is unavailable, wait 35mn for the refresh

    Attributes:
        _base_url : base url for the github api
        _db       : database connection
    """
    def __init__(self):
        self._base_url = "https://api.github.com/repos/"
        self._db       = Sqlite_db()

    def __exec_request(self,req):
        """Returns the result of the request

        Verify that the API is reachable
        Otherwise wait for the refresh
        Then return the result
        """
        r = requests.get("https://api.github.com/rate_limit")

        if int(json.loads(r.text or r.content)["rate"]["remaining"]) == 0:
            sleep(TEMPORISATION)

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
        last_release_json = {}
        owner = self._db.get_repo_owner(name)

        r = self.__exec_request(self._base_url+owner+"/"+name+"/commits")

        if r.ok :
            commitInfos = json.loads(r.text or r.content)
            for item in commitInfos:
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
        last_release_json = {}
        owner = self._db.get_repo_owner(name)

        r = self.__exec_request(self._base_url+owner+"/"+name+"/releases/latest")

        if r.ok :
            return json.loads(r.text or r.content)["tag_name"]
        
        return "Missing"

    def close_db(self):
        """Close the checker's database
        """
        self._db.close_db()

    def get_all_releases(self):
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
        realease_dict = {}
        repo_list     = []
        used_versions = self._db.get_used_versions()

        for elem in used_versions:
            repo_list.append(elem)

        for repository in repo_list:
            newest_infos = []
            newest_infos.append(self.__r_get_last_release(repository))
            newest_infos.append(self.__r_get_last_commit(repository))

            realease_dict[repository] = newest_infos

        return realease_dict
