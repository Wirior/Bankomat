text_title = R"""
______                _                              _   
| ___ \              | |                            | |  
| |_/ /  __ _  _ __  | | __  ___   _ __ ___    __ _ | |_ 
| ___ \ / _` || '_ \ | |/ / / _ \ | '_ ` _ \  / _` || __|
| |_/ /| (_| || | | ||   < | (_) || | | | | || (_| || |_ 
\____/  \__,_||_| |_||_|\_\ \___/ |_| |_| |_| \__,_| \__|    V:1.0                                                         
"""

text_admin = R"""
                 _               _         
     /\         | |             (_)        
    /  \      __| |  _ __ ___    _   _ __  
   / /\ \    / _` | | '_ ` _ \  | | | '_ \ 
  / ____ \  | (_| | | | | | | | | | | | | |
 /_/    \_\  \__,_| |_| |_| |_| |_| |_| |_|
"""

# from getpass import getpass # Importing the hidden password module for user input
# import inquirer  # Importing the inquirer module for interactive user prompts

import os  # Importing the os module to interact with the operating system
import time  # Importing the time module for time-related functions
import json  # Importing the json module for JSON file operations
from datetime import date  # Importing the date class from the datetime module
import random # Importing random function for slump actions
import matplotlib.pyplot as plt # importing pylot module to plot grapths
from tkinter import *
from tkinter import ttk

from email_validator import validate_email, EmailNotValidError  # Importing email validation functions

"""
Remember to replace the file path with your location of the files and replace the \\(backslah) with / 
"""
Path_Users = "C:/Users/William/My Drive/Gruppuppgift/Bankomat-main-gui/Users.json"  # Path to the users JSON file
Path_Passwords = "C:/Users/William/My Drive/Gruppuppgift/Bankomat-main-gui/Passwords.json"  # Path to the passwords JSON file
Path_Accounts = "C:/Users/William/My Drive/Gruppuppgift/Bankomat-main-gui/Accounts.json"  # Path to the accounts JSON file

today = date.today()  # Getting today's date

def read_file(filepath:str):
    """Fuction to read a json file and return a dump of json.
    - Return the json data
    """
    with open(filepath,"r") as a:
        return json.load(a)

def write_file(filepath:str, data, indent:int):
    """Fuction to write a dump to a json file, takes the filepath, data and number of indents.
    """
    with open(filepath, "w") as file:
        json.dump(data, file, indent=indent)
    return

def check_username(username:str):  
    """Function which takes the username and checks if it exists in the Users.json file.
    - Returns the user_id if user exists
    - Returns False if the user does not exist in the Users.json file.
    """
    user_data = read_file(Path_Users)
    # Locating the username in the .json file
    for i in user_data['master']:
        if username == i["user"]:
            user_id = i["user_id"]  # Getting user ID
            return True, user_id # Returning True if user ID match
    return False, 0 # Can't find user in Users.json

def check_password(user_id, password:str):
    """Function which takes imports user_id and password and checks if the profile password and password is correct and number of tries left.
    - Imports the user id
    - Imports the password submitted by the user
    - Returns None + error str if the accounts number of tries left are 0
    - Returns False + error str if the password is incorrect
    - Returns Accountnum if the account password matches the submitted psw
    """
    Passwords_data = read_file(Path_Passwords)
    # Reading user specific data from the stored .json file
    for val in Passwords_data["password"]:
        if user_id == val["user_id"]:
            user_psw = val["psw"]  # Getting user's password
            trys = val["trys"]  # Getting number of tries
            break
    if trys <= 0: return False, 0
    
    # Check if input password is the same as the stored password
    if password == user_psw:
        accountnum = val["account"]  # Getting account number
        correct_psw(user_id)
        return True, accountnum
    else:
        incorrect_psw(user_id)
        return None, trys-1
    
def incorrect_psw(user_id:str):
    """Function to increment the number of failed log ins a user has done 
    """
    Passwords_data = read_file(Path_Passwords)
    # Reading user specific data from the stored .json file
    for count, val in enumerate(Passwords_data["password"]):
        if user_id == val["user_id"]:
            trys = val["trys"]  # Getting number of tries
            break
    Passwords_data["password"][count]["trys"] = trys-1  # Updating the number of tries in the data
    write_file(Path_Passwords,Passwords_data,4)

