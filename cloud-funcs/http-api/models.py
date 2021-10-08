from google.cloud import firestore
import random
from datetime import datetime

class Shard(object):
    """
    A shard is a distributed counter. Each shard can support being incremented
    once per second. Multiple shards are needed within a Counter to allow
    more frequent incrementing.
    """

    def __init__(self):
        self._count = 0

    def to_dict(self):
        return {"count": self._count}


class Counter(object):
    """
    A counter stores a collection of shards which are
    summed to return a total count. This allows for more
    frequent incrementing than a single document.
    """

    def __init__(self, num_shards, collection_name):
        self._num_shards = num_shards
        self._collection_name = collection_name

    def init_counter(self, doc_ref):
        """
        Create a given number of shards as
        subcollection of specified document.
        """
        col_ref = doc_ref.collection(self._collection_name)

        # Initialize each shard with count=0
        for num in range(self._num_shards):
            shard = Shard()
            col_ref.document(str(num)).set(shard.to_dict())

    def increment_counter(self, doc_ref):
        """Increment a randomly picked shard."""
        doc_id = random.randint(0, self._num_shards - 1)

        shard_ref = doc_ref.collection(self._collection_name).document(str(doc_id))
        return shard_ref.update({"count": firestore.Increment(1)})
    
    def get_count(self, doc_ref):
        """Return a total count across all shards."""
        total = 0
        shards = doc_ref.collection(self._collection_name).list_documents()
        for shard in shards:
            total += shard.get().to_dict().get("count", 0)
        return total

class ExpiringCache:
    def __init__(self, ttl_sec):
        self._ttl_sec = ttl_sec
        self._cache = {}
    
    def put(self, key, value):
        self._cache[key] = (value, datetime.now())
    
    def get(self, key):
        if key not in self._cache:
            raise KeyError
        
        pair = self._cache[key]

        if (datetime.now() - pair[1]).seconds >= self._ttl_sec:
            # expired
            del self._cache[key]
            raise KeyError
        else:
            return pair[0]
