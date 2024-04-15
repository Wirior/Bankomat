"""

______                _                              _   
| ___ \              | |                            | |  
| |_/ /  __ _  _ __  | | __  ___   _ __ ___    __ _ | |_ 
| ___ \ / _` || '_ \ | |/ / / _ \ | '_ ` _ \  / _` || __|
| |_/ /| (_| || | | ||   < | (_) || | | | | || (_| || |_ 
\____/  \__,_||_| |_||_|\_\ \___/ |_| |_| |_| \__,_| \__|    V:1.0
                                                         
                                                         
"""

import os  # Importing the os module to interact with the operating system
import time  # Importing the time module for time-related functions
import json  # Importing the json module for JSON file operations
import inquirer  # Importing the inquirer module for interactive user prompts
from datetime import date, datetime, timedelta  # Importing the date, datetime and timedelta class from datetime module
from getpass import getpass # Importing the hidden password module for user input
import random # Importing random function for slump actions
import matplotlib.pyplot as plt # importing pylot module to plot grapths

from email_validator import validate_email, EmailNotValidError  # Importing email validation functions

"""
Remember to replace the file path with your location of the files and replace the \\(backslah) with / 
"""
Path_Users = "C:/Users/Dell/Documents/Python Scripts/Bankomat/Users.json"  # Path to the users JSON file
Path_Passwords = "C:/Users/Dell/Documents/Python Scripts/Bankomat/Passwords.json"  # Path to the passwords JSON file
Path_Accounts = "C:/Users/Dell/Documents/Python Scripts/Bankomat/Accounts.json"  # Path to the accounts JSON file

today = date.today()  # Getting today's date
days_lock_account = 15

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
            return user_id # Returning user ID
    return False # Can't find user in Users.json

def check_password(user_id:str, password:str):
    """Function which takes imports user_id and password and checks if the profile password and password is correct and number of tries left.
    - Imports the user id
    - Imports the password submitted by the user
    - Returns None + error str if the accounts number of tries left are 0
    - Returns False + error str if the password is incorrect
    - Returns list of account numbers if the account password matches the submitted psw
    """
    Passwords_data = read_file(Path_Passwords)
    # Reading user specific data from the stored .json file
    for val in Passwords_data["password"]:
        if user_id == val["user_id"]:
            user_psw = val["psw"]  # Getting user's password
            trys = val["trys"]  # Getting number of tries
            break
    if trys <= 0: return None, "Du har låst ditt konto, kontakta kundtjänst"
    
    # Check if input password is the same as the stored password
    if password == user_psw:
        account_num = val["account"] # Getting account number
        return account_num, 0
    else:
        incorrect_psw(user_id)
        return False, f"Fel lösenord, du har {trys-1} försök kvar"
    
def incorrect_psw(user_id:str):
    """Function to increment the number of failed log ins a user has done 
    - Imports user id to read password data
    - Return True when updated the accounts trys  
    """
    Passwords_data = read_file(Path_Passwords)
    # Reading user specific data from the stored .json file
    for count, val in enumerate(Passwords_data["password"]):
        if user_id == val["user_id"]:
            trys = val["trys"]  # Getting number of tries
            break
    Passwords_data["password"][count]["trys"] = trys-1  # Updating the number of tries in the data
    write_file(Path_Passwords,Passwords_data,4)
    return True

def transaction(account_num:str, type:str, amount:str, note:str, currency= "SEK"):
    """Function to write a transaction between accounts.
    - Imports the type of transaction; Uttag, Insättning
    - Imports the amount to be moved
    - Imports a note made by the user
    - Returns False if it is a savings account
    - Returns False + error message if the balance can't be transferd
    - Returns False + error if your savings go below 0 
    """
    # Check if it is a savings account
    if (account_num%2) == 0:
        return False, "Kan inte göra uttag och insättningar på Sparkonton"

    # Get data from json file
    Accounts_data = read_file(Path_Accounts)
    for val in Accounts_data[str(account_num)]:
        account_currency = val["currency"]
        account_balance = val["balance"]
        account_transaction = val["transaction"]
        account_date = val["date"]
        account_note = val["note"]
    
    exchanged_amount, error = currency_exchange(account_num, amount, currency)
    if error: return False, error # If there was an error during the exchange of currency then 

    if type == "Uttag": amount = -1*abs(float(exchanged_amount)) # Negating amount for withdrawals

    if (account_balance[0] + float(exchanged_amount)) < 0: return False, "Kan inte göra uttag större än saldot"

    # Adding the new transaction data to the account
    account_balance.insert(0, account_balance[0] + float(exchanged_amount))
    account_transaction.insert(0, type)
    account_date.insert(0, str(today))
    account_note.insert(0, note)

    write_file(Path_Accounts,Accounts_data,4)
    return True, 0