def correct_psw(user_id:str):
    """Function to reset number of log in attempts upon successful attempt"""
    
    Passwords_data = read_file(Path_Passwords)
    
    for count, val in enumerate(Passwords_data['password']):
        if user_id == val['user_id']:
            break
    Passwords_data['password'][count]['trys'] = 4
    write_file(Path_Passwords,Passwords_data,4)

def transaction(accountnum:str, type:str, amount, note:str):
    """Function to write a transaction between accounts.
    - Imports the type of transaction; Uttag, Insättning
    - Imports the amount to be moved
    - Imports a note made by the user
    - Returns False + error message if the balance can't be transferd
    """
    # Get data from json file
    Accounts_data = read_file(Path_Accounts)
    for val in Accounts_data[str(accountnum)]:
        account_balance = val["balance"]
        account_transaction = val["transaction"]
        account_date = val["date"]
        account_note = val["note"]
    
    # if isinstance(amount, (int, float)):  # pass tuple
    #     return False, "Strängar kan inte matas in"

    if type == "Uttag": amount = -1*abs(float(amount)) # Negating amount for withdrawals
    
    balance = account_balance[0] + float(amount)
    new_balance = round(balance, 2)
     
    # Adding the new transaction data to the account
    account_balance.insert(0, new_balance)
    account_transaction.insert(0, type)
    account_date.insert(0, str(today))
    account_note.insert(0, note)

    write_file(Path_Accounts,Accounts_data,4)

def account_transfer(accountnum:str, transfer_num:str, amount, note:str):
    """Function to write a transaction too and from your account.
    - Imports the amount to be moved
    - Imports a note made by the user
    - Returns False + error message if the balance can't be transferd
    - Returns True if successfull
    """
    # Get data from json file
    Accounts_data = read_file(Path_Accounts)
    for val in Accounts_data[str(accountnum)]:
        account_balance = val["balance"]
        account_transaction = val["transaction"]
        account_date = val["date"]
        account_note = val["note"]
    
    # if isinstance(amount, (int, float)):  # pass tuple
    #     return False, "Strängar kan inte matas in"

    # Trying to find the inputed account number
    trigger = True
    for val in Accounts_data: # Itterating through Accounts.json 
        if val == transfer_num and (val != str(accountnum)):
            trigger = False
            break  
    if trigger: False, "Kontonumret fanns inte att föra över till"

    remove_balance = account_balance[0] - abs(float(amount))
    removed_balance = round(remove_balance, 2)

    # Adding the new transaction data to the account
    account_balance.insert(0, removed_balance)
    account_transaction.insert(0, "Kontoöverföring")
    account_date.insert(0, str(today))
    account_note.insert(0, note)
    
    # Itterating through the Transfer Accounts data
    for val in Accounts_data[str(transfer_num)]: # Read the new account
        t_account_balance = val["balance"]
        t_account_transaction = val["transaction"]
        t_account_date = val["date"]
        t_account_note = val["note"]

        add_balance = t_account_balance[0] + abs(float(amount))
        added_balance = round(add_balance, 2)
    
    # Adding the new transaction data to the account
    t_account_balance.insert(0, added_balance)
    t_account_transaction.insert(0, "Kontoöverföring")
    t_account_date.insert(0, str(today))
    t_account_note.insert(0, note)

    write_file(Path_Accounts, Accounts_data, 4)
    return True, 0

def create_user(username:str,password:str):
    """Function to create a new account, and add all the users data to the .json file
    - Imports the users username
    - Imports the specific password
    """
    users_data = read_file(Path_Users)
    passwords_data = read_file(Path_Passwords)
    
    if validate_username(username) == False: # Validate email adress
        return 1
    
    if check_username(username)[0] == True: # Check if username already exists
        return 2
    
    user_id = create_id(users_data["master"],"user_id") # Create a unique 6 digit user_id  

    # Writing over the existing files with the new users data
    users_data["master"].append({"user":username,"user_id":user_id})
    write_file(filepath= Path_Users, data= users_data, indent= 2)
    
    passwords_data["password"].append({"user_id":user_id,"psw":password,"trys":4,"account":[]})
    write_file(filepath= Path_Passwords, data= passwords_data, indent= 2)
    
    return 0

