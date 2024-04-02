import os  # Importing the os module to interact with the operating system
import time  # Importing the time module for time-related functions
import json  # Importing the json module for JSON file operations
import inquirer  # Importing the inquirer module for interactive user prompts
from datetime import date  # Importing the date class from the datetime module
from getpass import getpass # Importing the hidden password module for user input
import random # Importing random function for slump actions
import matplotlib.pyplot as plt # importing pylot module to plot grapths

from email_validator import validate_email, EmailNotValidError  # Importing email validation functions

import numpy as np  # Importing numpy for numerical operations

today = date.today()  # Getting today's date
Path_Users = "C:/Users/Dell/Documents/Python Scripts/Bankomat/Users.json"  # Path to the users JSON file
Path_Passwords = "C:/Users/Dell/Documents/Python Scripts/Bankomat/Passwords.json"  # Path to the passwords JSON file
Path_Accounts = "C:/Users/Dell/Documents/Python Scripts/Bankomat/Accounts.json"  # Path to the accounts JSON file


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
                          choices=['Logga in', 'Ny användare', 'Debug', 'Avsluta'],
                          ),
        ]
        answers = inquirer.prompt(questions)  # Getting user's choice
        
        if answers["interaktion"] == 'Logga in':
            Log_in()  # Calling the Log_in function for user login
        elif answers["interaktion"] == 'Ny användare':
            New_user()  # Calling the New_user function for creating a new user
        elif answers["interaktion"] == 'Debug':
            Debug() # Calling the Debug function
        elif answers["interaktion"] == 'Avsluta':
            break  # Exiting the program


def Log_in():
    """
    Function for user login.
    """
    user_id, username = Username()  # Getting user ID and username
    if user_id and username:
        account_num = Password(user_id=user_id, username=username)  # Getting account number
        if account_num: Account(account_num=account_num)  # Accessing user's account
    
    return

def Username():
    """
    Function to verify the username.
    """
    # Read the Username data
    u = open(Path_Users, "r")
    user_data = json.load(u)
    u.close

    trys = 0  # Initializing attempt counter
    while True:
        # Displaying the text on screen
        os.system('cls')
        print("Bankomat \n")

        username = input("Användarnamn: ")  # Getting username from user
        trys += 1  # Incrementing attempt counter

        # Locating the username in the .json file
        for i in user_data['master']:
            if username == i["user"]:
                user_id = i["user_id"]  # Getting user ID
                return user_id, username  # Returning user ID and username
            if trys >= 4:
                print("För många konsekutiva misslyckade försök, omdirigerar dig till huvudsidan.")
                time.sleep(1.5)
                return 0,0 # Redirecting to the main page if too many unsuccessful attempts

        print("Användarnamnen som har skrivits in existerar inte")
        time.sleep(1.5)


def Password(user_id, username):
    """
    Function to verify the password.
    """
    # Read the pasword file
    p = open(Path_Passwords, "r")
    Passwords_data = json.load(p)
    p.close

    # Set Variables
    trys = 0
    user_psw = 0

    # Reading user specific data from the stored .json file
    for count, val in enumerate(Passwords_data["password"]):
        if user_id == val["user_id"]:
            user_psw = val["psw"]  # Getting user's password
            trys = val["trys"]  # Getting number of tries
            break

    # Loop the inner function to check password
    while True:
        # Displaying the text on the screen
        os.system('cls')
        print("Bankomat \n")
        print("Användarnamn:", username)

        # Check if the current number of tries exceeds the limit (4 tries)
        if trys <= 0:
            print("Du har låst ditt konto, var vänlig och kontakta kundtjänst för att låsa upp ditt kont")
            a = input("Tryck enter för att gå tillbaka till start...")  # Press enter to continue
            return
        
        password = getpass("Lösenord: " + u'\U0001f512')  # Getting password from user

        # Check if input password is the same as the stored password
        if password == user_psw:
            account_num = val["account"]  # Getting account number
            return account_num

        # If the password is incorrect
        else:
            trys -= 1  # Decrementing the number of tries
            print("Felaktigt lösenord")
            print("Du har ", trys, " försök kvar")
            time.sleep(2.5)
            Passwords_data["password"][count]["trys"] = trys  # Updating the number of tries in the data
            newData = json.dumps(Passwords_data, indent=4)

            # Opening the Passwords.json file and writing updated data
            with open(Path_Passwords, 'w') as file:
                file.write(newData)  # Writing over the current Passwords.json file with the updated data