def account_transfer(account_num:str, transfer_num:str, amount:float, note:str):
    """Function to write a transaction too and from your account.
    - Imports the amount to be moved
    - Imports a note made by the user
    - Returns False + error message if it is an savings account
    - Returns False + error message if the balance can't be transferd
    - Returns True if successfull
    """
    # Get data from json file
    Accounts_data = read_file(Path_Accounts)
    for val in Accounts_data[str(account_num)]:
        account_currency = val["currency"]
        account_balance = val["balance"]
        account_transaction = val["transaction"]
        account_date = val["date"]
        account_note = val["note"]
    
    # Trying to find the inputed account number
    trigger = True
    for val in Accounts_data: # Itterating through Accounts.json
        if val == transfer_num and (val != str(account_num)):
            trigger = False
            break 
    if trigger: return False, "Kontonumret fanns inte att föra över till"

    # Itterating through the Transfer Accounts data
    for val in Accounts_data[str(transfer_num)]: # Read the transfer account
        t_account_currency = val["currency"]
        t_account_balance = val["balance"]
        t_account_transaction = val["transaction"]
        t_account_date = val["date"]
        t_account_note = val["note"]
    
    # Checking if accounts are savings accounts
    if (int(transfer_num) % 2) == 0:
        if not check_days_passed(t_account_date[0], days_passed= days_lock_account): # Calculate if a set number of days passed since last event on account
            return False, f"Du kan endast överföra pengar till ett konto {days_lock_account} dagar från att senaste konto händelsen"
    if (int(account_num) % 2) == 0: 
        if not check_days_passed(account_date[0], days_passed= days_lock_account):
            return False, f"Du kan endast överföra pengar från ett konto {days_lock_account} dagar från att senaste konto händelsen"
    
    # Convert currency to the desired currency
    exchanged_amount ,error = currency_exchange(account_num= account_num, amount= amount, target_currency= t_account_currency)
    if error: return False, error 
    
    # Adding the new transaction data to the account
    account_balance.insert(0, account_balance[0] - abs(float(amount)))
    account_transaction.insert(0, "Kontoöverföring")
    account_date.insert(0, str(today))
    account_note.insert(0, note)

    # Adding the new transaction data to the account
    t_account_balance.insert(0, t_account_balance[0] + abs(float(exchanged_amount)))
    t_account_transaction.insert(0, "Kontoöverföring")
    t_account_date.insert(0, str(today))
    t_account_note.insert(0, note)

    write_file(Path_Accounts, Accounts_data, 4)
    return True, 0

def create_user(username:str,password:str):
    """Function to create a new account, and add all the users data to the .json file
    - Imports the users username
    - Imports the specific password
    - Returns False + Error message if valide_user or check_username fails
    - Returns True + 0 if sucessfylly created a user
    """
    users_data = read_file(Path_Users)
    passwords_data = read_file(Path_Passwords)
    
    email,enve = validate_username(username) # Validate email adress
    if not(email):
        return False, enve # returns the EmailNotValidError
    
    if check_username(username): # Check if username already exists
        return False, "The submitted emailadress already exists"
    
    user_id = create_id(users_data["master"],"user_id") # Create a unique 6 digit user_id  

    # Writing over the existing files with the new users data
    users_data["master"].append({"user":username,"user_id":user_id})
    write_file(filepath= Path_Users, data= users_data, indent= 2)
    
    passwords_data["password"].append({"user_id":user_id,"psw":password,"trys":4,"account":[]})
    write_file(filepath= Path_Passwords, data= passwords_data, indent= 2)
    
    return True, 0

