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


def get_wall_upload_server(vk_access_token, api_version, group_id):
    base_url = 'https://api.vk.com/method/'
    method = 'photos.getWallUploadServer'
    payload = {
        'access_token': vk_access_token,
        'v': api_version,
        'group_id': group_id,
    }
    response = requests.get(
        urljoin(base_url, method),
        params=payload
    )
    response.raise_for_status()
    response = response.json()
    if 'error' in response:
        raise requests.exceptions.HTTPError(response['error'])
    return response['response']['upload_url']


def upload_file(upload_url, file_path):
    with open(file_path, 'rb') as file:
        response = requests.post(upload_url, files={'photo': file})
    response.raise_for_status()
    response = response.json()
    if 'error' in response:
        raise requests.exceptions.HTTPError(response['error'])
    return response


def save_wall_photo(vk_access_token, api_version, group_id, server, photo, hash):
    base_url = 'https://api.vk.com/method/'
    method = 'photos.saveWallPhoto'
    payload = {
        'access_token': vk_access_token,
        'v': api_version,
        'group_id': group_id,
        'server': server,
        'photo': photo,
        'hash': hash,
    }
    response = requests.get(
        urljoin(base_url, method),
        params=payload
    )
    response.raise_for_status()
    response = response.json()
    if 'error' in response:
        raise requests.exceptions.HTTPError(response['error'])
    return response['response'][0]


def post_photo(vk_access_token, api_version, group_id, owner_id, photo_id, message):
    base_url = 'https://api.vk.com/method/'
    method = 'wall.post'
    payload = {
        'access_token': vk_access_token,
        'v': api_version,
        'owner_id': -group_id,
        'from_group': 1,
        'attachments': f'photo{owner_id}_{photo_id}',
        'message': message,
    }
    response = requests.get(
        urljoin(base_url, method),
        params=payload
    )
    response.raise_for_status()
    response = response.json()
    if 'error' in response:
        raise requests.exceptions.HTTPError(response['error'])


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

    try:
        upload_url = get_wall_upload_server(vk_access_token, api_version, group_id)
        upload_response = upload_file(upload_url, file_path)
        save_response = save_wall_photo(vk_access_token,
                                        api_version,
                                        group_id,
                                        upload_response['server'],
                                        upload_response['photo'],
                                        upload_response['hash'])
        post_photo(vk_access_token,
                   api_version,
                   group_id,
                   save_response["owner_id"],
                   save_response["id"],
                   comment)
    finally:
        file_path.unlink()
