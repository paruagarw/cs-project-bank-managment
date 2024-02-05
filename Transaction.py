#importing necessary modules/packages
import pip
pip.main(['install','mysql-connector-python-rf'])
from customtkinter import *
from CTkTable import *
import mysql.connector as sqlcon
from CTkMessagebox import CTkMessagebox
import datetime

conn =  sqlcon.connect(
    host="localhost",
    user="root",
    password="1234",
    database="BANK"
)
# Create transaction tables for all accounts when the application starts
def create_transaction_table(account_number):

    cursor = conn.cursor()
    cmd = f"CREATE TABLE IF NOT EXISTS ACC{account_number}(Date DATE, Transaction VARCHAR(150), amount INT)"
    print(cmd)
    cursor.execute(cmd)
    conn.commit()

def create_all_transaction_tables():
    cursor = conn.cursor()
    cmd = "SELECT AccountNo FROM accounts"
    cursor.execute(cmd)
    account_numbers = cursor.fetchall()

    for account_number in account_numbers:
        create_transaction_table(account_number[0])

create_all_transaction_tables()


#Setting Appearance
set_appearance_mode("light")
set_default_color_theme("green")

#Making the window and giving it title
app = CTk()
app.title("Bank management system")
app.geometry("1440x720")

#Forming the frame

controlFrame = CTkFrame(master=app, width=300, height=600, fg_color="#000000")
controlFrame.pack_propagate(False)
controlFrame.pack(expand=True, side="right")


frame = CTkFrame(master=app, width=960, height=680, fg_color="#000000")
frame.pack_propagate(False)
frame.pack(expand=True, side="right")

def back():
    global stop
    global start

    if stop>10:
        start -= 10
        stop -= 10
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
        start+=10
        stop+=10
        showValue = value[start:stop]
        table.configure(values=showValue)
        print(value)
        print(showValue)
    else:
        CTkMessagebox(title="Warning",message="No more records to display")
def search():
    global value
    cursor = conn.cursor()
    cmd = "SELECT * FROM accounts"
    print(cmd)
    cursor.execute(cmd)
    accounts = cursor.fetchall()

    for account in accounts:
        if int(accNo.get()) == account[0]:
            cmd = "SELECT * FROM ACC{}".format(account[0])
            print(cmd)
            cursor.execute(cmd)
            value = cursor.fetchall()
            showValue = value[start:stop]
            table.configure(values=showValue)
            break
    else:
        CTkMessagebox(title="Error",message="Account not found. Check account number!")

def reset():
    global stop
    global start

    start = 0
    stop = 10

    showValue = []
    table.configure(values=showValue)
    print(value)
    print(showValue)

def deposit():
    now = datetime.datetime.now()
    formatted_date = now.strftime('%Y-%m-%d')
    cursor = conn.cursor()
    cmd = "SELECT balance from accounts WHERE AccountNo = {}".format(accNo.get())
    cursor.execute(cmd)
    balance = cursor.fetchall()
    cmd = 'insert into ACC{} values("{}","{}",{})'.format(str(accNo.get()), formatted_date, "ACCOUNT_CREDITED",int(amount.get()))
    print(cmd)
    cursor.execute(cmd)
    conn.commit()

    cmd = "UPDATE accounts SET balance = {} WHERE AccountNo = {}".format(balance[0][0]+int(amount.get()),accNo.get())
    print(cmd)
    cursor.execute(cmd)
    conn.commit()
    CTkMessagebox(title="Depoit",message="Your account has been credited with {} rupees".format(amount.get()))
    search()
