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


import os  # Importing the os module to interact with the operating system
import json  # Importing the json module for JSON file operations
from datetime import date, datetime, timedelta  # Importing the date class from the datetime module
import random # Importing random function for slump actions
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from tkinter import ttk

from email_validator import validate_email, EmailNotValidError  # Importing email validation functions

path = os.path.dirname(os.path.realpath(__file__))
new_path = path.replace('\\', '/')

"""
Remember to replace the file path with your location of the files and replace the \\(backslah) with / 
"""
Path_Users = new_path + "/Users.json"  # Path to the users JSON file
Path_Passwords = new_path + "/Passwords.json"  # Path to the passwords JSON file
Path_Accounts = new_path + "/Accounts.json"  # Path to the accounts JSON file

today = date.today()  # Getting today's date

days_lock_account = 15

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
    
    # Get data from json file
    Passwords_data = read_file(Path_Passwords)
    for count, val in enumerate(Passwords_data['password']):
        if user_id == val['user_id']:
            break
    Passwords_data['password'][count]['trys'] = 4 # Resets number of attempts to 4
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

    if type == "Uttag": amount = -1*abs(float(amount)) # Negating amount for withdrawals
    
    balance = account_balance[0] + float(amount)
    new_balance = round(balance, 2)
     
    # Adding the new transaction data to the account
    account_balance.insert(0, new_balance)
    account_transaction.insert(0, type)
    account_date.insert(0, str(today))
    account_note.insert(0, note)

    write_file(Path_Accounts,Accounts_data,4)

def account_transfer(account_num:str, transfer_num:str, amount, note:str, source_currency:str):
    """Function to write a transaction too and from your account.
    - Imports the amount to be moved
    - Imports a note made by the user
    - Returns False + error message if the balance can't be transferd
    - Returns True if successfull
    """
    # Get data from json file
    Accounts_data = read_file(Path_Accounts)
    for val in Accounts_data[str(account_num)]:
        account_balance = val["balance"]
        account_transaction = val["transaction"]
        account_date = val["date"]
        account_note = val["note"]

        remove_balance = account_balance[0] - abs(float(amount))
        removed_balance = round(remove_balance, 2)
    
    # Itterating through the Transfer Accounts data
    for val in Accounts_data[str(transfer_num)]: # Read the new account
        t_account_balance = val["balance"]
        t_account_transaction = val["transaction"]
        t_account_date = val["date"]
        t_account_note = val["note"]
        t_account_currency = val['currency']
        
        exchanged_amount = currency_exchange(amount, source_currency, t_account_currency[0], 'transfer')
        add_balance = t_account_balance[0] + exchanged_amount
        added_balance = round(add_balance, 2)
    
        # Checking if accounts are savings accounts
    if (int(transfer_num) % 2) == 0 and t_account_note[0] != 'Konto skapades':
        if not check_days_passed(t_account_date[0], days_passed= days_lock_account): # Calculate if a set number of days passed since last event on account
            return False, f"Sparkonton kan endast modifieras {days_lock_account} dagar\n efter senaste händeslse"
    if (int(account_num) % 2) == 0 and account_note[0] != 'Konto skapades': 
        if not check_days_passed(account_date[0], days_passed= days_lock_account):
            return False, f"Sparkonton kan endast modifieras {days_lock_account} dagar\n efter senaste händeslse"


    # Adding the new transaction data to the account
    account_balance.insert(0, removed_balance)
    account_transaction.insert(0, "Kontoöverföring")
    account_date.insert(0, str(today))
    account_note.insert(0, note)

    # Adding the new transaction data to the account
    t_account_balance.insert(0, added_balance)
    t_account_transaction.insert(0, "Kontoöverföring")
    t_account_date.insert(0, str(today))
    t_account_note.insert(0, note)

    write_file(Path_Accounts, Accounts_data, 4)
    return True, 0

def check_days_passed(date_str: str, days_passed:int):
    """Function to check if a number of days has passed since a date.
    - Imports a string of a date
    - Imports number of that shuld have passed since a date
    - Returns True or False if that number of days has passed  
    """
    date_object = datetime.strptime(date_str, "%Y-%m-%d")
    # Get the current date
    current_date = datetime.now()

    days_until = date_object + timedelta(days=days_passed) # Add a year to the parsed date

    # Check if a year has passed since the date
    if current_date >= days_until:
        return True
    else:
        return False

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

def get_accounts(user_id:str, sort_type):
    """
    Creates lists of account id, type, currency and balance and returns them in a list.
    """

    passwords_data = read_file(Path_Passwords)
    accounts_data = read_file(Path_Accounts)

    # Reading user specific data from the stored .json file
    for val_psw in passwords_data["password"]:
        if user_id == val_psw["user_id"]: break

    account_list = val_psw['account']
    type_list = []
    for id in account_list: # Adds account type to empty list
        if id % 2 == 0:
            type_list.append('Sparkonto')
        elif id % 2 == 1:
            type_list.append('Betalkonto')

    name_list = []
    currency_list = []
    balance_list = []
    for val_acc in account_list: # Adds name, currency and balance to respective lists       
        for account in accounts_data[str(val_acc)]:
            name = account['name']
            currency = account['currency']
            balance = account['balance']
            name_list.append(name)
            currency_list.append(currency)
            balance_list.append(balance[0])

    # Sorts lists alphabetically or numerically depending on defined sort_type
    # sort_type is determined by which sorting button is pressed in the GUI 
    if sort_type == 0:
        combined = list(zip(name_list, account_list, type_list, balance_list, currency_list)) # zip combines the lists
        combined.sort() # Sorts combined list in alphabetical or numerical order depending on first list zipped, name_list in this case
        name_list, account_list, type_list, balance_list, currency_list = zip(*combined) # Splits up the combined list back into the individual lists

    elif sort_type == 1:
        combined = list(zip(account_list, name_list, type_list, balance_list, currency_list))
        combined.sort()
        account_list, name_list, type_list, balance_list, currency_list = zip(*combined)

    elif sort_type == 2:
        combined = list(zip(type_list, account_list, name_list, balance_list, currency_list))
        combined.sort()
        type_list, account_list, name_list, balance_list, currency_list = zip(*combined)

    elif sort_type == 3:
        combined = list(zip(balance_list, name_list, account_list, type_list, currency_list))
        combined.sort()
        combined.reverse()
        balance_list, name_list, account_list, type_list, currency_list = zip(*combined)

    elif sort_type == 4:
        combined = list(zip(currency_list, name_list, account_list, type_list, balance_list))
        combined.sort()
        currency_list, name_list, account_list, type_list, balance_list = zip(*combined)

    return name_list, account_list, type_list, balance_list, currency_list

