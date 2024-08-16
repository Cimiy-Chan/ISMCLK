'''
ISMCLK = Intelligent Smart Master Clock
Features:
1. Sync with customize PIC embedded slave clock via RS-232
2. Timer to trigger specific event.

Version controlled by GitHub: https://github.com/Cimiy-Chan/ISMCLK.git

'''

from tkinter import *
import tkinter.font as font, os
from ismclk_func import *
import tkinter as tk
from threading import *
from datetime import datetime
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

        #Path definition
        self.logo_path = os.path.join(self.cwd, 'img', 'black_cat.PNG')
        self.logo = tk.PhotoImage(file=self.logo_path) # Note: Only support PNG file.

        #Misc self initialization
        self.counter = 0
        self.image_label_h10 = ''
        self.image_label_h1 = ''
        self.image_label_m10 = ''
        self.image_label_m1 = ''
        self.image_label_s10 = ''
        self.image_label_s1 = ''                                        
        self.previous_time = ''
        self.image_h1 = ''
        self.image_h10 = ''
        self.image_m1 = ''
        self.image_m10 = ''
        self.image_s1 = ''
        self.image_s10 = ''

    def ismclk_main_panel (self):
        '''
        - Master clock main panel
        '''
        main_panel_width = 630
        main_panel_height = 300
        screen_width = self.root.winfo_screenwidth()
        #Put the main panel at top-center
        x = (screen_width / 2) - (main_panel_width / 2)
        y = 10

        # Main panel set up
        self.root.iconphoto(False, self.logo)
        self.root.geometry(f'{main_panel_width}x{main_panel_height}+{int(x)}+{int(y)}')  # Width x height
        self.root.configure(bg='seashell')
        self.root.resizable(False, False)
        self.root.wm_title(50 * ' ' + f'ISMCLK Main Panel Ver:{apps_ismclk.get_main_ver()}')

        #Frame setup
        frame = tk.Frame(self.root, width=630, height=120, bg='magenta3')


        #Dummy setup for positioning the digit location. It is used as partition.
        top_label = tk.Label(self.root, width=10, height=2, bg='chartreuse')
        dummy_label_h_a = tk.Label(frame, width=2, height=10, bg='red')
        dummy_label_h_b = tk.Label(frame, width=1, height=10, bg='red')
        dummy_label_hm = tk.Label(frame, width=4, height=10, bg='red')
        dummy_label_m_a = tk.Label(frame, width=1, height=10, bg='red')
        dummy_label_ms= tk.Label(frame, width=4, height=10, bg='red')
        dummy_label_s_a = tk.Label(frame, width=1, height=10, bg='red')


        #Positioning everything
        self.image_h10 = apps_ismclk.load_image(0)        
        self.image_h1 = apps_ismclk.load_image(0)
        self.image_m10 = apps_ismclk.load_image(0)       
        self.image_m1 = apps_ismclk.load_image(0)
        self.image_s10 = apps_ismclk.load_image(0)        
        self.image_s1 = apps_ismclk.load_image(0)

        top_label.pack(side = 'top')
        frame.pack(anchor='nw')
        frame.pack_propagate(0)
        dummy_label_h_a.pack(side='left')
        self.image_label_h10 = tk.Label(frame, image=self.image_h10)
        self.image_label_h10.pack(side ='left') # Need pack() to form an valid object. If .place is used, no valid obj formed
        dummy_label_h_b.pack(side='left')
        self.image_label_h1 = tk.Label(frame, image=self.image_h1)
        self.image_label_h1.pack(side ='left') 
        dummy_label_hm.pack(side='left')
        #
        self.image_label_m10 = tk.Label(frame, image=self.image_m10)
        self.image_label_m10.pack(side ='left') 
        dummy_label_m_a.pack(side='left')
        self.image_label_m1 = tk.Label(frame, image=self.image_m1)
        self.image_label_m1.pack(side ='left') 
        dummy_label_ms.pack(side='left')
        #
        self.image_label_s10 = tk.Label(frame, image=self.image_s10)
        self.image_label_s10.pack(side ='left') 
        dummy_label_s_a.pack(side='left')
        self.image_label_s1 = tk.Label(frame, image=self.image_s1)
        self.image_label_s1.pack(side ='left') 

    def trigger_event(self):
        '''
        - Timer trigger to do the event using recursive approach.
        - At the root.after(...), the event name has no '()'.
        '''
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        if current_time != self.previous_time:

            time_value = apps_ismclk.get_time(current_time)
            self.image_h10=apps_ismclk.load_image(time_value[0])
            self.image_h1=apps_ismclk.load_image(time_value[1])
            self.image_m10=apps_ismclk.load_image(time_value[2])
            self.image_m1=apps_ismclk.load_image(time_value[3])
            self.image_s10=apps_ismclk.load_image(time_value[4])
            self.image_s1=apps_ismclk.load_image(time_value[5])

            #Update display
            self.image_label_h10.config(image=self.image_h10)
            self.image_label_h1.config(image=self.image_h1)
            self.image_label_m10.config(image=self.image_m10)
            self.image_label_m1.config(image=self.image_m1)
            self.image_label_s10.config(image=self.image_s10)
            self.image_label_s1.config(image=self.image_s1)
            self.previous_time = current_time



        self.root.after(10, self.trigger_event) #Recursive

# Main program entry
if __name__=='__main__':
    '''
    - This is the main entry point of main program
    '''
    main_ver = 1
    main_sub_ver = 0

    apps_ismclk = Ismclk (main_ver, main_sub_ver) # This object instantiation should be run first
    tk_func = TkFunc()        
    apps_ismclk.write_log('INFO', f'Loading ISMCLK modules...Ver:{main_ver}.{main_sub_ver}')
    tk_func.ismclk_main_panel()
    tk_func.root.after(10, tk_func.trigger_event())
    tk_func.root.mainloop()    

    

    
    
 