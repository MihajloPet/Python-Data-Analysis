import json 
import json
import os
import regex as re
import sys


class password:
    #correct path has to be set up
    
    def __init__(self,server=None, username=None):
        self.server = server
        self.username = username
        
        self.f = open(file=self.json_file_path())
        self.data = json.loads(self.f.read())
        
        
    def get_password(self):        
        #returns password for specific combination of server and username
        for item in self.data['credentials']:
            if self.server.lower()==item['server'].lower() and self.username.lower()==item['username'].lower():
                return item['password']
    
    def server_username(self):
        # prints out all server names and usernames, password class can be run without any args
        for item in self.data['credentials']:
            print(f"server: '{item['server']}', username: '{item['username']}'" )
            
            
    def json_file_path(self):
        
        path = None
        vm_folder = 'C:\\Batches'
        qlid_final = ''

        #get QLID
        for d in os.listdir('C:/Users'):
            qlid = ''
            try:
                qlid = re.search('\w{2}\d{6}',d)[0]
            except:
                pass

            if len(qlid)>0:
                qlid_final = qlid



        #filepath - based on QLID
        if os.path.exists(vm_folder):
            path = 'C:\\Batches'
        elif len(qlid_final)>0:            
            path = f'C:\\Users\\{qlid_final}\\OneDrive - NCR Corporation\\Desktop\\Automation'
        else:
            print(f'Script was not able to find {vm_folder} folder, nor any folder with QLID within "C:/Users".')

        #check if filepath exists - first on VM then local
        if os.path.exists('C:\\Batches'):            
            path = 'C:\\Batches\\credentials.json'
        else:            
            path = f'C:\\Users\\{qlid_final}\\OneDrive - NCR Corporation\\Desktop\\Automation\\credentials.json'




        #check if credentials.json file is in folder if not notify and break the script
        if os.path.exists(path)==False:
            print(f'File does not exist: {path}')
            path =  None
            sys.exit()
        else:
            pass

        return path
