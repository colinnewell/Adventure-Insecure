# Running with Kubernetes

This is very early stages work to run the site under Kubernetes.

Note that we need to do things like utilize secrets.

```
kubectl create secret generic adventure \
    --from-literal=postgres-password=anothernotverysecurepassword \
    --from-literal=postgres-user=adventure \
    --from-literal=connection-string=postgresql://adventure:anothernotverysecurepassword@db:5432/adventure \
    --from-literal=ldap-admin-password=notaverysecurepassword \
    --from-literal=ldap-domain=adventure.org \
    --from-literal=ldap-organisation=Adventure

for f in deployments/*; do kubectl create -f $f; done
for f in services/*; do kubectl create -f $f; done
```

## Database upgrade

```
kubectl create -f jobs/db-update.yml
```

## Site url from Minikube

```
minikube service nginx --url
```
