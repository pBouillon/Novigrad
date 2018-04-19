# -*- coding: utf-8 -*-
# author: FlorianVaissiere - https://github.com/FlorianVaissiere

import time

from reportlab.lib.colors import black
from reportlab.lib.colors import green
from reportlab.lib.colors import red
from reportlab.lib.colors import yellow
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate

from sqlitedb import SqliteDB


class PdfGenerator:
    """Reference Pdf_Generator

    Class check and create a pdf report

    Attributes:
        _doc_param            : set document properties width height
        _formatted_time       : take the actual hour
        _styles_default       : create style for default _text
        _styles_title         : create style for title
        _styles_alert_uptodate: create style for alert up to date
        _styles_alert_commit  : create style for alert commit
        _styles_alert_release : create style for alert release
        _styles_space         : create style for spacing

    """

    def __init__(self, name="Dependency_Report.pdf") -> None:
        self._doc_param = SimpleDocTemplate(
            name,
            pagesize=letter,
            rightMargin=25,
            leftMargin=25,
            topMargin=25,
            bottomMargin=25
        )
        self._formatted_time = time.ctime()
        self._styles_default = ParagraphStyle(
            'title',
            font_Name='Helvetica-Bold',
            fontSize=12,
            leading=12,
            alignment=TA_LEFT,
            _textColor=black
        )
        self._styles_title = ParagraphStyle(
            'title',
            font_Name='Helvetica-Bold',
            fontSize=18,
            leading=42,
            alignment=TA_CENTER,
            _textColor=black
        )
        self._styles_alert_uptodate = ParagraphStyle(
            'uptodate',
            leading=12,
            backColor=green,
            borderColor=black,
            borderWidth=1,
            borderPadding=5,
            borderRadius=2,
            spaceBefore=10,
            spaceAfter=10
        )
        self._styles_alert_commit = ParagraphStyle(
            'commit',
            leading=12,
            backColor=yellow,
            borderColor=black,
            borderWidth=1,
            borderPadding=5,
            borderRadius=2,
            spaceBefore=10,
            spaceAfter=10
        )
        self._styles_alert_release = ParagraphStyle(
            'release',
            leading=12,
            backColor=red,
            borderColor=black,
            borderWidth=1,
            borderPadding=5,
            borderRadius=2,
            spaceBefore=10,
            spaceAfter=10
        )
        self._styles_space = ParagraphStyle(
            'space',
            leading=0,
            borderWidth=1,
            borderPadding=5,
            borderRadius=2,
            spaceBefore=5,
            spaceAfter=5
        )

    def generate_pdf(self, values: dict):
        """Generate PDF

        Check Dependencies
        Then order them 
        Finally create pdf report
        """
        db = SqliteDB()
        db_content = db.get_used_versions()
        db.close_db()

        _text = []

        _title = " - Dependencies Report - "
        _text.append(
            Paragraph(
                _title,
                self._styles_title
            )
        )
        _text.append(
            Paragraph(
                self._formatted_time,
                self._styles_title
            )
        )

        if bool(values):
            _text.append(
                Paragraph(
                    "UP TO DATE : ",
                    self._styles_alert_uptodate
                )
            )

            for _name in values:
                if (values[_name][0] == db_content[_name][0]
                    or values[_name][0] == 'Missing') \
                        and values[_name][1] == db_content[_name][1]:
                    _newest = _name + \
                              " : " + \
                              values[_name][0] + \
                              " - " + \
                              values[_name][1]

                    _text.append(
                        Paragraph(
                            _newest,
                            self._styles_default
                        )
                    )
                    _text.append(
                        Paragraph(
                            "",
                            self._styles_space
                        )
                    )

            _text.append(
                Paragraph(
                    "NEW COMMIT AVAILABLE : ",
                    self._styles_alert_commit
                )
            )

            for _name in values:
                if values[_name][1] != db_content[_name][1]:
                    _newest = _name + \
                              " : " + \
                              'https://github.com/' + \
                              db_content[_name][2] + \
                              '/' + _name + \
                              " " + \
                              values[_name][0] + \
                              " - " + \
                              values[_name][1]

                    _text.append(
                        Paragraph(
                            _newest,
                            self._styles_default
                        )
                    )
                    _text.append(
                        Paragraph(
                            "",
                            self._styles_space
                        )
                    )

            _text.append(
                Paragraph(
                    "NEW RELEASE AVAILABLE : ",
                    self._styles_alert_release
                )
            )

            for _name in values:
                if values[_name][0] != db_content[_name][0] \
                        and values[_name][0] != 'Missing':
                    _newest = _name + \
                              " : " + \
                              'https://github.com/' + \
                              db_content[_name][2] + \
                              '/' + _name + \
                              " - " + values[_name][0] + \
                              " - " + values[_name][1]

                    _text.append(
                        Paragraph(
                            _newest,
                            self._styles_default
                        )
                    )
                    _text.append(
                        Paragraph(
                            "",
                            self._styles_space
                        )
                    )

        else:
            exit(
                "Novigrad encountered an error checking, " +
                "whether the database is non-empty."
            )

        self._doc_param.build(_text)
