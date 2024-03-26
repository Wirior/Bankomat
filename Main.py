import os
import time
import json
import inquirer
from datetime import date

from email_validator import validate_email, EmailNotValidError

import numpy as np

today = date.today()
Path_Users = "C:/Users/Dell/Documents/Python Scripts/Bankomat/Users.json"
Path_Passwords = "C:/Users/Dell/Documents/Python Scripts/Bankomat/Passwords.json"
Path_Accounts = "C:/Users/Dell/Documents/Python Scripts/Bankomat/Accounts.json"

def start():
    os.system('cls')
    print("Bankomat \n")

    while True:
        #inquirer input from the terminal
        questions = [
        inquirer.List('interaktion',
                    message="Välj interaktion",
                    choices=['Logga in', 'Ny användare', 'Debug', 'Avsluta'],
                ),]
        answers = inquirer.prompt(questions)
        
        if answers["interaktion"] == 'Logga in': # Start signing in process
            Log_in()

        elif answers["interaktion"] == 'Ny användare': # Create a new user
            New_user()

        elif answers["interaktion"] == 'Debug': # test 
            print("#############")

        elif answers["interaktion"] == 'Avsluta': break # exit the program
    return


def Log_in():
    user_id, username = Username() # from the username function get the username and user_id
    
    account_num = Password(user_id= user_id, username= username) # Get the account nr from the password function
    if account_num:
        Account(account_num=account_num)
    
    return

def Username():
    # Read the Username data
    u = open(Path_Users, "r")
    user_data = json.load(u)
    u.close

    trys = 0
    while True:
        # Displaying the text on screen
        os.system('cls')
        print("Bankomat \n")
        
        username = input("Username: ")
        trys += 1

        # Locating the username in the .json file
        for i in user_data['master']:
            if username == i["user"]:
                user_id = i["user_id"]
                return user_id, username # returning the user_id and username 
            if trys >= 4:
                print("Too many unsucessfull trys in a row, redirecting you to the mainpage.")
                time.sleep(1.5)
                start()

        print("The username you submitted does not exist")
        time.sleep(1.5)


def Password(user_id, username):
    # Read the pasword file 
    p = open(Path_Passwords,"r")
    Passwords_data = json.load(p)
    p.close

    # Set Variables
    trys = 0
    user_psw = 0

    #reading user specific data from the stored .json file 
    for count, val in enumerate(Passwords_data["password"]):
        if user_id == val["user_id"]:
            user_psw = val["psw"]
            trys = val["trys"]
            break
    
    # Loop the inner function to check password
    while True:
        #displaying the text on the screen
        os.system('cls')
        print("Bankomat \n")
        print("Username:",username)
        
        # Check if the currect amount of trys exeeds the limit 4 tries
        if trys <= 0:
            print("You have locked your account, please contact support to unlock your account.")
            a = input("Press enter to go back to start...") # Press enter to go continue
            return
        
        password = input("Password: ") 
        
        # Chech if input password is the same as the stored password
        if password == user_psw:
            account_num=val["account"]
            return account_num
        
        # If the password is incorrect
        else:
            trys -= 1 # increment the number of tries by the user
            print("The password was incorrect")
            print("You have ", trys, " left")
            time.sleep(2.5)
            Passwords_data["password"][count]["trys"] = trys # rewrite the password data with the new number of tries 
            newData = json.dumps(Passwords_data, indent=4)

            # open the Passwords.json file
            with open(Path_Passwords, 'w') as file:
                file.write(newData) # Write over the current Passwords.json file with the amount pin tries


def Account(account_num):
    os.system('cls')
    print("Bankomat \n")

    while True:
        #inquirer input from the terminal
        questions = [
        inquirer.List('account',
                    message="Välj interaktion",
                    choices=['Genomför transaktion', 'Saldo historik', 'Transaktions historik', 'Logga ut'],
                ),]
        answers = inquirer.prompt(questions) # add the answeres to the 

        if answers["account"] == 'Genomför transaktion':
            Account_Transaction(account_num) # do transactions

        elif answers["account"] == 'Saldo historik':
            Account_Balance_History(account_num) # plot a graph for the account balance

        elif answers["account"] == 'Transaktions historik':
            Account_Transaction_History(account_num) # Get a list of all transactions

        elif answers["account"] == 'Logga ut': break # Go back
    return

def Account_Transaction(account_num):
    # Read the pasword file 
    a = open(Path_Accounts,"r",encoding='utf-8')
    Accounts_data = json.load(a)
    a.close

    for val in Accounts_data[str(account_num)]: # get the saved values from the Account.json file
        account_balance = val["balance"]
        account_transaction = val["transaction"]
        account_date = val["date"]
        account_note = val["note"]

    while True:
        os.system('cls')
        print("Bankomat \n")
    
        print("Nuvarande belopp:",account_balance[0], " kr")
        #inquirer input from the terminal
        questions = [
            inquirer.List('transaction',message="Välj interaktion",choices=["Uttag", "Insättning","Tillbaka"],),
        ]
        answers = inquirer.prompt(questions)

        # = = = = = = = = = = = = = = = = = = = =
        os.system('cls')
        print("Bankomat \n")

        if answers["transaction"] == 'Tillbaka': break # go back
        
        try:
            text1 = ("Skriv in " + answers["transaction"] + " beloppet \n")
            text2 = ("Passa på att göra en kort anteckning till " + answers["transaction"]  +"\n")
            value = abs(float(input(text1)))
            
            if answers["transaction"] == 'Uttag': value = value*-1 # changes the value to subract from the current balance         
            
            if account_balance[0]+value >=0:
                note = input(text2)
                
                #Add the new transaction to the first element of the list from the data
                account_balance.insert(0, account_balance[0]+value)
                account_transaction.insert(0, answers["transaction"])
                account_date.insert(0, str(today))
                account_note.insert(0, note)

                newData = json.dumps(Accounts_data, indent=4)
                with open(Path_Accounts, 'w', encoding='utf-8') as file: file.write(newData) # open the Passwords.json file and write over the current Accounts.json file
                
                print("Genomför transaktion...")
                time.sleep(1.5)
                
            else:
                print("Fel: För litet belopp på kontot") # "exempton" if the balance will go below 0 
                time.sleep(1.5)
                continue
        except:
            print("Fel: Incorrekta värden") # exeption if the input'ed value is not float
            time.sleep(1.5) 
        
    return
   
def Account_Balance_History(account_num):
    # Read the pasword file 
    a = open(Path_Accounts,"r",encoding='utf-8')
    Accounts_data = json.load(a)
    a.close

    for val in Accounts_data[str(account_num)]:
        account_balance = val["balance"]
        account_transaction = val["transaction"]
        account_date = val["date"]
        account_note = val["note"]

    while True:
        break
    return

def Account_Transaction_History(account_num):
# Read the pasword file 
    a = open(Path_Accounts,"r",encoding='utf-8')
    Accounts_data = json.load(a)
    a.close

    for val in Accounts_data[str(account_num)]:
        account_balance = val["balance"]
        account_transaction = val["transaction"]
        account_date = val["date"]
        account_note = val["note"]

    while True:
        break
    return



def New_user():
    os.system('cls')
    print("Bankomat \n")

    usr = input("Skriv in din mejladress \n")
    if check(usr): # check emailadress
        print(True)

    return

def check(email):
    try:
        v = validate_email(email) #uses the imported function to validate email 
        email = v["email"]  # replace with normalized form
        print(email)
        return True
    except EmailNotValidError as e:
        print(str(e))
        return False # returning false, and the exeptionflag that the email is not valid

def Debug():
    return


start()