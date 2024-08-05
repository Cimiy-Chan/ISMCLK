'''
This is the function class supported for OTPG application
'''

import xml.etree.ElementTree as ET
from pathlib import Path
import os, subprocess, sqlite3, socket, time
from datetime import datetime
from time import sleep
from threading import Thread
from cryptography.fernet import Fernet
#from requests import patch

class UidmtFunc():
    """
    - Class containing the function used by UIDMT application
    """
    def __init__(self, main_ver, main_sub_ver):
        self.main_ver = main_ver
        self.main_sub_ver = main_sub_ver
        self.log_path = os.path.join('c:\\uidmt', 'log', 'uidmt.log')
        self.pid = os.getpid()
        self.hostname = ''
        self.xml_hostname = ''
        self.db_networkpath=''
        self.default_username =''
        self.default_hashed_password = ''
        self.PRIVATE_KEY = 'IxkXNINr4ZAAsEIYJUpeUe51fP0HNT54SabeEq2KRiA='
        self.CONFIG_PATH = os.path.join('C:\\uidmt', 'conf', 'UIDMT_conf.xml')

        # Function version number
        self.func_ver = '1'
        self.func_sub_ver ='0'

        #Get computer hostname
        self.hostname = socket.gethostname()

        # Record version at log file for version tracking
        self.write_log('', '', init=1)
        self.write_log('INFO', f'Application start...')
        self.write_log('INFO', f'Loading UIDMT Func module...Ver:{self.func_ver}.{self.func_sub_ver}')

    def get_main_ver(self):
        """
        - Return apps veriosn number. Format: Ver.Subver
        """
        return f'{self.main_ver}.{self.main_sub_ver}'

    def write_log(self, log_type, log_info, init=0):
        """
        - Write the log information into file definded by log_path
        - Input: init. It is an optional variable. Default is 0, if not zero, it will dispalyed as "***". 
        - It usually for separator whenever the apps is launch
        - Return: N/A
        """
        log_msg = '***\n'
        t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if init == 0:
            log_msg = f'{t} [{self.pid}] {log_type}: {log_info}\n'
        with open(self.log_path, 'a') as f:
            f.writelines(log_msg)
        f.close()

    def load_config (self):
        """
        - Load the configuration file and parse the XML content
        - Input: N/A
        - Return: True/False. Return true if XML loading and parset correct, otherwise false.
        """
        bool_hostname_found = False
        try:
            config_root = ET.parse(self.CONFIG_PATH).getroot()
        except Exception as e:
            self.write_log('ERROR',f'Faill to read the config file: {self.CONFIG_PATH} with error: {e}')
        bool_status = True
        # Get the XML information
        if config_root is not None:
            for module in config_root:
                self.xml_hostname = module.get('hostname')
                if  self.xml_hostname == self.hostname :
                    bool_hostname_found = True
                    for setting in module:
                        setting_name = setting.get('name')
                        setting_value = setting.get('value')
                        
                        if not self.set_config(setting_name, setting_value):
                            self.write_log('ERROR', 'Config setup error. Name/Value pair not found')
                            return False
                            
            if not bool_hostname_found:
                self.write_log('ERROR', f'No hostname found at XML, pls. check module value. Your computer hostname:{self.hostname}')
                return False
            if bool_status == False:
                self.write_log('ERROR', 'Error in configuration file')
            return bool_status

    def set_config(self, name, value):
        """
        - Get the value from the name/value pair variable from XML file parse
        """
        
        try: 
            if name == '' : return False

            elif name.lower() == 'db_networkpath':
                self.db_networkpath = value
                self.db_networkpath = str(Path(self.db_networkpath).resolve()) #path_resolve gets the full path instead of mapped drive.
            elif name.lower() == 'default_username':
                self.default_username = value
            elif name.lower() == 'default_password':
                self.default_hashed_password = value
            return True
        except Exception as e:
            return False

    def data_hash (self, input_data):
        """
        - It is use to encrypt the input_data
        """
        f = Fernet(self.PRIVATE_KEY)
        return f.encrypt(bytes(input_data, 'UTF-8'))

    def dehash(self, hash_string):
        """
        - Dehash the hash_string
        - Return: (True/False, info_list). True if success in de-hashing with returned de-hash string other False with None
        """
        try:
            dehash_str = str(bytes.decode(Fernet(self.PRIVATE_KEY).decrypt(hash_string), 'UTF-8'))
            return [True, dehash_str]
        except Exception as e:
            self.write_log('ERROR', 'Dehashing exception error: Invalid hash format')
            return [False, '']
        
    def get_user_info (self,db_networkpath):
        """
        Get user registration information from database
        return in key format: {'user1':[badgename, password, accesslevel]}
        return: True/False, usernamelist, user_info_dict
        True/False: True if complete look for all information in db with complet username_list(key) with it associate user_info_dict
        """
        user_info_dict = {} #Dictionary
        username_list=[]
        item_dict={}
        try:
            conn = sqlite3.connect(os.path.join(db_networkpath, 'user_registration.db'))
            cursor = conn.execute('SELECT item, badgename, username, password, accesslevel from user_reg')
            for each_record in cursor:
                #Use username as the key
                user_info_dict[each_record[2]]=[each_record[1], each_record[3],each_record[4]] #{'username': [badgename, password, accesslevel]}
                username_list.append(each_record[2])
                item_dict[each_record[2]]=each_record[0] #{'username': item}
            conn.close()

            #Debug
            self.write_log('INFO', f'Compelete to search all information...{len(user_info_dict)} records are found')
            return [True, item_dict, username_list, user_info_dict]
        except Exception as e:
            self.write_log('ERROR', f'User registration data base error: {e}')
            return [False, None, None, None]


    def check_username(self, db_networkpath, user_name):
        """
        - Check incoming user_name exist on the current registration database
        - Input: user_name string
        - Return: Boolean: True if user_name is found at database
        """
        try:
            conn = sqlite3.connect(os.path.join(db_networkpath, 'user_registration.db'))
            cursor = conn.execute('SELECT username from user_reg')
            for each_record in cursor:
                
                if each_record[0] == user_name:
                    conn.close()
                    self.write_log('INFO', f'Registration database found the username "{user_name}" submitted')
                    return True #Match found
            conn.close()
            self.write_log('WARNING', f'Registration database not found the username "{user_name}" submitted')
            return False
        except Exception as e:
            self.write_log('ERROR', f'User registration data base error: {e}')
            return False
        
    def check_badgename(self, db_networkpath, badge_name):
        """
        - Check incoming badge_name exist on the current registration database
        - Input: user_name string
        - Return: Boolean: True if user_name is found at database
        """
        try:
            conn = sqlite3.connect(os.path.join(db_networkpath, 'user_registration.db'))
            cursor = conn.execute('SELECT badgename from user_reg')
            for each_record in cursor:
                if each_record[0] == badge_name:
                    conn.close()
                    self.write_log('INFO', f'Registration database found the badgename "{badge_name}" submitted')
                    return True #Match found
            conn.close()
            self.write_log('WARNING', f'Registration database not found the badgename "{badge_name}" submitted')
            return False
        except Exception as e:
            self.write_log('ERROR', f'User registration data base error: {e}')
            return False
    
    def update_db_record (self, db_networkpath, user_info_list):
        """
        - Upate db for specifice record.
        - Output: Boolean: True if successfully updated, otherwise False
        """

        try:
            conn = sqlite3.connect(os.path.join(db_networkpath, 'user_registration.db'))
            my_cursor = conn.cursor()
            item = user_info_list[0]
            badgename = user_info_list[1]
            username = user_info_list[2]
            pwd = user_info_list[3]
            accesslevel = user_info_list[4]
            sql_cmd = f"UPDATE USER_REG SET BADGENAME='{badgename}', USERNAME='{username}', PASSWORD='{pwd}', ACCESSLEVEL={accesslevel} WHERE ITEM={item}"
            my_cursor.execute(sql_cmd)
            conn.commit()
            conn.close()
            self.write_log('INFO', f'User information update successful with username "{username}" edited. Reference no. {item}')
            return True
        except Exception as e:
            self.write_log('ERROR', f'User information update error: {e}')
            return False
            
    def new_account_create_db (self, db_networkpath, new_account_info_list):
        """
        - Create a row record into the db for new account.
        - Input: db_networkpath (network path of user registration database)
        - new_account_info_list: List to store the necessary infor for new account creation.
        - Output: Boolen: Boolean: True if successfully create, otherwise False

        """

        if self.check_badgename(db_networkpath, new_account_info_list[0]) == False and self.check_username(db_networkpath, new_account_info_list[1]) == False:
            try:
                conn = sqlite3.connect(os.path.join(db_networkpath, 'user_registration.db'))
                my_cursor = conn.cursor()
                sql_cmd = f"INSERT INTO USER_REG (badgename, username, password, accesslevel) \
                           VALUES ('{new_account_info_list[0]}', '{new_account_info_list[1]}', '{new_account_info_list[2]}', {int(new_account_info_list[3])})"
                #print (sql_cmd)
                my_cursor.execute(sql_cmd)
                conn.commit()
                conn.close()
                self.write_log('INFO', f'New accout successfully created: Badge Name "{new_account_info_list[0]}", Username "{new_account_info_list[1]}", Access Level "{new_account_info_list[3]}"')
                return True
            except Exception as e:
                self.write_log('ERROR', f'New account creation request error: {e}')
                return False
        else:
            self.write_log('ERROR', f'Check Username or Badge name ready exist. New account create request cancelled')
            return False
        
    def account_delete_db (self, db_networkpath, user_name):
        """
        - Delete the user account for specific username
        - Input: db_networkpath (network path of user registration database)
        - user_name: Username provide by requestor that want to delete.
        - Output: Boolen: Boolean: True if successfully delete, otherwise False
        """
        if self.check_username(db_networkpath,user_name) == True:
            try: 
                conn = sqlite3.connect(os.path.join(db_networkpath, 'user_registration.db'))
                my_cursor = conn.cursor()
                sql_cmd = f"DELETE FROM USER_REG WHERE username = '{user_name}'"
                my_cursor.execute(sql_cmd)
                conn.commit()
                conn.close()
                self.write_log('INFO', f'Account with username "{user_name}" had been deleted')
                return True
            except Exception as e:
                self.write_log('ERROR', f'Account delete request error: {e}')
                return False
        else:
            self.write_log('ERROR', f'Username "{user_name}" not found. Account delete request cancelled')
            return False
        
