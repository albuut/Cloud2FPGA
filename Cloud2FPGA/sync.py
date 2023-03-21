import requests
import json
import os
import urllib.parse
import urllib.request
import subprocess
import time
import shutil

#Helper
def get_data(data_location):
    f = open(data_location,"r")
    return f.read()
#Boot Core
def get_core_type(location,core_type):
    search_location = location
    search = search_location.split('/')
    if core_type in search:
        return True
    else:
        return False
def change_dir(dir):
    cmd = f"cd {dir}"
    subprocess.run(cmd, shell=True)
def load_core(dir,location,id_user,ip_addr):
    change_dir(dir)
    if get_core_type(location,'NES'):              
        found_file = '../..' + location[3:]
        new_file = found_file.split('/')
        
        loc_exists = os.path.exists(found_file)
        while(not loc_exists):
            loc_exists = os.path.exists(found_file)
        
        nes_type = new_file[-1].split('.')[-1]
    
        if nes_type  == 'nes':
            new_file[-1] = 'boot1.rom'
        elif nes_type == 'fds':
            new_file[-1] = 'boot0.rom'
        elif nes_type == 'pal':
            new_file[-1] = 'boot3.rom'
            
        new_file = '/'.join(new_file)
        shutil.copy(found_file, new_file)
        
        new_exists = os.path.exists(new_file)
        while(not new_exists):
            new_exists = os.path.exists(new_file)
        
        nes_loc = f'/media/fat/_Console/NES_20221002.rbf'
        cmd = "echo 'load_core " + nes_loc + "' > /dev/MiSTer_cmd"
        subprocess.run(cmd, shell=True)
        flag_load = {'value':id_user, 'play_flag':None}
        requests.put('http://'+ ip_addr +':8000/account/UserSync', data=json.dumps(flag_load))
    elif get_core_type(location,'_Arcade'):
        found_file = '../..' + location[3:]
        loc_exists = os.path.exists(found_file)
        while(not loc_exists):
            loc_exists = os.path.exists(found_file)
        location = "/media/" + location  
        cmd = "echo 'load_core " + location + "' > /dev/MiSTer_cmd"
        subprocess.run(cmd, shell=True)
        flag_load = {'value':id_user, 'play_flag':None}
        requests.put('http://'+ ip_addr +':8000/account/UserSync', data=json.dumps(flag_load))
#Sync
def get_user_library(id_user,ip_addr):
    payload = {'value':id_user}
    r = requests.get('http://'+ ip_addr +':8000/account/userGame', params=payload)
    if r.status_code == 200:
        return json.loads(r.content)
def download_zip(game,new_state):
    if(game.get('game_type') == 'arcade'):
        urls = game.get('game_file_link').split(',')
        file_names = game.get('file_location').split(',')
        for i in range(len(file_names)):
            file_name = "../../" + file_names[i]
            if not os.path.exists(file_name):
                print(urls[i])
                print(file_name)
                urllib.request.urlretrieve(urls[i],file_name)
            new_state.append(file_name)
        
def download_mra_rbf(ip_addr, game, new_state):
    mra_location = urllib.parse.unquote("../.." + game.get('rma_file')[10:])
    rbf_location = urllib.parse.unquote("../.." + game.get('rbf_file')[10:])
        
    if not os.path.exists(mra_location):
        print(mra_location)
        url = 'http://' + ip_addr + ":8000" + game.get('rma_file')
        print(url)
        urllib.request.urlretrieve(url,mra_location)
    if not os.path.exists(rbf_location):
        print(mra_location)
        url = 'http://' + ip_addr + ":8000" + game.get('rbf_file')
        print(url)
        urllib.request.urlretrieve(url,rbf_location)
    new_state.append(mra_location)
    new_state.append(rbf_location)
def update_txt(file_location,data):
    data_set = set(data)
    data_set = list(data_set)
    with open(file_location, 'w') as f:
        f.writelines('\n'.join(data_set))
def read_txt(file_location):
    if not os.path.exists(file_location):
        open(file_location,'w')
    else:
        with open(file_location,'r') as file:
            lines = file.read().splitlines()
        return lines
def delete_games(prev_state,new_state):
    prev_set = set(prev_state)
    new_set = set(new_state)
    
    result_set = prev_set.difference(new_set)
    result_list = list(result_set)
    for game in result_list:
        if os.path.exists(game):
            os.remove(game)
        is_exist = os.path.exists(game)
        while(is_exist):
            is_exist = os.path.exists(game)
def update_storage(id_user,ip_addr):
    total, used, free = shutil.disk_usage('/')
    total_load = {'value':id_user, 'total_storage':total}
    requests.put('http://'+ ip_addr +':8000/account/UserSync', data=json.dumps(total_load))
    used_load = {'value':id_user, 'current_storage':used}
    requests.put('http://'+ ip_addr +':8000/account/UserSync', data=json.dumps(used_load))
def download(id_user,ip_addr):
    #get games from server
    user_library = get_user_library(id_user,ip_addr)
    #collect games to be downloaded
    if user_library is not None:
        new_state = []

        #Download games not on board
        for game in user_library:
            download_zip(game, new_state)
            download_mra_rbf(ip_addr, game, new_state)
    
        #Done Downloading, Update Server List
        update_txt("server_list.txt",new_state)
        prev_state = read_txt("device_list.txt")
    
        delete_games(prev_state, new_state)
    
        #Update Written List
        update_txt("device_list.txt",new_state)
        
        #reset flag
        flag_load = {'value':id_user, 'sync_flag':False}
        requests.put('http://'+ ip_addr +':8000/account/UserSync', data=json.dumps(flag_load))
        #update storage
        update_storage(id_user,ip_addr)

id_user = get_data('id_user.txt')
ip_addr = get_data('ip_addr.txt')
user_key = {'value':id_user}
root = '/'


while True:
    r = requests.get('http://'+ ip_addr +':8000/account/UserSync', params=user_key)
    if r.status_code == 200:
        user_data = json.loads(r.content)    

        sync_flag = user_data[0]['sync_flag']
        play_flag = user_data[0]['play_flag']

        if sync_flag:
            download(id_user,ip_addr)
        if play_flag:
            load_core('/', play_flag, id_user, ip_addr)                

    else:
        print("status_code:" + str(r.status_code))

    
