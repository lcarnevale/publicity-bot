# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""googleapi.py

This implementation does its best to follow the Robert Martin's Clean code guidelines.
The comments follows the Google Python Style Guide:
    https://github.com/google/styleguide/blob/gh-pages/pyguide.md
"""


import pickle
import base64
import os.path
import logging
from apiclient import errors
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


# If modify these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

class GoogleAPI:

    def __init__(self, emails_to, emails_cc, subject, body):
        """GoogleAPI inizializer.

        Args:
            emails_to (list<str>): email addresses of the recipients.
            emails_cc (list<str>): email addresses of the carbon copy recipients.
            subject (str): the subject of the email message.
            body (str): the text of the email message.
        """
        self.__emails_to = emails_to
        self.__emails_cc = ','.join(emails_cc)
        self.__emails_subject = subject
        self.__emails_body = body
        self.__service = build('gmail', 'v1', credentials=self.__get_credentials())
        self.__setup_logging()

    def __get_credentials(self):
        """Read or download the user token.

        The file token.pickle stores the user's access and refresh tokens. It is
        created automatically when the authorization flow completes the first
        request. If there are no (valid) credentials available, the user logs-in 
        using the browser.
        
        Returns:
            An object containing the user credentials.
        """
        credentials = None
        token_filepath = 'token.pickle'
        credentials_filepath = 'credentials.json'
        if os.path.exists(token_filepath):
            with open(token_filepath, 'rb') as token:
                credentials = pickle.load(token)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_filepath, SCOPES)
                credentials = flow.run_local_server(port=0)
            with open(token_filepath, 'wb') as token:
                pickle.dump(credentials, token)
        
        return credentials

    def __setup_logging(self, verbosity=False):
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
        for to in self.__emails_to:
            message = self.__create_message(to, self.__emails_cc)
            self.__send_message(to, message)

    def __create_message(self, to, cc):
        """Create the message for an email.

        Args:
            to (str): email address of the recipients.

        Returns:
            An object containing a base64url encoded email object.
        """
        message = MIMEText(self.__emails_body)
        message['to'] = to
        message['cc'] = cc
        message['subject'] = self.__emails_subject
        return {
            'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()
        }
    
    def __send_message(self, to, message, user_id='me'):
        """Send an email message.

        Args:
            to (str)
            user_id (str): User's email address. The special value "me"
                can be used to indicate the authenticated user.
            message (dict): Message to be sent.
        """
        try:
            message = (self.__service.users().messages().send(userId=user_id, body=message).execute())
            logging.info('[%s] - TO %s - CC %s' % (message['id'], to, self.__emails_cc))
        except errors.HttpError as e:
            logging.error('Error sending message to %s: %s' % (to, e))