def check_account(account_num:str):
    """Checks if account number is valid"""

    account_data = read_file(Path_Accounts)

    try:
        account_data[account_num] # Checks if account number exists in json
        
        if int(account_num) % 2: # Checks if account is "betalkonto"
            return True
        
        else: return False
    
    except: return None

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

def balance_history(accountnum:str):
    """Function to plot the balance hotory of a specif account number
    """
    accounts_data = read_file(Path_Accounts)
    # Itterate though the account and save the balance
    for val in accounts_data[str(accountnum)]:
        account_balance = val["balance"]
        account_date = val["date"]
    
    balance_dict = {}
    for balances, dates in zip(reversed(account_balance), reversed(account_date)): # Reverses order of retrieved lists to be in chronological order
        balance_dict[dates] = balances # Binds dates to balance in dictionary 
    
    date = list(balance_dict.keys()) # Splits dictionary into lists for date and balance in chronological order
    balance = list(balance_dict.values())          

    return balance, date

def get_history(accountnum:str, currency:str):
    """Function to create a list of all events in account
    """
    
    accounts_data = read_file(Path_Accounts)
    
    for account in accounts_data[str(accountnum)]: # Stores account events from json
        balance_list = account['balance']
        transaction_list = account['transaction']
        date_list = account['date']
        note_list = account['note']

    amount_list = [] # Creates empty list to store balance changes between events    
    for i, balance in enumerate(balance_list): # Calculates change in balance between events
        if i < (len(balance_list) - 1):
            amount = balance - balance_list[i + 1]
            amount_list.append(str(round(amount, 2)) + ' ' + currency)
    amount_list.append('') # Appends to list
        
    return amount_list, transaction_list, date_list, note_list

def delete_account(account_num:str, password:str):
    """Function to safly dispose of any unwanted accounts
    - Imports account number to find account
    - Imports password to verify the deletion
    - Returns account_list + error message if incorrect password or balance != 0
    - Returns account_list + 0 if successfull
    """
    passwords_data = read_file(Path_Passwords)
    accounts_data = read_file(Path_Accounts)

    for count, val in enumerate(passwords_data["password"]):
        account_list = val["account"]
        if account_num in val["account"]: break
    
    if not (val["psw"] == password): return False , "Fel lösenord, kontot var inte borttaget"

    # Get data from json
    for val in accounts_data[str(account_num)]:
        account_balance = val["balance"]
    if not (account_balance[0] == 0): return None , "Kontot får inte inneha något belopp, töm kontor först eller betala av skulden"

    account_list.remove(account_num) # Remove account number from password.json file
    accounts_data.pop(str(account_num)) # Remove the whole account from accounts.json

    write_file(filepath=Path_Passwords, data=passwords_data, indent= 4)
    write_file(Path_Accounts, accounts_data, 4)
    return True, "Kontot har tagits bort"

def currency_exchange(amount:str, source_currency:str, target_currency:str, type:str):
    """Functio do do currency exchange from a given value.
    - Imports account number
    - Imports amount to be exchanged
    - Imports the targeted currency
    - Returns the same value if the currency is the same
    - Returns False + error i the currency is not supported
    - Returns the transformed value based on the exchange rates
    """

    # Check if the target currency is the same as currency.
    if source_currency == target_currency: return abs(float(amount))
    
    # There are 5 exchange rates. From the 5 different currencies to the corresponding value in the target currency. The amount should be multiplied by this factor later.
    exchange_rates = {"SEK": {"USD": 0.12, "EUR": 0.11, "DKK": 0.84, "NOK": 1.32},
                      "USD": {"SEK": 8.69, "EUR": 0.91, "DKK": 6.76, "NOK": 10.56},
                      "EUR": {"SEK": 9.18, "USD": 1.10, "DKK": 7.43, "NOK": 11.62},
                      "DKK": {"SEK": 1.19, "USD": 0.15, "EUR": 0.13, "NOK": 1.57},
                      "NOK": {"SEK": 0.76, "USD": 0.09, "EUR": 0.086, "DKK": 0.64}}
    
    # Calculate the equivalent value in the target currency from the amount to be exchanged. 
    if type == 'transaction':
        exchanged_amount = float(amount) * exchange_rates[target_currency][source_currency]
    else:    
        exchanged_amount = float(amount) * exchange_rates[source_currency][target_currency]

    return exchanged_amount

def interest():
    """Function to calculate the intrest on an account if it is the first day of the month.
    Updates the .json file for all savings accounts with their given interest. 
    """
    interest_rate = random.uniform(1.00125,1.0055) # randomize the intrest rate
    # Check if it is the first of the month to run the rest of the intrest function  
    month = ['Januari', 'Februari', 'Mars', 'April', 'Maj', 'Juni', 'Juli', 'Augusti', 'September', 'Oktober', 'November', 'December']
    transaction_note = 'Ränta ' + month[today.month - 1] + ' ' + str(today.year)

    accounts_data = read_file(Path_Accounts)

    # Check if the transaction for this month has already been written
    for val in accounts_data['2']:
        account_transaction = val['transaction']
        for acc_transaction in account_transaction:
            if acc_transaction == transaction_note: return

    # Get data from json
    for account_num in accounts_data:
        if (int(account_num) % 2) == 0:
            # Read all the data from the account
            for val in accounts_data[str(account_num)]:
                account_balance = val["balance"]
                account_transaction = val["transaction"]
                account_date = val["date"]
                account_note = val["note"]

            # Calculate the intrest for the account
            new_balance = account_balance[0] * interest_rate
            added_balance = round(new_balance, 2)

            # Adding the new transaction data to the account
            account_balance.insert(0, added_balance)
            account_transaction.insert(0, transaction_note)
            account_date.insert(0, str(today))
            account_note.insert(0, f"Måndasränta {round(interest_rate,4)}% ")
    # Writing to file when all savings accounts have been added
    write_file(Path_Accounts, accounts_data, 4)  
    return

