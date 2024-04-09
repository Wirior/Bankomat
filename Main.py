text_title = """
______                _                              _   
| ___ \              | |                            | |  
| |_/ /  __ _  _ __  | | __  ___   _ __ ___    __ _ | |_ 
| ___ \ / _` || '_ \ | |/ / / _ \ | '_ ` _ \  / _` || __|
| |_/ /| (_| || | | ||   < | (_) || | | | | || (_| || |_ 
\____/  \__,_||_| |_||_|\_\ \___/ |_| |_| |_| \__,_| \__|    V:1.0                                                         
"""

text_admin = """
                 _               _         
     /\         | |             (_)        
    /  \      __| |  _ __ ___    _   _ __  
   / /\ \    / _` | | '_ ` _ \  | | | '_ \ 
  / ____ \  | (_| | | | | | | | | | | | | |
 /_/    \_\  \__,_| |_| |_| |_| |_| |_| |_|
"""

import os  # Importing the os module to interact with the operating system
import time  # Importing the time module for time-related functions
import json  # Importing the json module for JSON file operations
import inquirer  # Importing the inquirer module for interactive user prompts
from datetime import date  # Importing the date class from the datetime module
from getpass import getpass # Importing the hidden password module for user input
import random # Importing random function for slump actions
import matplotlib.pyplot as plt # importing pylot module to plot grapths
from tkinter import *
from tkinter import ttk

from email_validator import validate_email, EmailNotValidError  # Importing email validation functions

"""
Remember to replace the file path with your location of the files and replace the \\(backslah) with / 
"""
Path_Users = "C:/Users/William/My Drive/Gruppuppgift/Bankomat-main/Users.json"  # Path to the users JSON file
Path_Passwords = "C:/Users/William/My Drive/Gruppuppgift/Bankomat-main/Passwords.json"  # Path to the passwords JSON file
Path_Accounts = "C:/Users/William/My Drive/Gruppuppgift/Bankomat-main/Accounts.json"  # Path to the accounts JSON file

today = date.today()  # Getting today's date

def read_file(filepath:str):
    """Fuction to read a json file and return a dump of json.
    - Return the json data
    """
    with open(filepath,"r") as a:
        return json.load(a)

def write_file(filepath:str, data:json, indent:int):
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
    - Returns Account_num if the account password matches the submitted psw
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
        account_num = val["account"]  # Getting account number
        correct_psw(user_id)
        return True, account_num
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

def transaction(account_num:str, type:str, amount, note:str):
    """Function to write a transaction between accounts.
    - Imports the type of transaction; Uttag, Insättning
    - Imports the amount to be moved
    - Imports a note made by the user
    - Returns False + error message if the balance can't be transferd
    """
    # Get data from json file
    Accounts_data = read_file(Path_Accounts)
    for val in Accounts_data[str(account_num)]:
        account_balance = val["balance"]
        account_transaction = val["transaction"]
        account_date = val["date"]
        account_note = val["note"]
    
    if isinstance(amount, (int, float)):  # pass tuple
        return False, "Strängar kan inte matas in"

    if type == "Uttag": amount = -1*abs(float(amount)) # Negating amount for withdrawals

    # Adding the new transaction data to the account
    account_balance.insert(0, account_balance[0] + float(amount))
    account_transaction.insert(0, type)
    account_date.insert(0, str(today))
    account_note.insert(0, note)

    write_file(Path_Accounts,Accounts_data,4)
    return True, 0

def account_transfer(account_num:str, transfer_num:str, amount, note:str):
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
    
    if isinstance(amount, (int, float)):  # pass tuple
        return False, "Strängar kan inte matas in"

    # Trying to find the inputed account number
    trigger = True
    for val in Accounts_data: # Itterating through Accounts.json 
        if val == transfer_num and (val != str(account_num)):
            trigger = False
            break  
    if trigger: False, "Kontonumret fanns inte att föra över till"

    # Adding the new transaction data to the account
    account_balance.insert(0, account_balance[0] - abs(float(amount)))
    account_transaction.insert(0, "Kontoöverföring")
    account_date.insert(0, str(today))
    account_note.insert(0, note)
    
    # Itterating through the Transfer Accounts data
    for val in Accounts_data[str(transfer_num)]: # Read the new account
        t_account_balance = val["balance"]
        t_account_transaction = val["transaction"]
        t_account_date = val["date"]
        t_account_note = val["note"]
    
    # Adding the new transaction data to the account
    t_account_balance.insert(0, t_account_balance[0] + abs(float(amount)))
    t_account_transaction.insert(0, "Kontoöverföring")
    t_account_date.insert(0, str(today))
    t_account_note.insert(0, note)

    write_file(Path_Accounts, Accounts_data, 4)
    return True, 0

