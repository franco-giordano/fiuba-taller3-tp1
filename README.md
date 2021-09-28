# fiuba-taller3-tp1

Bucket URL: https://storage.googleapis.com/fgiordano-static/index.html

Deploy cloud func: `gcloud functions deploy get-counter --region=southamerica-east1 --entry-point get_counter --runtime python39 --trigger-http --allow-unauthenticated`

Pubsub:
- https://cloud.google.com/functions/docs/calling/pubsub
- reqs.txt: `google-cloud-pubsub` (creo)

TODO:
- duplicate inc function: one http-exposed and publish in pubsub, other pubsub-triggered and update firestore