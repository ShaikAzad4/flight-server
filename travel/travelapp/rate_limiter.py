import redis
from rest_framework.response import Response
from rest_framework.exceptions import Throttled

redist_client = redis.StrictRedis(host='localhost',port=
                                  6379, db=0, decode_responses=True)
def rate_limit(max_requests:int, time_window:int):
    def decorator(func):
        def wrapper(self, request, *args, **kwargs):
            client_id = request.user.id if request.user.is_authenticated else request.META.get('REMOTE_ADDR')
            endpoint = request.path
            redis_key = f'rate_limit:{client_id}:{endpoint}'

            current_requests = redist_client.get(redis_key)

            if current_requests is None:
                redist_client.set(redis_key,1,ex=time_window)
            elif int(current_requests) < max_requests:
                redist_client.incr(redis_key)
            else:
                retry_after = redist_client.ttl(redis_key)
                raise Throttled(
                    detail=f"Rate limit exceeded! Try again after {retry_after}"
                )
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator