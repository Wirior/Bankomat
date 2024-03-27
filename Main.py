import os  # Importing the os module to interact with the operating system
import time  # Importing the time module for time-related functions
import json  # Importing the json module for JSON file operations
import inquirer  # Importing the inquirer module for interactive user prompts
from datetime import date  # Importing the date class from the datetime module

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
    
    if user_id and username: account_num = Password(user_id=user_id, username=username)  # Getting account number
    
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

        username = input("Username: ")  # Getting username from user
        trys += 1  # Incrementing attempt counter

        # Locating the username in the .json file
        for i in user_data['master']:
            if username == i["user"]:
                user_id = i["user_id"]  # Getting user ID
                return user_id, username  # Returning user ID and username
            if trys >= 4:
                print("Too many unsucessfull trys in a row, redirecting you to the mainpage.")
                time.sleep(1.5)
                return 0,0 # Redirecting to the main page if too many unsuccessful attempts

        print("The username you submitted does not exist")
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
        print("Username:", username)

        # Check if the current number of tries exceeds the limit (4 tries)
        if trys <= 0:
            print("You have locked your account, please contact support to unlock your account.")
            a = input("Press enter to go back to start...")  # Press enter to continue
            return

        password = input("Password: ")  # Getting password from user

        # Check if input password is the same as the stored password
        if password == user_psw:
            account_num = val["account"]  # Getting account number
            return account_num

        # If the password is incorrect
        else:
            trys -= 1  # Decrementing the number of tries
            print("The password was incorrect")
            print("You have ", trys, " left")
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
    os.system('cls')
    print("Bankomat \n")

    while True:
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
    # Read the pasword file
    a = open(Path_Accounts, "r", encoding='utf-8')
    Accounts_data = json.load(a)
    a.close

    for val in Accounts_data[str(account_num)]:
        account_balance = val["balance"]
        account_transaction = val["transaction"]
        account_date = val["date"]
        account_note = val["note"]

    while True:
        os.system('cls')
        print("Bankomat \n")

        print("Nuvarande belopp:", account_balance[0], " kr")  # Printing current balance
        questions = [
            inquirer.List('transaction', message="Välj interaktion", choices=["Uttag", "Insättning", "Tillbaka"], ),
        ]
        answers = inquirer.prompt(questions)  # Getting user's choice
        print(answers['transaction'])

        # Handling user's transaction choice
        os.system('cls')
        print("Bankomat \n")

        if answers["transaction"] == 'Tillbaka': break  # Going back to the previous menu

        try:
            text1 = ("Skriv in " + answers["transaction"] + " beloppet \n")  # Prompting for transaction amount
            text2 = ("Passa på att göra en kort anteckning till " + answers["transaction"] + "\n")  # Prompting for a note
            value = abs(float(input(text1)))  # Getting transaction amount

            if answers["transaction"] == 'Uttag': value = value * -1  # Negating the amount for withdrawals

            if account_balance[0] + value >= 0:
                note = input(text2)  # Getting transaction note
                # Adding the new transaction data to the account
                account_balance.insert(0, account_balance[0] + value)
                account_transaction.insert(0, answers["transaction"])
                account_date.insert(0, str(today))
                account_note.insert(0, note)

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
    Function to view balance history.
    """
    # Read the pasword file
    a = open(Path_Accounts, "r", encoding='utf-8')
    Accounts_data = json.load(a)
    a.close

    for val in Accounts_data[str(account_num)]:
        account_balance = val["balance"]
        account_transaction = val["transaction"]
        account_date = val["date"]
        account_note = val["note"]

    while True:
        break  # Placeholder for balance history functionality
    return


def Account_Transaction_History(account_num):
    """
    Function to view transaction history.
    """
    # Read the pasword file
    a = open(Path_Accounts, "r", encoding='utf-8')
    Accounts_data = json.load(a)
    a.close

    for val in Accounts_data[str(account_num)]:
        account_balance = val["balance"]
        account_transaction = val["transaction"]
        account_date = val["date"]
        account_note = val["note"]

    while True:
        break  # Placeholder for transaction history functionality
    return


def New_user():
    """
    Function to create a new user.
    """
    os.system('cls')
    print("Bankomat \n")

    usr = input("Skriv in din mejladress \n")  # Prompting for email address
    if check(usr):
        print(True)

    return


def check(email):
    """
    Function to validate email address.
    """
    try:
        v = validate_email(email)  # Validating email
        email = v["email"]  # Normalizing email
        return True
    except EmailNotValidError as e:
        print(str(e))  # Printing error message for invalid email
        return False  # Returning False indicating the email is not valid


def Debug():
    """
    Placeholder function for debugging.
    """
    return


start()  # Starting the banking system

