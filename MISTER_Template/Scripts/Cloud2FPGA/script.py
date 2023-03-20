
import requests
import json
import math
import os

def get_data(data_location):
    f = open(data_location,"r")
    return f.read()


class Hashmap:
    global ip_addr 
    ip_addr = get_data("ip_addr.txt")
    global payload 
    user_id = get_data("id_user.txt")
    payload = {'value':user_id}
    def __init__(self, arrSize):
        self.size = arrSize
        self.map = [None] * self.size

    def _get_hash(self, key):
    #    hash = 0
     #   hash = key % self.size
      #  return hash
        hash = 0
        for char in str(key):
            hash += ord(char)
        return hash % self.size
    
    
    def add(self, key, value):
        key_hash = self._get_hash(key)
        key_value = [key, value]

        if self.map[key_hash] is None: #if cell is empty assign it
            self.map[key_hash] = list([key_value])
            return True
        else: #else check if it already exists if not add it
            for pair in self.map[key_hash]: #iterate through each pair in the map
                if pair[0] == key:
                    #do nothing same key is in the table already
                    return True
            self.map[key_hash].append(key_value)# add on to that cell of the map
            return True
    def get(self, key):
        key_hash = self._get_hash(key)
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                # print("pair[0]")
                # print(pair[0])
                # print("key:")
                # print(key)
                # print("\n")
                if pair[0] == key:
                    return ("1")
        else:
            return ("None")
    
    def delete(self, key):
        key_hash = self._get_hash(key)

        if self.map[key_hash] is None:
            return False
        for i in range(0, len(self.map[key_hash])): # we need the index to remove something from python
            if self.map[key_hash][i][0] == key:
                self.map[key_hash].pop(i)
                return True
    
    def print(self):
        print('-----Games------')
        for item in self.map:
            if item is not None:
                #print('-----item:')
                #print(len(item))
                #print(((item[0]))) #prints out the first game
                                   #item[x][y]: x=game  y=0 or 1 (0=hash key)(1=game info) 
                print(str(item))

                # for i in range(len(item)):
                #     print("XXXX----------------------")
                #     print(i)
                #     print(item[i][1])
                #     print("----------------------XXX\n\n")

    
    def output_file(self):
        #open file
        f5 = open("misterList.txt","w")
        for item in self.map:
            if item is not None:
                #print(len(item[0]))
                for i in range(len(item)):
                    f5.write((item[i][1]))
                
        f5.close()
    
def write_Game(text):
    print(text)
    
    #split up the file ['Azurian Attack', '/media/rmaFolder/Azurian%20Attack.mra', '/media/rbfFolder/jtcps1_20220819.rbf','arcade','https://archive.org/download/MAME220RomsOnlyMerged/azurian.zip', 'games/mame/azurian.zip\n']
    game = text.split(',')
    if game[3] == "arcade":
        print("arcade")
        #get the rma file replace the %20 characters that show up from .get()
        #print((game[1].replace('%20',' ')))
        split = (game[1].replace('%20',' ')).split('/')
        mra = split[3]

        split = (game[2].replace('%20',' ')).split('/')
        rbf = split[3]



        #write the mra file
        r4 = requests.get('http://' + ip_addr + ':8000/media/rmaFolder/' + mra)
        with open('../../_Arcade/'+mra,'wb') as fx:
            fx.write(r4.content)
        python_sucks = 0

        #write the rbf file
        if os.path.exists('../../_Arcade/cores/'+rbf):
            python_sucks = python_sucks + 1
        else:
            print("Writing rbf file")
            r5 = requests.get('http://'+ ip_addr + ':8000/media/rbfFolder/' + rbf)
            with open('../../_Arcade/cores/'+rbf,'wb') as fy:
                fy.write(r5.content)

        

        #check how many files need to be downloaded subtract off the mra file and game name
        #divide for how many pairs of files and paths
        num_files = int((len(game) - 3)/2)
        file_link = [] #['https://archive.org/download/mame.0229/bilyard.zip']    
        file_path = [] #['games/mame/athena.zip\n']


        for i in range(num_files):
            file_link.append(game[i+4]) #plus 3 start at the first download link skip 'game_name' and 'rma' and rbf and game_type
        
        for i in range(num_files):
            file_path.append(game[(num_files+i+4)]) #plus 2 start at the first download link skip 'game_name' and 'rma' and rbf and game_type
                                            #plus num_files to skip over the file_link

        
        # print(num_files)
        # print("file_link") #['https://archive.org/download/MAME220RomsOnlyMerged/azurian.zip']
        # print(str(file_link))
        # print("\n")
        # print("file_path") #['games/mame/azurian.zip\n']
        # print(str(file_path))
        # print("\n")

        #output the files. the Zip files
        for i in range(num_files):
            r1 = requests.get((file_link[i].strip('\n')).strip(' '))
            #get file
            with open('../../'+(file_path[i].strip('\n')).strip(' '),'wb') as fx:
                fx.write(r1.content)
    elif game[3]== "core":
        print("arcade")
        split = (game[1].replace('%20',' ')).split('/')
        game_folder = split[3]
        print(game_folder) #GBA

        split = (game[2].replace('%20',' ')).split('/')
        zip_name = split[3] #megaman.zip
        print(zip_name)

        #write the mra file
        r4 = requests.get('http://' + ip_addr + ':8000/media/rmaFolder/' + zip_name)
        with open('../../games/'+game_folder+'/'+zip_name,'wb') as fx:
            fx.write(r4.content)
        

