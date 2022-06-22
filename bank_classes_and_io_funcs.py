#!/usr/bin/env python

"""
@Author: Jonathan Presto
@Date: 2022-06-20

This Bank Model demonstrates Python OOP techniques.  This file serves as input 
to the main driver program "bank_main.py" to encapsulate the attributes 
and methods in the classes and subclasses listed below:

1. Class: Bank, Subclass: Branch
2. Class: Employee, Subclass: none
3. Class: Customer, Subclass: none
4. Class: BankAccount, Subclasses: CheckingAccount, SavingsAccount
5. Class: Service, Subclasses: CreditCard, LoanAccount

Each Class comes with two custom I/O functions:
1. The first function loads data from csv file to a dictionary of objects.
2. The second function writes data (loaded to memory) back to a csv file.
The second function is called after applying updates in the main driver program.

Example:
The main driver program "bank_main.py" demonstrates examples of usage.

"""


#import modules
import datetime
import csv
import pprint as pp
import pandas as pd
import re
import logging
from dateutil.relativedelta import relativedelta

# custom module needed to perform validate date and credit card number
from bank_data_quality_checks import *



################################################
##### Bank class, sub-classes and functions
################################################
class Bank:
    def __init__(self, bid, bank):
        self.bank_id = bid
        self.bank_name = bank
        
    def get_bank_id(self):
        return self.bank_id
    
    def get_bank_name(self):
        return self.bank_name


class Branch(Bank):
    def __init__(self, bid, bank, loc_id, branch):
        Bank.__init__(self, bid, bank)
        self.location_id = loc_id
        self.branch_name = branch
        
    def get_location_id(self):
        return self.location_id
    
    def get_branch_name(self):
        return self.branch_name
        
def load_bank_locations_file_to_dict(file):
    branches_dict = {}
    
    with open(file, 'r') as file:
        csvreader = csv.reader(file)
        # This skips the first header row of the CSV file.
        next(csvreader)
        
        for row in csvreader:
            bank_id, bank_name, location_id, branch_name  = row[0], row[1], row[2], row[3]
            loc = Branch(bank_id, bank_name, location_id, branch_name)  
            branches_dict[location_id] = loc
            
    logger.info("Bank locations file loaded to dictionary.")        
    return branches_dict

def write_bank_locations_to_file(data_dict, outfile):
    rows = []
    cols = ['bank_id', 'bank_name', 'location_id', 'branch_name']
    for key, val in data_dict.items():
        row = []
        row.append(val.get_bank_id())
        row.append(val.get_bank_name())
        row.append(val.get_location_id())
        row.append(val.get_branch_name())
        rows.append(row)

    # creating DataFrame from list of lists and write to csv
    df = pd.DataFrame(rows, columns=cols)
    df.to_csv(outfile, index=False)
    logger.info(f"Bank locations data was written to csv file at location {outfile}.")
       
    
################################################
##### BankAccount class, sub-classes and functions
################################################
class BankAccount:
    def __init__(self, cust_id, acct_num, bal=0):
        self.customer_id = cust_id
        self.account_number = acct_num
        self.balance = float(bal)
        
        if self.balance < 0:
            print("Initial balance cannot be less than 0!")
            self.balance = 0
    
    def get_customer_id(self):
        return self.customer_id

    def get_account_number(self):
        return self.account_number
    
    def get_balance(self):
        return self.balance

    def deposit(self, amount):
        self.balance += amount
        
    def withdraw(self, amount):
        self.balance -= amount
     
        
class SavingsAccount(BankAccount):
    def __init__(self, cust_id, acct_num, bal, ann_int_rate=0.008):
        BankAccount.__init__(self, cust_id, acct_num, bal)
        self.annual_interest_rate = float(ann_int_rate)
        
    def get_annual_interest_rate(self):
        return self.annual_interest_rate
    
    def get_balance_next_month(self):
        return round(self.balance*(1 + (self.annual_interest_rate/12)),2)
    
    def get_compounded_balance(self):
        print("Enter number of months to compound: ")
        months = int(input())
        return round(  self.balance*(1 + (self.annual_interest_rate/12))**(12*months/12),2)

        
