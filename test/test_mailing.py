# -*- coding: utf-8 -*-
# author: FlorianVaissiere - https://github.com/FlorianVaissiere

import sys
sys.path.append('src')

import src.com.novigard.util.mailing
from src.com.novigard.util.mailing import Mailing
import unittest.mock
from unittest.mock import patch

class TestMailingMethods(unittest.TestCase):

    def test_email_sender(self):
        with patch.object(Mailing, 'email_sender', return_value=True) as mock:
            mail = Mailing()
            mail.email_sender()
            self.assertEquals(mock.return_value, True) 



    def test_add_mailadress(self):
        _addmail = 'test@test.com'

        mail = Mailing()
        mail.add_mailadress(_addmail)

        self.assertEquals(mail._destination_mail[1], _addmail)   

if __name__ == '__main__':
    unittest.main()