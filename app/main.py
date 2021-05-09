# -*- coding: utf-8 -*-

from controllers import youtube, redis
from time import sleep
import traceback


def main():
    try:
        redis.set_video_id()
        active_live_chat_id = youtube.get_active_live_chat_id()
        page_token = None

        while True:
            messages, page_token = youtube.get_livechat_message(active_live_chat_id, page_token)
            print('got %s message(s)' % len(messages))

            for message in messages:
                redis.set_message(message)

            if page_token is None:
                break

            sleep(5)
    except RuntimeError:
        print(traceback.format_exc())
    finally:
        redis.delete_video_id()


if __name__ == '__main__':
    main()
