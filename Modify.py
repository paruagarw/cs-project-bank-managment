#importing necessary modules/packages
from customtkinter import *
from CTkMessagebox import CTkMessagebox
import mysql.connector as sqlcon

conn =  sqlcon.connect(
    host="localhost",
    user="root",
    password="1234",
    database="BANK"
)

cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS accounts(AccountNo BIGINT PRIMARY KEY,"
               "name VARCHAR(50),"
               "EmailId VARCHAR(100),"
               "PhoneNo INT,"
               "Address VARCHAR(255),"
               "Balance INT) ")
conn.commit()

#Setting Appearance
set_appearance_mode("light")
set_default_color_theme("green")

#Making the window and giving it title
app = CTk()
app.title("Bank Management System")
app.geometry("720x480")

#Forming the frame
accframe = CTkFrame(master=app, width=300, height=400, fg_color="#000000")
accframe.pack_propagate(False)
accframe.pack(expand=True, side="right")

frame = CTkFrame(master=app, width=300, height=460, fg_color="#000000")
frame.pack_propagate(False)
frame.pack(expand=True, side="right")


def show_warning():
    msg = CTkMessagebox(title="Warning Message!", message="Do you want to delete your account?",
                        icon="warning", option_1="Cancel", option_2="Yes")

    if msg.get() == "Yes":
        cmd = "DELETE FROM accounts WHERE AccountNo={}".format(accNo.get())
        cursor.execute(cmd)
        conn.commit()
        CTkMessagebox(title="Delete",message="Your account has been deleted")
        cmd = "RENAME TABLE ACC{} TO ARCHIVE{}".format(accNo.get(),accNo.get())
        #chk in sql cmd if works execute

def search():
    cursor = conn.cursor()
    cmd = "SELECT * FROM accounts"
    cursor.execute(cmd)
    accounts = cursor.fetchall()
    for account in accounts:
        if int(accNo.get()) == account[0]:
            name.delete(0, END)
            name.insert(0, account[1])
            email.delete(0, END)
            email.insert(0, account[2])
            phoneNo.delete(0, END)
            phoneNo.insert(0, account[3])
            address.delete(0, END)
            address.insert(0, account[4])
            break

    else:
        CTkMessagebox(title="Error",message="Account not found. Check account number!")
        name.delete(0, END)
        email.delete(0, END)
        phoneNo.delete(0, END)
        address.delete(0, END)


def delAcc():
    show_warning()
    search()
def modifyAcc():
    cmd = "UPDATE accounts SET name ='{}',EmailId='{}',PhoneNo={},Address='{}' WHERE AccountNo = {}".format(name.get(),email.get(),phoneNo.get(),address.get(),accNo.get())
    print(cmd)
    cursor.execute(cmd)
    conn.commit()
    CTkMessagebox(title="Updated",message="Your records have been updated!")


CTkLabel(master=frame,
         text="Current values",
         text_color="#F4DFC8",
         anchor="w",
         justify="left",
         font=("Helvetica", 24)).pack(anchor="w", pady=(15, 2), padx=(25, 0))

CTkLabel(master=frame,
         text="Your Name:",
         text_color="#F4DFC8",
         anchor="w",
         justify="left",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 5), padx=(25, 0))

name = (CTkEntry(master=frame,
                      width=225,
                      fg_color="#F4DFC8",
                      border_color="#601E88",
                      border_width=1,
                      text_color="#000000"))
name.pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame,
         text="Your EmailID:",
         text_color="#F4DFC8",
         anchor="w",
         justify="left",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 5), padx=(25, 0))

email = (CTkEntry(master=frame,
                      width=225,
                      fg_color="#F4DFC8",
                      border_color="#601E88",
                      border_width=1,
                      text_color="#000000"))
email.pack(anchor="w", padx=(25, 0))


CTkLabel(master=frame,
         text="Phone Number:",
         text_color="#F4DFC8",
         anchor="w",
         justify="left",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 5), padx=(25, 0))

phoneNo = (CTkEntry(master=frame,
                      width=225,
                      fg_color="#F4DFC8",
                      border_color="#601E88",
                      border_width=1,
                      text_color="#000000"))
phoneNo.pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame,
         text="Address:",
         text_color="#F4DFC8",
         anchor="w",
         justify="left",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 5), padx=(25, 0))

address = (CTkEntry(master=frame,
                      width=225,
                      fg_color="#F4DFC8",
                      border_color="#601E88",
                      border_width=1,
                      text_color="#000000"))
address.pack(anchor="w", padx=(25, 0))

modifyBtn = CTkButton(master=frame,
                    text="Modify account",
                    fg_color="#F4DFC8",
                    hover_color="#F4EAE0",
                    font=("Arial Bold", 12),
                    text_color="#000000",
                    width=225,
                    command=modifyAcc)
modifyBtn.pack(anchor="w", pady=(20, 5), padx=(25, 25))

delBtn = CTkButton(master=frame,
                    text="Delete Account",
                    fg_color="#F4DFC8",
                    hover_color="#F4EAE0",
                    font=("Arial Bold", 12),
                    text_color="#000000",
                    width=225,
                    command=delAcc)
delBtn.pack(anchor="w", pady=(0, 15), padx=(25, 25))


CTkLabel(master=accframe,
         text="Search Account",
         text_color="#F4DFC8",
         anchor="w",
         justify="left",
         font=("Helvetica", 24)).pack(anchor="w", pady=(15, 2), padx=(25, 0))

CTkLabel(master=accframe,
         text="Your account number:",
         text_color="#F4DFC8",
         anchor="w",
         justify="left",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 5), padx=(25, 0))

accNo = (CTkEntry(master=accframe,
                      width=225,
                      fg_color="#F4DFC8",
                      border_color="#601E88",
                      border_width=1,
                      text_color="#000000"))
accNo.pack(anchor="w", padx=(25, 0))


searchBtn = CTkButton(master=accframe,
                    text="Search Account",
                    fg_color="#F4DFC8",
                    hover_color="#F4EAE0",
                    font=("Arial Bold", 12),
                    text_color="#000000",
                    width=225,
                    command=search)
searchBtn.pack(anchor="w", pady=(15, 15), padx=(25, 25))


app.mainloop()
