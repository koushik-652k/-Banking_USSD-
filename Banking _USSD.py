# Mobile banking ( USSD (Unstructured Supplementary Service Data) interface )
import json

#        = {user_name : [passwd, bal, W_no, d_no, {transactions}]}
user_lst = {}
user_auth_status = False
user_inst = ""
cur_user = ""

def save_data():
    with open(r"Python\final\users.json", "w") as x:
        json.dump(user_lst, x)
    
def load_data():
    global user_lst
    try:
        with open(r"Python\final\users.json", "r") as x:
            user_lst = json.load(x)
    except:
        print("problem loading source !")
        user_lst = {"root": ["0000", 1000, 0, 0, {}]}  # Default data
        save_data()  

load_data()
class authentication():
    def user_auth(self):
        global user_auth_status, user_inst, cur_user
        user_inst = input("\nEnter user name : ")
        if user_inst in user_lst:
            cur_user = user_inst
            user_passwd = input("Enter password : ")
            if user_passwd == user_lst[cur_user][0]:
                print("Login successful !!!")
                user_auth_status = True
                save_data()
                return user_auth_status
            else:
                print("Password Dosent match !\n Retry again !!!")
        else:
            self.add_user()

    def add_user(self):
        y_n = input("Do you want to registed as new user (y/n) : ")
        if y_n.lower() == "y":
            new_user = input("Enter unique user name : ")
            if len(new_user) >= 4:
                new_user_passwd = input("Enter a password : ")
                if len(new_user_passwd) >= 4:
                    user_lst[new_user] = [new_user_passwd, 0, 0, 0, {}]
                    print("user added successfully")
                    y_n_ = input("dou you want to login (y/n) : ")
                    if y_n_.lower() == "y":
                        self.user_auth()
                    else:
                        print("thankyou for signing in !")
        else:
            print("Thankyou for using !!!")


        
tar_0 = authentication()
tar_0.user_auth()

class Balence():
    def balence_check(self):
        global user_lst, cur_user
        print("\nBalence : ",user_lst[cur_user][1])

class Withdrawal():
    def withdraw(self, x, t="C"):
        global user_lst, cur_user
        if (user_lst[cur_user][1] >= x):
            user_lst[cur_user][4]["w"+t+" - "+str(user_lst[cur_user][2]+1)] = x 
            user_lst[cur_user][2] += 1
            user_lst[cur_user][1] -= x
            print("withdrwal successful !")
            save_data()
        else:
            print("insufficient funds !")

class Banking(Balence, Withdrawal, authentication):
    def options(self):
        global cur_user
        actions = {
            "1": self.withdraw,
            "2": self.deposit,
            "3": self.balence_check,
            "4": self.trans,
            "5": self.loan_calc,
            "6": self.user_auth,
            "7": self.passwd_change
            }
        while True:
            print("\nuser : ",cur_user,"\n1. Withdraw\n2. Deposit\n3. Balence\n4. Transactions\n5. Loan Calc\n6. switch login"
            "\n7. Change password\n0. Exit")
            opt = input("select : ")
            if opt == "":
                print("Please select an option")
            elif int(opt) == 0:
                print("Thankyou for using our servieces !\n")
                exit()
            elif opt in actions:
                actions[opt]() 
            else:
                print("Invalid option, try again.")

            x = input("Press Enter to continue...")  

    def withdraw(self):
        print("\n1. Current account\n2. Savings account")
        sor = int(input("Enter : "))
        amt = int(input("Enter withdrawl amount : "))
        if sor == 2:
            cur_ac_lmt = 5000
            if (amt < cur_ac_lmt):
                super().withdraw(amt, "S")
            else:
                print("withdrawal limit for savings AC : ", cur_ac_lmt)            
        elif sor == 1:
            super().withdraw(amt)
        else:
            print("select a valid option !")    
            
    def deposit(self):
        global user_lst, cur_user
        x = int(input("\nEnter deposit amount : "))
        user_lst[cur_user][4]["D  - "+str(user_lst[cur_user][3]+1)] = x 
        user_lst[cur_user][3] += 1
        if x > 0:
            user_lst[cur_user][1] += x
            save_data()
            print("Updated bal : ", user_lst[cur_user][1])
        elif x < 0:
            print("Amount cannot be a negatieve number !")
        else:
            print("Amount can not be zero")

    def trans(self):
        global user_lst, cur_user
        print("\n")
        for key, val in user_lst[cur_user][4].items(): 
            print(key, ":", val)
        print("        ---------\nBal    :",user_lst[cur_user][1])

    def loan_calc(self):
        amt = int(input("\nEnter loan amount : "))
        lst = ["1. Govt servent", "2. Senior citizen", "3. Student"]
        for i in lst:
            print(i)
        itype = int((input("\nSelect category : ")))
        x = 0
        match itype:
            case 1:
                x = 8
            case 2:
                x = 10
            case 3:
                x = 8
            case _:
                print("Enter a valid input")
        yrs = int(input("\nEnter period in years : "))
        intrest = (amt * x * yrs)/100
        print("Intrest : ",intrest)

    def passwd_change(self):
        old_pwd = input("Enter old password : ")
        if old_pwd ==  user_lst[cur_user][0]:
            new_pwd = input("Enter new Password :")
            new_pwd_confirm = input("Renter new password :")
            if new_pwd == new_pwd_confirm:
                user_lst[cur_user][0] = new_pwd
                print("Password updated successfully !")
                save_data()
                super().user_auth()
            else:
                print("password dosent match ! \nplease try again !")
        else:
            print("password dosent match ! \nplease try again !")
tar_1 = Banking()

if user_auth_status:
    tar_1.options()