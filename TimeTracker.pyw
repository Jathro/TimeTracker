from tkinter import *
import os.path
import datetime

root = Tk()
root.geometry("300x200")
root.geometry("+820+340")

file_exists = os.path.isfile("TimeLog.txt")
#print (file_exists)

if (not file_exists):
    f = open("TimeLog.txt", "x")
    f.close()

def settext(text):
    TextActivity.set(text)

def ClockedOn():
    clk_on["state"] = "disabled"
    clk_off["state"] = "normal"
    switch_btn["state"] = "normal"

def ClockedOff():
    clk_off["state"] = "disabled"
    switch_btn["state"] = "disabled"
    clk_on["state"] = "normal"
    
def clock_on():
    Name = get_name.get().upper()
    Activity = text_input.get().upper()
    text_input.delete(0,END)
    if (Activity != ''):
        f = open("TimeLog.txt", "a")
        f.write(Name + "|" + Activity + "|CLKON:" + str(datetime.datetime.now()) + "\n")
        f.close()
        ClockedOn()
        settext(Name + " is working on " + Activity)
    else:
        settext("Please enter an Activity")

def clock_off():
    Name = get_name.get().upper()
    FullHistory = user_history(Name, "f")
    for x in FullHistory:
        if (Name == x[0:x.find("|")] and
            x.find("CLKON:") > 0 and
            x.find("CLKOFF:") == -1):
            x.replace("\n", "")
            FullHistory[FullHistory.index(x)] = FullHistory[FullHistory.index(x)] + "|CLKOFF:" + str(datetime.datetime.now())
    write_list_to_file(FullHistory)
    ClockedOff()
    settext(Name + " is clocked off")

def switch():
    clock_off()
    clock_on()

def user_history(name, mode):
    f = open("TimeLog.txt", "r")
    lines = f.read().splitlines()
    f.close()
    curr_list = []
    
    for x in lines:
        y = x[0:x.find("|")]
        if (y == name):
            curr_list.append(x)

    if (mode == "s"):
        return curr_list
    elif (mode == "f"):
        return lines
    
def get_current(name):
    current = user_history(name, "s")

    if (len(current) > 0):
        z = current[len(current)-1]
        if (z.find("CLKON:") > 0 and z.find("CLKOFF:") == -1):
            return("ClockedOn")
        else:
            return("ClockedOff")
    else:
        return("ClockedOff")

def next_action(HowClocked, Name):
    if (HowClocked == "ClockedOn"):
        ClockedOn()
        
    elif (HowClocked == "ClockedOff"):
        ClockedOff()

def write_list_to_file(FullList):
    with open("TimeLog.txt", 'w') as FileHandle:
        for ListItem in FullList:
            FileHandle.write('%s\n' % ListItem)

def start():
    name = get_name.get().upper()
    current = get_current(name)
    settext(name + " is " + current)
    next_action(current, name)

def quit():
    root.destroy()

def set_text(text):
    get_name.delete(0,END)
    get_name.insert(0,text)
    start()
    return
    

i = 1
TextActivity = StringVar()
settext("Welcome, Enter Name below")
TextLabel = Label(root, textvariable=TextActivity)
TextLabel.grid(row=i, column=1, columnspan=4)

L1 = Label(root, text="Name")
L1.grid(row=2, column=1)
get_name = Entry(root, width=20, borderwidth=2)
get_name.grid(row=i+1, column=2, columnspan=2)

L2 = Label(root, text="Activity")
L2.grid(row=3, column=1)
text_input = Entry(root, width=20, borderwidth=2)
text_input.grid(row=i+2, column=2, columnspan=2)
text_input.bind('<Key-Return>', start)

clk_on = Button(root, text="ClockOn", command=clock_on)
clk_on.grid(row=i+3, column=1)

clk_off = Button(root, text="ClockOff", command=clock_off)
clk_off.grid(row=i+3, column=2)

switch_btn = Button(root, text="Switch", command=switch)
switch_btn.grid(row=i+3, column=3)

exit_btn = Button(root, text="Exit", command=quit)
exit_btn.grid(row=i+4, column=1, columnspan=3)

name_btn = Button(root, text="Name", command=lambda:set_text("Peter"))
name_btn.grid(row=i+4, column=1, columnspan=1)

clk_on["state"] = "disabled"
clk_off["state"] = "disabled"
switch_btn["state"] = "disabled"

root.mainloop()
