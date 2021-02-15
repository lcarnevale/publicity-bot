# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""mailcli

This implementation does its best to follow the Robert Martin's Clean code guidelines.
The comments follows the Google Python Style Guide:
    https://github.com/google/styleguide/blob/gh-pages/pyguide.md
"""

__copyright__ = 'Copyright 2021, FCRlab at University of Messina'
__author__ = 'Christian Sicari <csicari@unime.it>, Lorenzo Carnevale <lcarnevale@unime.it>'
__credits__ = ''
__description__ = 'mailcli'


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
                        dest='emails_to',
                        help='CSV formatted file containing To emails.',
                        type=str,
                        required=True)

    parser.add_argument('-c', '--cc',
                        dest='emails_cc',
                        help='CSV formatted file containing CC emails.',
                        type=str)

    parser.add_argument('-s', '--subject',
                        dest='subject',
                        help='Subject of the email.',
                        type=str)

    parser.add_argument('-b', '--body',
                        dest='body',
                        help='Text of the email.',
                        type=str)

    parser.add_argument('-B', '--bodyfile',
                        dest='body_file',
                        help='File containing the text of the email.',
                        type=str)

    options = parser.parse_args()

    verbosity = options.verbosity
    to = pd.read_csv(options.emails_to)['to']
    cc = []
    if options.emails_cc:
        cc = pd.read_csv(options.emails_cc)['cc']
    subject = options.subject
    body_file = options.body_file
    body = options.body
    with open(body_file, 'r') as f:
        body = f.read()
    from_ = "FCRLab Unime"
    
    gapi = GoogleAPI(from_, to, cc, subject, body)
    gapi.send_all()

if __name__ == '__main__':
    main()