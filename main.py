from pathlib import Path
import random
from urllib.parse import urljoin

from environs import Env
import requests


def download_image(url, filename, payload=None):
    file_path = Path.cwd() / filename

    response = requests.get(url, params=payload)
    response.raise_for_status()

    with open(file_path, 'wb') as file:
        file.write(response.content)

    return file_path


def get_comics_count():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['num']


def get_comics(comics_number):
    url = f'https://xkcd.com/{comics_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    response = response.json()
    return response['img'], response['alt']


def call_vk_api(url, payload):
    response = requests.get(
        url,
        params=payload
    )
    response.raise_for_status()
    response = response.json()
    if 'error' in response:
        raise requests.exceptions.HTTPError(response['error'])
    return response


def publish_image(group_id, base_url, base_payload, file_path, comment):
    def call_vk(method, payload):
        url = urljoin(base_url, method)
        payload = base_payload | payload
        return call_vk_api(url, payload)

    payload = {
        'group_id': group_id,
    }
    upload_url = call_vk('photos.getWallUploadServer', payload)['response']['upload_url']

    with open(file_path, 'rb') as file:
        response = requests.post(upload_url, files={'photo': file})
        response.raise_for_status()
    response = response.json()
    if 'error' in response:
        raise requests.exceptions.HTTPError(response['error'])

    payload = {
        'group_id': group_id,
        'server': response['server'],
        'photo': response['photo'],
        'hash': response['hash'],
    }
    response = call_vk('photos.saveWallPhoto', payload)['response'][0]

    payload = {
        'owner_id': -group_id,
        'from_group': 1,
        'attachments': f'photo{response["owner_id"]}_{response["id"]}',
        'message': comment,
    }
    call_vk('wall.post', payload)


if __name__ == '__main__':
    env = Env()
    env.read_env()

    comics_count = get_comics_count()
    comics_number = random.randint(1, comics_count)
    comics_image, comment = get_comics(comics_number)
    file_path = download_image(comics_image, 'current_comics.png')

    vk_access_token = env.str('VK_ACCESS_TOKEN')
    group_id = env.int('VK_GROUP_ID')
    api_version = env.str('VK_API_VERSION', '5.131')
    base_url = 'https://api.vk.com/method/'
    base_payload = {
        'access_token': vk_access_token,
        'v': api_version,
    }

    publish_image(
        group_id,
        base_url,
        base_payload,
        file_path,
        comment,
    )

    try:
        file_path.unlink()
    except:
        print('Error while deleting file', file_path)
