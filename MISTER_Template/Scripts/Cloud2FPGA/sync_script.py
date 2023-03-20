
import requests
import json
import math
import os


def get_data(data_location):
    f = open(data_location,"r")
    return f.read()






global ip_addr 
ip_addr = get_data("ip_addr.txt")
global payload 
user_id = get_data("id_user.txt")
payload = {'value':user_id}
payload2 = {'value':user_id, 'play_flag':'Play megaman'}


try:
    r = requests.get('http://'+ ip_addr +':8000/account/UserSync', params=payload) #getting account info
    print("get")
    print(r.status_code)
    if r.status_code == 200:
        server_variables = json.loads(r.text)
        print(server_variables)

    print("put")
    r1 = requests.put('http://'+ ip_addr +':8000/account/UserSync', data=json.dumps(payload2))
    print(r1.status_code)
    print(r1.content)
    # print((payload2))
    # print(json.dumps(payload2))


except requests.exceptions.RequestException as e:
    raise SystemExit(e)