###############################

class Application(Tk): # Creates main application that the GUI is located in
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Defines application window properties
        self.title('Bankomat')
        self.minsize(675, 350)
        self.maxsize(675, 350)

        # Sets up variables shared between frames
        self.logged_userid = None
        self.logged_accounts = None
        self.logged_username = None
        self.logged_accountnum = None
        self.logged_sorttype = None
        self.logged_i = None
        
        # Sets up container frame
        container = Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # Initializes all frames for application
        self.frames = {}
        for F in (StartPage, Login, Create_Account, Admin, Logged_In, Account):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky='nsew')
        
        # Shows "StartPage" frame
        self.show_frame('StartPage')
        
    def show_frame(self, page_name): # Defines show_frame function used to switch between frames
        frame = self.frames[page_name]
        frame.tkraise()
        

class StartPage(Frame): # Sets up "StartPage" frame
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label_title = Label(self, text=text_title, font=('Courier', 8), justify=LEFT) # Creates label widget containing "Bankomat" ascii text
        
        # Creates buttons to switch to respective frames
        button_login = Button(self, text='Logga In',
                              command= lambda: controller.show_frame('Login')) # Button switches to frame "Login"
        button_create = Button(self, text='Skapa Konto',
                               command= lambda: controller.show_frame('Create_Account'))
        button_admin = Button(self, text='Admin',
                              command= lambda: controller.show_frame('Admin'))
        
        # Defines placement of all widgets within the frame using the grid function
        label_title.grid(column=0, row=0, sticky='n')
        button_login.grid(column=0, row=1, padx=10, sticky='w')
        button_create.grid(column=0, row=2, padx=10, pady=5, sticky='w')
        button_admin.grid(column=0, row=3, padx=10, sticky='w')
        
class Login(Frame): # Sets up "Login" frame    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        
        # Imports stored variables
        self.logged_accounts = self.controller.logged_accounts
        self.logged_username = self.controller.logged_username
        self.logged_userid = self.controller.logged_userid
        
        # Creates labels for frame
        label_title = Label(self, text='Logga In')
        label_user = Label(self, text='Användarnamn:')
        label_pin = Label(self, text='Lösenord:')
        self.label_error_exist = Label(self, text='Error: Inkorrekt Användarnamn', fg='red')
        self.label_error_pin = Label(self, text='', fg='red')
        self.label_error_locked = Label(self, text='Error: Konto Låst\nInga Försök Återstår', fg='red')
        
        # Creates entry widgets allowing user to write login information
        self.entry_user = Entry(self, cursor='xterm')
        self.entry_pin = Entry(self, cursor='xterm', show='*')

        # Creates button widgets
        button_login = Button(self, text='Logga In',
                              command= lambda: login(self.entry_user.get(), self.entry_pin.get()))
        button_back = Button(self, text='Gå Tillbaka',
                             command= lambda: controller.show_frame('StartPage'))
        
        # Defines placement of all widgets
        label_title.grid(column=0, row=0, columnspan=2)
        label_user.grid(column=0, row=1, sticky='e')
        label_pin.grid(column=0, row=2, pady=5, sticky='e')
        self.entry_user.grid(column=1, row=1, padx=5, sticky='w')
        self.entry_pin.grid(column=1, row=2, padx=5, pady=5, sticky='w')
        button_login.grid(column=0, row=5, pady=10, sticky='n', columnspan=2)
        button_back.grid(column=0, row=6, pady=10, sticky='s', columnspan=2)
        
        # Configure scaling of specific columns and rows within the frame
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        
        def login(username, pin): # Checks if username and password are correct
            self.clearerror()
            user_error, user_id = check_username(username)
            if user_error == True:
                error, trys = check_password(user_id, pin)
                if error == True: # If correct stores data in shared variables
                    self.controller.logged_userid = user_id
                    self.controller.logged_accounts = trys
                    self.controller.logged_username = self.entry_user.get()
                    controller.show_frame('Logged_In')
                
                elif error == False: # If account locked displays locked error message
                    self.label_error_locked.grid(column=0, row=5, sticky='s', pady=10, columnspan=2)
                
                elif error == None: # If password incorrect display attempts remaining error message
                    self.label_error_pin.config(text=('Error: Inkorrekt Lösenord\n' + str(trys) + ' Försök Återstår'))
                    self.label_error_pin.grid(column=0, row=5, sticky='s', pady=10, columnspan=2)
                    
            else: # Display account does not exist if username does not exist
                self.label_error_exist.grid(column=0, row=5, sticky='s', pady=10, columnspan=2)
        
    def clearframe(self): # Clears entry widgets
        self.entry_user.delete(0, END)
        self.entry_pin.delete(0, END)
    
    def clearerror(self): # Removes all error messages from frame
        self.label_error_exist.grid_forget()
        self.label_error_pin.grid_forget()
        self.label_error_locked.grid_forget()
    
    def tkraise(self, aboveThis=None): # Runs clearframe and clearerror whenever frame is raised (Displayed)
        self.clearframe()
        self.clearerror()
        super().tkraise(aboveThis)
                
