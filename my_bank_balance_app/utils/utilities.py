import os
import sys
import pandas as pd
import random
import mysql.connector


class utility_functions:
    """
    initialize class
    inputs : current working directory, database name

    """
    def __init__(self,path,db_name):
        try:
            self.path = path
            self.db_name = db_name

        except Exception as e:
            print("some error ", e)

    def authenticate_user(self):
        try:
            self.db = mysql.connector.connect(
                host = "localhost",
                user = "root",
                password = "mysql",
                database = self.db_name
            )
            if(self.db):
                print("database connected successfully")
            else:
                print("database connection failed")

            # try 3 attempts for correct user ID
            self.attempt = 0
            while True:
                self.uid = str(input("enter user id : "))
                self.cursor = self.db.cursor(buffered=True)
                self.cursor.execute("select user_id from user_table as u where u.user_id = " + f'"{self.uid}"')
                self.row = self.cursor.fetchall()
                if len(self.row) == 1:
                    print("access granted")
                    self.db.close()
                    return self.row
                else:
                    self.attempt += 1
                    print("Not valid user, Try again, attempt no. : {0}", format(self.attempt))
                    if self.attempt >= 3:
                        print("Exceed max attempts.")
                        self.db.close()
                        break
        except Exception as e:
           print(str(e))

    def get_balance(self,user):
        """
        get current balance of user
        :param userid:
        :return:
        """
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="mysql",
                database=self.db_name
            )
            if (self.db):
                print("database connected successfully")
            else:
                print("database connection failed")
            self.user = user
            self.cursor = self.db.cursor(buffered=True)
            self.cursor.execute("select * from bank_account as b where b.user_id = " + f'"{self.user}"')
            self.row = self.cursor.fetchall()
            print("------BALANCE------")
            print("\n UserID          : ", self.row[0][0])
            print("\n Account No.     : ", self.row[0][2])
            print("\n Account Balance : ", self.row[0][4])
            self.db.close()
            return 1

        except Exception as e:
            print(str(e))

    def withdraw_amt(self, user):
        """
        - check if user have sufficent balance for withdrawal
        - check if withdrawal does not leaves account balance less than 5000
        :param user:
        :return:
        """
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="mysql",
                database=self.db_name
            )
            self.user = user
            self.cursor = self.db.cursor(buffered=True)
            self.cursor.execute("select * from bank_account as b where b.user_id = " + f'"{self.user}"')
            self.row = self.cursor.fetchall()
            print("------BALANCE------")
            print("\n UserID          : ", self.row[0][0])
            print("\n Account No.     : ", self.row[0][2])
            print("\n Account Balance : ", self.row[0][4])
            balance = self.row[0][4]
            amt = float(input("\nPlease Enter amount to withdraw: "))
            ver_withdraw = input("Is this the correct amount, Yes or No ? " + str(amt) + " ")
            if ver_withdraw in ("Yes", "yes", "y","Y"):
                print("Verify withdraw")
            else:
                self.final()
                exit(0)

            if amt > balance:
                print("amount is exceeding your current balance")
                return 0
            elif balance-amt < 5000:
                print("your minimum balance must be 5000 or more ")
            else:

                bal_amt = balance-amt
                print("remaining balance is ", bal_amt)
                self.cursor.execute("UPDATE bank_account SET amount = " + str(bal_amt) + "WHERE user_id = " + f'"{self.user}"')
                self.cursor.execute("INSERT INTO transaction_table(user_id, bid, withdrawn_amount) VALUES(%s, %s, %s)", (self.user, self.row[0][1], amt))
                self.db.commit()
                self.db.close()
            self.db.close()
            return 1

        except Exception as e:
            print(str(e))

    def get_statement(self, user):
        """
        get the transactions between the given dates
        :param user:
        :return:
        """
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="mysql",
                database=self.db_name
            )
            self.user = user
            self.cursor = self.db.cursor(buffered=True)
            self.from_date = str(input("From date(YYYY-MM-DD) : "))
            self.to_date = str(input("From date(YYYY-MM-DD) : "))
            self.cursor.execute("select * from transaction_table WHERE (cast(transaction_date as date) BETWEEN " + f'"{self.from_date}"' + " AND " + f'"{self.to_date}"' + ") AND user_id = " + f'"{self.user}"')
            self.row = self.cursor.fetchall()
            print("----WITHDRAWAL STATUS-----")
            for val in self.row:
                print(val)

            self.db.close()
            return 1

        except Exception as e:
            print(str(e))

    def final(self):
        print("\nYour Transaction is complete")
        print("Transaction ID: ", random.randint(10000, 1000000))
        print("Thank you")
