# Serial port demo in console

import serial
import serial.tools
import serial.tools.list_ports as port_list
import time

ports = list(port_list.comports())
com_list = []

for each_ports in ports:
    com_list.append(str(each_ports))

print (f'PORT = {com_list[0].split()[0]}')

ser = serial.Serial(port = com_list[0].split()[0], 
                    baudrate=9600,
                    parity=serial.PARITY_ODD,
                    stopbits=serial.STOPBITS_TWO,
                    bytesize=serial.SEVENBITS)
xabc = 1
while True:
    #Get keyboard input
    x = input ('Input a string: ')
    if x == 'exit':
        ser.close()
        exit()
    else:
        x = x + '\\r\\n'
        ser.write(x.encode())
        out = ''
    time.sleep(1)
    print ('Test')

    for line in ser.read(100):
        print ('Test')
        print (f'Line = {line}')






'''
from tkinter import *

root = Tk()
root.geometry('1000x300')
frame = Frame(root, height=100, width=300)
frame.pack(side='left', anchor=NW)
frame.pack_propagate(0)

#bottomframe = Frame(root)
#bottomframe.pack( side = BOTTOM )

tk_label = Label(frame, text='Test', height=60, width=15)
tk_label.pack(side=LEFT)

redbutton = Button(frame, text="Red", fg="red")
redbutton.pack( side = RIGHT, anchor=NW)

greenbutton = Button(frame, text="Brown", fg="brown")
greenbutton.pack( side = LEFT )

bluebutton = Button(frame, text="Blue", fg="blue")
bluebutton.pack( side = LEFT )


#blackbutton = Button(bottomframe, text="Black", fg="black")
#blackbutton.pack( side = BOTTOM)

root.mainloop()
'''

'''
# importing tkinter
import tkinter as tk

# Function to update the image in label
def update_image_in_label():
    label_pic.config(image=image_2)

# tkinter application window
root = tk.Tk()
root.title("GeeksForGeeks")
root.geometry("400x200")
root.config(bg="green")

# Converting image to PhotoImage variables
image_1 = tk.PhotoImage(file="C:\\Cimiy20181027\\HomeProjects\\Python_PC\\ISMCLK\\img\\digit_00.png")
image_2 = tk.PhotoImage(file="C:\\Cimiy20181027\\HomeProjects\\Python_PC\\ISMCLK\\img\\digit_01.png")

# Label widget with image
label_pic = tk.Label(root, image=image_1)
label_pic.pack(pady=15)

# Button widget
update_button = tk.Button(root, text="Update image",
                          command=update_image_in_label, 
                          bg="black", fg="white", 
                          font=("Arial", 15))
update_button.pack()

# Run application
root.mainloop()
'''




'''
import tkinter as tk
from PIL import Image, ImageTk
import time


# Create the main window
root = tk.Tk()
root.title("Image in Frame Example")
root.geometry("400x400")  # Optional: set window size

# Create a frame within the main window
# Load the image using Pillow
image_path = 'C:\\Cimiy20181027\\HomeProjects\\Python_PC\\ISMCLK\\img\\digit_00.png'  # Replace with your image path
image = Image.open(image_path)
image_array = ['digit_00.png', 'digit_01.png','digit_02.png','digit_03.png','digit_04.png',
               'digit_05.png','digit_06.png','digit_07.png','digit_08.png','digit_09.png']


# Resize the image using the new resampling attribute
image = image.resize((150, 200), Image.Resampling.LANCZOS)

# Convert the image to a Tkinter-compatible photo image
photo_image = ImageTk.PhotoImage(image)

# Create a label widget to hold the image
image_label = tk.Label(root, image=photo_image).place(x=0, y=0)

# Place the label in the frame
root.mainloop()
'''