class Create_Account(Frame): # Sets up "Create_Account" frame    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # Creates label widgets
        label_title = Label(self, text='Skapa Konto')
        label_user = Label(self, text='Användarnamn:')
        label_pin = Label(self, text='Lösenord:')
        label_pin2 = Label(self, text='Upprepa Lösenord:')
        self.label_error_exists = Label(self, text='Error: Konto Finns Redan', fg='red')
        self.label_error_match = Label(self, text='Error: Lösenord Matchar Inte', fg='red')
        self.label_error_invalid = Label(self, text='Error: Ogiltigt Användarnamn\nAnvänd en Email-address', fg='red')
        self.label_success = Label(self, text='Konto Skapades', fg='lime green')
        
        # Creates entry widgets
        self.entry_user = Entry(self, cursor='xterm')
        self.entry_pin = Entry(self, cursor='xterm', show='*')
        self.entry_pin2 = Entry(self, cursor='xterm', show='*')
        
        # Creates button widgets
        button_create = Button(self, text='Skapa Konto',
                               command= lambda: create(self.entry_user.get(), self.entry_pin.get(), self.entry_pin2.get()))
        button_back = Button(self, text='Gå Tillbaka',
                             command= lambda: controller.show_frame('StartPage'))
               
        # Defines placement of all widgets in frame
        label_title.grid(column=0, row=0, columnspan=2)
        label_user.grid(column=0, row=1, sticky='e')
        label_pin.grid(column=0, row=2, pady=5, sticky='e')
        label_pin2.grid(column=0, row=3, sticky='e')
        self.entry_user.grid(column=1, row=1, padx=5, sticky='w')
        self.entry_pin.grid(column=1, row=2, padx=5, pady=5, sticky='w')
        self.entry_pin2.grid(column=1, row=3, padx=5, sticky='w')
        button_create.grid(column=0, row=5, pady=10, sticky='n', columnspan=2)
        button_back.grid(column=0, row=6, pady=10, sticky='s', columnspan=2)
                
        # Configures specific columns and rows in frame
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(0, weight=1)
        
        def create(username, pin, pin2): # Function to check if information provided by user is valid for account creation, if true creates account            
            self.clearerror()
            if pin != pin2: # Checks if passwords match
                self.label_error_match.grid(column=0, row=5, sticky='s', pady=10, columnspan=2)
                return
            
            if create_user(username, pin) == 0: # Displays success message if account created
                self.label_success.grid(column=0, row=5, sticky='s', pady=10, columnspan=2)
           
            elif create_user(username, pin) == 1: # Displays invalid username error
                self.label_error_invalid.grid(column=0, row=5, sticky='s', pady=10, columnspan=2) 
            
            elif create_user(username, pin) == 2: # Displays account already exists error
                self.label_error_exists.grid(column=0, row=5, sticky='s', pady=10, columnspan=2)
                            
    def clearentry(self): # Clears widgets
        self.entry_user.delete(0, END)
        self.entry_pin.delete(0, END)
        self.entry_pin2.delete(0, END)
        
    def clearerror(self): # Removes all error messages from frame
        self.label_error_exists.grid_forget()
        self.label_error_match.grid_forget()
        self.label_error_invalid.grid_forget()
        self.label_success.grid_forget()
    
    def tkraise(self, aboveThis=None): # Executes clearentry and clearerror functions when frame is raised
        self.clearentry()
        self.clearerror()
        super().tkraise(aboveThis)
        