def new_account(user_id:str, account_type:str, currency:str, name:str):
    """Function to add a new account to an existing profile
    - Imports user id to append the new account number
    - Imports account type to create (determained by even or odd account number)
    - Imports specified currency for the account.
    - Returns the new appended list of the account numbers.
    """
    accounts_data = read_file(Path_Accounts)
    passwords_data = read_file(Path_Passwords)

    # Reading user specific data from the stored .json file
    for val in passwords_data["password"]:
        if user_id == val["user_id"]: break
    
    if account_type == "Sparkonto":
        while True: # Creates a even number for savings account
            accountnum = create_id(passwords_data['password'],"account") # Create a unique 6 digit accountnum
            if (accountnum % 2) == 0: break
    elif account_type == "Betalkonto":
        while True: # Creates a odd number for payment account
            accountnum = create_id(passwords_data['password'],"account") # Create a unique 6 digit accountnum
            if (accountnum % 2) == 1: break

    account_list = val["account"].append(accountnum)
    write_file(filepath= Path_Passwords, data= passwords_data, indent= 2)

    # Appening new Account data
    new_bank_data = [{
        'name':[name],
        "currency":[currency],
        "balance": [0],
        "transaction": [""],
        "date": [str(today)],
        "note": ["Konto skapades"]
    }]
    accounts_data[accountnum] = new_bank_data
    write_file(filepath= Path_Accounts, data= accounts_data, indent= 3)
    
    return account_list

def get_accounts(user_id:str):
    """
    Creates lists of account id, type, currency and balance and returns them in a list.
    """

    passwords_data = read_file(Path_Passwords)
    accounts_data = read_file(Path_Accounts)

    # Reading user specific data from the stored .json file
    for val_psw in passwords_data["password"]:
        if user_id == val_psw["user_id"]: break

    account_list = val_psw['account']
    list.sort(account_list)
    type_list = []
    for id in account_list:
        if id % 2 == 0:
            type_list.append('Sparkonto')
        elif id % 2 == 1:
            type_list.append('Betalkonto')

    name_list = []
    currency_list = []
    balance_list = []
    for val_acc in account_list:        
        for account in accounts_data[str(val_acc)]:
            name = account['name']
            currency = account['currency']
            balance = account['balance']
            name_list.append(name)
            currency_list.append(currency)
            balance_list.append(balance[0])

    return name_list, account_list, type_list, balance_list, currency_list

def validate_username(email:str):
    """Function to validate email address.
    """
    try:
        # Check that the email address is valid. Turn on check_deliverability
        validate_email(email, check_deliverability=False)
        return True
    except:
        return False  # Returning False indicating the email is not valid

def create_id(data,id):
    """Function to create a unique 6 digit long number for account numbers or user id:s
    - Imports data sum and category. I.e. user_data["master"]
    - Imports identification to search through. I.e. "user_id"
    - Returns a unique 6 digit long number 
    """
    while True:
        new_id = random.randrange(100000, 999999)  # Generating a random user ID
        trigger = True
        for i in data:
            if new_id == i[id]: trigger = False
        if trigger: return new_id
        input("pause")

def balance_history(accountnum:str): # Det finns något sätt att embed:a pyplot i Tkinter appen
    """Function to plot the balance hotory of a specif account number
    """
    accounts_data = read_file(Path_Accounts)
    # Itterate though the account and save the balance
    for val in accounts_data[str(accountnum)]:
        account_balance = val["balance"]
        account_date = val["date"]
    
    balance = []
    for index in reversed(account_balance): balance.append(index) # Reversed list of the dates
    dates = []
    for index in reversed(account_date): dates.append(index) # Reversed list of the dates

    title = {'family':'sans-serif','color':'black','size':18} # Set the title with font, colour and size
    plt.locator_params(axis='x', nbins=4) # Number of ticks for the x-axis
    plt.xticks(rotation=30, ha="right") # Rotate the lable for the x-axis ticks by 30 degree

    plt.title(f"{str(accountnum)}: Saldo historik",loc= 'left', fontdict= title) # Title
    plt.xlabel("Datum") # X-lable
    plt.ylabel("Belopp [sek]") # Y-lable

    print("Stäng ner grafens fönstret för att fortsätta...")
    plt.plot(dates, balance)
    plt.show()
    return

