from random import randint

import sqlite3

conn = sqlite3.connect('card.s3db')   #coonect to database

cur = conn.cursor()   # create a curser

# create_database = "CREATE DATABASE CARD"
# cur.execute(create_database)
# cur.execute("CREATE TABLE card(id INTEGER,number TEXT,pin TEXT,balance INTEGER DEFAULT 0);")
cur.execute('''CREATE TABLE IF NOT EXISTS card (  
    id INTEGER PRIMARY KEY,
    number TEXT NOT NULL UNIQUE,
    pin TEXT NOT NULL UNIQUE,
    balance INTEGER DEFAULT 0
    );''')

#commit your command
conn.commit()





account_numbers = []
account = ()
pin = ()
cus_number = 0
customer = ()
customer_balance = 0
checksum = ()
full_account = ()


class Customers:
   # customers = []

    def __init__(self ,account_number, pin_number, balance):
        #self.customers.append(self)
        self.account_number = account_number
        self.pin_number = pin_number
        self.balance = balance
        self.cus_number= cus_number
        insertion = "INSERT INTO card(number, pin, balance) VALUES (:account_number, :pin_number , '0' )"
        cur.execute(insertion,{'account_number':account_number,'pin_number':pin_number})
        conn.commit()

def entry_menu():
    # choices = ["0", "1", "2"]
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    choice = input()
    if choice == "0":
        stop()
    elif choice == "1":
        create_account()
    elif choice == "2":
        log_in()


def account_menu():
    choice = ()
    while choice != "0":
        print("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")
        choice = input()
        if choice == "1":
            print("\nBalance: " + str(get_balance(input_number)) + "\n")
        elif choice =="2":
            add_income(int(input("Enter income:")),input_number)
        elif choice =="3":
            transfer_to=input('''
Transfer
Enter card number:''')

            if(Does_exist(transfer_to) and checkluhn(transfer_to)):
                amount = int(input("Enter how much money you want to transfer:"))
                if(amount<=get_balance(input_number)):
                    add_income(amount*-1,input_number)
                    add_income(amount,transfer_to)
                    print("Success!")
                else:
                    print("Not enough money!")
            elif(not checkluhn(transfer_to)):
                print("Probably you made mistake in card number. Please try again!")
                account_menu()
            else:
                print("Such a card does not exist.")
                account_menu()
        elif choice =="4":
            delete_account()
            print("The account has been closed!")
            entry_menu()
        elif choice == "5":
            print("\nYou have successfully logged out!\n")
            entry_menu()
        elif choice =="0":
            stop()
        else:
            print("Carefully Enter Correct value !! ")
            account_menu()
def Does_exist(cardnumber):
    Query = """
        SELECT number
        FROM card
        WHERE number = :var1
    """
    cur.execute(Query,{'var1':cardnumber})
    reply = cur.fetchone()
    return True if reply!=None else False

def delete_account():
    Query = """DELETE FROM card 
               WHERE number = :input_number
            ;
            """
    cur.execute(Query,{'input_number':input_number})
    conn.commit()
def add_income(Income,Card_Number):
    Query = """
            UPDATE card 
            SET balance = :variable
            WHERE number = :input_number
            ;
    """
    cur.execute(Query,{'input_number':Card_Number,'variable':Income+get_balance(Card_Number)})
    #idhar dikkat hai get balance me argument optional dena pdega nhi toh logged in ka addincore trasnfer to me add hoare
    conn.commit()

def get_balance(argument):
    Query= """
    SELECT balance 
    FROM card
    WHERE number = :var1
    ;"""
    cur.execute(Query,{'var1':argument})
    ans = cur.fetchone()
    return ans[0]

def create_account():
    global cus_number
    global account
    global customer
    account = ()
    generate_account()
    print("Your card has been created")
    print("Your card number:")
    print(str(full_account))
    generate_pin()
    print("Your card PIN:")
    print(str(pin) + "\n")
    cus_number += 1
    customer = Customers(str(full_account), str(pin), 0)

    entry_menu()

def generate_account():
    global account
    global full_account
    global checksum
    random_list = []
    account = ()
    i = 1
    while i <= 9:
        n = randint(0, 9)
        random_list.append(str(n))
        i += 1
    account = "".join(random_list)
    if account not in account_numbers:
        checksum = randint(1, 9)
        global full_account
        full_account = "400000" + str(account) + str(checksum)
        if checkluhn(full_account) :
            account_numbers.append(account)
        else:
            generate_account()
    else:
        generate_account()

def checkluhn(full_account):

    ndigits = len(full_account)
    nsum = 0
    issecond = True
    for i in range(0,ndigits):
        #d = ord(full_account[i]) - ord('0')
        d = int(full_account[i])
        if issecond:
            d = d * 2
            if d >=9 :
                d-=9
        nsum += d

        issecond = not issecond
    if nsum % 10 == 0:
        return True
    else:
        return False

def generate_pin():
    global pin
    random_list = []
    pin = ()
    i = 1
    while i <= 4:
        n = randint(0, 9)
        random_list.append(str(n))
        i += 1
    pin = "".join(random_list)

def log_in():
    global customer_balance
    print("\nEnter your card number:")
    global input_number
    input_number = input()
    print("Enter your PIN:")
    input_pin = input()
    fetch = """SELECT 
        pin,
        balance
    FROM 
        card
    WHERE
        number = :supplied_number
        ;
        """

    global aya
    cur.execute(fetch,{'supplied_number':input_number})
    aya = cur.fetchone()

    conn.commit()

    if aya != None and aya[0] ==  input_pin :
        print("\nYou have successfully logged in!\n")
        customer_balance = aya[1]
        account_menu()
    else:
        print("\nWrong card number or PIN!\n")
    entry_menu()

def stop():
    print("\nBye!")
    exit()


entry_menu()
conn.close()
