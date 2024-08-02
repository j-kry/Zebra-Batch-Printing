import tkinter as tk
import pyperclip as pc
from datetime import datetime
import sqlite3

# Main Program Function
def GenerateLabels(event):
   #  Reset the Error Label
    errLbl.configure(text="")
   #  Check that the entered starting number and quantity are both numbers greater than 0
    if (startEnt.get().isnumeric() and qEnt.get().isnumeric()):
        if (int(qEnt.get()) > 0):

            output = ""
            incNum = 0
            templ2 = templateH2 if smallPrintCheck == 0 else templateH2SmallPrinter

            InsertIntoLabelLog(prefixEnt.get(), startEnt.get(), qEnt.get())

            for x in range(0, int(qEnt.get())):
                incNum = int(startEnt.get()) + x
                incNum = str(incNum)
                if (len(incNum) < 4):
                    incNum = incNum.zfill(4)
                output += (templateH1 + str(prefixEnt.get()) +
                           incNum + templ2)

            # Copy the generated output to the clipboard
            PrepareOutput(output)
        else:
            errLbl.configure(fg=("#AA0000"),
                             text="Quantity must be greater than 0 😡")
    else:
        errLbl.configure(fg=("#AA0000"),
                         text="Only enter whole numbers 😡")
        
def PrepareOutput(text):
   pc.copy(text)
   savedLbl.configure(fg=("#00AA00"), text="Copied to clipboard!")
   # Wait 3 seconds and then hide the label again
   window.after(3000, lambda:savedLbl.config(text=""))

def DisplayLabelLog():
    con = sqlite3.connect("log.db")
    cur = con.cursor()
    dbList = cur.execute("SELECT name from sqlite_master WHERE name='label'")
    if(dbList.fetchone() == None):
        cur.execute("CREATE TABLE label(startLabel, quantity, printDate, who)")
   #  cur.execute("""INSERT INTO label VALUES('24P100', 10, '08-02-2024', 'Justin'),('24N100', 20, '08-02-2024', 'Matt')""")
   #  con.commit()
    results = cur.execute("SELECT * FROM label")
    labelLog.config(state="normal")
    labelLog.insert(tk.END, results.fetchall())
    labelLog.config(state="disabled")

def InsertIntoLabelLog(prefix, start, quantity):
   con = sqlite3.connect("log.db")
   cur = con.cursor()
   dbList = cur.execute("SELECT name from sqlite_master WHERE name='label'")
   if(dbList.fetchone() == None):
      cur.execute("CREATE TABLE label(startLabel, quantity, printDate, who)")
   
   cur.execute("""INSERT INTO label VALUES({t}, {q}, {d}, {n})""".format(t = prefix + start, q = quantity, d = datetime.now(), n = "Justin"))
   con.commit()
   results = cur.execute("SELECT * FROM label LIMIT 10")
   labelLog.config(state="normal")
   labelLog.insert(tk.END, results.fetchall())
   labelLog.config(state="disabled")
       

# Template 1 is for the large printer and template 2 is for the smaller printer
templateH1 = "^XA^FO45,30^A0,50,80^FDProperty of Thresholds^FS^FO45,90^BY4^BCN,80,Y,N,N,N^FD"
templateH2 = "^FS^FO480,90^A0,35^FD(773) - 572 - 5399^FS^FO530,140^A0,40,60^FDOption 1^FS^XZ"
templateH2SmallPrinter = "^FS^FO495,90^A0,35^FD(773) - 572 - 5399^FS^FO530,140^A0,40,60^FDOption 1^FS^XZ"

# Create the window and add elements to the interface
window = tk.Tk()
window.geometry("500x600")
window.title("Zebra Batch Label Generator")

errLbl = tk.Label(master=window, text="")
errLbl.pack()

prefixLbl = tk.Label(master=window, text="Enter the prefix (ex. 23P or 23N)")
prefixLbl.pack()

prefixEnt = tk.Entry(master=window, text="Prefix")
prefixEnt.pack()

startLbl = tk.Label(master=window, text="Enter the starting label #")
startLbl.pack()

startEnt = tk.Entry(master=window, text="Start")
startEnt.bind('<Return>', GenerateLabels)
startEnt.pack()

qLbl = tk.Label(master=window, text="How many labels to print?")
qLbl.pack()

qEnt = tk.Entry(master=window, text="Quantity")
qEnt.bind('<Return>', GenerateLabels)
qEnt.pack()

smallPrintCheck = tk.Checkbutton(master=window, text='If using the smaller printer please check this', onvalue=1, offvalue=0)
smallPrintCheck.pack()

printBtn = tk.Button(master=window, text="Generate Labels", width=15,)
printBtn.bind('<Button-1>', GenerateLabels)
printBtn.pack(pady=25)

savedLbl = tk.Label(master=window, text="")
savedLbl.pack(pady=1)

labelLogLbl = tk.Label(master=window, text="Last 10 Prints")
labelLogLbl.pack()

labelLog = tk.Text(master=window, bd="3", bg="light yellow", height=10, width=20, state="disabled")
labelLog.pack()
# On window load add text to the labelLog
window.after(0, DisplayLabelLog())

viewLogBtn = tk.Button(master=window, text="View Full Log", width=15)
viewLogBtn.pack()

window.mainloop()