def Account(account_num):
    """
    Function to manage user's account.
    """
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
            Account_Balance_History(account_num)  # Viewing balance history
        elif answers["account"] == 'Transaktions historik':
            Account_Transaction_History(account_num)  # Viewing transaction history
        elif answers["account"] == 'Logga ut':
            break  # Logging out


def Account_Transaction(account_num):
    """
    Function to perform a transaction.
    """
    # Read the Account file
    with open(Path_Accounts, "r", encoding='utf-8') as a: 
        Accounts_data = json.load(a)  # Loading account data from the JSON file

    # Extracting account details from the loaded data
    for val in Accounts_data[str(account_num)]:
        account_balance = val["balance"]
        account_transaction = val["transaction"]
        account_date = val["date"]
        account_note = val["note"]

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
        print(answers['transaction'])

        # Handling user's transaction choice
        os.system('cls')  # Clearing the screen
        print("Bankomat \n")

        if answers["transaction"] == 'Tillbaka': 
            break  # Going back to the previous menu

        try:
            text1 = ("Skriv in " + answers["transaction"] + " beloppet \n")  # Prompting for transaction amount
            text2 = ("Göra en kort anteckning till " + answers["transaction"] + "\n")  # Prompting for a note
            value = -1*abs(float(input(text1)))  # Getting transaction amount and negating it for withdrawals

            if answers["transaction"] == 'Insättning': 
                value = value * -1  # Positive the amount for deposit

            if account_balance[0] + value >= 0:
                # If the user wants to do a transaction between accounts. 
                if answers["transaction"] == "Kontoöverföring":
                    t_account_num = input("Skriv in kontonummer att skicka till: ")
                    trigger = False
                    for val in Accounts_data: # Itterating through Accounts.json 
                        if (val == t_account_num) and not(val == str(account_num)): trigger = True # Trying to find the inputed account number
                            
                    if not(trigger):
                        print("Kontonummret existerar inte, prova med ett annat.")
                        time.sleep(2)
                        break
                
                note = input(text2)  # Getting transaction note
                
                # Adding the new transaction data to the account
                account_balance.insert(0, account_balance[0] + value)
                account_transaction.insert(0, answers["transaction"])
                account_date.insert(0, str(today))
                account_note.insert(0, note)

                if trigger: # Check if it is a transaction between accounts
                    for val in Accounts_data[str(t_account_num)]: # Read the new account
                        t_account_balance = val["balance"]
                        t_account_transaction = val["transaction"]
                        t_account_date = val["date"]
                        t_account_note = val["note"]
                    
                    # Adding the new transaction data to the account
                    t_account_balance.insert(0, t_account_balance[0] + (-1*value))
                    t_account_transaction.insert(0, answers["transaction"])
                    t_account_date.insert(0, str(today))
                    t_account_note.insert(0, note)

                newData = json.dumps(Accounts_data, indent=4)  # Serializing updated data
                
                # Opening the Accounts.json file and writing updated data
                with open(Path_Accounts, 'w', encoding='utf-8') as file:
                    file.write(newData)  # Writing over the current Accounts.json file with the updated data

                print("Genomför transaktion...")  # Printing transaction success message
                time.sleep(1.5)

            else:
                print("Fel: För litet belopp på kontot")  # Printing error message for insufficient funds
                time.sleep(1.5)
                continue
        except:
            print("Fel: Incorrekta värden")  # Printing error message for incorrect values
            time.sleep(1.5)

    return

def Account_Balance_History(account_num):
    """
    Function to view transaction history.
    """
    # Read the pasword file
    with open(Path_Accounts, "r", encoding='utf-8') as a: Accounts_data = json.load(a)
    # Itterate though the account and save the balance 
    for val in Accounts_data[str(account_num)]:
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

    plt.plot(dates, balance)
    plt.show()

    return

