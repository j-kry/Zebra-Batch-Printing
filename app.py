# tkinter enter lower bound and upper bound
# loop to make each label templateH1 + assetNum + templateH2
# concat each label to the main string

### Update###
# Change the second input box to a quantity
# Enter starting tag and quantity to print

from tkinter.filedialog import asksaveasfilename
import customtkinter as ctk
import pyautogui as pag
import pyperclip as pc
from subprocess import Popen
import os
import time


def DoTheThing(event):
    errLbl.configure(text="")
    if (startEnt.get().isnumeric() and qEnt.get().isnumeric()):
        if (int(qEnt.get()) > 0):

            output = ""

            for x in range(0, int(qEnt.get())):
                output += (templateH1 +
                           str(int(startEnt.get()) + x) + templateH2)

            # FileSave(output)
            zPrint(output)
        else:
            errLbl.configure(text_color=("#AA0000"),
                             text="Quantity must be greater than 0 😡")
    else:
        errLbl.configure(text_color=("#AA0000"),
                         text="Only enter whole numbers 😡")


def SavePath():
    # Path = the one from the window
    filePath = asksaveasfilename(filetypes=[("Zebra Printer File", "*.prn")])

    # If filePath empty then return
    if not filePath:
        return

    return (filePath + ".prn")


def FileSave(text):
    try:
        path = SavePath()
        f = open(path, "x")
        f.write(text)
        f.close()
        savedLbl.configure(text_color="green",
                           text=f"Successfully saved to \"{path}\"")
    except:
        print("There is already a file with that name!!")

# Added 02-27-2023
# Need to run compiled program as admin


def zPrint(text):
    pc.copy(text)
    print(pag.size())
    Popen(['C:\Program Files (x86)\Zebra Technologies\Zebra Setup Utilities\App\PrnUtils'])
    time.sleep(3)
    pag.moveTo(600, 315)  # Move to printer
    pag.leftClick()
    pag.moveTo(1100, 675)  # Move to open communication
    pag.leftClick()
    pc.paste()
    pag.moveTo(1000, 250)  # Move to send to printer
    pag.leftClick()


templateH1 = "^XA^FO45,30^A0,50,80^FDProperty of Thresholds^FS^FO45,90^BY4^BCN,80,Y,N,N,N^FD"
templateH2 = "^FS^FO480,90^A0,35^FD(773) - 572 - 5399^FS^FO530,140^A0,40,60^FDOption 1^FS^XZ"

window = ctk.CTk()
window.geometry("330x230")
window.title("Zebra .PRN File Generator")
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

errLbl = ctk.CTkLabel(master=window, text="")
errLbl.pack()

startLbl = ctk.CTkLabel(master=window, text="Enter the starting label #")
startLbl.pack()

startEnt = ctk.CTkEntry(master=window, placeholder_text="Start")
startEnt.bind('<Return>', DoTheThing)
startEnt.pack()

qLbl = ctk.CTkLabel(master=window, text="How many labels to print?")
qLbl.pack()

qEnt = ctk.CTkEntry(master=window, placeholder_text="Quantity")
qEnt.bind('<Return>', DoTheThing)
qEnt.pack()

printBtn = ctk.CTkButton(master=window, text="Save to file", width=30)
printBtn.bind('<Button-1>', DoTheThing)
printBtn.pack(pady=10)

savedLbl = ctk.CTkLabel(master=window, text="", wraplength=250)
savedLbl.pack(pady=5)

window.mainloop()
