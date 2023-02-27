kubectl apply -f yaml/ingest-namespace.yaml
. scripts/.env
envsubst < yaml/ingest-deployment.yaml | kubectl apply -f -
unset DATABASE_URL
kubectl apply -f yaml/ingest-service.yaml

kubectl apply -f yaml/ingest-ingress.yaml
wait_time=60
echo "going to wait ${wait_time} seconds to check the ingress"
sleep ${wait_time}
kubectl get ingress -n ingest