def new_account(username:str,password:str):
    """Function to create a new account, and add all the users data to the .json file
    - Imports the users username
    - Imports the specific password
    """
    users_data = read_file(Path_Users)
    passwords_data = read_file(Path_Passwords)
    accounts_data = read_file(Path_Accounts)
 
    if validate_username(username) == False: # Validate email adress
        return 1
    
    if check_username(username) == True: # Check if username already exists
        return 2
    
    user_id = create_id(users_data["master"],"user_id") # Create a unique 6 digit user_id 
    account_num = create_id(passwords_data['password'],"account") # Create a unique 6 digit account_num 

    # Writing over the existing files with the new users data
    users_data["master"].append({"user":username,"user_id":user_id})
    write_file(filepath= Path_Users, data= users_data, indent= 2)
    
    passwords_data["password"].append({"user_id":user_id,"psw":password,"trys":4,"account":account_num})
    write_file(filepath= Path_Passwords, data= passwords_data, indent= 2)
    
    # Appening new Account data
    new_bank_data = [{
        "balance": [0],
        "transaction": [""],
        "date": [str(today)],
        "note": ["Konto skapades"]
    }]
    accounts_data[account_num] = new_bank_data
    write_file(filepath= Path_Accounts, data= accounts_data, indent= 3)
    return 0

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
            print(i)
            print(new_id, i[id])
            if new_id == i[id]: trigger = False
        if trigger: return new_id
        input("pause")

def balance_history(account_num:str): # Det finns något sätt att embed:a pyplot i Tkinter appen
    """Function to plot the balance hotory of a specif account number
    """
    accounts_data = read_file(Path_Accounts)
    # Itterate though the account and save the balance
    for val in accounts_data[str(account_num)]:
        account_balance = val["balance"]
        account_date = val["date"]
    
    balance = []
    for index in reversed(account_balance): balance.append(index) # Reversed list of the dates
    dates = []
    for index in reversed(account_date): dates.append(index) # Reversed list of the dates

    title = {'family':'sans-serif','color':'black','size':18} # Set the title with font, colour and size
    plt.locator_params(axis='x', nbins=4) # Number of ticks for the x-axis
    plt.xticks(rotation=30, ha="right") # Rotate the lable for the x-axis ticks by 30 degree

    plt.title(f"{str(account_num)}: Saldo historik",loc= 'left', fontdict= title) # Title
    plt.xlabel("Datum") # X-lable
    plt.ylabel("Belopp [sek]") # Y-lable

    print("Stäng ner grafens fönstret för att fortsätta...")
    plt.plot(dates, balance)
    plt.show()
    return

def transaction_history(account_num:str): # Den här måste också ändras för att skriva ut all data nu är det bara print
    """Function to itterate through the account history displaying it
    - Imports account number to read the files
    """
    accounts_data = read_file(Path_Accounts)
    
    # Print the information in the desired format
    print("{0:<20} | {1:<18} | {2:<16} | {3:<30}\n"
              .format("Saldo", "Transaktion", "Datum", "Anteckning"))
    # Itterates through the accounts json data, and prints out each element in order.
    for item in range(len(accounts_data[str(account_num)][0]['balance'])):
        balance = accounts_data[str(account_num)][0]['balance'][item]
        transaction = accounts_data[str(account_num)][0]['transaction'][item]
        date = accounts_data[str(account_num)][0]['date'][item]
        note = accounts_data[str(account_num)][0]['note'][item]
        
        print("{0:<20} | {1:<18} | {2:<16} | {3:<30}"
              .format(balance, transaction, date, note, item))
        
        if item >= 30: # Check if the item is equal to or larger than 30, if so: stop printing
            print("Kunde endast ladda in de senaste 30 transaktionerna")
            break
    input("Tryck enter för att fortsätta") # Remove this if needed

    return



def start():
    """
    Function to start the banking system.
    """
    while True:
        os.system('cls')  # Clearing the screen
        print("Bankomat \n")  # Printing a header

        # Presenting a list of options to the user
        questions = [
            inquirer.List('interaktion',
                          message="Välj interaktion",
                          choices=['Logga in', 'Ny användare', 'Avsluta'],
                          ),
        ]
        answers = inquirer.prompt(questions)  # Getting user's choice
        
        if answers["interaktion"] == 'Logga in':
            Log_in()  # Calling the Log_in function for user login
        elif answers["interaktion"] == 'Ny användare':
            New_user()  # Calling the New_user function for creating a new user
        elif answers["interaktion"] == 'Avsluta':
            break  # Exiting the program
    
    return

