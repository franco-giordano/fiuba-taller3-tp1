from google.cloud import firestore
from models import Counter
import base64
import json

SHARDS_AMOUNT = 20
TOPIC_NAME = "NEW_VISIT_EVENT"

# def get_counter(request):
#     if request.args and 'type' in request.args:
#         db = firestore.Client() # doc_ref
#         counter = Counter(SHARDS_AMOUNT, request.args.get('type') + "_shards")
#         return f'{counter.get_count(db)}'
#     else:
#         return 'Provide type with ?type=...'

# subscribed to topic
def store_incremented_counter(event, context):
    # print("""This Function was triggered by messageId {} published at {} to {}
    # """.format(context.event_id, context.timestamp, context.resource.get('data', None)))

    sent_dict = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    # print('cosa: {}'.format(cosa))
    # visit_type = sent_dict['visit_type']

    if sent_dict and 'visit_type' in sent_dict:
        db = firestore.Client() # doc_ref
        counter = Counter(SHARDS_AMOUNT, sent_dict.get('visit_type') + "_shards")
        counter.increment_counter(db)