# Function to withdraw from an account
def withdraw():
    now = datetime.datetime.now()
    formatted_date = now.strftime('%Y-%m-%d')
    cursor = conn.cursor()
    cmd = "SELECT balance from accounts WHERE AccountNo = {}".format(accNo.get())
    cursor.execute(cmd)
    balance = cursor.fetchall()

    # Check if the withdrawal amount is valid
    if int(amount.get()) > balance[0][0]:
        CTkMessagebox(title="Insufficient Balance", message="You do not have sufficient balance for this withdrawal.")
   
    else:
        cmd = 'insert into ACC{} values("{}","{}",{})'.format(str(accNo.get()), formatted_date, "ACCOUNT_DEBITED", int(amount.get()))
        print(cmd)
        cursor.execute(cmd)
        conn.commit()

        cmd = "UPDATE accounts SET balance = {} WHERE AccountNo = {}".format(balance[0][0] - int(amount.get()), accNo.get())
        print(cmd)
        cursor.execute(cmd)
        conn.commit()
        CTkMessagebox(title="Withdraw", message="Your account has been debited with {} rupees".format(amount.get()))
        search()

# Function to check account balance
def balance():
    cmd = "SELECT balance from accounts WHERE AccountNo = {}".format(accNo.get())
    cursor = conn.cursor()
    cursor.execute(cmd)
    balance = cursor.fetchall()

    # Check if the balance is above the minimum required
    if balance[0][0] >= 100:
        CTkMessagebox(title="Account Balance", message="You account has {} rupees only.".format(balance[0][0]))
    else:
        CTkMessagebox(title="Minimum Balance Requirement", message="A minimum balance of 100 should be maintained in the account.")

CTkLabel(master=frame,
         text="Your Transcation",
         text_color="#F4DFC8",
         anchor="w",
         justify="left",
         font=("Helvetica", 24)).pack(anchor="w", pady=(15, 2), padx=(25, 0))


value = []
start = 0
stop = 10
showValue = value[start:stop]

table = CTkTable(master=frame, row=10, column=3, values=showValue, font=("Helvetica", 12))
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
searchBtn.pack(anchor="w", pady=(15,0), padx=(25, 25))

balanceBtn = CTkButton(master=controlFrame,
                    text="Show balance",
                    fg_color="#F4DFC8",
                    hover_color="#F4EAE0",
                    font=("Arial Bold", 12),
                    text_color="#000000",
                    width=225,
                    command=balance)
balanceBtn.pack(anchor="w", pady=(5, 5), padx=(25, 25))

CTkLabel(master=controlFrame,
         text="Enter the amount below to\ndeposit or withdraw",
         text_color="#F4EAE0", anchor="w",
         justify="left",
         font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 25), pady=(15,5))


CTkLabel(master=controlFrame,
         text="Enter amount:",
         text_color="#F4DFC8",
         anchor="w",
         justify="left",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 5), padx=(25, 0))

amount = (CTkEntry(master=controlFrame,
                      width=225,
                      fg_color="#F4DFC8",
                      border_color="#601E88",
                      border_width=1,
                      text_color="#000000"))
amount.pack(anchor="w", padx=(25, 0))

depositBtn = CTkButton(master=controlFrame,
                    text="Deposit",
                    fg_color="#F4DFC8",
                    hover_color="#F4EAE0",
                    font=("Arial Bold", 12),
                    text_color="#000000",
                    width=225,
                    command=deposit)
depositBtn.pack(anchor="w", pady=(15, 5), padx=(25, 25))


withdrawBtn = CTkButton(master=controlFrame,
                    text="Withdraw",
                    fg_color="#F4DFC8",
                    hover_color="#F4EAE0",
                    font=("Arial Bold", 12),
                    text_color="#000000",
                    width=225,
                    command=withdraw)
withdrawBtn.pack(anchor="w", pady=(0, 15), padx=(25, 25))

CTkLabel(master=controlFrame,
         text="Click the buttons below to\ntoggle between record pages",
         text_color="#F4EAE0", anchor="w",
         justify="left",
         font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 25), pady=(15,5))

nextBtn = CTkButton(master=controlFrame,
                    text="View next 10 transaction",
                    fg_color="#F4DFC8",
                    hover_color="#F4EAE0",
                    font=("Arial Bold", 12),
                    text_color="#000000",
                    width=225,
                    command=nextPage)
nextBtn.pack(anchor="w", pady=(0, 15), padx=(25, 25))


backBtn = CTkButton(master=controlFrame,
                    text="View last 10 transaction",
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
