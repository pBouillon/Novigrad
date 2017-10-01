# -*- coding: utf-8 -*-
# author: FlorianVaissiere - https://github.com/FlorianVaissiere

import sys
sys.path.append('src')

from src.com.novigard.util.pdf_generator import Pdf_Generator
import unittest.mock
from unittest.mock import patch

class TestMailingMethods(unittest.TestCase):

    def test_generatePDF(self):
        with patch.object(Pdf_Generator, 'generatePDF', return_value=True) as mock:
            pdf = Pdf_Generator()
            pdf.generatePDF()
            self.assertEquals(mock.return_value, True)

if __name__ == '__main__':
    unittest.main()