#same as write_Game but now delete
def delete_Game(text):
    
    #split up the file ['Azurian Attack', '/media/rmaFolder/Azurian%20Attack.mra', 'arcade' ,'https://archive.org/download/MAME220RomsOnlyMerged/azurian.zip', 'games/mame/azurian.zip\n']
    game = text.split(',')
    if game[3] == "arcade":
        #get the rma file replace the %20 characters that show up from .get()
        #print((game[1].replace('%20',' ')))
        split = (game[1].replace('%20',' ')).split('/')
        mra = split[3]

        split = (game[2].replace('%20',' ')).split('/')
        rbf = split[3]


        
        #delete MRA file
        if os.path.exists('../../_Arcade/'+mra):
            os.remove('../../_Arcade/'+mra)
        # else:
            #do not remove the rbf file since one core supports multiple arcade games
            #print("File does not exist")


        #check how many files need to be downloaded subtract off the mra file and game name
        #divide for how many pairs of files and paths
        num_files = int((len(game) - 3)/2)

        file_link = [] #['https://archive.org/download/mame.0229/bilyard.zip']    
        file_path = [] #['games/mame/athena.zip\n']

        for i in range(num_files):
            file_link.append(game[i+4]) #plus 3 start at the first download link skip 'game_name' and 'rma' and rbf and game_type
        
        for i in range(num_files):
            file_path.append(game[(num_files+i+4)]) #plus 3 start at the first download link skip 'game_name' and 'rma' and rbf and game_type
                                            #plus num_files to skip over the file_link

        # zip_file = file_link[0].split('/') #['https:', '', 'archive.org', 'download', 'MAME216RomsOnlyMerged', '1942.zip']
        # last_elem = (len(zip_file) - 1) #last element in the array is the file name
        # print("zip_file")
        # print(last_elem)


        #delete the zip files
        for i in range(num_files):
            if os.path.exists('../../'+(file_path[i].strip('\n')).strip(' ')):
                os.remove('../../'+(file_path[i].strip('\n')).strip(' '))
            # else:
            #     print("File does not exist")

        #delete MRA file
    elif game[3]== "core":
        split = (game[1].replace('%20',' ')).split('/')
        game_folder = split[3]
        print(game_folder) #GBA

        split = (game[2].replace('%20',' ')).split('/')
        zip_name = split[3] #megaman.zip
        print(zip_name)
        
        #delete MRA file
        if os.path.exists('../../games/'+game_folder+'/'+zip_name):
            os.remove('../../games/'+game_folder+'/'+zip_name)
        # else:
            #do not remove the rbf file since one core supports multiple arcade games
            #print("File does not exist")

