import pathlib
import time
import pandas
from shutil import rmtree
import csv
import os

class User():
    
    def __init__(self):
       
        self.usr_id = None
        self.directory = None
        self.indx = {}
        self.nochar = 100
        self.log_check = False
        self.checked_users = None
        self.users_loged = None
        
    
    def create_folder(self, folder_path):
        
        self.session()
        logdata = pandas.read_csv('ServerAccessSession/Users.csv')
        if not self.log_check:
            return"\nLogin to access"
        p = int(logdata.loc[logdata['username'] == self.usr_id]['isAdmin'].values)
        if p == 1:
            curr_dir = "Root/Admin/"
        else:
            curr_dir = "Root/NotAdmin/"
        rmpath = os.path.join(curr_dir, str(self.usr_id), self.directory)
        total_avail_dir = []
        for sub in os.listdir(rmpath):
            path2 = os.path.join(rmpath, sub)
            if os.path.isdir(path2):
                total_avail_dir.append(sub)
        if folder_path in total_avail_dir:
            return "\nThis path is already created"
        os.mkdir(os.path.join(rmpath, folder_path))
        return"\nSuccess"

    def register(self, usr_id, passw, prior):
        
        self.session()

        logdata = pandas.read_csv('ServerAccessSession/Users.csv')
        var1 = 100
        if usr_id in logdata['username'].tolist():
            return "\nUsername not available"
        if usr_id == "" or passw == "" or prior == "":
            return "\nYou cannot register empty user"
        store = pandas.DataFrame(columns=['username', 'password', 'isAdmin'])
        store['username'] = [usr_id]
        store['password'] = passw
        if prior.lower() == 'admin':
            store['isAdmin'] = 1
            var1 = 1
        else:
            store['isAdmin'] = 0
            var1 = 0
        logdata = logdata.append(store)
        logdata.to_csv("ServerAccessSession/Users.csv", index=False)
        directoryname = str(usr_id)
        if var1 == 1:
            filepath = "Root/Admin/"
        else:
            filepath = "Root/NotAdmin/"

        os.mkdir(os.path.join(filepath, directoryname))
        return "\nRegistered user successfully."


    def login(self, usr_id, passw):
        
        dict1 = {}
        lst1 = []
        lst2 = []
        passw = int(passw)

        loginuser = pandas.read_csv('ServerAccessSession/logged_in_Users.csv')
        self.session()
        dict1 = self.checked_users.to_dict('split')
        n = len(dict1['data'])
        for i in range(0, n):
            lst1.append(dict1['data'][i][0])
            lst2.append(int(dict1['data'][i][1]))
            print(lst2)
        if self.log_check:
            return "\nAlready logged in"
        if usr_id not in lst1:
            return "\nUsername not registered"
        if passw not in lst2:
            return "\nWrong password!"
        if usr_id in loginuser['username'].tolist():
            return "\nLogged in from different address"

        self.log_check = True
        self.usr_id = usr_id
        self.directory = ""
        tstore = pandas.DataFrame(columns=['username'])
        tstore['username'] = [usr_id]
        loginuser = loginuser.append(tstore)
        loginuser.to_csv('ServerAccessSession/logged_in_Users.csv', index=False)

        return "\nLogin completed."


    def quit(self):
        
        loginuser = pandas.read_csv('ServerAccessSession/logged_in_Users.csv')
        try:
            if self.usr_id in loginuser['username'].tolist():
                login_rest = pandas.DataFrame(columns=['username'])
                login_rest.to_csv('ServerAccessSession/logged_in_Users.csv', index=False)
            self.usr_id = None
            self.directory = ""
            self.log_check = False
            self.indx = {}
            return "\nSigned out"
        except KeyError:
            return "\nSigned out"


    def delete1(self, usr_id, pasw):
       

        logdata = pandas.read_csv('ServerAccessSession/Users.csv')
        if self.log_check != True:
            return "\nlogin to proceed"
        if (logdata.loc[logdata['username'] == self.usr_id]['isAdmin'].values) != 1:
            return "\n need to be admin."
        if usr_id not in logdata['username'].tolist():
            return "\nNo user with username "+ usr_id + "found"
        if pasw != int(logdata.loc[logdata['username'] == usr_id]['password']):
            return "\nEnter the right password"
        #dataf = pandas.DataFrame(columns=['username', 'password', 'isAdmin'])
        n = int(logdata.loc[logdata['username'] == usr_id]['isAdmin'].values)
        
        lst1 = list()
        with open('ServerAccessSession/Users.csv', 'r') as readFile:
            reader = csv.reader(readFile)
            for row in reader:
                lst1.append(row)
                for field in row:
                    if field == usr_id:
                        lst1.remove(row)

        with open('ServerAccessSession/Users.csv', 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lst1)
        logdata = pandas.read_csv('ServerAccessSession/Users.csv')

        if self.usr_id == usr_id:
            self.quit()

        if n == 1:
            filepath = "Root/Admin/"
        else:
            filepath = "Root/NotAdmin/"
        path = os.path.join(filepath, str(usr_id))
        rmtree(path)
        return"\nDeleting" + usr_id +"is success"


    def change_folder(self, directory):
        
        logdata = pandas.read_csv('ServerAccessSession/Users.csv')
        self.session()

        if not self.log_check:
            return "\nLogin to access"
        n = int(logdata.loc[logdata['username'] == self.usr_id]['isAdmin'].values)
        if n == 1:
            filepath = "Root/Admin/"
        else:
            filepath = "Root/NotAdmin/"
        path = os.path.join(filepath, str(self.usr_id))

        dir4 = []
        for direc in os.walk(os.path.join(path)):
            dir4.append(os.path.normpath(os.path.realpath(direc)))
        path_change = os.path.join(path, self.directory, directory)
        path_change = os.path.normpath(os.path.realpath(path_change))
        print(self.directory)
        print(dir4)
        print(path_change)
        if path_change in dir4:
            self.directory = os.path.join(self.directory, directory)
            return "\n changed path to "+directory+"is success"
        else:
            return"\nenter correct path name"

    def commands(self):
        
        user_commands = ["register :","For registering the new user ,command:register <username> <password> <privilage>\n",
                 'login : ','To login, command:login <username> <password>,Note:password should be in integer\n',
                 'quit : ','To logout, command:quit\n',
                 'delete1 : ','To delete the user, command:delete1 <username> <password>\n',
                 'change_folder : ','To change the path, command:change_folder <name>\n',
                 'list : ','list of all files in the path, command:list\n',
                 'read_file : ','To read content from the file, command:read_file <name>\n',
                 'write_file : ','To write content into the file, command:write_file <name>\n',
                 'create_folder : ','To create new folder, command:create_folder <name>\n'
                ]

        msg = ''
        for i in range(0, len(user_commands), 2):
            msgline = ''.join([user_commands[i], user_commands[i+1]])
            msg += msgline + '*******\n'
            if i == len(user_commands):
                break
        return msg

    def list(self):
        
        self.session()
        logdata = pandas.read_csv('ServerAccessSession/Users.csv')
        if not self.log_check:
            return "\nLogin to access"
        p = (logdata.loc[logdata['username'] == self.usr_id]['isAdmin'].values)
        if p == 1:
            path = os.path.join("Root/Admin/", str(self.usr_id), self.directory)
        else:
            path = os.path.join("Root/NotAdmin/", str(self.usr_id), self.directory)
        dir4 = []
        for file_name in os.listdir(path):
            a = os.stat(os.path.join(path, file_name))
            dir4.append([file_name, str(a.st_size), str(time.ctime(a.st_ctime))])
        details = "\nFile|Size|Modified Date"
        for data in dir4:
            line = " | ".join([data[0], data[1], data[2]]) + "\n"
            details += "-------\n" + line
        return details


    def read_file(self, path):
        
        self.session()

        logdata = pandas.read_csv('ServerAccessSession/Users.csv')
        if not self.log_check:
            return "\nLogin to access"
        p = int(logdata.loc[logdata['username'] == self.usr_id]['isAdmin'].values)
        if p == 1:
            path_d = os.path.join("Root/Admin/", str(self.usr_id), self.directory)
            path2 = "Root/Admin"
        else:
            path_d = os.path.join("Root/NotAdmin/", str(self.usr_id), self.directory)
            path2 = "Root/NotAdmin"

        files = []
        for file in os.listdir(os.path.join(path2, self.usr_id, self.directory)):
            if os.path.isfile(os.path.join(path2, self.usr_id, self.directory, file)):
                files.append(file)

        if path not in files:
            return "\ngiven file not found"
        t_path = os.path.join(path_d, path)
        if t_path not in list(self.indx.keys()):
            self.indx[t_path] = 0
        with open(t_path, "r") as fi:
            cont = fi.read()
        old_inx = str(self.indx[t_path]*self.nochar)
        indx = self.indx[t_path]
        data = cont[indx*self.nochar:(indx+1)*self.nochar]
        self.indx[t_path] += 1
        self.indx[t_path] %= len(cont)//self.nochar+1
        return "\n" + "Read file from " + old_inx + " to " + str(int(old_inx)+self.nochar) + "are\n" + data


    def write_file(self, path, data):
       
        self.session()
        logdata = pandas.read_csv('ServerAccessSession/Users.csv')
        if not self.log_check:
            return "\nLogin to access!!"
        p = int(logdata.loc[logdata['username'] == self.usr_id]['isAdmin'].values)
        if p == 1:
            rmpath = os.path.join("Root/Admin/", str(self.usr_id), self.directory, path)
            path2 = "Root/Admin/"
        else:
            rmpath = os.path.join("Root/NotAdmin/", str(self.usr_id), self.directory, path)
            path2 = "Root/NotAdmin/"
        t_file = []

        for file in os.listdir(os.path.join(path2, self.usr_id, self.directory)):
            if os.path.isfile(os.path.join(path2, self.usr_id, self.directory, file)):
                t_file.append(file)

        str1 = ""
        for i in data:
            str1 += i
        if path in t_file:
            with open(rmpath, "a+") as file:
                file.write(str1)
            file.close()
            return"\nSuccess written"
        with open(rmpath, "w+") as file:
            file.write(str1)
        file.close()
        return"\nSuccessfully written"


    
    def rm_tree(self, rmpath):
        
        for child in pathlib.Path(rmpath).iterdir():
            if child.is_file():
                child.unlink()
            else:
                self.rm_tree(child)
        rmpath.rmdir()
    def session(self):
        
        self.checked_users = pandas.read_csv("ServerAccessSession/Users.csv")
        self.users_loged = pandas.read_csv("ServerAccessSession/logged_in_Users.csv")
    
    
