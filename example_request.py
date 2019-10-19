from datetime import datetime
import requests
from requests.exceptions import Timeout, ConnectionError
import config

# my id 248960000
def _is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def _log(message, response=None):
    print(message)
    if response:
        print(response)
    print('=======================')


def _make_request(url, kind, data=None):
    """
    Выполняет get запрос к серверу и производит авторизацию при запросе

    :param url: url запроса
    :param technical_login: технический логин бота
    :param password: пароль

    :return: словарь с ответом сервера или None в случае ошибки
    """
    technical_login = config.SERVER_LOGIN
    password = config.SERVER_PASSWORD

    _log('Current request:\nURL: {url}\nLogin: {login}\nPassword: {password}'.format(
        url=url, login=technical_login, password=password
    ))

    try:
        #обработка видов запросов
        if kind == 'post':
            r = requests.post(url, auth=(technical_login, password))
        elif kind == 'delete':
            r = requests.delete(url, auth=(technical_login, password))
        elif kind == 'get':
            r = requests.get(url, auth=(technical_login, password))
        elif kind == 'json':
            r = requests.post(url, json=data, auth=(technical_login, password))
    except Timeout:
        _log('Timeout error')
        return None
    except ConnectionError:
        _log('Connection error')
        return None

    try:
        json_request = r.json()
    except:
        json_request = "The request is empty"

    if not r.ok:
        _log('Status error', json_request)
        return None

    if json_request == "The request is empty":
        _log("The request is empty")
        return None

    print(json_request)
    return json_request


def post_json(json1, json2):
    '''
        Пример post запроса с отправлением json
    '''
    url = '{base_url}/url_were_post'.format(base_url=config.BASE_URL)

    jjson = {
      "json1": json1,
      "json2": json2
    }
    _log('Current request:\n : post_json')
    response = _make_request(url, 'json', jjson)



def get_request(param):
    '''
    простой get запрос
    param: любой необходимый параметр для построения url
    :return: нужное значение
    '''
    url = '{base_url}/some_list/{param}'.format(base_url=config.BASE_URL, param=param)
    _log('Current request:\n get_request()\n param:{param}'.format(param=param))
    response = _make_request(url, 'get')
    if response is None:
        return None
    else:
        return response



def post_request(param_for_post):
    '''
    простой post запрос
    param_for_post: то, что нужно отправить на сервер
    :return:
    '''
    url = '{base_url}/place_for_post/{param_for_post}/'.format(base_url=config.BASE_URL, param_for_post=param_for_post)
    _log('Current request:\n post_request()')
    response = _make_request(url, 'post')
    if response is None:
        return None


def delete_request(param_for_delete):
    url = '{base_url}/root/remove/{param_for_delete}'.format(base_url=config.BASE_URL, param_for_delete=param_for_delete)
    _log('Current request:\n delete_request()')
    request = _make_request(url, 'delete')