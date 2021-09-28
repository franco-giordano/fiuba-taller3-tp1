from google.cloud import firestore
from models import Counter
# import logging

# logger = logging.getLogger('root')
# logger.setLevel(logging.DEBUG)
# logger.debug("Logging started")

SHARDS_AMOUNT = 20

def init_counter(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    if request.args and 'type' in request.args:
        # Add a new document
        db = firestore.Client() # doc_ref
        counter = Counter(SHARDS_AMOUNT, request.args.get('type') + "_shards")
        counter.init_counter(db)
        # logger.info("Counter home created!")

        return f'Created shards for {request.args.get("type")}'
    else:
        return 'Provide type with ?type=...'

def get_counter(request):
    if request.args and 'type' in request.args:
        db = firestore.Client() # doc_ref
        counter = Counter(SHARDS_AMOUNT, request.args.get('type') + "_shards")
        return f'{counter.get_count(db)}'
    else:
        return 'Provide type with ?type=...'

def inc_counter(request):
    if request.args and 'type' in request.args:
        db = firestore.Client() # doc_ref
        counter = Counter(SHARDS_AMOUNT, request.args.get('type') + "_shards")
        counter.increment_counter(db)

        return f'OK'
    else:
        return 'Provide type with ?type=...'
