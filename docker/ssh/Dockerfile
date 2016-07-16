# sshd
#
# VERSION               0.0.2

FROM debian:jessie
MAINTAINER Colin Newell <colin.newell@gmail.com>
# based on config by Sven Dowideit <SvenDowideit@docker.com>

COPY ldap-selections /tmp
RUN debconf-set-selections /tmp/ldap-selections
RUN apt-get update && apt-get install -y openssh-server libnss-ldapd sudo 
RUN mkdir /var/run/sshd
RUN echo 'root:screencast' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config
COPY sudoers /etc/sudoers.d/access-role-developer

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
RUn echo 'session    required    pam_mkhomedir.so skel=/etc/skel/ umask=0077' >> /etc/pam.d/common-session:

#ENV NOTVISIBLE "in users profile"
#RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]