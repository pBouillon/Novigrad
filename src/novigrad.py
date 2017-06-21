# -*- coding: utf-8 -*-
# author: pBouillon - https://github.com/pBouillon

import argparse
from argparse      import ArgumentParser
import csv
import git_checker
from git_checker   import Git_Checker
import json
import mailing
from mailing       import Mailing
import os
from os            import fork
from os            import setsid
from os            import umask
import pdf_generator
from pdf_generator import Pdf_Generator
import sched
from sched         import scheduler
import sqlite_db
from sqlite_db     import Sqlite_db
import sys
import time
from time          import sleep
from time          import time


"""Constant: integer equals to 24 hours"""
LATENCY = 60*60*24

def daemonize():
    """Daemonize the script

    Run the script as a daemon
    """
    pid = fork()
    if pid!=0:
        exit()

    setsid()
    pid = fork()
    if pid!=0:
        exit()
        
    sys.stderr = open('etc/novigrad_logs.txt', 'w+')

def check_dependencies_and_report(novigrad_sched, novigrad_mail):
    """Run novigrad every LATENCY seconds

    Gether infos
    Generate PDF
    Send it
    Then set up its next run in LATENCY seconds
    """
    checker = Git_Checker()
    report = checker.get_all_releases()
    checker.close_db()

    name = "Dependency_Report.pdf"
    try:
        with open('etc/config.json', 'r') as settings_json:
            datas = json.load(settings_json)
            name = datas["report_name"]
    except FileNotFoundError:
        exit("Error: Novigrad/etc/config.json is missing")

    pdf = Pdf_Generator(name)
    pdf.generatePDF(report)

    novigrad_mail.email_sender()

    novigrad_sched.enter(
        LATENCY, 1, 
        check_dependencies_and_report,
        (novigrad_sched,mail_service)
    )

def parse_args(mail_service):
    """Parse the program's arguments

    -m to update the mailing list
    -d to add a dependency

    helper generate himself
    """
    parser = argparse.ArgumentParser(
        prog       = "./novigrad.py",
        description= '''Update checker tool for github dependencies'''
    )
    parser.add_argument(
        '-b',
        '--background', 
        action='store_true',
        help   = 'Run novigrad as a daemon'
    )
    parser.add_argument(
        '-d',
        '--dependency',
        nargs  = 4,
        help   = 'add a depency to the sqlite database, set release to "Missing"'+\
               ' if they are none',
        metavar=('"repo_name"', '"used_release"','"used_commit"','"repo_owner"')
    )
    parser.add_argument(
        '-m',
        '--mail', 
        nargs  = 1,
        type   = str, 
        help   = 'add the mail to the mailing list',
        metavar=('mail_adress')
    )
    parser.add_argument(
        '-t',
        '--time', 
        nargs  = 1,
        type   = int, 
        help   = 'change the delay between mails',
        metavar=('time in seconds')
    )

    args = vars(parser.parse_args())

    if args["background"]:
        daemonize()

    if args["dependency"]:
        details = args["dependency"]
        with open('etc/dependencies.csv', 'a', newline='') as file:
            file.write(
                details[0]+","+details[1]+","+details[2]+","+details[3]
            )

    if args["mail"]:
        mail_service.add_mailadress(args["mail"][0])

    if args["time"]:
        global LATENCY
        LATENCY = args["time"][0]

if __name__ == '__main__':
    mail_service = Mailing()
    parse_args(mail_service)

    db = Sqlite_db()
    verif = bool(db.get_used_versions())
    db.close_db()

    if not verif:
        exit("Please, fill the database before running novigrad")

    s = scheduler(time, sleep)
    s.enter(
        LATENCY, 1, 
        check_dependencies_and_report, 
        (s, mail_service)
    )
    s.run()
