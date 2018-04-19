# -*- coding: utf-8 -*-
# author: FlorianVaissiere - https://github.com/FlorianVaissiere

import unittest.mock
from unittest.mock import patch

from pdfgenerator import PdfGenerator


class TestMailingMethods(unittest.TestCase):

    def test_generatePDF(self):
        with patch.object(PdfGenerator, 'generatePDF', return_value=True) as mock:
            pdf = PdfGenerator()
            pdf.generate_pdf({})
            self.assertEquals(mock.return_value, True)


if __name__ == '__main__':
    unittest.main()
