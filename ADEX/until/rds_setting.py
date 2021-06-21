import redis

# from config.dataConfig import redisparams

# pool = redis.ConnectionPool(host=redisparams.get('host'), port=redisparams.get('port'),
#                             password=redisparams.get('pwd'), db=redisparams.get('db'))


pool = redis.Connection(host='localhost', port=6379, db=0)


redisConnect = redis.Redis(connection_pool=pool)


class RedisUtil:
    @staticmethod
    def get(name):
        return

    @staticmethod
    def set(name, value):
        return redisConnect.set(name, value)

    @staticmethod
    def publish(channel, msg):
        redisConnect.publish(channel, msg)


