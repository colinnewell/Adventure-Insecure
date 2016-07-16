#!/bin/sh
IP=`docker inspect --format '{{ range .NetworkSettings.Networks}}{{ .IPAddress }}{{end}}' adventure_ldap_1`
echo ldapsearch -x -h $IP -b dc=adventure,dc=org -D "cn=admin,dc=adventure,dc=org" -w \$password
ldapsearch -x -h $IP -b dc=adventure,dc=org -D "cn=admin,dc=adventure,dc=org" -w notaverysecurepassword
