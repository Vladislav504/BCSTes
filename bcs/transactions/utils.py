import requests
from requests.models import Response
from typing import Any, List
from django.conf import settings

from .exceptions import NoRequestError, RequestError


def check_response(response: Response):
    '''
    Проверка статусе запроса
    Вызывает RequestError или NoRequestError
    '''
    if not response:
        raise NoRequestError()
    if not response.ok:
        raise RequestError()


class HttpRequester:
    '''
    Вспомогательный класс, расширяет get и post методов requests проверкой статуса запроса.
    '''
    check = check_response

    @classmethod
    def get(cls, url: str):
        response = requests.get(url)
        cls.check(response)
        return response

    @classmethod
    def post(cls, url: str, payload: dict):
        response = requests.post(url, json=payload)
        cls.check(response)
        return response


def log(message):
    '''
    Лог сообщения в консоль
    '''
    print(message)


def log_error(error_class: Exception, message: str):
    '''
    Декоратор для перехвата и логгирования ошибок, используется для дебага
    Ошибка вызывается заново после завершения логгирования
    '''
    def catch_error(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except error_class as e:
                log(message)
                raise error_class(message)

        return wrapper

    return catch_error


def make_rpc_request(method: str, params: List[Any] = None):
    '''
    Отправляем запрос к серверу на выполнение метода через JSON RPC.
    '''
    url = settings.RPC_URL
    payload = {'jsonrpc': "2.0", 'id': "1", 'method': method}
    if params is not None:
        payload['params'] = params
    response = requests.post(url, json=payload)
    log(response.text)
    content = response.json()
    if content['error']:
        raise RequestError()
    return content
