#!/usr/bin/python3
"""Quicktest
Usage:
    quicktest.py search <host> <email>
    quicktest.py login <host> <dn> <password>
    quicktest.py login_by_email <host> <email> <password>
    quicktest.py (-h | --help | --version)
Options:
    -h, --help            Show this screen and exit.
"""
from ldap import LDAP
from docopt import docopt
from ldap3 import Server, Connection


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Quicktest 0.1')
    server = arguments['<host>']
    l = LDAP(Server(server), 'dc=adventure,dc=org') 
    if arguments['search']:
        e = l.user_info_by_email(arguments['<email>'], ['displayName'])
        print(e)
    if arguments['login']:
        if l.check_password(arguments['<dn>'], arguments['<password>']):
            print("Logged in")
        else:
            print("FAIL")
    if arguments['login_by_email']:
        dn = l.find_user_by_email(arguments['<email>'])
        if dn:
            if l.check_password(dn, arguments['<password>']):
                print("Logged in")
            else:
                print("FAIL")
        else:
            print("FAIL")
