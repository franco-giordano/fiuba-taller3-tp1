from google.cloud import firestore
from google.cloud import pubsub_v1
from models import Counter

import base64
import json
import os


# Instantiates a Pub/Sub client
publisher = pubsub_v1.PublisherClient()
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
TOPIC_NAME = "NEW_VISIT_EVENT"
SHARDS_AMOUNT = 20

# def init_counter(request):
#     """Responds to any HTTP request.
#     Args:
#         request (flask.Request): HTTP request object.
#     Returns:
#         The response text or any set of values that can be turned into a
#         Response object using
#         `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
#     """

#     if request.args and 'type' in request.args:
#         # Add a new document
#         db = firestore.Client() # doc_ref
#         counter = Counter(SHARDS_AMOUNT, request.args.get('type') + "_shards")
#         counter.init_counter(db)
#         # logger.info("Counter home created!")

#         return f'Created shards for {request.args.get("type")}'
#     else:
#         return 'Provide type with ?type=...'


def get_counter(request):
    if request.args and 'visit_type' in request.args:
        db = firestore.Client()  # doc_ref
        counter = Counter(SHARDS_AMOUNT, request.args.get('visit_type') + "_shards")
        return f'{counter.get_count(db)}'
    else:
        return ('Provide visit type with ?visit_type=...', 400)


def inc_counter(request):
    if request.args and 'visit_type' in request.args:
        # db = firestore.Client() # doc_ref
        # counter = Counter(SHARDS_AMOUNT, request.args.get('type') + "_shards")
        # counter.increment_counter(db)

        # request_json = request.get_json(silent=True)

        message = request.args.get('visit_type')

        print(f'Publishing message to topic {TOPIC_NAME}')

        # References an existing topic
        topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)

        message_json = json.dumps({'visit_type': message})
        message_bytes = message_json.encode('utf-8')

        # Publishes a message
        try:
            publish_future = publisher.publish(topic_path, message_bytes)
            publish_future.result()  # Verify the publish succeeded
            return 'Message published.'
        except Exception as e:
            print(e)
            return (e, 500)

    else:
        return ('Provide type with ?visit_type=...', 400)
