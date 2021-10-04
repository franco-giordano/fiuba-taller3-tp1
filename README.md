# fiuba-taller3-tp1

Bucket URL: https://storage.googleapis.com/fgiordano-static/
App URL: https://southamerica-east1-taller3-fgiordano.cloudfunctions.net/app?page=home

Deploy cloud func: `gcloud functions deploy get-counter --region=southamerica-east1 --entry-point get_counter --runtime python39 --trigger-http --allow-unauthenticated`

Deploy with topic trigger: `gcloud functions deploy FUNC_NAME --trigger-topic MY_TOPIC --region=southamerica-east1 --entry-point ENTRYPOINT --runtime python39`

Pubsub:
- https://cloud.google.com/functions/docs/calling/pubsub
- reqs.txt: `google-cloud-pubsub` (creo)

TODO:
- review deduplication methods and ACK in gcloud pubsub
- decide on retry policy for fetch() in main.js


INFRA TESTS:
- using memorystore
- more/less collection shards
- more/less max instances in gcfs?