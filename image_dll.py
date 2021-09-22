import os
import sys
from urllib.request import urlretrieve
from urllib.error import HTTPError

list_path = 'images{}list.txt'.format(os.path.sep)

if __name__ == '__main__':
    if not os.path.isfile(list_path):
        sys.exit(1)
    else:
        with open(list_path, 'r', encoding='utf-8') as img_list:
            for line in img_list:
                line_clean = line.rstrip().split(' - ')
                name = line_clean[0]
                link = line_clean[1]
                try:
                    if not os.path.isfile("images/{}.jpg".format(name)):
                        urlretrieve(link, "images/{}.jpg".format(name))
                        print('Image {} get'.format(name))
                    else:
                        continue
                except HTTPError:
                    continue