def validate_username(email:str):
    """Function to validate email address.
    - Imports emailadress
    - Returns False + Error if the email is not valid
    - Returnes the email + 0 if the email is valid
    """
    try:
        # Check that the email address is valid. Turn on check_deliverability
        emailinfo = validate_email(email, check_deliverability=False)
        return emailinfo.normalized, 0
    except EmailNotValidError as e:
        return False,str(e)  # Returning False indicating the email is not valid

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

def balance_history(account_num:str): # Det finns något sätt att embed:a pyplot i Tkinter appen
    """Function to plot the balance hotory of a specif account number
    """
    accounts_data = read_file(Path_Accounts)
    # Itterate though the account and save the balance
    for val in accounts_data[str(account_num)]:
        account_currency = val["currency"]
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
    plt.ylabel(f"Belopp [{account_currency}]") # Y-lable

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
        # if last element
        if item == (len(accounts_data[str(account_num)][0]['balance']) - 1):
            balance = accounts_data[str(account_num)][0]['balance'][item]
        else:
            # For every other element
            balance = accounts_data[str(account_num)][0]['balance'][item] - accounts_data[str(account_num)][0]['balance'][item+1]
        transaction = accounts_data[str(account_num)][0]['transaction'][item]
        date = accounts_data[str(account_num)][0]['date'][item]
        note = accounts_data[str(account_num)][0]['note'][item]
        
        print("{0:<20} | {1:<18} | {2:<16} | {3:<30}"
              .format(round(balance,2), transaction, date, note, item))
        
        if item >= 30: # Check if the item is equal to or larger than 30, if so: stop printing
            print("Kunde endast ladda in de senaste 30 transaktionerna")
            break
    input("Tryck enter för att fortsätta") # Remove this if needed

    return

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
            account_num = create_id(passwords_data['password'],"account") # Create a unique 6 digit account_num
            if (account_num % 2) == 0: break
    elif account_type == "Betalkonto":
        while True: # Creates a odd number for payment account
            account_num = create_id(passwords_data['password'],"account") # Create a unique 6 digit account_num
            if (account_num % 2) == 1: break

    val["account"].append(account_num)
    
    write_file(filepath= Path_Passwords, data= passwords_data, indent= 2)

    # Appening new Account data
    new_bank_data = [{
        "name": name, 
        "currency": currency,
        "balance": [0],
        "transaction": [""],
        "date": [str(today)],
        "note": ["Konto skapades"]
    }]
    accounts_data[account_num] = new_bank_data
    write_file(filepath= Path_Accounts, data= accounts_data, indent= 4)
    
    return val["account"]

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
    
    if not (val["psw"] == password): return account_list , "Fel lösenord, kontot var inte borttaget"

    # Get data from json
    for val in accounts_data[str(account_num)]:
        account_balance = val["balance"]
    if not (account_balance[0] == 0): return account_list , "Kontot får inte inneha något belopp, töm kontor först eller betala av skulden"

    account_list.remove(account_num) # Remove account number from password.json file
    accounts_data.pop(str(account_num)) # Remove the whole account from accounts.json

    write_file(filepath=Path_Passwords, data=passwords_data, indent= 4)
    write_file(Path_Accounts, accounts_data, 4)
    return account_list, 0

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
    
def interest():
    """Function to calculate the intrest on an account if it is the first day of the month.
    Updates the .json file for all savings accounts with their given interest. 
    """
    interest_rate = random.uniform(1.00125,1.0055) # randomize the intrest rate
    # Check if it is the first of the month to run the rest of the intrest function  
    if not (today.day == 1): return

    accounts_data = read_file(Path_Accounts)
    # Get data from json
    for account_num in accounts_data:
        if (int(account_num) % 2) == 0:
            # Read all the data from the account
            for val in accounts_data[str(account_num)]:
                account_balance = val["balance"]
                account_transaction = val["transaction"]
                account_date = val["date"]
                account_note = val["note"]
            # Check if the account has 
            if not check_days_passed(account_date[0], days_passed= 1): break
            # Calculate the intrest for the account
            new_balance = account_balance[0] * interest_rate

            # Adding the new transaction data to the account
            account_balance.insert(0, new_balance)
            account_transaction.insert(0, "Månads ränta")
            account_date.insert(0, str(today))
            account_note.insert(0, f"Måndasräntan låg på {round(interest_rate,4)}% ")
    # Writing to file when all savings accounts have been added
    write_file(Path_Accounts, accounts_data, 4)  
    return

