# -*- coding: utf-8 -*-
# author: pBouillon - https://github.com/pBouillon

import argparse
import json
import sys
import time
import os
from os import fork
from os import setsid
import sched
from sched import scheduler
import time
from time import sleep
from time import strftime
from time import time

import src.com.novigard.db.sqlite_db
from src.com.novigard.db.sqlite_db import Sqlite_db
import src.com.novigard.util.git_checker
from src.com.novigard.util.git_checker import Git_Checker
import src.com.novigard.util.mailing
from src.com.novigard.util.mailing import Mailing
import src.com.novigard.util.pdf_generator
from src.com.novigard.util.pdf_generator import Pdf_Generator

"""Constant: integer equals to 24 hours"""
LATENCY = 60*60*24
"""Gobal var: check the offline mode"""
verbose = False

def daemonize():
    """Daemonize the script

    Run the script as a daemon
    """
    pid = fork()
    if pid < 0:
        exit ('An error occured on the first fork')
    elif pid!=0:
        exit()

    setsid()
    if pid < 0:
        exit ('An error occured on the second fork')
    elif pid!=0:
        exit()

    sys.stderr = open('etc/novigrad_logs.txt', 'w+')

def check_dependencies_and_report(novigrad_mail):
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

    novigrad_sched = scheduler(time, sleep)
    novigrad_sched.enter(
        LATENCY, 1,
        check_dependencies_and_print,
        ()
    )
    novigrad_sched.run()

def check_dependencies_and_print():
    """Run novigrad every LATENCY seconds

    Gether infos
    Generate output
    Then set up its next run in LATENCY seconds
    """
    checker = Git_Checker()
    report = checker.get_all_releases()
    checker.close_db()

    output = '\n\n********************************************\n' + \
                strftime("%Y-%m-%d %H:%M") + "\n\n"
    for e in report:
        output += '> ' + e + ' > last version: ' + report[e][0] +\
                    ' | last commit: ' + report[e][1] + '\n'

    with open('etc/report.txt', 'a+', newline='') as file:
        file.write (output)

    print ('\n### REPORT PRINTED ###\n')

    novigrad_sched = scheduler(time, sleep)
    novigrad_sched.enter(
        LATENCY, 1,
        check_dependencies_and_print,
        ()
    )
    novigrad_sched.run()

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
        action = "store_true",
        help   = 'Run novigrad as a daemon'
    )
    parser.add_argument(
        '-d',
        '--dependency',
        nargs  = 4,
        help   = 'add a depency to the sqlite database, set release to "Missing"'+\
               ' if they are none',
        metavar=('"name"', '"release"','"commit"','"owner"')
    )
    parser.add_argument(
        '-m',
        '--mail',
        nargs  = 1,
        type   = str,
        help   = 'add the mail to the mailing list',
        metavar=('mail')
    )
    parser.add_argument(
        '-t',
        '--time',
        nargs  = 1,
        type   = int,
        help   = 'change the delay between mails',
        metavar=('seconds')
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action = "store_true",
        help   = 'put the report in etc/reports.txt instead of an email'
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

    if args["verbose"]:
        global verbose
        verbose = True


if __name__ == '__main__':
    mail_service = Mailing()
    parse_args(mail_service)

    db = Sqlite_db()
    verif = bool(db.get_used_versions())
    db.close_db()

    if not verif:
        exit("Please, fill the database before running novigrad")

    s = scheduler(time, sleep)
    if verbose:
        print ('\nVerbose mode launched,\nReport will be generated on '+\
                'etc/reports.txt in ' + str(LATENCY) + ' seconds\n')
        s.enter(
            LATENCY, 1,
            check_dependencies_and_print,
            ()
        )
    else:
        s.enter(
            LATENCY, 1,
            check_dependencies_and_report,
            (mail_service)
        )
    s.run()