# def transaction_history(accountnum:str): # Den här måste också ändras för att skriva ut all data nu är det bara print
#     """Function to itterate through the account history displaying it
#     - Imports account number to read the files
#     """
#     accounts_data = read_file(Path_Accounts)
    
#     # Print the information in the desired format
#     print("{0:<20} | {1:<18} | {2:<16} | {3:<30}\n"
#               .format("Saldo", "Transaktion", "Datum", "Anteckning"))
#     # Itterates through the accounts json data, and prints out each element in order.
#     for item in range(len(accounts_data[str(accountnum)][0]['balance'])):
#         balance = accounts_data[str(accountnum)][0]['balance'][item]
#         transaction = accounts_data[str(accountnum)][0]['transaction'][item]
#         date = accounts_data[str(accountnum)][0]['date'][item]
#         note = accounts_data[str(accountnum)][0]['note'][item]
        
#         print("{0:<20} | {1:<18} | {2:<16} | {3:<30}"
#               .format(balance, transaction, date, note, item))
        
#         if item >= 30: # Check if the item is equal to or larger than 30, if so: stop printing
#             print("Kunde endast ladda in de senaste 30 transaktionerna")
#             break
#     input("Tryck enter för att fortsätta") # Remove this if needed

#     return


class Application(Tk): # Creates main application that the UI is located in
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title('Bankomat')
        self.minsize(675, 350)
        self.maxsize(675, 350)
        self.logged_userid = None
        self.logged_accounts = None
        self.logged_username = None
        self.logged_accountnum = None
        self.logged_i = None
        
        container = Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (StartPage, Login, Create_Account, Admin, Logged_In, Account):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky='nsew')
        
        self.show_frame('StartPage')
        
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        

class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label_title = Label(self, text=text_title, font=('Courier', 8), justify=LEFT)
        button_login = Button(self, text='Logga In',
                              command= lambda: controller.show_frame('Login'))
        button_create = Button(self, text='Skapa Konto',
                               command= lambda: controller.show_frame('Create_Account'))
        button_admin = Button(self, text='Admin',
                              command= lambda: controller.show_frame('Admin'))
        
        label_title.grid(column=0, row=0, sticky='n')
        button_login.grid(column=0, row=1, padx=10, sticky='w')
        button_create.grid(column=0, row=2, padx=10, pady=5, sticky='w')
        button_admin.grid(column=0, row=3, padx=10, sticky='w')
        