def currency_exchange(account_num:str, amount:str, target_currency:str):
    """Functio do do currency exchange from a given value.
    - Imports account number
    - Imports amount to be exchanged
    - Imports the targeted currency
    - Returns the same value if the currency is the same
    - Returns False + error i the currency is not supported
    - Returns the transformed value based on the exchange rates
    """
    # Read the Accounts.json file
    accounts_data = read_file(Path_Accounts)
    
    # Read currency from the account 
    source_currency = accounts_data[str(account_num)][0]['currency']

    # Check if the target currency is the same as currency.
    if source_currency == target_currency: return abs(float(amount)), 0
    
    # There are 5 exchange rates. From the 5 different currencies to the corresponding value in the target currency. The amount should be multiplied by this factor later.
    exchange_rates = {"SEK": {"USD": 0.12, "EUR": 0.11, "DKK": 0.84, "NOK": 1.32},
                      "USD": {"SEK": 8.69, "EUR": 0.91, "DKK": 6.76, "NOK": 10.56},
                      "EUR": {"SEK": 9.18, "USD": 1.10, "DKK": 7.43, "NOK": 11.62},
                      "DKK": {"SEK": 1.19, "USD": 0.15, "EUR": 0.13, "NOK": 1.57},
                      "NOK": {"SEK": 0.76, "USD": 0.09, "EUR": 0.086, "DKK": 0.64}}
    
    # Check if the selected target currency is among the 5 exchange rates. 
    if target_currency not in exchange_rates[source_currency]: return False, "Den angivna målvalutan stöds inte för valutaväxling."
    
    # Calculate the equivalent value in the target currency from the amount to be exchanged. 
    exchanged_amount = float(amount) * exchange_rates[source_currency][target_currency]
    return exchanged_amount, 0



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
    account_list = [0]
    # Get username
    while True:
        # Displaying the text on screen
        os.system('cls')
        print("Bankomat \n")

        username = str(input("Användarnamn: ") or "0") # Getting username from user
        if username == "0": return
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
            account_list, error = check_password(user_id, password)
            
            if error == 0: break
            else:
                print(error)
                input("Tryck enter för att fortsätta")
                if account_list == None: return
        

        while True:
            os.system('cls')
            print("Bankomat \n")
            
            print(f"Inloggad som: {username}")
            questions = [
                inquirer.List('konto', message="Logga in som", choices=['Befintligt konto', 'Nytt konto', 'Logga ut', 'Ta bort konto'], ), ] # Get the alternatives of what the user wants to do
            answers = inquirer.prompt(questions)  # Getting user's choice

            if answers["konto"] == 'Befintligt konto':
                os.system('cls')
                print("Bankomat \n")
            
                print(f"Inloggad som: {username}")
                if not account_list: continue
                questions = [inquirer.List('account_num', message="Välj konto", choices=account_list, ), ] # Select what account you whant to log in to
                answers = inquirer.prompt(questions)  # Getting user's choice
                account_num = answers["account_num"]
                if account_num:
                    # Logged in on the account
                    while True:
                        accounts_data = read_file(Path_Accounts)
                        
                        os.system('cls')
                        print("Bankomat \n")

                        print(f"Inloggad på: {account_num}: {accounts_data[str(account_num)][0]['name']}\nSaldo: {accounts_data[str(account_num)][0]['balance'][0]} in {accounts_data[str(account_num)][0]['currency']}")
                        questions = [ inquirer.List('account', message="Välj interaktion", choices=['Genomför transaktion', 'Saldo historik', 'Transaktions historik', 'Byt konto'], ), ]
                        answers = inquirer.prompt(questions)  # Getting user's choice

                        if answers["account"] == 'Genomför transaktion':
                            Account_Transaction(account_num)  # Performing a transaction
                        elif answers["account"] == 'Saldo historik':
                            balance_history(account_num)  # Viewing balance history
                        elif answers["account"] == 'Transaktions historik':
                            transaction_history(account_num)  # Viewing transaction history
                        elif answers["account"] == 'Byt konto':
                            break  # Swaping account out
            elif answers["konto"] == 'Nytt konto':
                # Create a new bank account 
                os.system('cls')
                print("Bankomat \n")
                
                print(f"Inloggad som: {username}")
                questions = [inquirer.List('konto_typ',message="Välj konto typ", choices=['Sparkonto', 'Betalkonto'],),] # Select type of account
                konto = inquirer.prompt(questions)  # Getting user's choice
                
                questions = [inquirer.List('konto_valuta', message="Kontots valuta", choices=['SEK', 'USD', 'EUR', 'DKK', "NOK"],),] # Select type of currency for account
                konto2 = inquirer.prompt(questions)  # Getting user's choice
                name = input("Skiv ett namn för kontot: ")

                account_list = new_account(user_id,konto["konto_typ"],konto2["konto_valuta"], name) # Create a new account

            elif answers["konto"] == 'Ta bort konto':
                if not account_list: continue
                os.system('cls')
                print("Bankomat \n")

                questions = [inquirer.List('delete_account_num', message="Välj konto att ta bort", choices=account_list, ), ] # Select wht account you whant to delete
                answers = inquirer.prompt(questions)  # Getting user's choice
                password = getpass("Lösenord: " + u'\U0001f512')
                account_list, error = delete_account(account_num= answers["delete_account_num"], password= password)
                
                if error != 0:
                    print(error)
                    time.sleep(2)
                     
            elif answers["konto"] == 'Logga ut':
                break  # Logging out
    return

