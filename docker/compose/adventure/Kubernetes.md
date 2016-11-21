# Running with Kubernetes

This is very early stages work to run the site under Kubernetes.

```
kubectl create secret generic adventure \
    --from-literal=postgres-password=anothernotverysecurepassword \
    --from-literal=postgres-user=adventure \
    --from-literal=connection-string=postgresql://adventure:anothernotverysecurepassword@db:5432/adventure \
    --from-literal=ldap-admin-password=notaverysecurepassword \
    --from-literal=ldap-domain=adventure.org \
    --from-literal=ldap-organisation=Adventure

kubectl create -f deployments/
kubectl create -f services/
```

## Database upgrade

```
kubectl create -f jobs/db-update.yml
```

## Site url from Minikube

```
minikube service nginx --url
```
