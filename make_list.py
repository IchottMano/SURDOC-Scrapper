from os import path, mkdir, listdir
from bs4 import BeautifulSoup as BSoup
from re import compile

list_path = 'images{}list.txt'.format(path.sep)


def append_to_list(num, offset, link):
    if not offset:
        with open(list_path, 'a', encoding='utf-8') as text:
            text.write('{} - {}\n'.format(str(num).zfill(4), link))
    else:
        with open(list_path, 'a', encoding='utf-8') as text:
            text.write('{}_{} - {}\n'.format(str(num).zfill(4), offset, link))


def get_image_link_html(request, num):
    """
    Fetches link from HTML code and downloads image
    :param request: Request Object
    :param num: Page number
    :return: None
    """
    # Arranges HTML data to BeautifulSoup format
    html_data = BSoup(request, 'html.parser')

    # Searches for link with "original" in name
    lnk = html_data.body.find_all(href=compile("original"))
    if len(lnk) == 1:
        append_to_list(num, 0, lnk[0].attrs['href'])
    elif not len(lnk):
        pass  # TODO
    else:
        counter = 1
        for image in lnk:
            append_to_list(num, counter, image.attrs['href'])
            counter += 1
    return None


if __name__ == '__main__':

    if not path.isdir('images'):
        mkdir('images')
        with open('images{}list.txt'.format(path.sep), 'w', encoding='utf-8') as txt:
            pass

    for htmlfile in listdir('html'):
        with open('html{}{}'.format(path.sep, htmlfile), 'rb') as file:
            page = file.read()
        number = int(htmlfile.split('.')[0])
        get_image_link_html(page, number)

