from redis_om import get_redis_connection


redis = get_redis_connection(host="localhost", port="6379", password="sOmE_sEcUrE_pAsS", decode_responses=True)