def Account_Transaction(account_num):
    """
    Function to perform a transaction.
    """
    # Read the Account file
    accounts_data = read_file(Path_Accounts)
    
    for val in accounts_data[str(account_num)]:
        account_currency = val["currency"]
        account_balance = val["balance"]
        
    while True:
        os.system('cls')  # Clearing the screen
        print("Bankomat \n")

        # Printing current balance
        print("Nuvarande belopp:", round(account_balance[0],2), " "+ account_currency)  
        
        # Prompting user to choose a transaction type
        questions = [ inquirer.List('transaction', message="Välj interaktion", choices=["Uttag", "Insättning", "Kontoöverföring", "Tillbaka"], ), ]
        answers = inquirer.prompt(questions)  # Getting user's choice
        
        # Handling user's transaction choice
        os.system('cls')  # Clearing the screen
        print("Bankomat \n")

        if answers["transaction"] == 'Tillbaka': 
            break  # Going back to the previous menu
        
        text1 = ("Skriv in " + answers["transaction"] + " beloppet \n")  # Prompting for transaction amount
        text2 = ("Göra en kort anteckning till " + answers["transaction"] + "\n")  # Prompting for a note
        status = True
        error = ""

        try:
            value = float(input(text1))  # Getting transaction amount and negating it for withdrawals
        except:
            value = 0
            status = False
            error = "Strängar kan inte hanteras"
        note = input(text2)  # Getting transaction note

        if not error:
            if answers["transaction"] == "Kontoöverföring":
                t_account_num = input("Skriv in kontonummer att skicka till: ")
                # Doing transactions between accounts
                status, error = account_transfer(account_num,t_account_num,value,note)
            else:
                # Prompting user to choose a transaction type
                questions = [ inquirer.List('currency', message=f"Vilken valuta ska {answers['transaction']} vara i?", choices=["SEK", "EUR", "USD", "NOK", "DKK"], ), ]
                currency = inquirer.prompt(questions)  # Getting user's choice
                # Doing personal transactions, to and from user 
                status, error = transaction(account_num, answers["transaction"], value, note, currency["currency"])
            
        if status: break
        print(error)
        time.sleep(3)

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
                    print("Lösenorden matchar inte, skriv in ditt lösenord igen")
                    time.sleep(2)
        status, error = create_user(username,password)
        if status: break
        print(error)
        time.sleep
    return

if __name__ == '__main__': # Starts the application
    interest() # If it is the first month calculate the given intrest for all accounts
    start()  # Starting the banking system
