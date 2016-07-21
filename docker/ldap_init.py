#!/usr/bin/python
from ldap3 import Server, Connection, ALL


class LDAP:

    def __init__(self, connection, dn):

        self.connection = connection
        self.raise_exceptions = True
        self.dn = dn

    def add_group(self, name, id_num):
        self.connection.add('cn=%s,ou=Groups,%s' % (name, self.dn), 'posixGroup', {
            'cn': name,
            'gidNumber': id_num,
        })

    def add_sudo_group(self, group):
        self.connection.add('cn=%s,ou=SUDOers,%s' % (group, self.dn), 
                ['top', 'sudoRole'], {
            'cn': group,
            'sudoUser': group,
            'sudoHost': 'ALL',
            'sudoCommand': 'ALL',
        })

    def add_user(self, username, name, surname, password, group_id, user_id):
        # escape usernames
        # FIXME: hash password.
        self.connection.add('uid=%s,ou=People,%s' % (username, self.dn), ['posixAccount','inetOrgPerson', 'shadowAccount'], {
            'uid': username,
            'sn': surname,
            'displayName': name,
            'cn': name,
            'userPassword': password,
            'gidNumber': group_id,
            'uidNumber': user_id,
            'homeDirectory': '/home/%s' % username,
            'loginShell': '/bin/bash',
            'gecos': '',
            'description': 'Test user',
        })


server = Server('172.21.0.2')
conn = Connection(server, user="cn=admin,dc=adventure,dc=org", password="notaverysecurepassword")
conn.bind()
ldap = LDAP(conn, 'dc=adventure,dc=org')

ldap.add_group('developers', 5000)
ldap.add_user('dev1', 'Developer 1', '1', 'insecure', 5000, 10000)
ldap.add_sudo_group('%developers')