def load_savings_file_to_dict(file):
    savings_account_dict = {}
    
    with open(file, 'r') as file:
        csvreader = csv.reader(file)
        # This skips the first header row of the CSV file.
        next(csvreader)
        
        for row in csvreader:
            cust_id, acct_num, bal, ann_int_rate  = row[0], row[1], row[2], row[3]
            acct = SavingsAccount(cust_id, acct_num, bal, ann_int_rate)   
            savings_account_dict[acct_num] = acct
            
    logger.info("Savings account file loaded to dictionary.")        
    return savings_account_dict 
                    
def write_savings_accounts_to_file(data_dict, outfile):
    rows = []
    cols = ['customer_id', 'account_number', 'balance', 'annual_interest_rate']
    for key, val in data_dict.items():
        row = []
        row.append(val.get_customer_id())
        row.append(val.get_account_number())
        row.append(round(val.get_balance(),2))
        row.append(val.get_annual_interest_rate())
        rows.append(row)

    # creating DataFrame from list of lists and write to csv
    df = pd.DataFrame(rows, columns=cols)
    df.to_csv(outfile, index=False)
    logger.info(f"Savings accounts data was written to csv file at location {outfile}.")
                    
class CheckingAccount(BankAccount):
    
    MIN_BALANCE = 25.00
    WITHDRAWAL_FEE = 0.25
    OVERDRAFT_FEE = 18.00
    
    def __init__(self, cust_id, acct_num, bal):
        BankAccount.__init__(self, cust_id, acct_num, bal)
        self.__min_balance = float(CheckingAccount.MIN_BALANCE)
        self.__withdrawal_fee = float(CheckingAccount.WITHDRAWAL_FEE)
        self.__overdraft_fee = float(CheckingAccount.OVERDRAFT_FEE)
        
        if self.balance < self.__min_balance:
            print("Minimum balance for checking must be at least $25.00!")
            while self.balance < self.__min_balance:
                print(f"Re-enter initial balance of at least ${self.__min_balance:,.2f}: ")
                self.balance = int(input())

    def withdraw(self, amount):
        self.balance -= amount
        self.balance -= self.__withdrawal_fee
        print(f"Amount withdrawn is ${amount:,.2f}. New balance with applied fees is ${self.balance:,.2f}")
        
        if self.balance < 0:
            self.balance -= self.__overdraft_fee
            print(f"An overdraft fee of ${self.__overdraft_fee:,.2f} has been applied due to negative balance!")
            print(f"Your new balance is: ${self.balance:,.2f}")

                  
def load_checking_file_to_dict(file):
    checking_account_dict = {}
    
    with open(file, 'r') as file:
        csvreader = csv.reader(file)
        # This skips the first header row of the CSV file.
        next(csvreader)
        
        for row in csvreader:
            cust_id, acct_num, bal  = row[0], row[1], row[2]
            acct = CheckingAccount(cust_id, acct_num, bal)   
            checking_account_dict[acct_num] = acct
    
    logger.info("Checking account file loaded to dictionary.")
    return checking_account_dict     


def write_checking_accounts_to_file(data_dict, outfile):
    rows = []
    cols = ['customer_id', 'account_number', 'balance']
    for key, val in data_dict.items():
        row = []
        row.append(val.get_customer_id())
        row.append(val.get_account_number())
        row.append(round(val.get_balance(),2))
        rows.append(row)

    # creating DataFrame from list of lists and write to csv
    df = pd.DataFrame(rows, columns=cols)
    df.to_csv(outfile, index=False)
    logger.info(f"Checking accounts data was written to csv file at location {outfile}.")
     
 
    
