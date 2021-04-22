import time, pyautogui, keyboard, threading
from tkinter import *

window = Tk()

window.title("Autoclicker")
#functions
def clickedStart():
    print("Button Clicked")
    time.sleep(3)
    run = True
    intervalInt = None
    try:
        intervalInt = int(text.get())
    except:
        pass
    
    start = time.time()
    while run == True:
        if keyboard.is_pressed('P'): #Key to stop Clicking
            run == False
            break
        if intervalInt != None:
            if time.time() >= (start + intervalInt):
                pyautogui.click()
                start= time.time()
        else:
            pyautogui.click()

label = Label(window, text = "Click Delay")
label.grid(column= 1, row= 0, padx = (75, 10))

text= Entry(window, width = 10)
text.grid(column = 1, row = 1, padx = (75, 10))
window.geometry('250x100')
#Button
btn = Button(window, text = "Start Clicking", command  = clickedStart, bg = "green", fg  = "lightgreen")
btn.grid(column = 1, row = 2, padx = (75, 10), pady = (15,10))


window.mainloop()