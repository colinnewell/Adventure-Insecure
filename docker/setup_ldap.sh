#!/bin/sh
IP=`docker inspect --format '{{ range .NetworkSettings.Networks}}{{ .IPAddress }}{{end}}' adventure_ldap_1`
echo ldapadd -x -h $IP -D cn=admin,dc=adventure,dc=org -w notaverysecurepassword -f initial_schema.ldif
ldapadd -x -h $IP -D cn=admin,dc=adventure,dc=org -w notaverysecurepassword -f initial_schema.ldif
echo installed posix schemas.
echo ldapsearch -x -h $IP -b dc=adventure,dc=org -D "cn=admin,dc=adventure,dc=org" -w devpassword
ldapsearch -x -h $IP -b dc=adventure,dc=org -D "cn=admin,dc=adventure,dc=org" -w notaverysecurepassword