################################################
##### Customer class and functions
################################################

class Customer:
    def __init__(self, cust_id, member_dt, first, last, birth_dt, st_addr, cty, st, zipc, phone):
        self.customer_id = cust_id
        
        try:
            if is_valid_date(member_dt): 
                self.membership_date = datetime.date.fromisoformat(member_dt)
            else:
                logger.error(f"Invalid membership date entered for cust {cust_id}!")
                print(f"Invalid membership date entered for cust {cust_id}! Re-enter date (YYYY-MM-DD): ")
                mem_dt = input()
                self.set_membership_date(mem_dt)
                
        except AttributeError:
            pass 
                
        self.first_name = first
        self.last_name = last
        
        try:
            if is_valid_date(birth_dt):
                self.birth_date = birth_dt
            else:
                logger.error(f"Invalid birth date entered for cust {cust_id}!")
                print(f"Invalid birth date entered for cust {cust_id}! Re-enter date (YYYY-MM-DD): ")
                dob = input()
                self.set_birth_date(dob)
        except AttributeError:
            pass
        
        self.street_address = st_addr
        self.city = cty
        self.state = st
        self.zip_code = zipc
        self.phone_number = phone
    
    # set methods for updating attributes
    def set_membership_date(self, member_dt):
        if is_valid_date(member_dt):
            self.membership_date = datetime.date.fromisoformat(member_dt)
            logger.info(f"Membership date updated to {self.membership_date} for cust {self.customer_id}.")
        else:
            print('Enter valid membership date: ')
            mem_dt = input()
            self.set_membership_date(mem_dt)
    
    def set_first_name(self, first):
        self.first_name = first
        logger.info(f"First name updated for cust {self.customer_id}.")
        
    def set_last_name(self, last):
        self.last_name = last
        logger.info(f"Last name updated for cust {self.customer_id}.")
    
    def set_birth_date(self, birth_dt):
        if is_valid_date(birth_dt):
            self.birth_date = datetime.date.fromisoformat(birth_dt)
            logger.info(f"Birth date updated to {self.birth_date} for cust {self.customer_id}.")
        else:
            print('Enter valid birth date: ')
            dob = input()
            self.set_birth_date(dob)
        
    def set_street_address(self, addr):
        self.street_address = addr
        logger.info(f"Street address updated for cust {self.customer_id}.")
        
    def set_city(self, cty):
        self.city = cty
        logger.info(f"City updated for cust {self.customer_id}.")
        
    def set_state(self, st):
        self.state = st
        logger.info(f"State updated for cust {self.customer_id}.")
    
    def set_zip_code(self, zipc):
        self.zip_code = zipc
        logger.info(f"Zip code updated for cust {self.customer_id}.")
        
    def set_phone_number(self, phone):
        self.phone_number = phone
        logger.info(f"Phone updated for cust {self.customer_id}.")
        
    # get methods
    def get_customer_id(self):
        return self.customer_id
    
    def get_membership_date(self):
        return self.membership_date
    
    def get_first_name(self):
        return self.first_name
    
    def get_last_name(self):
        return self.last_name
    
    def get_birth_date(self):
        return self.birth_date
    
    def get_street_address(self):
        return self.street_address
    
    def get_city(self):
        return self.city
    
    def get_state(self):
        return self.state
    
    def get_zip_code(self):
        return self.zip_code
        
    def get_phone_number(self):
        return self.phone_number
        
    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_address(self):
        return "{}, {}, {}  {}".format(self.street_address, self.city, self.state, self.zip_code)


