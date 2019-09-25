# https://m.golfzon.com/webs/game/nasmo/user?filter=0&size=500
# login
# data를 저장.


import os
import json
import requests


JSON_FILENAME = 'nasmo.json'
DOWNLOAD_DIR = 'nasmo'


def get_filename_from_url(url):
    try:
        d = url.split('/')
        filename = d[-1]
        return filename
    except Exception as e:
        return None


def main():
    nasmo_dir = os.path.join(os.getcwd(), DOWNLOAD_DIR)
    os.makedirs(nasmo_dir, exist_ok=True)
    json_data = open(JSON_FILENAME, encoding='UTF-8').read()
    data = json.loads(json_data)

    if 'results' in data and 'data' in data['results'] and 'entitys' in data['results']['data']:
        items = data['results']['data']['entitys']

    listfile = os.path.join(nasmo_dir, 'filelist.txt')
    f = open(listfile, 'w')
    for item in items:
        url = item['movieUrl']
        filename = get_filename_from_url(url)
        res = requests.get(url, allow_redirects=True)
        filepath = os.path.join(nasmo_dir, filename)
        open(filepath, 'wb').write(res.content)
        f.write("file '{}'\n".format(filename))
    f.close()

    os.chdir(nasmo_dir)
    os.system('ffmpeg -f concat -i filelist.txt -c copy nasmo.mp4')


if __name__ == "__main__":
    main()