class Login(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.logged_accounts = self.controller.logged_accounts
        self.logged_username = self.controller.logged_username
        self.logged_userid = self.controller.logged_userid
        label_title = Label(self, text='Logga In')
        label_user = Label(self, text='Användarnamn:')
        label_pin = Label(self, text='Pin-kod:')
        self.label_error_exist = Label(self, text='Error: Inkorrekt Användarnamn', fg='red')
        self.label_error_pin = Label(self, text='', fg='red')
        self.label_error_locked = Label(self, text='Error: Konto Låst\nInga Försök Återstår', fg='red')
        self.entry_user = Entry(self, cursor='xterm')
        self.entry_pin = Entry(self, cursor='xterm', show='*')
        button_login = Button(self, text='Logga In',
                              command= lambda: login(self.entry_user.get(), self.entry_pin.get()))
        button_back = Button(self, text='Gå Tillbaka',
                             command= lambda: controller.show_frame('StartPage'))
        
        label_title.grid(column=0, row=0, columnspan=2)
        label_user.grid(column=0, row=1, sticky='e')
        label_pin.grid(column=0, row=2, pady=5, sticky='e')
        self.entry_user.grid(column=1, row=1, padx=5, sticky='w')
        self.entry_pin.grid(column=1, row=2, padx=5, pady=5, sticky='w')
        button_login.grid(column=0, row=5, pady=10, sticky='n', columnspan=2)
        button_back.grid(column=0, row=6, pady=10, sticky='s', columnspan=2)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        
        def login(username, pin):
            self.clearerror()
            user = check_username(username)
            if user[0] == True:
                trys = check_password(user[1], pin)
                if trys[0] == True:
                    self.controller.logged_userid = user[1]
                    self.controller.logged_accounts = trys[1]
                    self.controller.logged_username = self.entry_user.get()
                    controller.show_frame('Logged_In')
                
                elif trys[0] == False:
                    self.label_error_locked.grid(column=0, row=5, sticky='s', pady=10, columnspan=2)
                
                elif trys[0] == None:
                    self.label_error_pin.config(text=('Error: Inkorrekt Pin-kod\n' + str(trys[1]) + ' Försök Återstår'))
                    self.label_error_pin.grid(column=0, row=5, sticky='s', pady=10, columnspan=2)
                    
            else:
                self.label_error_exist.grid(column=0, row=5, sticky='s', pady=10, columnspan=2)
        
    def clearframe(self):
        self.entry_user.delete(0, END)
        self.entry_pin.delete(0, END)
    
    def clearerror(self):
        self.label_error_exist.grid_forget()
        self.label_error_pin.grid_forget()
        self.label_error_locked.grid_forget()
    
    def tkraise(self, aboveThis=None):
        self.clearframe()
        self.clearerror()
        super().tkraise(aboveThis)
                
class Create_Account(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label_title = Label(self, text='Skapa Konto')
        label_user = Label(self, text='Användarnamn:')
        label_pin = Label(self, text='Pin-kod:')
        label_pin2 = Label(self, text='Upprepa Pin:')
        self.label_error_exists = Label(self, text='Error: Konto Finns Redan', fg='red')
        self.label_error_match = Label(self, text='Error: Pin-koder Matchar Inte', fg='red')
        self.label_error_invalid = Label(self, text='Error: Ogiltigt Användarnamn\nAnvänd en Email-address', fg='red')
        self.label_success = Label(self, text='Konto Skapades', fg='lime green')
        self.entry_user = Entry(self, cursor='xterm')
        self.entry_pin = Entry(self, cursor='xterm')
        self.entry_pin2 = Entry(self, cursor='xterm')
        button_create = Button(self, text='Skapa Konto',
                               command= lambda: create(self.entry_user.get(), self.entry_pin.get(), self.entry_pin2.get()))
        button_back = Button(self, text='Gå Tillbaka',
                             command= lambda: controller.show_frame('StartPage'))
               
        label_title.grid(column=0, row=0, columnspan=2)
        label_user.grid(column=0, row=1, sticky='e')
        label_pin.grid(column=0, row=2, pady=5, sticky='e')
        label_pin2.grid(column=0, row=3, sticky='e')
        self.entry_user.grid(column=1, row=1, padx=5, sticky='w')
        self.entry_pin.grid(column=1, row=2, padx=5, pady=5, sticky='w')
        self.entry_pin2.grid(column=1, row=3, padx=5, sticky='w')
        button_create.grid(column=0, row=5, pady=10, sticky='n', columnspan=2)
        button_back.grid(column=0, row=6, pady=10, sticky='s', columnspan=2)
                
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(0, weight=1)
        
        def create(username, pin, pin2):            
            self.clearerror()
            if pin != pin2:
                self.label_error_match.grid(column=0, row=5, sticky='s', pady=10, columnspan=2)
                return
            
            if create_user(username, pin) == 0:
                self.label_success.grid(column=0, row=5, sticky='s', pady=10, columnspan=2)
           
            elif create_user(username, pin) == 1:
                self.label_error_invalid.grid(column=0, row=5, sticky='s', pady=10, columnspan=2) 
            
            elif create_user(username, pin) == 2:
                self.label_error_exists.grid(column=0, row=5, sticky='s', pady=10, columnspan=2)
                            
    def clearentry(self):
        self.entry_user.delete(0, END)
        self.entry_pin.delete(0, END)
        self.entry_pin2.delete(0, END)
        
    def clearerror(self):
        self.label_error_exists.grid_forget()
        self.label_error_match.grid_forget()
        self.label_error_invalid.grid_forget()
        self.label_success.grid_forget()
    
    def tkraise(self, aboveThis=None):
        self.clearentry()
        self.clearerror()
        super().tkraise(aboveThis)
        
class Logged_In(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.logged_accounts = self.controller.logged_accounts
        self.logged_username = self.controller.logged_username
        self.logged_userid = self.controller.logged_userid
        self.logged_accountnum = self.controller.logged_accountnum
        self.logged_i = self.controller.logged_i
        frame_info = Frame(self)
        label_loggedtext = Label(frame_info, text='Inloggad som:')
        self.label_user = Label(frame_info, text='', fg='magenta')
        button_logout = Button(frame_info, text='Logga ut',
                               command= lambda: logout())
        button_create = Button(self, text='Skapa Konto',
                               command= lambda: self.create_account())
        
        frame_info.grid(column=0, row=0, sticky='w', columnspan=5)
        label_loggedtext.grid(column=0, row=0, sticky='w', pady=5)
        button_logout.grid(column=2, row=0, sticky='w')
        button_create.grid(column=5, row=0, sticky='e')

        self.columnconfigure(4, weight=1)
        self.rowconfigure(10, weight=1)

        def logout():
            controller.show_frame('StartPage')

    def create_account(self):
        create_window = Toplevel(self.controller)
        create_window.title('Skapa Konto')
        create_window.minsize(400, 150)
        create_window.maxsize(400, 150)

        label_name = Label(create_window, text='Kontonamn:')
        entry_name = Entry(create_window, cursor='xterm')
        button_create = Button(create_window, text='Skapa',
                               command= lambda: create())
        frame_type = Frame(create_window, borderwidth=1, relief='solid')
        frame_currency = Frame(create_window, borderwidth=1, relief='solid')
        
        options_type = [
            'Välj Kontotyp',
            'Sparkonto',
            'Betalkonto'
        ]

        options_currency = [
            'Välj Valuta',
            'SEK',
            'EUR'
        ]

        frame_type.grid(column=0, row=1, padx=5, pady=5, sticky='w', columnspan=2)
        frame_currency.grid(column=1, row=1, padx=45, pady=5, sticky='w')
        
        clicked_type = StringVar()
        clicked_type.set('Välj Kontotyp')
        clicked_currency = StringVar()
        clicked_currency.set('Välj Valuta')
        option_type = ttk.OptionMenu(frame_type, clicked_type, *options_type)
        option_type.config(width=12, style='TMenubutton')
        option_currency = ttk.OptionMenu(frame_currency, clicked_currency, *options_currency)
        option_currency.config(width=10, style='TMenubutton')
        
        style = ttk.Style()
        style.configure('TMenuButton')

        label_name.grid(column=0, row=0, padx=5, sticky='w')
        entry_name.grid(column=1, row=0, sticky='w')
        option_type.pack()
        option_currency.pack()
        button_create.grid(column=2, row=1)

        create_window.columnconfigure(2, weight=1)
        create_window.rowconfigure(3, weight=1)

        def create():
            new_account(self.controller.logged_userid, clicked_type.get(), clicked_currency.get(), entry_name.get())
            self.update_accounts()

            

    def update_accounts(self):
        self.clear()
        account_list = get_accounts(self.controller.logged_userid)

        self.buttons = []
        for i, name in enumerate(account_list[0]):
            button = Button(self, text=name, relief='solid', borderwidth=1, width=75, height=2, anchor='w', padx=5,
                            command= lambda i=i: switch_to(account_list[1][i], i))
            button.grid(column=0, row=(1+i), columnspan=4, sticky='w')
            self.buttons.append(button)
        
        for i, account in enumerate(account_list[1]):
            button = Button(self, text=account, relief='solid', borderwidth=1, width=75, height=2, anchor='w', padx=5,
                            command= lambda i=i: switch_to(account_list[1][i], i))
            button.grid(column=1, row=(1+i), columnspan=4, sticky='w')
            self.buttons.append(button)

        for i, type in enumerate(account_list[2]):
            button = Button(self, text=type, relief='solid', borderwidth=1, width=65, height=2, anchor='w', padx=5,
                            command= lambda i=i: switch_to(account_list[1][i], i))
            button.grid(column=2, row=(1+i), columnspan=4, sticky='w')
            self.buttons.append(button)          

        for i, balance in enumerate(account_list[3]):
            button = Button(self, text=balance, relief='solid', borderwidth=1, width=20, height=2, anchor='e', padx=5,
                            command= lambda i=i: switch_to(account_list[1][i], i))
            button.grid(column=3, row=(1+i), sticky='e')
            self.buttons.append(button)      

        for i, currency in enumerate(account_list[4]):
            button = Button(self, text=currency, relief='solid', borderwidth=1, width=45, height=2, anchor='w', padx=5,
                            command= lambda i=i: switch_to(account_list[1][i], i))
            button.grid(column=4, row=(1+i), columnspan=4, sticky='e')
            self.buttons.append(button) 

            def switch_to(accountnum, i):
                self.controller.logged_accountnum = accountnum
                self.controller.logged_i = i
                self.controller.show_frame('Account')       

    def clear(self):        
        try:
            for button in self.buttons:
                button.grid_forget()
        except: None

    def update_user(self):
        self.label_user.config(text=self.controller.logged_username)
        self.label_user.grid(column=1, row=0, padx=5, sticky='w')

    def tkraise(self, aboveThis=None):
        self.update_user()
        self.update_accounts()
        super().tkraise(aboveThis)

class Account(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.logged_accountnum = self.controller.logged_accountnum
        self.logged_userid = self.controller.logged_userid
        self.logged_i = self.controller.logged_i

        self.frame = Frame(self, borderwidth=1, relief='solid')
        label = Label(self, text='Kontonummer:')
        self.label_balance = Label(self, text='', fg='lime green')
        self.label_accountnum = Label(self, text='', fg='magenta')
        button_back = Button(self, text='Tillbaka',
                             command= lambda: controller.show_frame('Logged_In'))
        button_deposit = Button(self, text='Insättning',
                                command= lambda: set_frame('Insättning'))
        button_withdraw = Button(self, text='Uttag',
                                 command= lambda: set_frame('Uttag'))
        button_transaction = Button(self, text='Överföring',
                                    command= lambda: set_transfer())
        
        self.frame.grid(column=2, row=2, rowspan=10, sticky='n')
        label.grid(column=0, row=0, pady=5)
        self.label_accountnum.grid(column=1, row=0, padx=5)
        self.label_balance.grid(column=3, row=0, sticky='e')
        button_back.grid(column=2, row=0, sticky='w')
        button_deposit.grid(column=0, row=1, sticky='w', padx=5)
        button_withdraw.grid(column=0, row=2, pady=5, sticky='w', padx=5)
        button_transaction.grid(column=0, row=3, sticky='w', padx=5)

        self.columnconfigure(3, weight=1)
        self.rowconfigure(10, weight=1)

        def set_frame(type:str):
            self.clear()
            label_deposit = Label(self.frame, text=type + ':')
            label_note = Label(self.frame, text='Anteckning:')
            label_currency = Label(self.frame, text=self.currency)
            button_confirm = Button(self.frame, text='Godkänn')
            entry_amount = Entry(self.frame, cursor='xterm')
            textbox_note = Text(self.frame, cursor='xterm', width=33, height=5)
            label_success = Label(self.frame, text=type + ' lyckades', fg='lime green')
            label_error = Label(self.frame, text=type + ' måste vara ett nummer', fg='red')
            button_confirm.config(command= lambda: trans(type))

            label_deposit.grid(column=0, row=0, sticky='w', padx=5, pady=5)
            entry_amount.grid(column=0, row=1, sticky='w', padx=5, columnspan=2)
            label_currency.grid(column=2, row=1, sticky='w')
            label_note.grid(column=0, row=3, sticky='w', padx=5)
            textbox_note.grid(column=0, row=4, sticky='w', columnspan=4, padx=5, pady=5)
            button_confirm.grid(column=3, row=1, padx=5, sticky='e')

            self.frame.columnconfigure(3, weight=1)

            def trans(type:str):
                label_error.grid_forget()
                label_success.grid_forget()
                try:
                    value = float(entry_amount.get())
                    transaction(self.controller.logged_accountnum, type, value, textbox_note.get('1.0', 'end-1c'))
                    label_success.grid(column=1, row=0, sticky='w', padx=5, columnspan=3)
                    entry_amount.delete(0, END)
                    textbox_note.delete('1.0', END)
                    self.update_account()


                except:
                    label_error.grid(column=1, row=0, sticky='e', padx=5, columnspan=3)

        def set_transfer():
            self.clear()
            label_transfer = Label(self.frame, text='Överföring:')
            label_account = Label(self.frame, text=self.controller.logged_accountnum, borderwidth=1, relief='solid')
            label_to = Label(self.frame, text='Till')
            label_note = Label(self.frame, text='Anteckning:')
            label_error = Label(self.frame, text='Överföring måste vara ett nummer', fg='red')
            label_choose = Label(self.frame, text='Välj ett konto', fg='red')
            label_success = Label(self.frame, text='Överföring Lyckades', fg='lime green')
            label_currency = Label(self.frame, text=self.currency)
            frame_accounts = Frame(self.frame, borderwidth=1, relief='solid')
            button_confirm = Button(self.frame, text='Godkänn',
                                    command= lambda: transfer())
            entry_amount = Entry(self.frame, cursor='xterm')
            textbox_note = Text(self.frame, cursor='xterm', width=33, height=5)

            option_accounts = [
                'Välj Konto'
            ]

            accounts = get_accounts(self.controller.logged_userid)
            for i, account in enumerate(accounts[0]):
                if i != self.controller.logged_i:
                    new_account = str(account).strip("[']")
                    option_accounts.append(new_account + ': ' + str(accounts[1][i]))
            
            clicked_account = StringVar()
            clicked_account.set('Välj Konto')
            option_accounts = ttk.OptionMenu(frame_accounts, clicked_account, *option_accounts)
            option_accounts.config(width=10)

            label_transfer.grid(column=0, row=0, sticky='w', columnspan=3, padx=5)
            label_account.grid(column=0, row=1, pady=5, sticky='e', padx=5)
            label_to.grid(column=1, row=1, padx=5, sticky='w')
            label_note.grid(column=0, row=3, sticky='w', padx=5)
            label_currency.grid(column=1, row=2, sticky='w', padx=5)
            frame_accounts.grid(column=2, row=1, sticky='w')
            textbox_note.grid(column=0, row=4, sticky='w', columnspan=4, padx=5, pady=5)
            option_accounts.pack()
            entry_amount.grid(column=0, row=2, sticky='w', padx=5, pady=5)
            button_confirm.grid(column=2, row=2, sticky='e', padx=5)

            self.frame.columnconfigure(3, weight=1)

            def transfer():
                label_error.grid_forget()
                label_choose.grid_forget()
                label_success.grid_forget()
                try:
                    value = float(entry_amount.get())
                    transfer_account = clicked_account.get().split(': ')

                except:
                    label_error.grid(column=1, row=0, sticky='e', padx=5, columnspan=3)
                    return

                if clicked_account.get() != 'Välj Konto' and value < accounts[3][self.controller.logged_i]:
                    account_transfer(self.controller.logged_accountnum, transfer_account[1].strip("'"), value, textbox_note.get('1.0', 'end-1c'))
                    label_success.grid(column=1, row=0, sticky='w', padx=5, columnspan=3)
                    self.update_account()

                else:
                    label_choose.grid(column=1, row=0, sticky='e', padx=5, columnspan=3)
                

    def clear(self):
        self.frame.destroy()
        self.frame = Frame(self, borderwidth=1, relief='solid')
        self.frame.grid(column=2, row=2, rowspan=10, sticky='n')        

    def update_account(self):
        accounts = get_accounts(self.controller.logged_userid)
        balance = accounts[3][self.controller.logged_i]
        currency = accounts[4][self.controller.logged_i]
        self.currency = currency[0]
        self.label_balance.config(text='Saldo: ' + str(balance) + ' ' + str(self.currency))
        self.label_accountnum.config(text=self.controller.logged_accountnum)

    def tkraise(self, aboveThis=None):
        self.clear()
        self.update_account()
        super().tkraise(aboveThis)
        
class Admin(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label_title = Label(self, text=text_admin, font=('Courier', 8), justify=LEFT)
        self.entry_user = Entry(self, cursor='xterm')
        button_reset_trys = Button(self, text='Återställ Försök',
                                   command= lambda: reset(self.entry_user.get()))
        button_back = Button(self, text='Gå Tillbaka',
                             command= lambda: controller.show_frame('StartPage'))
        
        label_title.grid(column=0, row=0, sticky='n', columnspan=2)
        self.entry_user.grid(column=0, row=1, sticky='e', padx=10)
        button_reset_trys.grid(column=1, row=1, sticky='w')
        button_back.grid(column=0, row=6, pady=10, sticky='s', columnspan=2)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(6, weight=1)
        
        def reset(username):
            id = check_username(username)
            if id[0] == True:
                print('Attempts Reset')
                correct_psw(id[1])
            else:
                print('Account Not Found')    
                    
    def clearframe(self):
        self.entry_user.delete(0, END)
        
    def tkraise(self, aboveThis=None):
        self.clearframe()
        super().tkraise(aboveThis)


if __name__ == '__main__': # Starts the application
    app = Application()
    app.mainloop()