def load_customer_file_to_dict(file):
    customers_dict = {}
    
    with open(file, 'r') as file:
        csvreader = csv.reader(file)
        # This skips the first header row of the CSV file.
        next(csvreader)
        
        for i, row in enumerate(csvreader):
            member_dt = row[1]
            birth_dt = row[4]
            try:
                if is_valid_date(member_dt) and is_valid_date(birth_dt):
                    cust_id, member_dt, first, last, birth_dt, st_addr, cty, st, zipc, phone = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]
                    cust = Customer(cust_id,  member_dt, first, last, birth_dt, st_addr, cty, st, zipc, phone)   
                    customers_dict[cust_id] = cust
                else:
                    logger.error(f"Invalid date detected at row {i} when loading customers from file! Skipping record.")
            except AttributeError:
                next(csvreader)
                
    logger.info("Customers file loaded to dictionary.")       
    return customers_dict


def write_customers_to_file(data_dict, outfile):
    rows = []
    cols = ['customer_id', 'membership_date', 'first_name', 'last_name', 'birth_date', 'street_address', 'city', 'state', 'zip_code', 'phone_number']
    for key, val in data_dict.items():
        row = []
        row.append(val.get_customer_id())
        row.append(val.get_membership_date())
        row.append(val.get_first_name())
        row.append(val.get_last_name())
        row.append(val.get_birth_date())
        row.append(val.get_street_address())
        row.append(val.get_city())
        row.append(val.get_state())
        row.append(val.get_zip_code())
        row.append(val.get_phone_number())
        rows.append(row)

    # creating DataFrame from list of lists and write to csv
    df = pd.DataFrame(rows, columns=cols)
    df.to_csv(outfile, index=False)
    logger.info(f"Customers data was written to csv file at location {outfile}.")
    

    
################################################
##### Employee class and functions
################################################
class Employee:
    def __init__(self, emp_id, loc_id, first, last, sal, start_dt, term_dt=None):
        self.employee_id = emp_id
        self.location_id = loc_id
        self.emp_first_name = first
        self.emp_last_name = last
        self.salary = float(sal)
        
        try:
            if is_valid_date(start_dt):
                self.start_date = datetime.date.fromisoformat(start_dt)
            else:
                logger.error(f"Invalid start date entered for employee {emp_id}! Re-enter date (YYYY-MM-DD): ")
                st_dt = input()
                self.set_start_date(st_dt)
        except AttributeError:
            pass
        
        self.termination_date = term_dt
       
    # set methods for updating
    def set_location_id(self, loc_id):
        self.location_id = loc_id
        logger.info(f"Location ID updated to {self.location_id} for employee {self.employee_id}.")
        
    def set_emp_first_name(self, first):
        self.emp_first_name = first
        logger.info(f"First name updated to {self.emp_first_name} for employee {self.employee_id}.")
        
    def set_emp_last_name(self, last):
        self.emp_last_name = last
        logger.info(f"Last name updated to {self.emp_last_name} for employee {self.employee_id}.")
        
    def set_salary(self, sal):
        self.salary = float(sal)
        logger.info(f"Salary updated to {self.salary} for employee {self.employee_id}.")
        
    def set_start_date(self, start_dt):
        if is_valid_date(start_dt):
            self.start_date = datetime.date.fromisoformat(start_dt)
            logger.info(f"Start date updated to {self.start_date} for employee {self.employee_id}.")
        else:
            print('Enter valid start date: ')
            st_dt = input()
            self.set_start_date(st_dt)

    def set_termination_date(self, term_dt):
        if is_valid_date(term_dt):
            self.termination_date = datetime.date.fromisoformat(term_dt)
            logger.info(f"Termination date updated to {self.termination_date} for employee {self.employee_id}.")
        else:
            print('Enter valid termination date: ')
            t_dt = input()
            self.set_termination_date(t_dt)
    
    # get methods
    def get_employee_id(self):
        return self.employee_id
    
    def get_location_id(self):
        return self.location_id
    
    def get_emp_first_name(self):
        return self.emp_first_name
    
    def get_emp_last_name(self):
        return self.emp_last_name
    
    def get_salary(self):
        return self.salary
    
    def get_start_date(self):
        return self.start_date
    
    def get_termination_date(self):
        return self.termination_date
    
    def get_tenure_years(self):
        if self.termination_date is None:
            return relativedelta(datetime.date.today(), self.start_date).years
        else:
            return relativedelta(self.termination_date, self.start_date).years
        
