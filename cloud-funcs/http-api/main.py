from google.cloud import firestore
from google.cloud import pubsub_v1
from models import Counter

import base64
import json
import os

def fix_cors(f):
    def decorated(request):
        if request.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '3600'
            }

            return ('', 204, headers)

        headers = {
            'Access-Control-Allow-Origin': '*'
        }
        return (*f(request), headers)

    return decorated


# Instantiates a Pub/Sub client
publisher = pubsub_v1.PublisherClient()
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
TOPIC_NAME = os.getenv('TOPIC_NAME')  # "NEW_VISIT_EVENT"
SHARDS_AMOUNT = int(os.getenv('SHARDS_AMOUNT'))


def init_counter(request):
    request_json = request.get_json()
    if request_json and 'visit_type' in request_json:
        # Add a new document
        db = firestore.Client()  # doc_ref
        counter = Counter(
            SHARDS_AMOUNT, request_json['visit_type'] + "_shards")
        counter.init_counter(db)
        # logger.info("Counter home created!")

        return f"Created shards for {request_json['visit_type']}"
    else:
        return 'Provide type with ?visit_type=...'


@fix_cors
def get_counter(request):
    if request.args and 'visit_type' in request.args:
        db = firestore.Client()  # doc_ref
        counter = Counter(SHARDS_AMOUNT, request.args.get(
            'visit_type') + "_shards")
        return ({'msg': f'{counter.get_count(db)}'}, 200)
    else:
        return ({'err': 'Provide visit type with ?visit_type=...'}, 400)


@fix_cors
def inc_counter(request):
    # TODO:
    # - arreglar retry policies
    if request.method != 'POST':
        return ({'err': 'Method not allowed'}, 400)

    if request.args and 'visit_type' in request.args:
        message = request.args.get('visit_type')
        topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)
        message_json = json.dumps({'visit_type': message})
        message_bytes = message_json.encode('utf-8')
        try:
            publish_future = publisher.publish(topic_path, data=message_bytes)
            publish_future.result()  # Verify the publish succeeded
            return ({'msg': 'Message published.'}, 200)
        except Exception as e:
            print(e)
            return ({'err': e}, 500)

    else:
        return ({'err': 'Provide type with ?visit_type=...'}, 400)
