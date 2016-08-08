#!/bin/sh
docker inspect --format '{{ range .NetworkSettings.Networks}}{{ .Gateway }}{{end}}' adventure_site_1