def load_employees_file_to_dict(file):
    employees_dict = {}
    
    with open(file, 'r') as file:
        csvreader = csv.reader(file)
        # This skips the first header row of the CSV file.
        next(csvreader)
        
        # create dictionary of employee objects
        for i, row in enumerate(csvreader):
            start_dt = row[5]
            try:
                if is_valid_date(start_dt):
                    emp_id, loc_id, first, last, sal, start_dt, term_dt = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
                    emp = Employee(emp_id, loc_id, first, last, sal, start_dt, term_dt)
                    employees_dict[emp_id] = emp
                else:
                    logger.error(f"Invalid start date detected at row {i} when loading employees from file! Skipping record.")
            except AttributeError:
                next(csvreader)
    
    logger.info("Employees file loaded to dictionary.")
    return employees_dict


def write_employees_to_file(data_dict, outfile):
    rows = []
    cols = ['employee_id', 'location_id', 'first_name', 'last_name', 'salary', 'start_date', 'termination_date']
    for key, val in data_dict.items():
        row = []
        row.append(val.get_employee_id())
        row.append(val.get_location_id())
        row.append(val.get_emp_first_name())
        row.append(val.get_emp_last_name())
        row.append(round(val.get_salary(),2))
        row.append(val.get_start_date())
        row.append(val.get_termination_date())
        rows.append(row)
        
    # creating DataFrame from list of lists and write to csv
    df = pd.DataFrame(rows, columns=cols)
    df.to_csv(outfile, index=False)
    logger.info(f"Employees data was written to csv file at location {outfile}.")
    

################################################
##### Service class, sub-classes and functions
################################################
class Service:
    def __init__(self, cust_id, ann_int_rate, bal=0):
        self.customer_id = cust_id
        self.annual_interest_rate = float(ann_int_rate)
        self.balance = float(bal)
        
    def set_annual_interest_rate(self, ann_int_rate):
        self.annual_interest_rate = float(ann_int_rate)
        logger.info(f"Annual interest rate updated to {self.annual_interest_rate} for cust {cust_id}.")
        
    def get_balance(self):
        return self.balance
    
    def get_annual_interest_rate(self):
        return self.annual_interest_rate
    
    def get_customer_id(self):
        return self.customer_id
    
    def make_payment(self, amount):
        print("Prior balance was ${:,.2f}".format(self.balance))
        self.balance -= amount
        print("Payment of ${:,.2f} received. New balance is ${:,.2f}.".format(amount, self.balance))

# Class CreditCard inherits from parent class Service
class CreditCard(Service):
    
    CASH_ADVANCE_FEE = 50
    CREDIT_LINE = 8000
    
    def __init__(self, cust_id, ann_int_rate, bal, ccn):
        Service.__init__(self, cust_id, ann_int_rate, bal)
        self.available_credit = float(CreditCard.CREDIT_LINE) - float(bal)
        self.balance = float(bal)
               
        if is_valid_card_number(ccn):
            self.credit_card_number = ccn
        else:
            raise Exception('Invalid card number entered. Object instance not created!')
        
    def make_purchase(self, amount):
        self.balance += amount
        self.available_credit -= amount
        
    def withdraw_cash(self, amount):
        self.balance += amount
        self.balance += CreditCard.CASH_ADVANCE_FEE
        self.available_credit -= amount
        self.available_credit -= CreditCard.CASH_ADVANCE_FEE
    
    def apply_interest(self):
        self.balance = self.balance*(1+self.annual_interest_rate/12)
        self.available_credit = CreditCard.CREDIT_LINE - self.balance
    
    def get_available_credit(self):
        return self.available_credit
    
    def get_credit_card_number(self):
        return self.credit_card_number


