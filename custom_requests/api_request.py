import requests
from config_data.config import RAPID_API_KEY, RAPID_API_HOST


def api_request(method_endswith=str,
                params=dict,
                method_type=str
                ):
    """
    This function makes requests to API

    :param method_endswith: depends on the GET method
    :param params: optional parameters as API requires
    :param method_type: GET or POST
    :return: data in json format
    """

    url = f"https://motorcycles-by-api-ninjas.p.rapidapi.com{method_endswith}"

    if method_type == 'GET':
        return get_request(
            url=url,
            params=params
        )
    else:
        return post_request(
            url=url,
            params=params
        )


def get_request(url, params):
    try:
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
            print('Сбой запроса к серверу')
    except Exception as exc:
        print(exc, type(exc), 'Что-то пошло не так.. Попробуйте ещё раз.')


# def post_request(url, params):
#     try:
#         response = requests.post(
#                 url,
#                 headers={"X-RapidAPI-Key":  RAPID_API_KEY,
#                          "X-RapidAPI-Host": RAPID_API_HOST},
#                 params=params,
#                 timeout=15
#         )
#         if response.status_code == requests.codes.ok:
#             print(response.json())
#             return response.json()
#     except Exception as exc:
#         print(exc, type(exc), 'Что-то пошло не так.. Попробуйте ещё раз.')
