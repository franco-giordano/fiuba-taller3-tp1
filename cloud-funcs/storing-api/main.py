from google.cloud import firestore
from models import Counter
import base64
import json
import os

SHARDS_AMOUNT = int(os.getenv('SHARDS_AMOUNT'))

# subscribed to topic
def store_incremented_counter(event, context):
    # TODO: analizar deduplication
    
    sent_dict = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    
    if sent_dict and 'visit_type' in sent_dict:
        db = firestore.Client() # doc_ref
        counter = Counter(SHARDS_AMOUNT, sent_dict.get('visit_type') + "_shards")
        counter.increment_counter(db)
