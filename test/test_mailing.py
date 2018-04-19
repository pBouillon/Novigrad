# -*- coding: utf-8 -*-
# author: FlorianVaissiere - https://github.com/FlorianVaissiere

import unittest.mock
from unittest.mock import patch

from mailing import Mailing


class TestMailingMethods(unittest.TestCase):

    def test_email_sender(self):
        with patch.object(Mailing, 'email_sender', return_value=True) as mock:
            mail = Mailing()
            mail.email_sender()
            self.assertEquals(mock.return_value, True)

    def test_add_mail_address(self):
        address = 'test@test.com'

        mail = Mailing()
        mail.add_mail_address(address)

        self.assertEquals(mail._destination_mail[1], address)


if __name__ == '__main__':
    unittest.main()
