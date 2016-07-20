#!/bin/sh
IP=`docker inspect --format '{{ range .NetworkSettings.Networks}}{{ .IPAddress }}{{end}}' adventure_ldap_1`
ldapsearch -x -h $IP -b 'dc=adventure,dc=org' '(objectclass=*)'
