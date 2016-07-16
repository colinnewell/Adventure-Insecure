all: ldap-image nginx-image ssh-image adventure-image

ldap-image:
	docker build -t adventure/ldap ldap

nginx-image:
	docker build -t adventure/nginx nginx

ssh-image:
	docker build -t adventure/sshd ssh

adventure-image:
	docker build -t adventure/adventure ..