#SENDING 2 GAMES [{} ,{}]
# [{'id': 1, 'game_name': '4D Warriors (315-5162)', 'game_file_link': 'https://archive.org/download/MAME216RomsOnlyMerged/4dwarrio.zip', 'file_location': 'games/mame/4dwarrio.zip', 'game_year': 9999, 'cover': 'https://www.igdb.com/ find the image', 'file_size': 10.0, 'rma_file': '/media/rmaFolder/4D%20Warriors%20(315-5162).mra', 'rbf_file': '/media/rbfFolder/SEGASYS1_20210618.rbf'},
# {'id': 4, 'game_name': 'Adventure Quiz Capcom World 2 -Japan 920611-', 'game_file_link': 'https://archive.org/download/MAME217RomsOnlyMerged/MAME%200.217%20ROMs%20%28merged%29.zip/cworld2j.zip', 'file_location': 'games/mame/cworld2j.zip', 'game_year': 1941, 'cover': 'https://www.igdb.com/ find the image', 'file_size': 10.0, 'rma_file': '/media/rmaFolder/Adventure%20Quiz%20Capcom%20World%202%20-Japan%20920611-.mra', 'rbf_file': '/media/rbfFolder/jtcps1_20220819.rbf'}]


#----------------------------------main code---------------------
try:
    python_sucks = 0
    r = requests.get('http://'+ ip_addr +':8000/account/userGame', params=payload) #getting account info
    #r = requests.get('http://127.0.0.1:8000/media/rmaFolder/19XX_The_War_Against_Destiny_Euro_960104.mra', params=payload) #downloading the file
    #print(r.status_code )
    if r.status_code == 200:

        #print("---------------------------------")
        #print("connected")


        #turn json text into python objects
        server_list = json.loads(r.text)
        #get the number of games
        web_num_games = len(server_list)
        #length of the table should be size*1.3
        hash_size = math.ceil(1.3*web_num_games)
        #create the serve Game list hashmap  
        h_web = Hashmap(hash_size)
        #Create a new file
        f = open("serverList.txt","w")
        #print(server_list)


        if server_list == []: #this when the server sends an empty list the hash wont be divided by zero
            print("no list on server")
    #-------Check if file exists and Check if the file is empty then Lines_test=0 else Lines_test>=1
            if os.path.exists("misterList.txt"):
                f_check = open("misterList.txt","r")
                Lines_test = f_check.readlines()
                f_check.close()

    #-------check if the misterList game file exists. if it does then delete all the game on the mister list
            if os.path.exists("misterList.txt") and (len(Lines_test)>0):
                print("there are games on mister")
                #print("file exists!!\n")
                #read in the file
                f2 = open("misterList.txt","r")
                #read the previous misterList.txt games
                Lines = f2.readlines()
                #get the size of the hash table
                hash_size = math.ceil(1.3*len(Lines))
                #create the Mister hashmap
                h_mister = Hashmap(hash_size)
                #The number of games currently in the misterList.txt
                mister_num_games = len(Lines)
                f2.close()
                #print(len(Lines))
    #-----------Add in the games to the mister hash map
                for x in range(mister_num_games): 
                    #get the current game string
                    game=Lines[x].split(',')
                    h_mister.add(game[0], Lines[x])
                
    #-----------#check to see if the misterList.txt games are on the web hash map, If not remove them from the Hash and delete the file
                for x in range(mister_num_games): 
                    #print("Remove the game here the function to remove the game file")
                    #print("Delete")
                    game=Lines[x].split(',')
                    print("Delete")
                    print(game[0])
                    h_mister.delete(game[0])
                    delete_Game(Lines[x])
                    f3 = open("misterList.txt","w") #write an empty file

                
            else:
                #do nothing the user is syncing with no games on the list and the mister file is empty
                python_sucks = 1
                print("no games on mister and server list is empty. do nothing")






