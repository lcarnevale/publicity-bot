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
from api.google.googleapi import GoogleAPI


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

    parser.add_argument('-t', '--to',
                        dest='emails_to_file',
                        help='CSV formatted file containing To emails.',
                        type=str,
                        required=True)

    parser.add_argument('-c', '--cc',
                        dest='emails_cc_file',
                        help='CSV formatted file containing CC emails.',
                        type=str)

    parser.add_argument('-s', '--subject',
                        dest='subject',
                        help='Subject of the email.',
                        type=str,
                        required=True)

    parser.add_argument('-b', '--body',
                        dest='body_file',
                        help='File containing the text of the email.',
                        type=str,
                        required=True)

    options = parser.parse_args()

    verbosity = options.verbosity

    emails_to = read_to_emails(options.emails_to_file)
    emails_cc = read_cc_emails(options.emails_cc_file)
    emails_subject = options.subject
    emails_body = read_body(options.body_file)
    
    gapi = GoogleAPI(emails_to, emails_cc, emails_subject, emails_body)
    gapi.send_all()

def read_to_emails(emails_to_file):
    return pd.read_csv(emails_to_file)['to']

def read_cc_emails(emails_cc_file):
    emails_cc = []
    if emails_cc_file:
        cc = pd.read_csv(emails_cc_file)['cc']
    return emails_cc

def read_body(body_file):
    body = ''
    with open(body_file, 'r') as f:
        body = f.read()
    return body


if __name__ == '__main__':
    main()