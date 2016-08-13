all: ldap-image nginx-image ssh-image adventure-image

ldap-image:
	docker build -t adventure/ldap ldap

nginx-image:
	docker build -t adventure/nginx nginx

ssh-image:
	docker build -t adventure/sshd ssh

adventure-image:
	docker build -t adventure/adventure ..

tag:
	docker tag adventure/adventure quay.io/colinn/adventure-site
	docker tag adventure/ldap quay.io/colinn/adventure-ldap
	docker tag adventure/nginx quay.io/colinn/adventure-nginx
	docker tag adventure/ssh quay.io/colinn/adventure-ssh

push:
	docker push quay.io/colinn/adventure-site
	docker push quay.io/colinn/adventure-ldap
	docker push quay.io/colinn/adventure-nginx
	docker push quay.io/colinn/adventure-ssh

update:
	docker pull debian:jessie
	docker pull osixia/openldap
	docker pull python:3
	docker pull nginx
