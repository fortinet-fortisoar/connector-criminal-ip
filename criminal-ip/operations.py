"""
Copyright start
MIT License
Copyright (c) 2024 Fortinet Inc
Copyright end
"""

import requests
import time
from connectors.core.connector import get_logger, ConnectorError

logger = get_logger('criminal-ip')


def make_api_call(method="GET", endpoint="", config=None, params=None, data=None, json_data=None):
    try:
        headers = {
            "x-api-key": config.get('api_key')
        }
        server_url = config.get('server_url').strip('/')
        if not server_url.startswith('https://') and not server_url.startswith('http://'):
            server_url = "https://" + server_url
        server_url = server_url + endpoint
        response = requests.request(method=method,
                                    url=server_url,
                                    headers=headers, data=data, json=json_data, params=params,
                                    verify=config.get('verify_ssl'))

        if response.ok and (response.json().get('status') not in [401, 413, 414, 415, 500, 403]):
            return response.json()
        else:
            if response.text != "":
                err_resp = response.json()
                failure_msg = err_resp['message']
                error_msg = 'Response [{0}: Details: {1}]'.format(err_resp.get('status'),
                                                                  failure_msg if failure_msg else '')
            else:
                error_msg = 'Response [{0}:{1}]'.format(response.status_code, response.reason)
            logger.error(error_msg)
            raise ConnectorError(error_msg)
    except requests.exceptions.SSLError:
        logger.error('An SSL error occurred')
        raise ConnectorError('An SSL error occurred')
    except requests.exceptions.ConnectionError:
        logger.error('A connection error occurred')
        raise ConnectorError('A connection error occurred')
    except requests.exceptions.Timeout:
        logger.error('The request timed out')
        raise ConnectorError('The request timed out')
    except requests.exceptions.RequestException:
        logger.error('There was an error while handling the request')
        raise ConnectorError('There was an error while handling the request')
    except Exception as err:
        raise ConnectorError(str(err))


def get_domain_reputation(config, params):
    endpoint = "/v1/domain/scan"
    response = make_api_call(method='POST', endpoint=endpoint, data=params, config=config)
    data = response.get('data')
    while not data:
        time.sleep(15)
        response = make_api_call(method='POST', endpoint=endpoint, data=params, config=config)
        data = response.get('data')
    scan_id = response.get('data').get('scan_id')
    get_scan_status(scan_id, config)
    return make_api_call(method='GET', endpoint=f'/v2/domain/report/{scan_id}', data=params, config=config)


def get_scan_status(scan_id, config):
    endpoint = f"/v1/domain/status/{scan_id}"
    response = make_api_call(method='GET', endpoint=endpoint, config=config)
    scan_percentage = response.get('data', {}).get('scan_percentage')
    if scan_percentage == -1:
        raise ConnectorError('A connection error occurred')
    if scan_percentage == -2:
        raise ConnectorError('Domain does not exist')
    while scan_percentage != 100:
        time.sleep(15)
        response = make_api_call(method='GET', endpoint=endpoint, config=config)
        scan_percentage = response.get('data', {}).get('scan_percentage')


def _check_health(config):
    try:
        endpoint = f"/v1/user/me"
        make_api_call(method='POST', endpoint=endpoint, config=config)
        return True
    except Exception as e:
        logger.error("Invalid Credentials: %s" % str(e))
        raise ConnectorError("Invalid Credentials")


operations = {
    'get_url_reputation': get_domain_reputation,
    'get_ip_reputation': get_domain_reputation,
    'get_domain_reputation': get_domain_reputation
}
