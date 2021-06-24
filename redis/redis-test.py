"This is a script to test connection to a redis cluster during 1000 seconds"

import redis
import time
import os

print('Starting Redis connection test script...')

r = redis.StrictRedis(host='<our redis endpoint>', port=<your redis port>, db=0)

def redis_availability(r):
    try:
        r.ping()
        print("Successlully connected to redis!!")
    except (redis.exceptions.ConnectionError, ConnectionRefusedError):
        print('No connection to REDIS server')
        return False
    return True
    
if redis_availability(r):
    print('Setting a test key!!' + ' ' + str(r.set('test_key', '123')))

    for i in range(1000):
        try:
            print('Getting test_key: ' + str(r.get('test_key')))
            time.sleep(1)
        except (redis.exceptions.ConnectionError, ConnectionRefusedError):
            print('we lost connection to Redis!')
            continue