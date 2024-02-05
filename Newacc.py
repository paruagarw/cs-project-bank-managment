from customtkinter import *
from CTkMessagebox import CTkMessagebox
import mysql.connector as sqlcon
import random
import smtplib
import datetime

# Database connection
conn = sqlcon.connect(
    host="localhost",
    user="root",
    password="1234",
    database="BANK",
    auth_plugin='mysql_native_password'
)

# Cursor creation
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS accounts(AccountNo BIGINT PRIMARY KEY,"
               "name VARCHAR(50),"
               "EmailId VARCHAR(100),"
               "PhoneNo BIGINT,"
               "Address VARCHAR(255),"
               "Balance BIGINT) ")
conn.commit()

# Setting appearance
set_appearance_mode("light")
set_default_color_theme("green")

# Creating main application window
app = CTk()
app.title("Bank Management System")
app.geometry("320x480")

# Creating a frame
frame = CTkFrame(master=app, width=300, height=460, fg_color="#000000")
frame.pack_propagate(False)
frame.pack(expand=True, side="right")


# Function to close the application
def close():
    exit()


# Function to generate a random account number
def accountNumberGenerator():
    rng = range(100000000000, 999999999999)
    return random.choice(rng)

def sendEmail(name1,accountNumber,openingAmount):
    # Sending email notification
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login("acc.bankmanagment@gmail.com", "asmr vwwv mpwl tvhh")
    message = f'''Dear {name1},
       We are delighted to inform you that your bank account has been created successfully.
    Your account details are as follows:
        Account Number: {accountNumber}
        Initial Deposit: {openingAmount}
        In this digital era, we understand the importance of convenience and accessibility. Our  platform empowers you to effortlessly and conveniently   manage your finances, view transactions,credit or debit money in your account. Our  user-friendly interface is designed to simplify every aspect of your banking interactions..All of your  details are secured with encryption, ensuring the confidentiality of your personal information.
Thank you for choosing us as your financial partner. We are honored to be part of your financial journey and look forward to providing you with excellent service. Welcome to a world of banking made simple and secure

 Regards
'''

    s.sendmail("acc.bankmanagment@gmail.com", email.get(), message)
    s.quit()

# Function to create a new account
def createAcc():
    # Check if all fields are filled
    if name.get() != "" and email.get() != "" and phoneNo.get() != "" and address.get() != "" and openingAmnt.get() != "":
        # Check additional criteria for phone number, email, and address
        if phoneNo.get().isdigit() and len(phoneNo.get()) == 10:
            if "@" in email.get()and "." in email.get():

            # Check if opening amount is greater than or equal to 2000
                if int(openingAmnt.get()) >= 2000:
                    cursor = conn.cursor()
                    cmd = "SELECT * FROM accounts"
                    cursor.execute(cmd)
                    accountList = [i[0] for i in cursor.fetchall()]

                    while True:
                        accountNumber = accountNumberGenerator()
                        name1 = name.get()
                        openingAmount = openingAmnt.get()
                        if accountNumber not in accountList:
                            sendEmail(name1,accountNumber,openingAmount)

                            # Inserting data into the accounts table
                            cmd = "INSERT INTO accounts VALUES({},'{}','{}',{},'{}',{})".format(
                                accountNumber, name.get(), email.get(), int(phoneNo.get()), address.get(), int(openingAmnt.get())
                            )
                            cursor.execute(cmd)
                            CTkMessagebox(
                                title="Account Created", message=f"Your account has been created. Account number: {accountNumber}"
                            )
                            conn.commit()

                            # Creating a transaction table for the new account
                            cmd = f"CREATE TABLE ACC{str(accountNumber)}(Date DATE, Transaction VARCHAR(150),amount INT)"
                            cursor.execute(cmd)
                            conn.commit()

                            # Adding an initial transaction for the new account
                            now = datetime.datetime.now()
                            formatted_date = now.strftime("%Y-%m-%d")
                            cmd = 'insert into ACC{} values("{}","{}",{})'.format(
                                str(accountNumber), formatted_date, "ACCOUNT_CREDITED", openingAmnt.get()
                            )
                            cursor.execute(cmd)
                            conn.commit()

                            exit()
            else:
                CTkMessagebox(title="Error",message="Please enter a valid email-id")
        else:
            CTkMessagebox(title="Error",message="Please enter a valid phone number")
    else:
        CTkMessagebox(title="Empty Field", message="Please ensure all the details are filled.")


# Labels and Entry widgets for user input
CTkLabel(master=frame,
         text="Create New Account",
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

name = CTkEntry(master=frame,
                width=225,
                fg_color="#F4DFC8",
                border_color="#601E88",
                border_width=1,
                text_color="#000000")
name.pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame,
         text="Your EmailID:",
         text_color="#F4DFC8",
         anchor="w",
         justify="left",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 5), padx=(25, 0))

email = CTkEntry(master=frame,
                 width=225,
                 fg_color="#F4DFC8",
                 border_color="#601E88",
                 border_width=1,
                 text_color="#000000")
email.pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame,
         text="Phone Number:",
         text_color="#F4DFC8",
         anchor="w",
         justify="left",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 5), padx=(25, 0))

phoneNo = CTkEntry(master=frame,
                   width=225,
                   fg_color="#F4DFC8",
                   border_color="#601E88",
                   border_width=1,
                   text_color="#000000")
phoneNo.pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame,
         text="Address:",
         text_color="#F4DFC8",
         anchor="w",
         justify="left",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 5), padx=(25, 0))

address = CTkEntry(master=frame,
                   width=225,
                   fg_color="#F4DFC8",
                   border_color="#601E88",
                      border_width=1,
                      text_color="#000000")
address.pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame,
         text="Opening Amount:",
         text_color="#F4DFC8",
         anchor="w",
         justify="left",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 5), padx=(25, 0))

openingAmnt = (CTkEntry(master=frame,
                        width=225,
                        fg_color="#F4DFC8",
                        border_color="#601E88",
                        border_width=1,
                        text_color="#000000"))
openingAmnt.pack(anchor="w", padx=(25, 0))

createBtn = CTkButton(master=frame,
                      text="Create an account",
                      fg_color="#F4DFC8",
                      hover_color="#F4EAE0",
                      font=("Arial Bold", 12),
                      text_color="#000000",
                      width=225,
                      command=createAcc)
createBtn.pack(anchor="w", pady=(5, 5), padx=(25, 25))

exitBtn = CTkButton(master=frame,
                    text="Exit",
                    fg_color="#F4DFC8",
                    hover_color="#F4EAE0",
                    font=("Arial Bold", 12),
                    text_color="#000000",
                    width=225,
                    command=close)

exitBtn.pack(anchor="w", pady=(0, 15), padx=(25, 25))

app.mainloop()
