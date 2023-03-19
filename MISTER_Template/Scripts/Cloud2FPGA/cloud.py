import subprocess
import datetime
import urllib.parse

import requests
import json
import math
import os
import shutil
import time

#request logic

#Board Logic
def change_dir(dir):
    cmd = f"cd {dir}"
    subprocess.run(cmd, shell=True)
def load_core(dir,location):
    change_dir(dir)
    cmd = "echo 'load_core " + location + "' > /dev/MiSTer_cmd"
    subprocess.run(cmd, shell=True)
def get_data(data_location):
    if os.path.exists(data_location):
        f = open(data_location,"r")
        data = f.read()
        f.close()
    return data
def get_file_type(file):
    copy_file = file
    return copy_file.split('.')[-1]
def is_game_file(file):
    copy_file = file
    file_type = get_file_type(copy_file)
    if (file_type == 'zip' or file_type == 'rbf' or file_type == 'mra'):
        return True
    else:
        return False
def extract_server_list(library_location):
    if os.path.exists(library_location):
        f = open(library_location,"r")
        lines = f.readlines()
        f.close()
        games = []
        files_to_check = []
        data = []
        for L in lines:
            L = L.strip('\n')
            games.append(L.split(','))
        for game in games:
            temp = []
            if 'core' in game:
                for g in game:
                    g = urllib.parse.unquote(g)
                    temp.append(g)
            if 'arcade' in game:
                for g in game:
                    g = urllib.parse.unquote(g)
                    g = g.split('/')
                    temp.append(g[-1])
            data.append(temp)
        for i in range(len(data)):
            if 'arcade' in data[i]:
                data[i] = [*set(data[i])]
        return data
    else:
        print("Failure to open")
def check_directory(file_list):
    if 'arcade' in file_list:
        core_type = 'arcade'
        file_list.remove('arcade')
        game_files = []
        
        for f in file_list:
            if(is_game_file(f)):
                game_files.append(f)
        file_list.clear()
        
        check_files = []
        for game in game_files:
            root = "/media/fat/"
            game_type = get_file_type(game)
            if game_type == 'zip':
                root1 = root + "games/mame/" + game
                root2 = root + "games/hbmame/" + game
                if os.path.exists(root1):
                    check_files.append(game)
                if os.path.exists(root2):
                    check_files.append(game)
            elif game_type == 'mra':
                root = root + "_Arcade/" + game
                if os.path.exists(root):
                    check_files.append(game)
            elif game_type == 'rbf':
                root = root + "_Arcade/cores/" + game
                if os.path.exists(root):
                    check_files.append(game)
        set1 = set(game_files)
        set2 = set(check_files)
        unique_values = set1.difference(set2) | set2.difference(set1)
        
        if(len(list(unique_values)) != 0):
            file_list.append(list(unique_values))   
    elif 'core' in file_list:
        if(os.path.exists(file_list[1])):
            file_list.clear()
def is_synced(library_location):
    file = extract_server_list(library_location)
    for f in file:
        check_directory(f)
    file = [lst for lst in file if lst]           
    if len(file) == 0:
        return True
    else:
        return False 
''' 
def files_to_delete(prev_state,new_state):
    delete_list = []
    for prev in prev_state:
        for new in new_state:
            if not (prev[0] in new):
                delete_list.append(prev)
                break
    return delete_list
def is_deleted(delete_list):
    check_files = []
    for d_list in delete_list:
        if 'arcade' in d_list:
            for d in d_list:
                root = "/media/fat/"
                game_type = get_file_type(d)
                if(game_type == 'zip'):
                    root1 = root + "games/mame/" + d
                    root2 = root + "games/hbmame/" + d
                    if os.path.exists(root1):
                        check_files.append(d)
                    if os.path.exists(root2):
                        check_files.append(d)
                elif game_type == 'mra':
                    root = root + "_Arcade/" + d
                    if os.path.exists(root):
                        check_files.append(d)
                elif game_type == 'rbf':
                    root = root + "_Arcade/cores/" + d
                    if os.path.exists(root):
                        check_files.append(d)         
        elif 'core' in d_list:
            if(os.path.exists(file_list[1])):
                check_files.append(d_list)
    print(check_files)
    if(len(check_files) == 0):
        return True
    else:
        return False
'''

root = "/"
id_user = get_data("id_user.txt")
ip_addr = get_data("ip_addr.txt")
payload = {'value':id_user}

while True:
    try:
        r = requests.get('http://'+ ip_addr +':8000/account/UserSync', params=payload) #getting account info

        if r.status_code == 200:
            server_variables = json.loads(r.text)
        
            sync_flag = server_variables[0]['sync_flag']
            sync_done_flag = server_variables[0]['sync_done_flag']
            play_flag = server_variables[0]['play_flag']
        
            #Current Limitation is only Arcade Cores
            #you set play_flag to the file location
            if(play_flag):
                load_core(root,play_flag)
                #print("Playing a game")
                time.sleep(5)
                #Send a post since to update played
        
            if(sync_flag):
                print("Calling a sync")
                cmd = ['python','sync.py']
                subprocess.call(cmd)
                sync_status = is_synced('serverList.txt')
                while not sync_status:
                    sync_status = is_synced('serverList.txt')
                    print("not all synced")
                    time.sleep(1)
                #Send a Post to tell done
                print("sync done")
                time.sleep(5)
                sd_path = "/media/fat"
                storage = shutil.disk_usage(sd_path)
        print("Polling")
        time.sleep(5)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

#loads game
#location = "/media/fat/_Arcade/Athena.mra"
#load_core(root,location)