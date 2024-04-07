def get_api_url(prefix='', version='v1', app_name='', url_name=''):
    url = f'{prefix}/{version}/' if prefix and version else f'{version}/'

    if app_name:
        url = f'{url}{app_name}'

    if url_name:
        url = f'{url}{url_name}'

    return url