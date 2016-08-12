#!/usr/bin/python
from ldap3 import Server, Connection, ALL, MODIFY_ADD
from ldap3.utils.dn import escape_attribute_value
import string
from crypt import crypt
from random import SystemRandom


class LDAP:

    def __init__(self, connection, dn):

        self.connection = connection
        self.raise_exceptions = True
        self.dn = dn

    def add_group(self, name, id_num):
        self.connection.add('cn=%s,ou=Groups,%s' % (escape_attribute_value(name), self.dn), 'posixGroup', {
            'cn': name,
            'gidNumber': id_num,
        })

    def add_sudo_group(self, group):
        self.connection.add('cn=%s,ou=SUDOers,%s' % (escape_attribute_value(group), self.dn), 
                ['top', 'sudoRole'], {
            'cn': group,
            'sudoUser': group,
            'sudoHost': 'ALL',
            'sudoCommand': 'ALL',
        })

    def add_user(self, username, name, surname, password, group_id, user_id):
        alphabet = string.ascii_letters + string.digits
        salt = ''.join(SystemRandom().choice(alphabet) for i in range(16))
        c = '{crypt}' + crypt(password, '$6$%s$' % salt)
        self.connection.add('uid=%s,ou=People,%s' % (escape_attribute_value(username), self.dn), ['posixAccount','inetOrgPerson', 'shadowAccount'], {
            'uid': username,
            'sn': surname,
            'displayName': name,
            'cn': name,
            'userPassword': c,
            'gidNumber': group_id,
            'uidNumber': user_id,
            'homeDirectory': '/home/%s' % username,
            'loginShell': '/bin/bash',
            'gecos': '',
            'mail': '%s@babel.com' % username,
            'description': 'Test user',
        })

    def add_user_to_group(self, username, group):
        self.connection.modify('cn=%s,ou=Groups,%s' % (escape_attribute_value(group), self.dn),
                {
                    'memberUid': [(MODIFY_ADD, [username])],
                })


server = Server('172.23.0.3')
conn = Connection(server, user="cn=admin,dc=adventure,dc=org", password="notaverysecurepassword")
conn.bind()
ldap = LDAP(conn, 'dc=adventure,dc=org')

ldap.add_group('developer', 5000)
ldap.add_user('dev1', 'Developer 1', '1', 'insecure', 5000, 10000)
ldap.add_user_to_group('dev1', 'developer')
ldap.add_sudo_group('%developer')
ldap.add_sudo_group('dev1')

