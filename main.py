#importing necessary modules/packages
from customtkinter import *
from CTkMessagebox import CTkMessagebox

#Setting Appearance
set_appearance_mode("light")
set_default_color_theme("green")

#Making the window and giving it title
app = CTk()
app.title("Home")
app.geometry("320x480")

#Forming the frame
frame = CTkFrame(master=app, width=300, height=460, fg_color="#000000")
frame.pack_propagate(False)
frame.pack(expand=True, side="right")

option = "Select an Option"
def optionSelected(choice):
    global option
    if choice != option:
        option = choice
def createAcc():
    os.system(f'python newacc.py 1')
def close():
    exit()
def confirmSelection():
    if option != "Select an Option":
        if option == "Withdraw Amount" or option == "Balance Amount":
            os.system(f'python transaction.py 1')
        elif option == "All account holder list":
            os.system(f'python account.py 1')
        elif option == "Close an account" or option == "Modify an account":
            os.system(f'python modify.py 1')
    else:
        CTkMessagebox(title="Error",message="Option not selected!",icon="warning")


#Forming Welcome label
CTkLabel(master=frame,
         text="Welcome",
         text_color="#F4DFC8",
         anchor="w",
         justify="left",
         font=("Helvetica", 24)).pack(anchor="w", pady=(50, 2), padx=(25, 0))

#Forming a label to configure or connect to a server
CTkLabel(master=frame,
         text="This is a bank management system software\nSelect an option from the menu below",
         text_color="#F4EAE0", anchor="w",
         justify="left",
         font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 20), pady=(15,5))

CTkLabel(master=frame,
         text="Select an option: ",
         text_color="#F4DFC8",
         anchor="w",
         justify="left",
         font=("Helvetica", 16)).pack(anchor="w", pady=(5, 2), padx=(25, 0))

operation = CTkOptionMenu(master=frame,
                          values=["Select an Option",
                                         "Withdraw Amount",
                                         "Balance Amount",
                                         "All account holder list",
                                         "Close an account",
                                         "Modify an account"],
                          width=225,
                          command=optionSelected,
                          fg_color="#F4EAE0",
                          button_color="#F4EAE0",
                          button_hover_color="#F4DFC8",
                          text_color="#000000")
operation.pack(anchor="w", padx=(25, 0), pady=(5,15))

selectBtn = CTkButton(master=frame,
                      text="Select",
                      fg_color="#F4DFC8",
                      hover_color="#F4EAE0",
                      font=("Arial Bold", 12),
                      text_color="#000000",
                      width=225,
                      command=confirmSelection)
selectBtn.pack(anchor="w", pady=(0, 15), padx=(25, 25))

CTkLabel(master=frame,
         text="Don't have an account\nCreate one with us!",
         text_color="#F4EAE0", anchor="w",
         justify="left",
         font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 25), pady=(15,5))

accBtn = CTkButton(master=frame,
                    text="Create an account",
                    fg_color="#F4DFC8",
                    hover_color="#F4EAE0",
                    font=("Arial Bold", 12),
                    text_color="#000000",
                    width=225,
                    command=createAcc)
accBtn.pack(anchor="w", pady=(0, 15), padx=(25, 25))


exitBtn = CTkButton(master=frame,
                    text="Exit",
                    fg_color="#F4DFC8",
                    hover_color="#F4EAE0",
                    font=("Arial Bold", 12),
                    text_color="#000000",
                    width=225,
                    command=close)
exitBtn.pack(anchor="w", pady=(25, 15), padx=(25, 25))

app.mainloop()

