#!/bin/sh
ldapsearch -x -h 172.21.0.2 -b 'dc=adventure,dc=org' '(objectclass=*)'
