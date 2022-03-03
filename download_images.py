import csv
import os

import requests
from tqdm import tqdm


# Example URL:
# https://icons.wowdb.com/retail/medium/achievement_level_10.jpg


def download_files(urls, download_dir, extension='.jpg'):
    """
    Downloads files from a url list
    """
    with requests.Session() as request:
        for url in urls:
            name = url.split('.jpg')[0].split('/')[-1]
            response = request.get(url, stream=True)

            total_size_in_bytes = int(response.headers.get('content-length', 0))
            block_size = 1024
            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, colour='blue')

            if response.status_code == 200:
                path = os.path.join(download_dir, name + extension)
                with open(path, 'wb') as file:
                    for data in response.iter_content(block_size):
                        progress_bar.update(len(data))
                        file.write(data)

            progress_bar.close()

            if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                print('Something went wrong!')


def get_urls_from_csv(path, limit=None):
    urls = []
    count = 0
    with open(path) as achievements_csv:
        reader = csv.reader(achievements_csv, delimiter=',')
        # Omit headers
        next(reader)
        for row in reader:
            if limit:
                count += 1
            if limit and count > limit:
                break

            url = row[5]
            urls.append(url)

    return urls


achievements_urls = get_urls_from_csv('./data/achievements.csv')
download_files(achievements_urls, './static/achievements')