#-------This means that the serve list is not empty so add/delete the games
        else:   
    #-------output the web server list to a file and add it to the hash table h_web. 
            #I get division by zero in modulus operator
            for x in range(web_num_games):
                output = (server_list[x]['game_name']+","+server_list[x]['rma_file']+","+server_list[x]['rbf_file']+","+server_list[x]['game_type']+","+server_list[x]['game_file_link']+","+server_list[x]['file_location']+"\n")
                f.write(output)
                h_web.add(server_list[x]['game_name'], output)
            f.close()
            #h_web.print()
            #print("-----------Above-server-Games--------------------\n")

    #-------Check if file exists and Check if the file is empty then Lines_test=0 else Lines_test>=1
            if os.path.exists("misterList.txt"):
                f_check = open("misterList.txt","r")
                Lines_test = f_check.readlines()
                f_check.close()

    #-------check if the misterList game file exists. if it does then add/delete the games
            if os.path.exists("misterList.txt") and (len(Lines_test)>0):
                #print("file exists!!\n")
                #read in the file
                f2 = open("misterList.txt","r")
                #read the previous misterList.txt games
                Lines = f2.readlines()
                #get the size of the hash table
                hash_size = math.ceil(1.3*len(Lines))
                #create the Mister hashmap
                h_mister = Hashmap(hash_size)
                #The number of games currently in the misterList.txt
                mister_num_games = len(Lines)
                f2.close()

                #print(len(Lines))
    #-----------Add in the games to the mister hash map
                for x in range(mister_num_games): 
                    #get the current game string
                    game=Lines[x].split(',')
                    h_mister.add(game[0], Lines[x])
                
    #-----------#check to see if the misterList.txt games are on the web hash map, If not remove them from the Hash and delete the file
                for x in range(mister_num_games): 
                    game=Lines[x].split(',')
                    #print(game[0])
                    temp = h_web.get(game[0])
                    #print(temp)
                    if temp == "1":
                        python_sucks =0
                        #print("Do nothing")
                        #game[0]=game_name,   Lines=game download link and path
                        #h_mister.add(game[0], Lines[x])
                    else:
                        #print("Remove the game here the function to remove the game file")
                        #print("Delete")
                        h_mister.delete(game[0])
                        delete_Game(Lines[x])

                    #print("\n")
                #print("-----------Above-delete-Games--------------------\n\n")


    #-----------#check to see if the web games are on the mister hash map, If not add them to the hash map and add the files
                
                #read in the web server list
                f3 = open("serverList.txt","r")
                #read the previous misterList.txt games
                Lines = f3.readlines()
                #h_mister.print()  
                #print("((((((((((()))))))))))")
                temp = h_mister.get('Billiard')
                #print(temp)
                f3.close()
                for x in range(web_num_games): 
                    game=Lines[x].split(',')
                    temp = h_mister.get((game[0]))
                    #print((game[0].strip('\n')))
                    #print(temp)
                    if temp == "1":
                        python_sucks = 0
                        #print("Do nothing")
                        #game[0]=game_name,   Lines=game download link and path
                        #h_mister.add(game[0], Lines[x])
                    else:
                        #print("Remove the game here the function to remove the game file")
                        #print("ADD")
                        h_mister.add(game[0],Lines[x])
                        #print(Lines[x])
                        write_Game(Lines[x])
                    
                    #print("\n")

                #Output the hashmap to the misterfile

                #h_mister.print()  
                h_mister.output_file()
                #print(h_mister.print())
                #print(h_mister.get("game2"))

                #print("-----------Above-ADD-Games--------------------\n")

    #-------if the file does not axist then create it
            else:
                f3 = open("misterList.txt","w")
                for x in range(web_num_games):
                    #print("file does not exists!!")
                    output = (server_list[x]['game_name']+","+server_list[x]['rma_file']+","+server_list[x]['rbf_file']+","+server_list[x]['game_type']+","+server_list[x]['game_file_link']+","+server_list[x]['file_location']+"\n")
                    f3.write(output)
                    h_web.add(server_list[x]['game_name'], output) #add to hashmap
                    write_Game(output)


                f3.close()



    else:
        python_sucks =0
        #print("could not connect to server")
except requests.exceptions.RequestException as e:
    raise SystemExit(e)


