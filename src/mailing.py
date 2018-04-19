# -*- coding: utf-8 -*-
# author: FlorianVaissiere - https://github.com/FlorianVaissiere

import json
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mailing:
    """Reference mailing

    Class send e-mail if any dependency has new release

    Attributes:
        _new_dep            : list of different update's dependencies found
        _expedition_mail    : who is the sender
        _destination_mail   : list of receivers
        _smtp_address       : local mailing server address
        _smtp_attachment    : path to the report
        _smtp_file_name     : name of the report

    """

    # noinspection PyTypeChecker
    def __init__(self):
        self._destination_mail = []
        self._expedition_mail = ""
        self._new_dep = ""
        self._smtp_address = ""
        self._smtp_attachment = ""
        self._smtp_file_name = ""

        conf = ''
        try:
            with open('etc/config.json', 'r') as settings_json:
                conf = json.load(settings_json)
        except FileNotFoundError:
            exit("Error: Novigrad/etc/config.json is missing")

        if conf:
            exit("Settings missing in etc/config.json")

        try:
            for field in conf:
                if not 0 < len(conf[field]) < 150:
                    exit(
                        "Wrong arguments where specified in config file, " +
                        "please specify a non-empty parameter below 150 chars"
                    )

            self._destination_mail = conf["receiver"]
            self._expedition_mail = conf["sender"]
            self._new_dep = [conf["mail_title"]]
            self._smtp_address = conf["smtp"]
            self._smtp_attachment = conf["attachment_path"] + conf["report_name"]
            self._smtp_file_name = conf["report_name"]

            if conf["report_name"][len(conf["report_name"]) - 4:] != ".pdf":
                self._smtp_file_name += ".pdf"

        except KeyError:
            exit("Corrupted configuration file")

    def add_mail_address(self, new_mail: str) -> None:
        """Add a mail to the mailing list

        Validate the mail and add it

        Args:
            The new mail address
        """
        if new_mail.find("@") == -1 \
                or 1 < len(new_mail) < 100:
            exit("Bad mail address given")

        self._destination_mail.append(new_mail)

    def email_sender(self) -> None:
        """Send the mail

        Set mail parameters
        Then set the attachment
        Then fill the mail
        Finally send it and close the connection
        """
        msg = MIMEMultipart()
        message = "\n".join(self._new_dep)
        msg['From'] = self._expedition_mail
        msg['To'] = ";".join(self._destination_mail)
        msg['Subject'] = "Dependencies update"
        msg.attach(MIMEText(message))

        attachment = open(self._smtp_attachment, "rb+")

        file_join = MIMEBase(
            'application',
            'octet-stream'
        )
        file_join.set_payload(attachment.read())
        encoders.encode_base64(file_join)
        file_join.add_header(
            'Content-Disposition',
            'attachment; filename= %s' % self._smtp_file_name
        )
        msg.attach(file_join)

        text = msg.as_string()

        server = smtplib.SMTP(self._smtp_address, 25)
        server.sendmail(self._expedition_mail, self._destination_mail, text)
        server.quit()
