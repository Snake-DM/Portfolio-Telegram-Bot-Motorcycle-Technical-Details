from collections.abc import Iterable
from typing import Callable, Any
from loguru import logger

import requests
from config_data.config import RAPID_API_KEY, RAPID_API_HOST


@logger.catch
def api_request(method_endswith: str,
                params: dict,
                method_type: str
                ) -> Any:
    """
    This function makes requests to API

    :param method_endswith: API url finish, it depends on the GET method
    :param params: optional parameters as API requires
    :param method_type: GET or POST
    :return: a function based on methods GET or POST
    """

    url = f"https://motorcycles-by-api-ninjas.p.rapidapi.com{method_endswith}"

    if method_type == 'GET':
        return get_request(url, params)


@logger.catch
def get_request(url: str, params: dict) -> Any:
    """
    Function gets data from a server based on API parameters

    :param url: str
    :param params: dict
    :return: json object
    """

    response = requests.get(
        url=url,
        headers={"X-RapidAPI-Key": RAPID_API_KEY,
                 "X-RapidAPI-Host": RAPID_API_HOST},
        params=params,
        timeout=15
    )
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        logger.debug('Server Error')
        return