def load_credit_card_file_to_dict(file):
    credit_card_account_dict = {}
    
    with open(file, 'r') as file:
        csvreader = csv.reader(file)
        # This skips the first header row of the CSV file.
        next(csvreader)
        
        for i,row in enumerate(csvreader):
            ccn = row[3]
            try:
                if is_valid_card_number(ccn):
                    cust_id, ann_int_rate, bal, ccn  = row[0], row[1], row[2], row[3]
                    acct = CreditCard(cust_id, ann_int_rate, bal, ccn)   
                    credit_card_account_dict[ccn] = acct
                else:
                    logger.error(f"Invalid credit card detected at row {i} when loading credit cards from file! Skipping record.")
            except ValueError:
                next(csvreader)
                
    logger.info("Credit card file loaded to dictionary.")        
    return credit_card_account_dict


def write_credit_card_accounts_to_file(data_dict, outfile):
    rows = []
    cols = ['customer_id', 'annual_interest_rate', 'balance', 'credit_card_number']
    for key, val in data_dict.items():
        row = []
        row.append(val.get_customer_id())
        row.append(val.get_annual_interest_rate())
        row.append(round(val.get_balance(),2))
        row.append(val.get_credit_card_number())
        rows.append(row)

    # creating DataFrame from list of lists and write to csv
    df = pd.DataFrame(rows, columns=cols)
    df.to_csv(outfile, index=False)
    logger.info(f"Credit cards data was written to csv file at location {outfile}.")


# Class LoanAccount
class LoanAccount(Service):
    
    def __init__(self, cust_id, ann_int_rate, bal, loan_amt, loan_acct_num, num_years):
        Service.__init__(self, cust_id, ann_int_rate, bal)
        self.loan_amount = float(loan_amt)
        self.loan_account_number = loan_acct_num
        self.number_of_years = int(num_years)
        
    def get_loan_amount(self):
        return round(self.loan_amount,2)        
    
    def get_loan_account_number(self):
        return self.loan_account_number
    
    def get_number_of_years(self):
        return self.number_of_years
    
    def get_monthly_payment(self):
        P = self.get_loan_amount()
        months = self.get_number_of_years() * 12
        rate = self.get_annual_interest_rate()

        #calculate monthly payment
        monthly_payment = (rate/12) * (1/(1-(1+rate/12)**(-months)))*P
        return round(monthly_payment,2)

def load_loan_file_to_dict(file):
    loan_account_dict = {}
    
    with open(file, 'r') as file:
        csvreader = csv.reader(file)
        # This skips the first header row of the CSV file.
        next(csvreader)
        
        for row in csvreader:
            cust_id, ann_int_rate, bal, loan_amt, acct_num, years  = row[0], row[1], row[2], row[3], row[4], row[5]
            acct = LoanAccount(cust_id, ann_int_rate, bal, loan_amt, acct_num, years)   
            loan_account_dict[acct_num] = acct
    
    logger.info("Loan accounts file loaded to dictionary.")
    return loan_account_dict

    
def write_loan_accounts_to_file(data_dict, outfile):
    rows = []
    cols = ['customer_id', 'annual_interest_rate', 'balance', 'loan_amount', 'loan_account_number', 'number_of_years']
    for key, val in data_dict.items():
        row = []
        row.append(val.get_customer_id())
        row.append(val.get_annual_interest_rate())
        row.append(round(val.get_balance(),2))
        row.append(round(val.get_loan_amount(),2))
        row.append(val.get_loan_account_number())
        row.append(int(val.get_number_of_years()))
        rows.append(row)

    # creating DataFrame from list of lists and write to csv
    df = pd.DataFrame(rows, columns=cols)
    df.to_csv(outfile, index=False)
    logger.info(f"Loan accounts data was written to csv file at location {outfile}.")
   
    
### EOF