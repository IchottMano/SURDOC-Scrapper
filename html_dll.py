from urllib3 import PoolManager
import os
from time import sleep

http = PoolManager()
links = 'http://www.surdoc.cl/registro/2-{}'
pagenum = 5508
my_range = list(range(1, pagenum))


def is_ready(number):
    return '{}.html'.format(str(number).zfill(4)) in os.listdir('{}{}html'.format(os.getcwd(), os.path.sep))


if __name__ == '__main__':
    for num in my_range:
        if is_ready(num):
            pass
        else:
            page = http.request('GET', links.format(num))
            print('Got page {}.\n{} pages left.'.format(num, pagenum - num))
            with open('html{}{}.html'.format(os.path.sep, str(num).zfill(4)), 'wb') as htmlfile:
                htmlfile.write(page.data)
            sleep(0.5)
