import redis as redis_cli
import os
from datetime import datetime

REDIS_HOST = os.getenv('REDIS_HOST', '')
VIDEO_ID = os.getenv('VIDEO_ID', '')

redis = redis_cli.Redis(host=REDIS_HOST, db=0)

KEYS = ['id', 'snippet.publishedAt', 'snippet.displayMessage', 'authorDetails.displayName']
NAME_KEY = 'id'
TIMESTAMP_KEY = 'snippet.publishedAt'
EXPIRE = 259200


def set_video_id():
    if VIDEO_ID is None:
        raise Exception
    redis.set('video_id', VIDEO_ID)
    redis.expire('video_id', EXPIRE)

    return


def del_video_id():
    redis.delete('video_id')
    return


def set_message(message):
    try:
        name = message.get(NAME_KEY, '')
        for key in KEYS:
            redis.hset(name, key, message.get(key, ''))

        score = datetime.fromisoformat(message.get(TIMESTAMP_KEY, '')).timestamp()
        redis.zadd('keys_%s' % VIDEO_ID, {name: score})

        redis.expire(name, EXPIRE)
        redis.expire('keys_%s' % VIDEO_ID, EXPIRE)

    except Exception as e:
        # 処理を継続する
        print(message)
        print(e)


def delete_video_id():
    redis.delete('video_id')