def Log_in():
    """
    Function for user login.
    """
    # Get username
    while True:
        # Displaying the text on screen
        os.system('cls')
        print("Bankomat \n")

        username = input("Användarnamn: ")  # Getting username from user
        if username=="":
            break
        user_id = check_username(username) # Check if the username exists 
        if user_id: break

        print("Användarnamnen som har skrivits in existerar inte")
        time.sleep(2)
    
    # Check password
    if user_id and username:
        while True:
            # Displaying the text on the screen
            os.system('cls')
            print("Bankomat \n")
            print("Användarnamn:", username)
            password = getpass("Lösenord: " + u'\U0001f512')
            account_num, error = check_password(user_id, password)
            if account_num: break
            else:
                print(error)
                input("Tryck enter för att fortsätta")
                if account_num == None: return
        
        if account_num:
            while True:
                os.system('cls')
                print("Bankomat \n")

                print(f"Inloggad på: {account_num}")
                questions = [
                    inquirer.List('account',
                                message="Välj interaktion",
                                choices=['Genomför transaktion', 'Saldo historik', 'Transaktions historik', 'Logga ut'],
                                ),
                ]
                answers = inquirer.prompt(questions)  # Getting user's choice

                if answers["account"] == 'Genomför transaktion':
                    Account_Transaction(account_num)  # Performing a transaction
                elif answers["account"] == 'Saldo historik':
                    balance_history(account_num)  # Viewing balance history
                elif answers["account"] == 'Transaktions historik':
                    transaction_history(account_num)  # Viewing transaction history
                elif answers["account"] == 'Logga ut':
                    break  # Logging out
    return

def Account_Transaction(account_num):
    """
    Function to perform a transaction.
    """
    # Read the Account file
    accounts_data = read_file(Path_Accounts)
    
    for val in accounts_data[str(account_num)]:
        account_balance = val["balance"]
        
    while True:
        os.system('cls')  # Clearing the screen
        print("Bankomat \n")

        # Printing current balance
        print("Nuvarande belopp:", account_balance[0], " kr")  
        
        # Prompting user to choose a transaction type
        questions = [
            inquirer.List('transaction', message="Välj interaktion", choices=["Uttag", "Insättning", "Kontoöverföring", "Tillbaka"], ),
        ]
        answers = inquirer.prompt(questions)  # Getting user's choice
        
        # Handling user's transaction choice
        os.system('cls')  # Clearing the screen
        print("Bankomat \n")

        if answers["transaction"] == 'Tillbaka': 
            break  # Going back to the previous menu
        
        text1 = ("Skriv in " + answers["transaction"] + " beloppet \n")  # Prompting for transaction amount
        text2 = ("Göra en kort anteckning till " + answers["transaction"] + "\n")  # Prompting for a note
        
        value = input(text1)  # Getting transaction amount and negating it for withdrawals
        note = input(text2)  # Getting transaction note

        if answers["transaction"] == "Kontoöverföring":
            t_account_num = input("Skriv in kontonummer att skicka till: ")
            status, error = account_transfer(account_num,t_account_num,value,note)
        else:
            status, error = transaction(account_num, answers["transaction"], value, note)
        
        if status: break
        print(error)
        time.sleep(2)

    return

def New_user():
    """
    Function to create a new user.
    """
    username = ""  # Initializing username variable
    password = ""
    while True:
        os.system('cls')  # Clearing the screen
        print("Bankomat \n")
        status = False
        while not(status):
            username = input("Skriv in din mejladress: ")  # Prompting for email address
            
            while True:
                password = getpass("Lösenord: " + u'\U0001f512')  # Prompting for password
                print("Vänligen upprepa lösenordet")
                c_psw = getpass("Lösenord: " + u'\U0001f512')  # Prompting for password confirmation
                if password == "" or c_psw == "":
                    return
                elif password == c_psw:
                    status= True
                    break
                else:
                    print("Lösenorden matchar inte skriv in ditt lösenord igen")
                    time.sleep(2)
        status, error = new_account(username,password)
        if status: break
        print(error)
        time.sleep
    return

class Application(Tk): # Creates main application that the UI is located in
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title('Bankomat')
        self.minsize(675, 350)
        self.maxsize(675, 350)
        self.logged_user = None
        
        container = Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (Menu, Login, Create_Account, Admin, Logged_In):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky='nsew')
        
        self.show_frame('Menu')
        
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        

class Menu(Frame):
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
        self.logged_user = self.controller.logged_user
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
                             command= lambda: controller.show_frame('Menu'))
        
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
                    self.controller.logged_user = trys[1]
                    print(trys[1])
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
                             command= lambda: controller.show_frame('Menu'))
               
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
            
            if new_account(username, pin) == 0:
                self.label_success.grid(column=0, row=5, sticky='s', pady=10, columnspan=2)
           
            elif new_account(username, pin) == 1:
                self.label_error_invalid.grid(column=0, row=5, sticky='s', pady=10, columnspan=2) 
            
            elif new_account(username, pin) == 2:
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
        self.logged_user = self.controller.logged_user
        
class Admin(Frame):
    
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label_title = Label(self, text=text_admin, font=('Courier', 8), justify=LEFT)
        self.entry_user = Entry(self, cursor='xterm')
        button_reset_trys = Button(self, text='Återställ Försök',
                                   command= lambda: reset(self.entry_user.get()))
        button_back = Button(self, text='Gå Tillbaka',
                             command= lambda: controller.show_frame('Menu'))
        
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