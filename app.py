#tkinter enter lower bound and upper bound
#loop to make each label templateH1 + assetNum + templateH2
#concat each label to the main string

from tkinter.filedialog import asksaveasfilename
import customtkinter as ctk

def DoTheThing(event):
    errLbl.configure(text="")
    if(startEnt.get().isnumeric() and endEnt.get().isnumeric()):
        if(endEnt.get() > startEnt.get()):

            output = ""

            for x in range(int(startEnt.get()), int(endEnt.get()) + 1):
                output += (templateH1 + str(x) + templateH2)

            FileSave(output)
        else:
            errLbl.configure(text_color=("#AA0000"), text="End number must be bigger than start number 😡")
    else:
        errLbl.configure(text_color=("#AA0000"), text="Only enter whole numbers 😡")

def SavePath():
    #Path = the one from the window
    filePath = asksaveasfilename(filetypes=[("Zebra Printer File", "*.prn")])

    #If filePath empty then return
    if not filePath:
        return

    return(filePath + ".prn")

def FileSave(text):
    try:
        path = SavePath()
        f = open(path, "x")
        f.write(text)
        f.close()
        savedLbl.configure(text_color="green", text=f"Successfully saved to \"{path}\"")
    except:
        print("There is already a file with that name!!")

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

endLbl = ctk.CTkLabel(master=window, text="Enter the ending label #")
endLbl.pack()

endEnt = ctk.CTkEntry(master=window, placeholder_text="End")
endEnt.bind('<Return>', DoTheThing)
endEnt.pack()

printBtn = ctk.CTkButton(master=window, text="Save to file", width=30)
printBtn.bind('<Button-1>', DoTheThing)
printBtn.pack(pady=5)

savedLbl = ctk.CTkLabel(master=window, text="", wraplength=250)
savedLbl.pack(pady=5)

window.mainloop()