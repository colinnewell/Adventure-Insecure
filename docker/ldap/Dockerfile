FROM osixia/openldap
MAINTAINER Colin Newell <colin.newell@gmail.com>

COPY perms.ldif /container/service/slapd/assets/config/bootstrap/ldif/02-security.ldif
COPY schema.OpenLDAP /container/service/slapd/assets/config/bootstrap/schema/mmc/sudo.schema
