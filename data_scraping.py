from bs4 import BeautifulSoup as BSoup
from os import path, listdir
import json


def get_artist(data):
    for data_string in data:
        if data_string.find('Creador:') != -1:
            return data_string[(data_string.find('Creador:') + 8):data_string.find('Dimensiones:')].split(',')[0]
    return 'N/A'


def get_object(data):
    for data_string in data:
        if data_string.find('Objeto:') != -1:
            return data_string[(data_string.find('Objeto:') + 7):data_string.find('Creador:')]
    return 'N/A'


def get_title(data):
    has_title = False
    for data_string in data:
        if has_title:
            return data_string.rstrip()
        elif data_string.find('Título') != -1:
            has_title = True
            continue
        else:
            continue
    return 'N/A'


def get_technique_material(data):
    for data_string in data:

        # Word finding
        if data_string.find('Técnica / Material:') != -1:
            my_str = data_string
            second_limit = my_str.find('Transcripción:')
            if second_limit != -1:
                my_str = my_str[:second_limit]
            third_limit = my_str.find('Descripción:')
            if third_limit != -1:
                my_str = my_str[:third_limit]
            my_str = my_str[(my_str.find('Técnica / Material:') + 19):]
            my_list = my_str.strip(' - ').replace(' - ', ', ').split(', ')
            good_list = list()

            # Word separation
            for word in my_list:
                if word.istitle():
                    good_list.append(word)
                else:
                    buffer = ''
                    for x in range(len(word)):
                        if word[x].isupper():
                            if not x:
                                buffer += word[x]
                            else:
                                if word[x-1] == ' ':
                                    buffer += word[x]
                                else:
                                    good_list.append(buffer)
                                    buffer = ''
                                    buffer += word[x]
                        else:
                            buffer += word[x]
                    if buffer:
                        good_list.append(buffer)
            my_str = ', '.join(good_list)
            return my_str
    return 'N/A'


def get_date(data):
    for data_string in data:
        if data_string.find('Fecha de creación:') != -1:
            my_str = data_string
            second_limit = my_str.find('Historia')
            if second_limit != -1:
                my_str = my_str[:second_limit]
            third_limit = my_str.find('Referencias')
            if third_limit != -1:
                my_str = my_str[:third_limit]
            fourth_limit = my_str.find('Estilo')
            if fourth_limit != -1:
                my_str = my_str[:fourth_limit]
            my_str = my_str[(my_str.find('Fecha de creación:') + 18):]
            my_str = my_str.replace('\xa0', '').lstrip()
            return my_str
    return 'N/A'


def get_features(request, num):

    html_data = BSoup(request, 'html.parser', from_encoding='utf-8')

    data_list = list(filter(lambda x: not (x == '' or x == ' ' or x[0] == ' '), html_data.get_text().split('\n')))
    index_list = list()
    for a in range(len(data_list)):
        if "CDATA" in data_list[a]:
            index_list.append(a)
    data = data_list[index_list[-2]+3:index_list[-1]]
    del data_list, index_list
    infodict = {}

    tecnica = "Técnica/Material"
    titulo = 'Título'

    infodict.update({'Artista': get_artist(data)})
    infodict.update({tecnica: get_technique_material(data)})
    infodict.update({'Objeto': get_object(data)})
    infodict.update({titulo: get_title(data)})
    infodict.update({'Fecha': get_date(data)})

    return infodict


if __name__ == "__main__":

    with open('data.json', 'w', encoding="utf-8") as f:
        json.dump(dict(), f, ensure_ascii='False')

    for htmlfile in listdir('html'):
        with open('html{}{}'.format(path.sep, htmlfile), 'rb') as file:
            page = file.read()
        number = int(htmlfile.split('.')[0])
        if not path.isfile('images{}{}.jpg'.format(path.sep, str(number).zfill(4))) and \
                not path.isfile('images{}{}_1.jpg'.format(path.sep, str(number).zfill(4))):
            continue
        else:
            feat = get_features(page, number)

            with open('data.json', 'r', encoding="utf-8") as f:
                data = json.load(f)

                data.update({int(number): feat})

            with open('data.json', 'w', encoding='utf-8') as f:
                raw = json.dump(data, f, indent=1, ensure_ascii=False)

            print('ready data {}'.format(number))



