'''
ISMCLK = Intelligent Smart Master Clock
Features:
1. Sync with customize PIC embedded slave clock via RS-232
2. Timer to trigger specific event.

Version controlled by GitHub: https://github.com/Cimiy-Chan/ISMCLK.git

'''

from tkinter import Toplevel, StringVar, ttk, messagebox, Button
import tkinter.font as font, os
from ismclk_func import *
from PIL import Image, ImageTk
import tkinter as tk
from threading import *
import time


class TkFunc:
    def __init__(self):


        root = tk.Tk()

        # Font definition
        self.root = root
        self.FONT_STYLE = 'Ubuntu'
        self.font_size_10 = font.Font(family=self.FONT_STYLE, size=10)
        self.font_size_12 = font.Font(family=self.FONT_STYLE, size=12)        
        self.font_size_18 = font.Font(family=self.FONT_STYLE, size=18)
        self.cwd = os.getcwd()

        # Path definition
        self.logo_path = os.path.join(self.cwd, 'img', 'black_cat.PNG')
        self.logo = tk.PhotoImage(file=self.logo_path) # Note: Only support PNG file.
        self.image_path = 'C:\\Cimiy20181027\\HomeProjects\\Python_PC\\ISMCLK\\img'

        self.image_array = ['digit_00.png', 'digit_01.png','digit_02.png','digit_03.png','digit_04.png',
               'digit_05.png','digit_06.png','digit_07.png','digit_08.png','digit_09.png']
        
        #Misc self initialization
        self.counter = 0
        self.image_label = 0
        self.image_h1 = ''
        self.image_h10 = ''

    def ismclk_main_panel (self):
        '''
        - Master clock main panel
        '''
        main_panel_width = 500
        main_panel_height = 300
        screen_width = self.root.winfo_screenwidth()
        #Put the main panel at top-center
        x = (screen_width / 2) - (main_panel_width / 2)
        y = 10

        # Main panel set up
        self.root.iconphoto(False, self.logo)
        self.root.geometry(f'{main_panel_width}x{main_panel_height}+{int(x)}+{int(y)}')  # Width x height
        self.root.resizable(False, False)
        self.root.wm_title(50 * ' ' + f'ISMCLK Main Panel Ver:{apps_ismclk.get_main_ver()}')

        #Frame setup
        frame_h = tk.Frame(self.root, width=360, height=240, bg='magenta3')
        frame_h.pack(side = 'left')
        frame_h.pack_propagate(0)

        #Dummy setup for positioning the digit location
        dummy_label_h_a = tk.Label(frame_h, width=1, height=10, bg='magenta3')
        dummy_label_h_b = tk.Label(frame_h, width=1, height=10, bg='magenta3')
        dummy_label_h_c = tk.Label(frame_h, width=1, height=10, bg='magenta3')        

        #Positioning everything
        #In frame: dummy_label_h_a | image_label_h1 | dummy_label_h_b | image_label_h10 | dummy_label_h_c
        dummy_label_h_a.pack(side='left')
        self.image_h1 = self.load_image(0)        
        self.image_h10 = self.load_image(1)
        self.image_label_h1 = tk.Label(frame_h, image=self.image_h1)

        self.image_label_h1.pack(side ='left') # Need pack() to form an valid object. If .place is used, no valid obj formed
        dummy_label_h_b.pack(side='left')
        self.image_label_h10 = tk.Label(frame_h, image=self.image_h10)
        self.image_label_h10.pack(side ='left') # Need pack() to form an valid object. If .place is used, no valid obj formed
        dummy_label_h_c.pack(side='left')



                           




    def trigger_event(self):
        '''
        - Timer trigger to do the event using recursive approach.
        - At the root.after(...), the event name has no '()'.
        '''

        if self.counter == 10:
            self.counter = 0
        #print (f'Event triggher: {self.counter}')
        self.image_h1 = self.load_image(self.counter)
        self.image_label_h1.config(image=self.image_h1)
        self.image_label_h10.config(image=self.image_h1)        
        self.counter = self.counter + 1

        self.root.after(1000, self.trigger_event) #Recursive



    def load_image(self, digit_val):

        if digit_val <= 0 or digit_val > 9:
            digit_val = 0

        image = Image.open(os.path.join(self.image_path, self.image_array[digit_val]))
        #Image resize
        image_resize = image.resize((150,200), Image.Resampling.LANCZOS)
        ret_image = ImageTk.PhotoImage(image_resize)
        return ret_image


# Main program entry
if __name__=='__main__':
    '''
    - This is the main entry point of main program
    '''
    main_ver = 1
    main_sub_ver = 0

    tk_func = TkFunc()        
    apps_ismclk = Ismclk (main_ver, main_sub_ver)
    apps_ismclk.write_log('INFO', f'Loading ISMCLK modules...Ver:{main_ver}.{main_sub_ver}')
    tk_func.ismclk_main_panel()
    tk_func.root.after(10, tk_func.trigger_event())    
    tk_func.root.mainloop()    

    

    
    
 