class Logged_In(Frame): # Sets up "Logged_In" frame
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # Imports necessary shared variables
        self.logged_accounts = self.controller.logged_accounts
        self.logged_username = self.controller.logged_username
        self.logged_userid = self.controller.logged_userid
        self.logged_accountnum = self.controller.logged_accountnum
        self.logged_sorttype = self.controller.logged_sorttype
        self.logged_i = self.controller.logged_i

        # Creates frame within the "Logged_In" frame for displaying username and logout button
        frame_info = Frame(self)

        # Creates labels for users username within the "frame_info" frame
        label_loggedtext = Label(frame_info, text='Inloggad som:')
        self.label_user = Label(frame_info, text='', fg='magenta')

        # Creates button widgets
        button_logout = Button(frame_info, text='Logga ut',
                               command= lambda: logout())
        button_create = Button(self, text='Skapa Konto',
                               command= lambda: self.create_account())
        button_accountname = Button(self, text='Kontonamn', relief='solid', borderwidth=1, width=75, height=1, anchor='w', padx=5,
                                    command= lambda: self.update_accounts(0))
        button_accountid = Button(self, text='Konto-id', relief='solid', borderwidth=1, width=75, height=1, anchor='w', padx=5,
                                  command= lambda: self.update_accounts(1))
        button_accounttype = Button(self, text='Kontotyp', relief='solid', borderwidth=1, width=65, height=1, anchor='w', padx=5,
                                    command= lambda: self.update_accounts(2))
        button_accountbalance = Button(self, text='Saldo', relief='solid', borderwidth=1, width=20, height=1, anchor='e', padx=5,
                                       command= lambda: self.update_accounts(3))
        button_accountcurrency = Button(self, text='Valuta', relief='solid', borderwidth=1, width=45, height=1, anchor='w', padx=5,
                                        command= lambda: self.update_accounts(4))
        
        # Creates canvas and frame widgets related to account scrolling
        self.canvas_accounts = Canvas(self, borderwidth=0)
        self.frame_canvas = Frame(self.canvas_accounts, borderwidth=0)
        
        # Defines placement of all widgets within frame(s)
        frame_info.grid(column=0, row=0, sticky='w', columnspan=5)
        label_loggedtext.grid(column=0, row=0, sticky='w', pady=5)
        button_logout.grid(column=2, row=0, sticky='w')
        button_create.grid(column=5, row=0, sticky='e')
        button_accountname.grid(column=0, row=1, columnspan=4, sticky='w')
        button_accountid.grid(column=1, row=1, columnspan=4, sticky='w')
        button_accounttype.grid(column=2, row=1, columnspan=4, sticky='w')
        button_accountbalance.grid(column=3, row=1, sticky='e')
        button_accountcurrency.grid(column=4, row=1, columnspan=4, sticky='e')
        self.canvas_accounts.grid(column=0, row=2, columnspan=6, rowspan=100, sticky='nwse')
        self.canvas_accounts.create_window((0, 0), window=self.frame_canvas, anchor='nw')    

        # Configures specific column and row
        self.columnconfigure(4, weight=1)
        self.rowconfigure(100, weight=1)

        def logout(): # Go back to "StartPage"
            controller.show_frame('StartPage')        

    def create_account(self): # Creates window for account creation
        create_window = Toplevel(self.controller)
        
        # Defines properties for new window
        create_window.title('Skapa Konto')
        create_window.minsize(400, 150)
        create_window.maxsize(400, 150)

        # Creates widgets for new window
        label_name = Label(create_window, text='Kontonamn:')
        label_error = Label(create_window, text='Måste välja kontotyp och valuta', fg='red')
        label_success = Label(create_window, text='Konto skapades', fg='lime green')
        label_error_name = Label(create_window, text='Konto måste namnges', fg='red')
        entry_name = Entry(create_window, cursor='xterm')
        button_create = Button(create_window, text='Skapa',
                               command= lambda: create())
        
        # Creates list of available options for account type
        options_type = [
            'Betalkonto',
            'Sparkonto'
        ]

        # Creates list of available optinos for currency
        options_currency = [
            'SEK',
            'USD',
            'EUR',
            'DKK',
            'NOK'
        ]

        # Creates specific design for OptionMenu widget
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('custom.TMenubutton', background='white', bordercolor='black', borderthickness=1, arrowsize=3)
        style.map('custom.TMenubutton', background=[('active', 'light gray')])

        # Creates dropdown menu with the option defined above
        clicked_type = StringVar()
        clicked_currency = StringVar()
        option_type = ttk.OptionMenu(create_window, clicked_type, 'Välj Kontotyp', *options_type)
        option_type.config(width=12, style='custom.TMenubutton')
        option_currency = ttk.OptionMenu(create_window, clicked_currency, 'Välj Valuta', *options_currency)
        option_currency.config(width=10, style='custom.TMenubutton')
        
        # Defines placement of all widgets within window
        label_name.grid(column=0, row=0, padx=5, sticky='w')
        entry_name.grid(column=1, row=0, sticky='w')
        option_type.grid(column=0, row=1, padx=5, pady=5, sticky='w', columnspan=2)
        option_currency.grid(column=1, row=1, padx=45, pady=5, sticky='w', columnspan=2)
        button_create.grid(column=2, row=1)

        # Configures specific column and row
        create_window.columnconfigure(2, weight=1)
        create_window.rowconfigure(3, weight=1)

        def create(): # Function to create new account
            label_error.grid_forget()
            label_error_name.grid_forget()
            label_success.grid_forget()
            
            # If user has input name for account and chosen account type and currency function creates new account within users account
            # Otherwise displays error messages pertaining to specific error
            if clicked_type.get() != 'Välj Kontotyp' and clicked_currency.get() != 'Välj Valuta' and entry_name.get() != '':
                    new_account(self.controller.logged_userid, clicked_type.get(), clicked_currency.get(), entry_name.get())
                    label_success.grid(column=2, row=0, sticky='e')
                    entry_name.delete(0, END)
                    option_type.grid(column=0, row=1, padx=5, pady=5, sticky='w', columnspan=2)
                    option_currency.grid(column=1, row=1, padx=45, pady=5, sticky='w', columnspan=2)
                    self.update_accounts(0)
            
            elif entry_name.get() == '':
                label_error_name.grid(column=2, row=0, sticky='e')

            else:
                label_error.grid(column=2, row=0, sticky='e')
                            
    def update_accounts(self, sort_type): # Refreshes list of accounts depending on sort_type
        self.clear()     
        
        try: # Retrieves all accounts within users account, if there are none nothing happens
            name_list, account_list, type_list, balance_list, currency_list = get_accounts(self.controller.logged_userid, sort_type)

            self.buttons = [] # Creates empty list for all created buttons
            # Buttons need to be in a list in order to be easily removed when needed
            for i, name in enumerate(name_list): # Creates button displaying account name, moves to tied account when pressed
                button = Button(self.frame_canvas, text=str(name).strip("[]{'}"), relief='solid', borderwidth=1, width=75, height=2, anchor='w', padx=5,
                                command= lambda i=i: switch_to(account_list[i], sort_type, i))
                button.grid(column=0, row=(0+i), columnspan=4, sticky='w')
                self.buttons.append(button)
            
            for i, account in enumerate(account_list): # Creates button displaying account number, moves to tied account when pressed
                button = Button(self.frame_canvas, text=account, relief='solid', borderwidth=1, width=75, height=2, anchor='w', padx=5,
                                command= lambda i=i: switch_to(account_list[i], sort_type, i))
                button.grid(column=1, row=(0+i), columnspan=4, sticky='w')
                self.buttons.append(button)

            for i, type in enumerate(type_list): # Creates button displaying account type, moves to tied account when pressed
                button = Button(self.frame_canvas, text=type, relief='solid', borderwidth=1, width=65, height=2, anchor='w', padx=5,
                                command= lambda i=i: switch_to(account_list[i], sort_type, i))
                button.grid(column=2, row=(0+i), columnspan=4, sticky='w')
                self.buttons.append(button)          

            for i, balance in enumerate(balance_list): # Creates button displaying account balance, moves to tied account when pressed
                button = Button(self.frame_canvas, text='{:,}'.format(balance).replace(',', ' '), relief='solid', borderwidth=1, width=20, height=2, anchor='e', padx=5,
                                command= lambda i=i: switch_to(account_list[i], sort_type, i))
                button.grid(column=3, row=(0+i), sticky='e')
                self.buttons.append(button)      

            for i, currency in enumerate(currency_list): # Creates button displaying account currency, moves to tied account when pressed
                button = Button(self.frame_canvas, text=currency, relief='solid', borderwidth=1, width=45, height=2, anchor='w', padx=5,
                                command= lambda i=i: switch_to(account_list[i], sort_type, i))
                button.grid(column=4, row=(0+i), columnspan=4, sticky='e')
                self.buttons.append(button)
            
            self.update_scrollregion()
            
            if len(self.buttons) < 40: # If there are more than eight rows of buttons the user gains the ability to scroll the list with mousewheel
                self.canvas_accounts.unbind_all('<MouseWheel>')
            else:
                self.canvas_accounts.bind_all('<MouseWheel>', self.on_mousewheel)
            
        except: None

        def switch_to(accountnum, sort_type, i): # Switches to account with matching account number
            # Stores necessary shared variables
            self.controller.logged_accountnum = accountnum
            self.controller.logged_sorttype = sort_type
            self.controller.logged_i = i
            self.controller.show_frame('Account')
            
    def update_scrollregion(self): # Updates the scrollable region depending on amount of buttons
        def update_scrollregion():   
            self.canvas_accounts.config(scrollregion=self.canvas_accounts.bbox('all'))       
        self.canvas_accounts.after_idle(update_scrollregion)

    def clear(self): # Removes all buttons if there are any        
        try:
            for button in self.buttons:
                button.grid_forget()
        except: None

    def update_user(self): # Displays stored username in label_user widget
        self.label_user.config(text=self.controller.logged_username)
        self.label_user.grid(column=1, row=0, padx=5, sticky='w')

    def on_mousewheel(self, event): # Scrolls when mousewheel is scrolled
        self.canvas_accounts.yview_scroll(-1*event.delta//120, 'units')

    def tkraise(self, aboveThis=None): # Executes update_user and update_accounts with default sort_type when frame is raised
        self.update_user()
        self.update_accounts(0)
        super().tkraise(aboveThis)

class Account(Frame): # Sets up "Account" frame
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # Imports necessary shared variables
        self.logged_accountnum = self.controller.logged_accountnum
        self.logged_userid = self.controller.logged_userid
        self.logged_sorttype = self.controller.logged_sorttype
        self.logged_i = self.controller.logged_i

        # Creates frame for displaying account operations
        self.frame = Frame(self, borderwidth=1, relief='solid')
        
        # Creates label widgets
        label = Label(self, text='Kontonummer:')
        self.label_balance = Label(self, text='', fg='lime green')
        self.label_accountnum = Label(self, text='', fg='magenta')

        # Creates button widgets
        button_back = Button(self, text='Tillbaka',
                             command= lambda: controller.show_frame('Logged_In'))
        self.button_show = Button(self, text='Visa Historik',
                             command= lambda: show_plot())
        self.button_deposit = Button(self, text='Insättning',
                                command= lambda: set_frame('Insättning'))
        self.button_withdraw = Button(self, text='Uttag',
                                 command= lambda: set_frame('Uttag'))
        self.button_transaction = Button(self, text='Överföring',
                                    command= lambda: set_transfer())
        self.button_history = Button(self, text='Visa Transaktioner',
                                command= lambda: show_history())
        self.button_delete = Button(self, text='Ta Bort Konto',
                               command= lambda: set_delete())
                
        # Defines placement of widgets
        label.grid(column=0, row=0, pady=5)
        self.label_accountnum.grid(column=1, row=0, padx=5)
        self.label_balance.grid(column=2, row=0, sticky='e')
        button_back.grid(column=2, row=0, sticky='w')
        self.frame.grid(column=2, row=2, rowspan=10, sticky='wn', columnspan=3)
        
        # Create empty list to store account type specific buttons
        self.buttons = []

        # Configures size of specific column and row
        self.columnconfigure(2, weight=1)
        self.rowconfigure(10, weight=1)
        
        def set_frame(type:str): # Sets up widgets in frame for deposit or withdraw operation depending on type variable
            self.clear()
            
            # Creates widgets for frame
            label_deposit = Label(self.frame, text=type + ':')
            label_note = Label(self.frame, text='Anteckning:')
            button_confirm = Button(self.frame, text='Godkänn',
                                    command= lambda: trans(type))
            entry_amount = Entry(self.frame, cursor='xterm')
            textbox_note = Text(self.frame, cursor='xterm', width=33, height=5)
            label_message = Label(self.frame, text='')

            # Creates list of currency options
            options_currency = [
                'SEK',
                'USD',
                'EUR',
                'DKK',
                'NOK'
            ]

            # Defines design for optionmenu widget
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('custom.TMenubutton', background='white', bordercolor='black', borderthickness=1, arrowsize=3)
            style.map('custom.TMenubutton', background=[('active', 'light gray')])

            # Creates optionmenu widget with options defined above
            clicked_currency = StringVar()
            option_currency = ttk.OptionMenu(self.frame, clicked_currency, self.currency, *options_currency)
            option_currency.config(style='custom.TMenubutton', width=5)

            # Defines placement of all widgets within frame
            label_deposit.grid(column=0, row=0, sticky='w', padx=5, pady=5)
            entry_amount.grid(column=0, row=1, sticky='w', padx=5, columnspan=2)
            option_currency.grid(column=2, row=1, sticky='w')
            label_note.grid(column=0, row=3, sticky='w', padx=5)
            textbox_note.grid(column=0, row=4, sticky='w', columnspan=4, padx=5, pady=5)
            button_confirm.grid(column=3, row=1, padx=5, sticky='e')
            label_message.grid(column=1, row=0, sticky='w', padx=5, columnspan=3)

            # Configures size of column
            self.frame.columnconfigure(3, weight=1)

            def trans(type:str): # Performs transaction
                
                try: # Checks if user has provided a valid float for the currency_exchange function
                    value = currency_exchange(entry_amount.get(), self.currency, clicked_currency.get(), 'transaction')
                    
                    if value <= self.balance or type == 'Insättning': # Checks if user tries to withdraw more than available balance
                        transaction(self.controller.logged_accountnum, type, value, textbox_note.get('1.0', 'end-1c'))
                        label_message.config(text=type + ' lyckades', fg='lime green')
                        entry_amount.delete(0, END) # Clears entry widget
                        textbox_note.delete('1.0', END) # Clears text widget
                        self.update_account(self.sorttype)
                    
                    else:
                        label_message.config(text='Uttag måste vara mindre än saldo', fg='red')

                except:
                    label_message.config(text=type + ' måste vara ett belopp', fg='red')

        def set_transfer(): # Sets up frame for transfer operation
            self.clear()
            
            # Creates widgets for frame
            label_transfer = Label(self.frame, text='Överföring:')
            label_account = Label(self.frame, text=self.controller.logged_accountnum, borderwidth=1, relief='solid')
            label_to = Label(self.frame, text='Till')
            label_note = Label(self.frame, text='Anteckning:')
            label_error = Label(self.frame, text='')
            label_currency = Label(self.frame, text=self.currency)
            button_confirm = Button(self.frame, text='Godkänn',
                                    command= lambda: transfer())
            entry_amount = Entry(self.frame, cursor='xterm')
            entry_account = Entry(self.frame, cursor='xterm')
            textbox_note = Text(self.frame, cursor='xterm', width=33, height=5)

            # Defines styles for optionmenu widgets
            style = ttk.Style()
            style.theme_use('clam')
            style.configure('custom.TMenubutton', background='white', bordercolor='black', borderthickness=1, arrowsize=3)
            style.map('custom.TMenubutton', background=[('active', 'light gray')])
            style.configure('label.TMenubutton', background='white', bordercolor='black', borderthickness=1, arrowsize=0, arrowpadding=0)
            style.map('label.TMenubutton', background=[('active', 'white')])            

            option_accounts = [] # Creates list to store all of users other accounts
            accounts = get_accounts(self.controller.logged_userid, 0) # Retrieves accounts
            
            for i, account in enumerate(accounts[0]): # Appends account names to previously defined list along with account number
                if i != self.controller.logged_i:
                    new_account = str(account).strip("[']")
                    option_accounts.append(new_account + ': ' + str(accounts[1][i]))
            option_accounts.append('Annan användare...') # Adds option to transfer to other users account
            
            def on_option_change(*args): # When option in optionmenu is changed check if "Annan användare..." is selected
                if clicked_account.get() == 'Annan användare...':
                    option_accounts.grid_forget()
                    entry_account.grid(column=2, row=2, sticky='w', columnspan=10) # Adds entry widget instead of optionmenu
            
            # Creates optionmenu for selecting other account
            clicked_account = StringVar()
            clicked_account.trace_add('write', on_option_change)
            option_accounts = ttk.OptionMenu(self.frame, clicked_account, 'Välj Konto', *option_accounts)
            option_accounts.config(width=15, style='custom.TMenubutton')
            
            # Creates optionmenus without the ability to select options in order to create a label with a similar design to the previous optionmenu
            current_account = StringVar()
            current_currency = StringVar()
            label_account = ttk.OptionMenu(self.frame, current_account, self.controller.logged_accountnum)
            label_account.config(width=6, style='label.TMenubutton')
            label_currency = ttk.OptionMenu(self.frame, current_currency, self.currency)
            label_currency.config(width=4, style='label.TMenubutton')

            # Defines placement of all widgets within frame
            label_transfer.grid(column=0, row=0, sticky='w', columnspan=3, padx=5)
            label_error.grid(column=0, row=1, sticky='w', padx=5, columnspan=10)
            label_account.grid(column=0, row=2, pady=5, sticky='w', padx=5)
            label_to.grid(column=1, row=2, padx=5, sticky='w')
            label_note.grid(column=0, row=4, sticky='w', padx=5, columnspan=3)
            label_currency.grid(column=3, row=3, sticky='w', padx=5)
            textbox_note.grid(column=0, row=5, sticky='w', columnspan=4, padx=5, pady=5)
            option_accounts.grid(column=2, row=2, sticky='w', columnspan=10)
            entry_amount.grid(column=0, row=3, sticky='w', padx=5, pady=5, columnspan=3)
            button_confirm.grid(column=3, row=3, sticky='e', padx=5)

            # Configures size of column
            self.frame.columnconfigure(3, weight=1)

            def transfer(): # Performs transfer operation
                
                try: # Checks if user has provided a valid float
                    value = float(entry_amount.get())
                    
                    # Retrieves account number for selected or provided account
                    if clicked_account.get() == 'Annan användare...':
                        transfer_account = entry_account.get()
                    else:
                        transfer_account = clicked_account.get().split(': ')

                except: # Displays error message
                    label_error.config(text='Överföring måste vara ett belopp', fg='red')
                    return

                # Checks if transfer is valid and if user has selected an account to transfer to from the provided list
                if clicked_account.get() != 'Välj Konto' and value < self.balance and entry_account.get() == '':
                    error, text = account_transfer(self.controller.logged_accountnum, transfer_account[1].strip("'"), value, textbox_note.get('1.0', 'end-1c'), self.currency)
                    if error: # Transfer has been performed
                        label_error.config(text='Överföring lyckades', fg='lime green')
                        self.update_account(self.sorttype)

                    elif error == False:
                        label_error.config(text=text, fg='red')

                elif entry_account.get() != '': # Checks if user has provided anything in the entry_account widget
                    
                    res = check_account(transfer_account)

                    if res: # Checks if account number is valid
                        error, text = account_transfer(self.controller.logged_accountnum, transfer_account, value, textbox_note.get('1.0', 'end-1c'), self.currency)
                        if error: # Transfer has been performed
                            label_error.config(text='Överföring lyckades', fg='lime green')
                            self.update_account(self.sorttype)

                        elif value > self.balance:
                            label_error.config(text='För stort belopp', fg='red')
                    
                    elif res == False:
                        label_error.config(text='Kan endast överföra till \nandra användares betalkonto', fg='red')

                    elif res == None:
                        label_error.config(text='Felaktigt kontonummer', fg='red')
                    
        def show_plot(): # Sets up frame to display matplotlib plot of account history
            self.clear()
            balance, dates = balance_history(self.controller.logged_accountnum)
            title = {'family':'sans-serif','color':'black','size':14}
            fig = Figure(figsize=(4, 2.5))
            fig.subplots_adjust(left=0.18, right=0.9, top=0.86, bottom=0.30)
            fig.tight_layout()
            ax = fig.add_subplot(111)
            
            ax.plot(dates, balance)
            ax.set_xlabel('Datum')
            ax.set_ylabel('Saldo ' + self.currency)
            ax.set_title(f"{str(self.controller.logged_accountnum)}: Saldo Historik",loc= 'left',fontdict=title)
            
            for label in ax.get_xticklabels():
                label.set_rotation(30)
                label.set_fontsize(8)
            
            canvas = FigureCanvasTkAgg(fig, master=self.frame)
            canvas.draw()
            canvas.get_tk_widget().pack()
            
        def show_history(): # Sets up frame to display account history
            self.clear()

            # Creates widgets for frame
            label_date = Label(self.frame, text='Datum', relief='ridge', bg='white', borderwidth=1)
            label_transaction = Label(self.frame, text='Transaktionstyp', relief='ridge', bg='white', borderwidth=1)
            label_amount = Label(self.frame, text='Överfört Belopp', relief='ridge', bg='white', borderwidth=1)
            label_note = Label(self.frame, text='Anteckning', relief='ridge', bg='white', borderwidth=1)
            listbox_history_date = Listbox(self.frame, relief='ridge', width=10) # Listbox() is a widget that displays a list of values in a scrollable box format
            listbox_history_transaction = Listbox(self.frame, relief='ridge', width=22)
            listbox_history_amount = Listbox(self.frame, relief='ridge')
            listbox_history_note = Listbox(self.frame, relief='ridge')
            listboxes = [listbox_history_date, listbox_history_transaction, listbox_history_amount, listbox_history_note]
            
            # Retrieves account history and splits it into four lists
            amount_list, transaction_list, date_list, note_list = get_history(self.controller.logged_accountnum, self.currency)
            
            for i in date_list: # Adds dates to first listbox
                listbox_history_date.insert(END, i)
            listbox_history_date.grid(column=0, row=1, sticky='nswe')

            for i in transaction_list: # Adds transaction types to second listbox
                listbox_history_transaction.insert(END, i)
            listbox_history_transaction.grid(column=1, row=1, sticky='nswe')

            for i in amount_list: # Adds transfered amount to third listbox
                listbox_history_amount.insert(END, i)
            listbox_history_amount.grid(column=2, row=1, sticky='nswe')

            for i in note_list: # Adds user-provided note to third listbox
                listbox_history_note.insert(END, i)
            listbox_history_note.grid(column=3, row=1, sticky='nswe')
                    
            # Defines placement of labels in frame
            label_date.grid(column=0, row=0, sticky='nswe')
            label_transaction.grid(column=1, row=0, sticky='nswe')
            label_amount.grid(column=2, row=0, sticky='nswe')
            label_note.grid(column=3, row=0, sticky='nswe')

            def on_mousewheel(event): # Makes the user able to control all listboxes at the same time with their mousewheel
                for listbox in listboxes:
                    listbox.yview_scroll(-1*event.delta//120, 'units')   
                return 'break'         
            
            for listbox in listboxes: # Binds MouseWheel to function giving it control over listboxes
                listbox.bind('<MouseWheel>', on_mousewheel)                        
        
        def set_delete(): # Sets up frame to delete current account
            self.clear()
            
            # Creates widgets for frame
            label_delete = Label(self.frame, text='Radera Konto:')
            label_warning = Label(self.frame, text='Detta går inte att ångra!', font=('Courier', 8))
            label_message = Label(self.frame, text='')
            label_pin = Label(self.frame, text='Lösenord:')
            entry_pin = Entry(self.frame, cursor='xterm')
            button_confirm = Button(self.frame, text='Bekräfta',
                                    command= lambda: delete())

            # Defines placement of widgets within frame
            label_delete.grid(column=0, row=0, sticky='w', padx=5, pady=2)
            label_warning.grid(column=0, row=1, sticky='w', padx=5, columnspan=3)
            label_message.grid(column=0, row=2, sticky='w', padx=5, columnspan=3)
            label_pin.grid(column=0, row=3, sticky='w', padx=5, pady=5)
            entry_pin.grid(column=1, row=3, sticky='w')
            button_confirm.grid(column=2, row=3, sticky='w', padx=5)
            
            def delete(): # Switches button when "Bekräfta" button is pressed
                button_confirm.config(text='Är du säker?', command= lambda: delete_confirm())

            def delete_confirm(): # Attempts to delete account
                result = delete_account(self.controller.logged_accountnum, entry_pin.get())

                if result[0] == False: # User provided incorrect password
                    label_message.config(text='Fel lösenord, kontot har inte tagits bort', fg='red')
                    self.after(500, lambda: reset())

                elif result[0] == None: # Account was not empty
                    label_message.config(text='Kontot måste tömmas innan det kan raderas', fg='red')
                    self.after(500, lambda: reset())

                elif result[0] == True: # Account has successfully been removed
                    label_message.config(text='Kontot har tagits bort', fg='lime green')
                    self.after(1000, lambda: controller.show_frame('Logged_In'))

            def reset(): # Resets frame to inital state
                button_confirm.config(text='Bekräfta', command= lambda: delete())
                entry_pin.delete(0, END)

    def check_buttons(self): # Defines placement of all buttons in self.buttons list
        for i ,button in enumerate(self.buttons):
            button.grid(column=0, row=1+i, sticky='w', padx=5, pady=3, columnspan=2)

    def clear_buttons(self): # Resets buttons
        for button in self.buttons:
            button.grid_forget()

        if not self.controller.logged_accountnum % 2: # Checks account type
            self.buttons = [self.button_transaction, self.button_show, self.button_history, self.button_delete]
        
        else:
            self.buttons = [self.button_deposit, self.button_withdraw, self.button_transaction, self.button_show, self.button_history, self.button_delete]


    def clear(self): # Removes frame containing operations and recreates it blank
        self.frame.destroy()
        self.frame = Frame(self, borderwidth=1, relief='solid')
        self.frame.grid(column=2, row=2, rowspan=10, sticky='n')        

    def update_account(self, sort_type): # Updates account number and balance displayed at the top of the frame
        accounts = get_accounts(self.controller.logged_userid, sort_type)
        self.balance = accounts[3][self.controller.logged_i]
        currency = accounts[4][self.controller.logged_i]
        self.currency = currency[0]
        self.label_balance.config(text='Saldo: ' + '{:,}'.format(self.balance).replace(',', ' ') + ' ' + str(self.currency))
        self.label_accountnum.config(text=self.controller.logged_accountnum)

    def tkraise(self, aboveThis=None): # Executes clear, update_account, clear_buttons and check_buttons functions along with importing sorttype shared varible whenever frame is raised
        self.sorttype = self.controller.logged_sorttype
        self.clear()
        self.update_account(self.sorttype)
        self.clear_buttons()
        self.check_buttons()
        super().tkraise(aboveThis)
        
class Admin(Frame): # Sets up "Admin" frame
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # Creates widgets for frame
        label_title = Label(self, text=text_admin, font=('Courier', 8), justify=LEFT)
        self.entry_user = Entry(self, cursor='xterm')
        button_reset_trys = Button(self, text='Återställ Försök',
                                   command= lambda: reset(self.entry_user.get()))
        button_back = Button(self, text='Gå Tillbaka',
                             command= lambda: controller.show_frame('StartPage'))
        
        # Defines placement of all widgets in frame
        label_title.grid(column=0, row=0, sticky='n', columnspan=2)
        self.entry_user.grid(column=0, row=1, sticky='e', padx=10)
        button_reset_trys.grid(column=1, row=1, sticky='w')
        button_back.grid(column=0, row=6, pady=10, sticky='s', columnspan=2)
        
        # Configues size of columns and row
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(6, weight=1)
        
        def reset(username): # Resets number of login attempts for provided user account
            id = check_username(username)
            if id[0] == True:
                print('Attempts Reset')
                correct_psw(id[1])
            else:
                print('Account Not Found')    
                    
    def clearframe(self): # Clear entry widget
        self.entry_user.delete(0, END)
        
    def tkraise(self, aboveThis=None): # Executes clearframe function whenever frame is raised
        self.clearframe()
        super().tkraise(aboveThis)


if __name__ == '__main__': # Starts the application
    interest()
    app = Application()
    app.mainloop()