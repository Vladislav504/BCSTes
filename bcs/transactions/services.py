import requests


def get_new_address():
    url = "http://bcs_tester:iLoveBCS@140.82.36.227:3669"
    payload = {'jsonrpc': "2.0", 'id': "1", 'method': 'getnewaddress'}
    response = requests.post(url, json=payload)
    return response.json()['result']


