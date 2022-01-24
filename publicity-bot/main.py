# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""main.py

This implementation does its best to follow the Robert Martin's Clean code guidelines.
The comments follows the Google Python Style Guide:
    https://github.com/google/styleguide/blob/gh-pages/pyguide.md
"""

__copyright__ = 'Copyright 2021, FCRlab at University of Messina'
__author__ = 'Lorenzo Carnevale <lcarnevale@unime.it>'
__credits__ = 'Christian Sicari <csicari@unime.it>'
__description__ = 'This project aims making easy the delivery of Call For Papers invitations.'


import argparse
import pandas as pd
from api.emailapi import EmailAPI


def main():
    description = ('%s\n%s' % (__author__, __description__))
    epilog = ('%s\n%s' % (__credits__, __copyright__))
    parser = argparse.ArgumentParser(
        description = description,
        epilog = epilog
    )

    parser.add_argument('-v', '--verbosity',
                        dest='verbosity',
                        help='Logging verbosity level',
                        action="store_true")

    parser.add_argument('-H', '--host',
                        dest='host',
                        help='SMTP hostname',
                        type=str,
                        required=True)

    parser.add_argument('-p', '--port',
                        dest='port',
                        help='SMTP port',
                        type=int,
                        required=True)

    parser.add_argument('-f', '--from',
                        dest='email_from',
                        help='From email.',
                        type=str,
                        required=True)

    parser.add_argument('-t', '--to',
                        dest='email_to_file',
                        help='CSV formatted file containing To emails.',
                        type=str,
                        required=True)

    parser.add_argument('-c', '--cc',
                        dest='email_cc_file',
                        help='CSV formatted file containing CC emails.',
                        type=str)

    parser.add_argument('-s', '--subject',
                        dest='email_subject_file',
                        help='File containing the subject of the email.',
                        type=str,
                        required=True)

    parser.add_argument('-b', '--body',
                        dest='email_body_file',
                        help='File containing the text of the email.',
                        type=str,
                        required=True)

    options = parser.parse_args()

    verbosity = options.verbosity

    host = options.host
    port = options.port
    email_from = options.email_from
    email_to = read_email_to(options.email_to_file)
    email_cc = read_email_cc(options.email_cc_file)
    email_subject = read_email_subject(options.email_subject_file)
    email_body = read_email_body(options.email_body_file)
    password = input("Type your password and press enter: ")
    
    api = EmailAPI(
        host,
        port,
        email_from,
        email_to,
        email_cc,
        email_subject,
        email_body,
        password
    )
    api.send_all()

def read_email_to(email_to_file):
    return pd.read_csv(email_to_file)['to']

def read_email_cc(email_cc_file):
    email_cc = []
    if email_cc_file:
        cc = pd.read_csv(email_cc_file)['cc']
    return email_cc

def read_email_subject(email_subject_file):
    subject = ''
    with open(email_subject_file, 'r') as f:
        subject = f.read()
    return subject 

def read_email_body(email_body_file):
    body = ''
    with open(email_body_file, 'r') as f:
        body = f.read()
    return body


if __name__ == '__main__':
    main()