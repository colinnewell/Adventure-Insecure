from ldap3 import Connection, SUBTREE
from ldap3.utils.dn import escape_attribute_value


class LDAP:

    def __init__(self, server, dn):

        self.server = server
        self.dn = dn

    def connection(self, user=None, password=None):
        conn = Connection(self.server, user=user, password=password)
        conn.bind()
        return conn

    def find_user_by_email(self, email):
        entry = self.user_info_by_email(email, ['dn'])
        if entry:
            return entry['dn']
        return None

    def user_info_by_email(self, email, attributes):
        search_filter = '(mail=%s)' % escape_attribute_value(email)
        base = 'ou=People,%s' % self.dn
        c = self.connection()
        c.search(
            search_base=base,
            search_filter=search_filter,
            search_scope=SUBTREE,
            attributes=attributes,
            size_limit=1,
            time_limit=5,
        )
        for entry in c.response:
            return entry
        return None

    def check_password(self, user_dn, password):
        c = Connection(self.server, user=user_dn, password=password)
        return c.bind()
