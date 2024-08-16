'''
This is the function class sopported for ISMCLK application

'''
import xml.etree.ElementTree as ET
from pathlib import Path
import os, socket
from datetime import datetime
from time import sleep
from PIL import Image, ImageTk

class Ismclk():
    '''
    Class continaing the functions used by ISMCLK applicaion
    '''
    def __init__(self, main_ver, main_sub_ver):
        self.main_ver = main_ver
        self.main_sub_ver = main_sub_ver
        self.cwd = os.getcwd() #Get current working path
        self.log_path = os.path.join(self.cwd, 'log', 'ismclk.log')
        self.config_path = os.path.join(self.cwd, 'conf', 'ismclk.xml')
        self.hostname = socket.gethostname()
        self.pid = os.getpid()
        self.xml_hostname = ''

        #XML definintion
        self.slave_clock_id = ''
        self.protocol_code = ''
        self.digit_file_img_prefix = ''
        self.event_trigger = ''
        self.bool_24h = False

        # Path definition
        self.image_path = 'C:\\Cimiy20181027\\HomeProjects\\Python_PC\\ISMCLK\\img'

        self.image_array = ['digit_00.png', 'digit_01.png','digit_02.png','digit_03.png','digit_04.png',
               'digit_05.png','digit_06.png','digit_07.png','digit_08.png','digit_09.png']


    def get_main_ver(self):
        '''
        - Return apps version number. Format: Ver.Subver
        '''
        return f'{self.main_ver}.{self.main_sub_ver}'
    
    def write_log (self, log_type, log_info, init=0):
        '''
        - Write the log information into file definded by log_path
        - Input: init. It is an optional variable. Default is 0. If not zero, it will display as "***".
        - It's usually for separator whenever the apps is launch.
        - Return: N/A
        '''
        log_msg = '***\n'
        t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if init == 0:
            log_msg = f'{t} [{self.pid}] {log_type}: {log_info}\n'
        with open(self.log_path, 'a') as f:
            f.writelines(log_msg)
        f.close()

    def load_config(self):
        '''
        - Load the configuration file and parse the XML content
        - Input: N/A
        - Return: True/False. Return true if XML loading and parset correct, otherwise false.        
        '''
        bool_hostname_found = False
        bool_status = False
        try: 
            config_root = ET.parse(self.config_path).getroot()
            bool_status = True
        except Exception as e:
            self.write_log('ERROR', f'Fail to read config file: {self.config_path} with error: {e}')
        # Get the XML information
        if config_root is not None:
            for module in config_root:
                self.xml_hostname = module.get('hostname')
                if self.xml_hostname == self.hostname:
                    bool_hostname_found = True
                    for setting in module:
                        setting_name = setting.get('name')
                        setting_value = setting.get('value')
                        bool_check = self.set_config(setting_name, setting_value)
                        if not bool_check:
                            self.write_log('ERROR', f'Config setup error. Name="{setting_name}", Value="{setting_value}" not match with system')
                            return False
            if not bool_hostname_found:
                self.write_log('ERROR', f'No hostname found at XML file. Your computer hostname: {self.hostname}')
                return False
            if not bool_status:
                self.write_log('ERROR', 'Error in configuration file')
                return bool_status

    def set_config(self, name, value):
        '''
        - Get the value form the name/value pair variable from XML file parser
        '''
        bool_name_valid = False
        try:
            if name == '': return False

            match name.lower():
                case 'slave_clock_id':
                    self.slave_clock_id = value
                    bool_name_valid = True
                case 'protocol_code':
                    self.protocol_code = value
                    bool_name_valid = True
                case 'digit_file_img_prefix':
                    self.digit_file_img_prefix = value
                    bool_name_valid = True
                case 'event_trigger':
                    self.event_trigger = value
                    bool_name_valid = True
                case 'bool_24h':
                    self.bool_24h = value
                    bool_name_valid = True
            return bool_name_valid
        except Exception as e:
            self.write_log('ERROR', f'Error in configuration setup with exception {e}')
            return False
            
    def get_time (self, time_str):
        '''
        - Get time string with format: HH:MM:SS
        - return time arrary with format: [H10, H1, M10, M1, S10, S1]
        - All values are integer: 0-9. H10=10th digit of hour, H1=1st digit of hour and so on
        '''
        split_str = []
        temp_time_info = [] #Integer, single digit
        result_time_info = []

        split_str = time_str.split(':')
        try:
            for hms in split_str:
                temp_time_info.append(int(hms)) #Now time_info will be [HH, MM, SS] integer array
            for each_time_unit in temp_time_info: #In sequence: HH->MM->S
                unit_10 = int(each_time_unit/10)
                unit_1 = each_time_unit - int(each_time_unit/10)*10
                result_time_info.append(unit_10)
                result_time_info.append(unit_1)
            return result_time_info
        except Exception as e:
            self.write_log('ERROR', e)
            return [0,0,0,0,0,0]

    def load_image(self, digit_val):

        if digit_val <= 0 or digit_val > 9:
            digit_val = 0

        image = Image.open(os.path.join(self.image_path, self.image_array[digit_val]))
        #Image resize
        image_resize = image.resize((75,100), Image.Resampling.LANCZOS)
        ret_image = ImageTk.PhotoImage(image_resize)
        return ret_image
