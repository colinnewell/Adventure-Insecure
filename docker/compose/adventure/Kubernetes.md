# Running with Kubernetes

This is very early stages work to run the site under Kubernetes.

Note that we need to do things like utilize secrets.

```
kubectl create -f deployments/*
kubectl create -f services/*
```

## Database upgrade

```
kubectl create -f jobs/db-update.yml
```

## Site url from Minikube

```
minikube service nginx --url
```
