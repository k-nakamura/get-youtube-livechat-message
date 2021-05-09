# -*- coding: utf-8 -*-

from googleapiclient import discovery
from googleapiclient import errors
import os
from retry import retry

DEVELOPER_KEY = os.environ.get('API_KEY', '')
VIDEO_ID = os.getenv('VIDEO_ID', '')

api_service_name = "youtube"
api_version = "v3"

youtube = discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)


@retry(errors.HttpError, tries=5, delay=2)
def get_active_live_chat_id():
    response = youtube.videos().list(
        id=VIDEO_ID,
        part="liveStreamingDetails",
    ).execute()

    items = response.get('items', [])
    if len(items) > 0:
        return items[0].get('liveStreamingDetails', {}).get('activeLiveChatId')
    else:
        return ''


@retry(errors.HttpError, tries=5, delay=2)
def get_livechat_message(chat_id, page_token=None):
    response = youtube.liveChatMessages().list(
        liveChatId=chat_id,
        part="id,snippet,authorDetails",
        pageToken=page_token,
    ).execute()

    items = response.get('items', [])
    next_page_token = response.get('nextPageToken', None)

    formatted_items = []

    for i in items:
        formatted_i = __flatten_dict(i)
        formatted_i['snippet.publishedAt'] = __fix_timestamp_milli_sec_digits(formatted_i['snippet.publishedAt'])
        formatted_items.append(formatted_i)

    return formatted_items, next_page_token


# Python 3.9 required
def __flatten_dict(input_dict, prefixes=None):
    if prefixes is None:
        prefixes = []

    new_dict = {}
    for k, v in input_dict.items():
        if type(v) == dict:
            new_dict |= __flatten_dict(v, prefixes + [k])
        else:
            new_dict |= {'.'.join(prefixes + [k]): v}
    return new_dict


def __fix_timestamp_milli_sec_digits(s):
    # APIからのレスポンスのうち、タイムスタンプのミリ秒の桁数がまちまちなので補正する
    n = s.find('+') - s.find('.')
    return '+'.join([s.split('+')[0] + '0' * (7 - n), s.split('+')[1]])
