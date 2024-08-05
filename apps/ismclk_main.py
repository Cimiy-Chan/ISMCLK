'''
ISMCLK = Intelligent Smart Master Clock
Features:
1. Sync with customize PIC embedded slave clock via RS-232
2. Timer to trigger specific event.

Version controlled by GitHub: https://github.com/Cimiy-Chan/ISMCLK.git

'''

from tkinter import Toplevel, StringVar, ttk, messagebox
import tkinter.font as font 
import tkinter as tk 
from ismclk_func import *

class TkFunc:
    def __init__(self, root):
        self.root = root

        # Font definition
        self.FONT_STYLE = 'Ubuntu'
        self.font_size_10 = font.Font(family=self.FONT_STYLE, size=10)
        self.font_size_12 = font.Font(family=self.FONT_STYLE, size=12)        
        self.font_size_18 = font.Font(family=self.FONT_STYLE, size=18)

        # Path definition
        self.CONF_PATH = ''

    def ismclk_main_panel (self):
        '''
        - Master clock main panel
        '''
        main_panel_width = 500
        main_panel_height = 70
        screen_width = self.root.winfo_screenwidth()
        #Put the main panel at top-center
        x = (screen_width / 2) - (main_panel_width / 2)
        y = 10

        # Main panel set up
        self.root.iconphoto(False, self.logo)
        self.panel_stack.append(self.root)        
        self.root.geometry(f'{main_panel_width}x{main_panel_height}+{int(x)}+{int(y)}')  # Width x height
        self.root.resizable(False, False)
        self.root.wm_title(50 * ' ' + f'UIDMT Main Panel Ver:{apfdfdffdf.get_main_ver()}')


# Main program entry
if __name__=='__main__':
    '''
    - This is the main entry point of main program
    '''
    main_ver = 1
    main_sub_ver = 0

    apps_ismclk = Ismclk (main_ver, main_sub_ver)
    apps_ismclk.write_log('INFO', f'Loading ISMCLK modules...Ver:{main_ver}.{main_sub_ver}')
    apps_ismclk.load_config()
