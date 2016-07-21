# sshd
#
# VERSION               0.0.2

FROM debian:jessie
MAINTAINER Colin Newell <colin.newell@gmail.com>
# based on config by Sven Dowideit <SvenDowideit@docker.com>

COPY ldap-selections /tmp
RUN debconf-set-selections /tmp/ldap-selections
RUN apt-get update && apt-get install -y openssh-server libnss-ldapd sudo-ldap
RUN mkdir /var/run/sshd
RUN echo 'root:screencast' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config
COPY sudoers /etc/sudoers.d/access-role-developer

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
RUN echo 'session    required    pam_mkhomedir.so skel=/etc/skel/ umask=0077' >> /etc/pam.d/common-session:
RUN echo '-:ALL EXCEPT root (login):ALL EXCEPT LOCAL' >> /etc/security/access.conf
RUN echo "sudoers_base ou=SUDOers,dc=adventure,dc=org" >>/etc/ldap/ldap.conf
RUN echo "BASE dc=adventure,dc=org" >>/etc/ldap/ldap.conf
RUN echo "URI  ldap://ldap/ " >>/etc/ldap/ldap.conf


#ENV NOTVISIBLE "in users profile"
#RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22
COPY entrypoint.sh /entrypoint.sh
CMD ["/entrypoint.sh"]
