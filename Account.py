#importing necessary modules/packages
from customtkinter import *
from CTkTable import *
import mysql.connector as sqlcon
from CTkMessagebox import CTkMessagebox

conn =  sqlcon.connect(
    host="localhost",
    user="root",
    password="1234",
    database="BANK"
)

cursor = conn.cursor()
cmd = "SELECT * FROM accounts"
cursor.execute(cmd)

#Setting Appearance
set_appearance_mode("light")
set_default_color_theme("green")

#Making the window and giving it title
app = CTk()
app.title("Bank management system")
app.geometry("1440x720")

#Forming the frame

controlFrame = CTkFrame(master=app, width=300, height=480, fg_color="#000000")
controlFrame.pack_propagate(False)
controlFrame.pack(expand=True, side="right")


frame = CTkFrame(master=app, width=960, height=680, fg_color="#000000")
frame.pack_propagate(False)
frame.pack(expand=True, side="right")

def back():
    global stop
    global start

    if stop>20:
        start -= 20
        stop -= 20
        showValue = value[start:stop]
        table.configure(values=showValue)
        print(value)
        print(showValue)
    else:
        CTkMessagebox(title="Warning", message="No previous records to display")
def nextPage():
    global stop
    global start

    if len(value)>stop:
        start+=20
        stop+=20
        showValue = value[start:stop]
        table.configure(values=showValue)
        print(value)
        print(showValue)
    else:
        CTkMessagebox(title="Warning",message="No more records to display")
def search():
    inputAcc =  accNo.get()
    for i in value:
        if int(inputAcc) == i[0]:
            showValue = [i]
            table.configure(values=showValue)
            print(value)
            print(showValue)

def reset():
    global stop
    global start

    start = 0
    stop = 20

    showValue = value[start:stop]
    table.configure(values=showValue)
    print(value)
    print(showValue)


value = cursor.fetchall()
start = 0
stop = 20
showValue = value[start:stop]

CTkLabel(master=frame,
         text="Displaying all account records",
         text_color="#F4DFC8",
         anchor="w",
         justify="left",
         font=("Helvetica", 24)).pack(anchor="w", pady=(15, 2), padx=(25, 0))
print(showValue)
table = CTkTable(master=frame, row=20, column=6, values=showValue, font=("Helvetica", 12))
table.pack(expand=True, fill="both", padx=5, pady=5)

CTkLabel(master=controlFrame,
         text="Search records",
         text_color="#F4DFC8",
         anchor="w",
         justify="left",
         font=("Helvetica", 24)).pack(anchor="w", pady=(15, 2), padx=(25, 0))

CTkLabel(master=controlFrame,
         text="Enter account number:",
         text_color="#F4DFC8",
         anchor="w",
         justify="left",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 5), padx=(25, 0))

accNo = (CTkEntry(master=controlFrame,
                      width=225,
                      fg_color="#F4DFC8",
                      border_color="#601E88",
                      border_width=1,
                      text_color="#000000"))
accNo.pack(anchor="w", padx=(25, 0))


searchBtn = CTkButton(master=controlFrame,
                    text="Search",
                    fg_color="#F4DFC8",
                    hover_color="#F4EAE0",
                    font=("Arial Bold", 12),
                    text_color="#000000",
                    width=225,
                    command=search)
searchBtn.pack(anchor="w", pady=(15, 15), padx=(25, 25))


CTkLabel(master=controlFrame,
         text="Click the buttons below to\ntoggle between record pages",
         text_color="#F4EAE0", anchor="w",
         justify="left",
         font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 25), pady=(15,5))

nextBtn = CTkButton(master=controlFrame,
                    text="View next 20 records",
                    fg_color="#F4DFC8",
                    hover_color="#F4EAE0",
                    font=("Arial Bold", 12),
                    text_color="#000000",
                    width=225,
                    command=nextPage)
nextBtn.pack(anchor="w", pady=(0, 15), padx=(25, 25))


backBtn = CTkButton(master=controlFrame,
                    text="View last 20 records",
                    fg_color="#F4DFC8",
                    hover_color="#F4EAE0",
                    font=("Arial Bold", 12),
                    text_color="#000000",
                    width=225,
                    command=back)
backBtn.pack(anchor="w", pady=(0, 15), padx=(25, 25))


resetBtn = CTkButton(master=controlFrame,
                    text="Reset Table",
                    fg_color="#F4DFC8",
                    hover_color="#F4EAE0",
                    font=("Arial Bold", 12),
                    text_color="#000000",
                    width=225,
                    command=reset)
resetBtn.pack(anchor="w", pady=(0, 15), padx=(25, 25))


app.mainloop()
