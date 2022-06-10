import os
from utils.utilities import utility_functions
import random

class main_app:

    def package(self):
        try:
            path = os.getcwd()
            self.database_name = "bank_db"
            # Authenticate the user and Get the User ID
            db = utility_functions(path, self.database_name).authenticate_user()
            self.user = db[0][0]
            print("Your user ID is :", self.user)

            while True:
                # Printing menu
                print("\n1 - Balance \t 2 - Withdraw \t 3 - Get Statement \t 4 - Quit ")
                self.choice = int(input("\nEnter your selection: "))

                if self.choice == 1:
                    # get the user balance
                    bal = utility_functions(path, self.database_name).get_balance(self.user)
                elif self.choice == 2:
                    # withdraw the amount
                    withdraw = utility_functions(path, self.database_name).withdraw_amt(self.user)
                elif self.choice == 3:
                    # get the statement
                    stmt = utility_functions(path,self.database_name).get_statement(self.user)
                elif self.choice == 4:
                    stmt = input("Are you sure you want to quit?, Yes, or No:")
                    if stmt == "Yes" or "yes" or "y":
                        utility_functions(None, None).final()
                        break
                    else:
                        main_app().package()
                elif self.choice == 5:
                    print("invalid choice")

        except Exception as e:
            print(e)

t = main_app().package()