def Account_Transaction_History(account_num):
    """
    Function to view balance history.
    """
    # Read the pasword file
    with open(Path_Accounts, "r", encoding='utf-8') as a: Accounts_data = json.load(a)

    # Print the information in the desired format
    print("{0:<20} | {1:<18} | {2:<16} | {3:<30}\n"
              .format("Saldo", "Transaktion", "Datum", "Anteckning"))
    # Itterates through the accounts json data, and prints out each element in order.
    for item in range(len(Accounts_data[str(account_num)][0]['balance'])):
        balance = Accounts_data[str(account_num)][0]['balance'][item]
        transaction = Accounts_data[str(account_num)][0]['transaction'][item]
        date = Accounts_data[str(account_num)][0]['date'][item]
        note = Accounts_data[str(account_num)][0]['note'][item]
        
        print("{0:<20} | {1:<18} | {2:<16} | {3:<30}"
              .format(balance, transaction, date, note, item))
        
        if item >= 30: # Check if the item is equal to or larger than 30, if so: stop printing
            print("Kunde endast ladda in de senaste 30 transaktionerna")
            break
    input("\nTryck enter för att gå tillbaka...")
    return


def New_user():
    """
    Function to create a new user.
    """
    # Read the Username data
    with open(Path_Users, "r") as u: # Opening the Users.json file in read mode
        user_data = json.load(u) # Loading user data from the JSON file
    
    # Read the pasword file
    with open(Path_Passwords, "r") as p: Passwords_data = json.load(p)

    # Read the Account file
    with open(Path_Accounts, "r", encoding='utf-8') as a: Accounts_data = json.load(a)
    
    username = ""  # Initializing username variable
    while True:
        os.system('cls')  # Clearing the screen
        print("Bankomat \n")

        if username == "":
            usr = input("Skriv in din mejladress: ")  # Prompting for email address
            username = check(usr)  # Validating the email address
        
        # Locating the username in the .json file
        for i in user_data['master']:
            if username == i["user"]:
                print("Användarnamnet existerar redan, vänligen skriv in ett nytt användarnamn.\n")
                input("Tryck enter för att fortsätta...")
                username = ""  # Resetting username if it already exists

        if username != "":
            psw = getpass("Lösenord: " + u'\U0001f512')  # Prompting for password
            print("Vänligen upprepa lösenordet")
            c_psw = getpass("Lösenord: " + u'\U0001f512')  # Prompting for password confirmation

            # Validating passwords
            if psw == "" or c_psw == "":
                return
            elif psw == c_psw:
                break
            else:
                print("Lösenorden matchar inte skriv in ditt lösenord igen")
                time.sleep(2)

    # Creating user_id
    while True:
        user_id = random.randrange(100000, 999999)  # Generating a random user ID
        trigger = False
        for i in user_data['master']:
            if user_id == i["user_id"]:
                trigger = True
        if not trigger:
            break

    # Creating account id
    while True:
        account = random.randrange(100000, 999999)  # Generating a random account ID
        trigger = False
        for i in Passwords_data['password']:
            if account == i["account"]:
                trigger = True
        if not trigger:
            break

    # Appending new user data
    user_data["master"].append({"user":username,"user_id":user_id})
    # Opening the Users.json file and writing the new user data
    with open(Path_Users, 'w') as file:
        json.dump(user_data, file, indent=2)

    # Appending new password data
    Passwords_data["password"].append({"user_id":user_id,"psw":psw,"trys":4,"account":account})
    # Opening the Passwords.json file and writing the new user data
    with open(Path_Passwords, 'w') as file:
        json.dump(Passwords_data, file, indent=2)

    # Appening new Account data
    new_bank_data = [{
        "balance": [0],
        "transaction": [""],
        "date": [str(today)],
        "note": ["Konto skapades"]
    }]
    Accounts_data[account] = new_bank_data
    # Opening the Accounts.json file and writing the new user data
    with open(Path_Accounts, 'w') as file:
        json.dump(Accounts_data, file, indent=3)
    
    print("Skapar ny användare...")
    time.sleep(2)
    return


def check(email):
    """
    Function to validate email address.
    """
    try:
        # Check that the email address is valid. Turn on check_deliverability
        emailinfo = validate_email(email, check_deliverability=False)
        email = emailinfo.normalized
        return email
    except EmailNotValidError as e:
        print(str(e)) # Printing error message for invalid email
        time.sleep(2)
        return ""  # Returning False indicating the email is not valid


def Debug():
    """
    Placeholder function for debugging.
    """
    return

start()  # Starting the banking system

