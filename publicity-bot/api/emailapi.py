# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
This implementation does its best to follow the Robert Martin's Clean code guidelines.
The comments follows the Google Python Style Guide:
    https://github.com/google/styleguide/blob/gh-pages/pyguide.md
"""

__copyright__ = 'Copyright 2021, FCRlab at University of Messina'
__author__ = 'Lorenzo Carnevale <lcarnevale@unime.it>'
__credits__ = ''
__description__ = 'SMTP Gmail Client'

import ssl
import logging
from smtplib import SMTP_SSL
from email.mime.text import MIMEText

class EmailAPI:

    def __init__(self, host, port, email_from, emails_to, emails_cc, subject, body, password):
        """EmailAPI inizializer.

        Args:
            host: 
            emails_to (list<str>): email addresses of the recipients.
            emails_cc (list<str>): email addresses of the carbon copy recipients.
            subject (str): the subject of the email message.
            body (str): the text of the email message.
        """
        self.__host = host
        self.__port = port
        self.__email_from = email_from
        self.__emails_to = emails_to
        self.__emails_cc = ','.join(emails_cc)
        self.__emails_subject = subject
        self.__emails_body = body
        self.__password = password
        self.__setup_logging()

    def __setup_logging(self, verbosity=False):
        """
        TODO: store log into a specific path
        """
        format = "%(asctime)s %(filename)s:%(lineno)d %(levelname)s - %(message)s"
        # filename='log/mailcli.log'
        datefmt = "%d/%m/%Y %H:%M:%S"
        level = logging.INFO
        if (verbosity):
            level = logging.DEBUG
        # logging.basicConfig(filename=filename, filemode='a', format=format, level=level, datefmt=datefmt)
        logging.basicConfig(format=format, level=level, datefmt=datefmt)

    def send_all(self):
        """Send message to all emails
        """
        logging.info('SUBJECT %s' % (self.__emails_subject))
        context = ssl.create_default_context()
        with SMTP_SSL(self.__host, self.__port, context=context) as client:
            # client.set_debuglevel(verbose)
            client.login(self.__email_from, self.__password)
            for to in self.__emails_to:
                message = self.__create_message(self.__email_from, to, self.__emails_cc)
                self.__send_message(client, self.__email_from, to, message)

    def __create_message(self, email_from, email_to, email_cc):
        """Create the message for an email.

        Args:
            to (str): email address of the recipients.

        Returns:
            An object containing a base64url encoded email object.
        """
        message = MIMEText(self.__emails_body, 'plain')
        message['from'] = email_from
        message['to'] = email_to
        message['cc'] = email_cc
        message['subject'] = self.__emails_subject
        return message.as_string()

    def __send_message(self, client, email_from, to, message):
        """Send an email message.

        Args:
            to (str)
            message (dict): Message to be sent.
        """
        logging.info('send email to %s' % (to))
        try:
            client.sendmail(email_from, to, message)
            logging.info('send email to %s ... completed' % (to))
        except Exception as e:
            logging.error('send email to %s ... failed because %s' % (to, e))
