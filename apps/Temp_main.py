'''
UIDMT = User ID Management Tool
This application should be used with the user registration database


Version 1.0
Date: 20-Sep-2023
'''

from uidmt_func import *
from tkinter import Toplevel, StringVar, ttk,messagebox
import tkinter.font as font
import tkinter as tk

class TkFunc:
    def __init__(self, root):
        self.root = root
        self.obj_btn_create=''
        self.obj_btn_edit=''
        self.obj_btn_delete=''    
        self.panel_stack=[]
        self.user_info_search_result=[]
        self.default_username=''
        self.default_password=''
        self.db_item = 0
        self.badgename = ''
        self.update_db_user_info=[]

        # Font definition
        self.FONT_STYLE = 'Ubuntu'
        self.font_size_10 = font.Font(family=self.FONT_STYLE, size=10)
        self.font_size_12 = font.Font(family=self.FONT_STYLE, size=12)        
        self.font_size_18 = font.Font(family=self.FONT_STYLE, size=18)

        self.CONF_PATH = 'c:\\uidmt\\conf\\UIDMT_conf.xml'

        self.logo = tk.PhotoImage(file='c:\\uidmt\\apps\\img\\Nexperia_logo.PNG')  # Note only support PNG file

    def uidmt_main_panel (self):
        """
        - Main panel for UIDMT apps
        """
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
        self.root.wm_title(50 * ' ' + f'UIDMT Main Panel Ver:{apps_uidtm.get_main_ver()}')

        self.btn_create = tk.Button(root, text='Create', font=self.font_size_12, bg='Teal', fg='White',
                                    command=lambda: self.account_create())
        self.btn_edit = tk.Button(root, text='Read/Edit', font=self.font_size_12, bg='Teal', fg='White',
                                    command=lambda: self.account_edit())                                  
        self.btn_delete = tk.Button(root, text='Delete', font=self.font_size_12, bg='Salmon', fg='White',
                                    command=lambda: self.account_delete())

        self.btn_create.pack()
        self.btn_edit.pack()
        self.btn_delete.pack()
        self.btn_create.place(x=50, y=20, width=100, height=30)
        self.btn_edit.place(x=200, y=20, width=100, height=30)
        self.btn_delete.place(x=350, y=20, width=100, height=30)

        self.btn_create.config(state=tk.DISABLED)        
        self.btn_edit.config(state=tk.DISABLED)        
        self.btn_delete.config(state=tk.DISABLED)   

        #Check config panel
        if os.path.exists(self.CONF_PATH) and apps_uidtm.load_config():
            apps_uidtm.write_log('INFO', 'Load config...OK')

            #Run Login Panel
            self.login_panel()                     

            #Close action
            self.root.protocol('WM_DELETE_WINDOW', self.main_panel_quit)

        else:
            msg1 = 'Error...c:\\uidmt\\conf\\UIDMT_conf.xml not exist'
            msg2 = f'Last host name at XML: {apps_uidtm.xml_hostname}'
            msg3 = f'Your computer hostname: {apps_uidtm.hostname}'
            apps_uidtm.write_log('ERROR', msg1)
            apps_uidtm.write_log('ERROR', msg2)
            apps_uidtm.write_log('ERROR', msg3)
            messagebox.showerror('Error', f'{msg1}\n{msg2}\n{msg3}' )
            os._exit(0)

    def main_panel_quit(self):
        apps_uidtm.write_log('INFO', 'Application quit...')
        self.root.destroy()


    def login_panel(self):
        # Build login panel
        login_panel = Toplevel(self.root)
        self.panel_stack.append(login_panel)
        login_panel.iconphoto(False, self.logo)
        x = self.root.winfo_x()
        y = self.root.winfo_y()  # Get position of main panel
        login_panel.geometry(f'300x110+{x + 200}+{y + 120}')
        login_panel.title('Login Request')
        login_panel.resizable(False, False)
        login_panel.grab_set()  # disable the main panel
        tk.Label(login_panel, text='Username: ').place(x=5, y=10)
        tk.Label(login_panel, text='Password: ').place(x=5, y=40)
        entry_username = StringVar()
        entry_password = StringVar()
        tk.Entry(login_panel, textvariable=entry_username, width=33).place(x=75, y=10)
        tk.Entry(login_panel, textvariable=entry_password, show='*', width=33).place(x=75, y=40)

        # Run login_validate_action when 'Login' button pressed.
        btn_login = tk.Button(login_panel, text='Login', bg='Teal', fg='White', font=self.font_size_12,
                              command=lambda: self.login_validation(entry_username, entry_password))

        btn_login.pack()
        btn_login.place(x=75, y=70, height=30, width=150)

        login_panel.protocol('WM_DELETE_WINDOW', self.login_panel_quit)

    def login_panel_quit(self):
        """
        Special case in here in for quit action, user cannot be destroy the login panel
        Until user login correctly.
        So the statment 'self.panel_stack.pop().destroy()' will not be used
        """
        #self.panel_stack[len(self.panel_stack)-1].grab_set() 
        os._exit(0)

    def user_info_panel_edit(self):
        # Build login panel
        info_panel = Toplevel(self.root)
        self.panel_stack.append(info_panel)
        info_panel.iconphoto(False, self.logo)
        x = self.root.winfo_x()
        y = self.root.winfo_y()  # Get position of main panel
        info_panel.geometry(f'300x110+{x + 200}+{y + 120}')
        info_panel.title('User Info')
        info_panel.resizable(False, False)
        info_panel.grab_set()  # disable the main panel
        tk.Label(info_panel, text='Username: ', font=self.font_size_12).place(x=5, y=10)
        combo_username = ttk.Combobox(info_panel, font=self.font_size_12, height=20, width=18, values=tuple(self.user_info_search_result[2]))
        combo_username.current(0) #Set the first one is default value

        # Run login_validate_action when 'select' button pressed.
        btn_select = tk.Button(info_panel, text='Select', bg='Teal', fg='White', font=self.font_size_12,
                              command=lambda: self.user_input_panel_edit(combo_username.get()))

        btn_select.pack()
        combo_username.pack(side='left') #Add scroll-bar at the left side
        combo_username.place(x=90, y=10)
        combo_username.config(state='readonly')
        btn_select.place(x=75, y=60, height=30, width=150)

        info_panel.protocol('WM_DELETE_WINDOW', self.panel_quit_grab_set)



    def user_info_panel_delete(self):
        # Build login panel
        info_panel_delete = Toplevel(self.root)
        self.panel_stack.append(info_panel_delete)
        info_panel_delete.iconphoto(False, self.logo)
        x = self.root.winfo_x()
        y = self.root.winfo_y()  # Get position of main panel
        info_panel_delete.geometry(f'300x110+{x + 200}+{y + 120}')
        info_panel_delete.title('Delete panel')
        info_panel_delete.resizable(False, False)
        info_panel_delete.grab_set()  # disable the main panel
        tk.Label(info_panel_delete, text='Username: ', font=self.font_size_12).place(x=5, y=10)
        combo_username = ttk.Combobox(info_panel_delete, font=self.font_size_12, height=20, width=18, values=tuple(self.user_info_search_result[2]))
        combo_username.current(0) #Set the first one is default value

        # Run login_validate_action when 'select' button pressed.
        btn_select = tk.Button(info_panel_delete, text='Select', bg='Teal', fg='White', font=self.font_size_12,
                              command=lambda: self.record_delete(combo_username.get()))

        btn_select.pack()
        combo_username.pack(side='left') #Add scroll-bar at the left side
        combo_username.place(x=90, y=10)
        combo_username.config(state='readonly')
        btn_select.place(x=75, y=60, height=30, width=150)

        info_panel_delete.protocol('WM_DELETE_WINDOW', self.panel_quit_grab_set)

    def delete_confirm_panel(self, username):
        # Build login panel
        delete_panel = Toplevel(self.root)
        self.panel_stack.append(delete_panel)
        delete_panel.iconphoto(False, self.logo)
        x = self.root.winfo_x()
        y = self.root.winfo_y()  # Get position of main panel
        delete_panel.geometry(f'300x150+{x + 200}+{y + 120}')
        delete_panel.title('Delete confirm')
        delete_panel.resizable(False, False)
        delete_panel.grab_set()  # disable the main panel
        tk.Label(delete_panel, text=f'Username: {username}', font=self.font_size_12).place(x=5, y=10)
        tk.Label(delete_panel, text=f'Badge name: {self.user_info_search_result[3][username][0]}', font=self.font_size_12).place(x=5, y=40)
        tk.Label(delete_panel, text='             Are you sure to delete?', font=self.font_size_12).place(x=5, y=80)        

        #Yes/No button to confirm delete
        btn_yes = tk.Button(delete_panel, text='Yes', bg='Teal', fg='White', font=self.font_size_12,
                              command=lambda: self.confirm_deleted(username))
        btn_no = tk.Button(delete_panel, text='No', bg='Salmon', fg='White', font=self.font_size_12,
                              command=lambda: self.panel_quit_grab_set())

        btn_yes.pack()
        btn_no.pack()
        btn_yes.place(x=75, y=110, height=30, width=50)
        btn_no.place(x=175, y=110, height=30, width=50)      

        delete_panel.protocol('WM_DELETE_WINDOW', self.panel_quit_grab_set)

    def user_input_panel_edit(self, username_selected):
        # Build login panel
        apps_uidtm.write_log('INFO', f'Username: "{username_selected}" selected for edit/read')
        self.panel_stack.pop().destroy() #Self destroy and go to upper panel
        input_panel_edit = Toplevel(self.root)
        self.panel_stack.append(input_panel_edit)
        input_panel_edit.iconphoto(False, self.logo)
        x = self.root.winfo_x()
        y = self.root.winfo_y()  # Get position of main panel
        input_panel_edit.geometry(f'300x180+{x + 200}+{y + 120}')
        input_panel_edit.title('Edit Panel')
        input_panel_edit.resizable(False, False)
        input_panel_edit.grab_set()  # disable the main panel
        tk.Label(input_panel_edit, text='Username: ', font=self.font_size_12).place(x=5, y=10)
        tk.Label(input_panel_edit, text='Badge Name: ', font=self.font_size_12).place(x=5, y=40)
        tk.Label(input_panel_edit, text='Password: ', font=self.font_size_12).place(x=5, y=90)

        self.db_item = self.user_info_search_result[1][username_selected]
        self.badgename_fix = self.user_info_search_result[3][username_selected][0]
        dehash_pwd = apps_uidtm.dehash(self.user_info_search_result[3][username_selected][1])
        if dehash_pwd[0] == False: #Invalid password
            dehash_pwd[1] = '???'
        username_change = StringVar()
        password_change = StringVar()
        username_entry = tk.Entry(input_panel_edit, textvariable=username_change, font=self.font_size_12, width=15)
        password_entry = tk.Entry(input_panel_edit, textvariable=password_change, font=self.font_size_12, width=15)
        tk.Label(input_panel_edit,  text=self.badgename_fix, font=self.font_size_12).place(x=120, y=40)

        # Run login_validate_action when 'Login' button pressed.
        btn_submit = tk.Button(input_panel_edit, text='Submit', bg='Teal', fg='White', font=self.font_size_12,command=lambda: self.edit_submit(username_change.get(), password_change.get()))

        btn_submit.pack()
        username_entry.pack()
        password_entry.pack()

        username_entry.insert(0, username_selected)
        password_entry.insert(0, dehash_pwd[1])
        btn_submit.place(x=75, y=140, height=30, width=150)
        username_entry.place(x=120, y=10)
        password_entry.place(x=120, y=90)

        input_panel_edit.protocol('WM_DELETE_WINDOW', self.panel_quit_grab_set)

    def user_input_panel_create(self):
        # Build login panel
        input_panel_create = Toplevel(self.root)
        self.panel_stack.append(input_panel_create)
        input_panel_create.iconphoto(False, self.logo)
        x = self.root.winfo_x()
        y = self.root.winfo_y()  # Get position of main panel
        input_panel_create.geometry(f'300x180+{x + 200}+{y + 120}')
        input_panel_create.title('Create Panel')
        input_panel_create.resizable(False, False)
        input_panel_create.grab_set()  # disable the main panel
        tk.Label(input_panel_create, text='Badge Name: ', font=self.font_size_12).place(x=5, y=10)
        tk.Label(input_panel_create, text='Username: ', font=self.font_size_12).place(x=5, y=40)
        tk.Label(input_panel_create, text='Password: ', font=self.font_size_12).place(x=5, y=90)

        badgename_input = StringVar()
        username_input = StringVar()
        password_input = StringVar()

        badgename_entry = tk.Entry(input_panel_create, textvariable=badgename_input, font=self.font_size_12, width=15)
        username_entry = tk.Entry(input_panel_create, textvariable=username_input, font=self.font_size_12, width=15)
        password_entry = tk.Entry(input_panel_create, textvariable=password_input, font=self.font_size_12, width=15)        


        # Run login_validate_action when 'Login' button pressed.
        btn_create = tk.Button(input_panel_create, text='Create', bg='Teal', fg='White', font=self.font_size_12,command=lambda: self.create_submit(badgename_input.get(), username_input.get(), password_input.get()))

        btn_create.pack()
        badgename_entry.pack()
        username_entry.pack()
        password_entry.pack()


        btn_create.place(x=75, y=140, height=30, width=150)
        badgename_entry.place(x=120, y=10)
        username_entry.place(x=120, y=40)
        password_entry.place(x=120, y=90)

        input_panel_create.protocol('WM_DELETE_WINDOW', self.panel_quit_grab_set)

    def warning_panel(self):
        # Build login panel
        warning_panel = Toplevel(self.root)
        self.panel_stack.append(warning_panel)
        warning_panel.iconphoto(False, self.logo)
        x = self.root.winfo_x()
        y = self.root.winfo_y()  # Get position of main panel
        warning_panel.geometry(f'500x70+{x + 0}+{y + 120}')
        warning_panel.title('Warning...')
        warning_panel.resizable(False, False)
        warning_panel.grab_set()  # disable the main panel
        warning_label = tk.Label(warning_panel, text='Warning: For Authorized Person Only...', fg='red', font=self.font_size_18)
        warning_label.pack()
        warning_label.place(x=40, y=10)

        warning_panel.protocol('WM_DELETE_WINDOW', self.panel_quit_grab_set)

    def login_validation(self, username, password):
        res_dehash = apps_uidtm.dehash(apps_uidtm.default_hashed_password)
        if res_dehash[0] and not res_dehash[1] == '': 
            if username.get() == apps_uidtm.default_username and password.get() == res_dehash[1]:
                self.btn_create.config(state=tk.NORMAL)
                self.btn_edit.config(state=tk.NORMAL)
                self.btn_delete.config(state=tk.NORMAL)
                apps_uidtm.write_log('INFO', 'Login success...')
                self.panel_quit_grab_set()
                self.warning_panel()
            else:
                apps_uidtm.write_log('ERROR', 'Login fail...')
                messagebox.showerror('Error in login', 'Login Fail...')

    def account_create(self):
        self.user_info_search_result = apps_uidtm.get_user_info(apps_uidtm.db_networkpath) 
        self.user_input_panel_create()
        
    def account_edit(self):
        self.user_info_search_result = apps_uidtm.get_user_info(apps_uidtm.db_networkpath)
        if self.user_info_search_result[0] and not self.user_info_search_result[2]==None and not self.user_info_search_result[3]==None:
            self.user_info_panel_edit()

    def account_delete(self):
        self.user_info_search_result = apps_uidtm.get_user_info(apps_uidtm.db_networkpath)
        if self.user_info_search_result[0] and not self.user_info_search_result[2]==None and not self.user_info_search_result[3]==None:
            self.user_info_panel_delete()

    def edit_submit(self, username_change, password_change):
        #Check username_change value is ready exist in database
        bool_check_key = username_change in self.user_info_search_result[1].keys()
        if bool_check_key:
            username_item = self.user_info_search_result[1][username_change]
        if not bool_check_key or (username_item == self.db_item): #If no key -> username is not exist in current db
            hashed_pwd = apps_uidtm.data_hash(password_change).decode()
            self.update_db_user_info=[self.db_item, self.badgename_fix, username_change, hashed_pwd, 4]
            bool_update = apps_uidtm.update_db_record(apps_uidtm.db_networkpath, self.update_db_user_info)
            if bool_update:
                self.panel_quit_grab_set()
                apps_uidtm.write_log('INFO', f'Update successfully with username: "{username_change}" edited')
                messagebox.showinfo('Update successful', 'Update successfully')
            else:
                self.panel_quit_grab_set()
                apps_uidtm.write_log('ERROR', 'Update fail...\nPlease go to log file to see for detail')
                messagebox.showerror('Update fail', 'Update fail...\nPlease go to log file to see for detail')
        else:
            self.panel_quit_grab_set()
            apps_uidtm.write_log('ERROR', f'Username: "{username_change}" already exist')
            messagebox.showerror('Update fail', f'Username: "{username_change}" already exist')

    def create_submit(self, badgename, username, password):
        if not badgename=='' and not username=='' and not password=='':
            hashed_pwd = apps_uidtm.data_hash(password).decode()
            new_account_info_list = [badgename, username, hashed_pwd, 4] #Accesslevel fix to 4
            bool_new_account = apps_uidtm.new_account_create_db(apps_uidtm.db_networkpath, new_account_info_list)
            self.panel_quit_grab_set()
            if bool_new_account:
                messagebox.showinfo('Account create successful', f'Account create sucessful\n\nBadgename: {badgename}\nUsername: {username}')
            else:
                messagebox.showerror('Account create fail', f'Account create fail...\nPlease go to log file to see for detail')
        else:
            self.panel_quit_grab_set()
            messagebox.showerror('Account create fail', f'Account create fail...\nInput fields empty or Badgename/Username ready exist')

    def confirm_deleted(self, username):
        bool_delete = apps_uidtm.account_delete_db(apps_uidtm.db_networkpath, username)
        self.panel_quit_grab_set()

        if bool_delete:
            messagebox.showinfo('Delete successful', f'Delete successful: Account with username: "{username}" had been deleted')
        else:
            messagebox.showerror('Delete fail...', 'Delete fail...\nPlease go to log file to see for detail')

    def record_delete(self, username):
        apps_uidtm.write_log('INFO', f'Username: "{username}" selected for delete')        
        self.panel_quit_grab_set()
        self.delete_confirm_panel(username)

    def panel_quit_grab_set(self):
        self.panel_stack.pop().destroy() #Self destroy and go to upper panel
        self.panel_stack[len(self.panel_stack)-1].grab_set()




# Main program entry
if __name__=='__main__':
    """
    - This is the main entry point of main program
    """
    main_ver = 1
    main_sub_ver = 0

    apps_uidtm = UidmtFunc(main_ver, main_sub_ver)
    root = tk.Tk()
    tk_func = TkFunc(root)
    apps_uidtm.write_log('INFO', f'Loading UIDMT main module...Ver:{main_ver}.{main_sub_ver}')
    tk_func.uidmt_main_panel()
    root.mainloop()

