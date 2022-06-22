#!/usr/bin/env python

"""
@Author: Jonathan Presto
@Date: 2022-06-20

This main driver program demonstrates the Bank Model using Python OOP techniques.
Before executing program, it is imperative to import the custom modules as shown
below at import statements.  There are 2 custom modules that should be imported 
from the same directory as this file.

Refer to the UML Diagram file "UML_Diagram_Bank_System.pdf" to get an overview
of the various classes and subclasses.

This demo will perform three high-level steps for each class:
1. Load the csv file into a dictionary of objects for that class.
2. Perform some updates and/or instantiations of new objects for that class.
3. Write the data from dictionary of objects back to a csv file. 

EXECUTION:
To execute this driver program from command line, make sure the following 3 files are 
saved in the same directory.
1. bank_main.py
2. bank_data_quality_checks.py
3. bank_classes_and_io_funcs.py

Open new terminal and navigate to the directory where files are saved and execute:
%  python bank_main.py

You may be prompted to input valid dates in YYYY-MM-DD.  This is deliberate to 
demo the data quality check utility.

Refer to text file "console_output_demo.txt" for sample output of driver.  

EXAMPLES:
When creating new objects for each class, make sure you input all the positional
args in order.  Below are some examples.

1. Class Employee
	(a) To create a new employee, enter positional args into Employee class:
	employee_id, location_id, first_name, last_name, salary, start_date
    emp_objects_dict['3004'] = Employee('3004', '106', Joe, Smith, 75000, '2017-09-25')
    
    (b) To set termination date of existing employee, call method on dict object:
    emp_objects_dict['3004'].set_termination_date('2022-06-01') 
    
2. Class Customer
    (a) To create a new customer, enter positional args into Customer class:
    customer_id, membership_date, first_name, last_name, birth_date, street_address,
    city, state, zip_code, phone_number
    cust_objects_dict['600000'] = Customer('600000', '2019-01-01', 'Susan', 'Smith',
            '1970-05-05', '123 Main St', 'Los Angeles', 'CA', '90002', '213-555-4434')
            
    (b) To update phone number, call method on dict object:
    cust_objects_dict['600000'].set_phone_number('213-566-2298')
    
3. Subclass CheckingAccounts
   (a) To create a new checking account, enter positional args into CheckingAccount class:
   customer_id, account_number, balance
   checking_acct_objects_dict['168555100'] = CheckingAccount('600000', '168555100', 500)
   
   (b) To withdraw from checking account:
   checking_acct_objects_dict['168555100'].withdraw(60)
   
   (c) To deposit into checking account:
   checking_acct_objects_dict['168555100'].deposit(800)  
   

For the other classes, please review the UML diagram and the __init__ methods for 
each class/subclass in the file "bank_classes_and_io_funcs.py" and take note of
the positional args and their data types.

"""

import datetime
import csv
import pprint as pp
import pandas as pd
import re
import logging
from dateutil.relativedelta import relativedelta

# import custom utilities
from bank_classes_and_io_funcs import *
from bank_data_quality_checks import *


def main():

    print("\n\n\n__________________DEMO BANK CLASS__________________") 
    # Load bank location objects
    bank_locations_objects_dict = load_bank_locations_file_to_dict("sample_input/BankLocations.csv")
    print("Bank locations initial load: ")
    for k, v in bank_locations_objects_dict.items():
        print(k, ': ', v.get_bank_id(), v.get_bank_name(), v.get_location_id(), v.get_branch_name())
    
    # adding new branch location
    print("\nAdding new branch location...")
    bank_locations_objects_dict['107'] = Branch('15', 'Wells Fargo', '107', 'Studio City Branch')
    print("Bank locations updated: ")
    for k, v in bank_locations_objects_dict.items():
        print(k, ': ', v.get_bank_id(), v.get_bank_name(), v.get_location_id(), v.get_branch_name())
    print("Output to csv file...")
    write_bank_locations_to_file(bank_locations_objects_dict, "sample_output/BankLocations.csv")
    
    
    print("\n\n\n__________________DEMO CUSTOMER CLASS__________________") 
    # Load customer objects from file    
    cust_objects_dict = load_customer_file_to_dict("sample_input/Customers.csv")
    
    print("Customers initial load: ")
    for k, v in cust_objects_dict.items():
        print(k, ': ', v.get_full_name(), 'at', v.get_address(), v.get_birth_date(), v.get_membership_date())  
    
    print("\nUpdating last name for customer_id 60000...")
    cust_objects_dict['600000'].set_last_name('Smith-Coleman')
    
    print("Creating new customer with clean data...")
    cust_objects_dict['600010'] = Customer('600010' ,'2022-01-09', 'Randy', 'Moore', '1945-05-05', '123 Elm Street', 'Eagle Rock', 'CA', '92256', '323-555-3333')

    print("Creating new customer with invalid membership date and birth date...")
    cust_objects_dict['600011'] = Customer('600011' ,'2022-01-99', 'Mary', 'Crawford', '1845-06-95', '889 Riverdale Ct', 'Pasadena', 'CA', '91103', '323-552-1122')

    print("Customers updated: ")
    for k, v in cust_objects_dict.items():
        print(k, ': ', v.get_full_name(), 'at', v.get_address(), v.get_birth_date(), v.get_membership_date())
    print("Output to csv file...")
    write_customers_to_file(cust_objects_dict, "sample_output/Customers.csv")


    print("\n\n\n__________________DEMO EMPLOYEE CLASS__________________")  
    #load employee objects from file
    emp_objects_dict = load_employees_file_to_dict("sample_input/Employees.csv")
    print("Employees initial load: ")
    for k, v in emp_objects_dict.items():
        print(k, ': ', v.get_emp_first_name(), v.get_emp_last_name(), v.get_start_date(), v.get_termination_date())
    print("Terminating employee 3001...")    
    emp_objects_dict['3001'].set_termination_date('2022-06-21')
    print("Employees updated: ")
    for k, v in emp_objects_dict.items():
        print(k, ': ', v.get_emp_first_name(), v.get_emp_last_name(), v.get_start_date(), v.get_termination_date())
    print("Output to csv file...")
    write_employees_to_file(emp_objects_dict, "sample_output/Employees.csv")
    

    print("\n\n\n__________________DEMO CHECKING ACCOUNT SUBCLASS__________________")
    #load checking account objects from file
    checking_acct_objects_dict = load_checking_file_to_dict("sample_input/CheckingAccounts.csv")
    print("Checking accounts initial load: ")
    for k, v in checking_acct_objects_dict.items():
        print(k, ': ', v.get_customer_id(), v.get_account_number(), '${:,.2f}'.format(v.get_balance()))
    print("Creating checking accounts for cust 600008 and cust 600009...")
    checking_acct_objects_dict['168555140'] = CheckingAccount('600008', '168555140', '800.50')
    checking_acct_objects_dict['168555145'] = CheckingAccount('600009', '168555145', '900.00')
    print("Withdrawing $1000 for checking account 168555120...")
    checking_acct_objects_dict['168555120'].withdraw(1000)
    print("Depositing $700 for checking account 168555105...")    
    checking_acct_objects_dict['168555105'].deposit(700)
    print("Withdrawing $600 for checking account 168555100, an amount greater than current balance...")  
    checking_acct_objects_dict['168555100'].withdraw(600)    
    print("Checking accounts updated: ")
    for k, v in checking_acct_objects_dict.items():
        print(k, ': ', v.get_customer_id(), v.get_account_number(), '${:,.2f}'.format(v.get_balance()))
    print("Output to csv file...")
    write_checking_accounts_to_file(checking_acct_objects_dict, "sample_output/CheckingAccounts.csv")
    

    print("\n\n\n__________________DEMO SAVINGS ACCOUNT SUBCLASS__________________") 
    #load savings account objects from file
    savings_acct_objects_dict = load_savings_file_to_dict("sample_input/SavingsAccounts.csv")
    print("Savings accounts initial load: ")
    for k, v in savings_acct_objects_dict.items():
        print(k, ': ', v.get_customer_id(), v.get_account_number(), '${:,.2f}'.format(v.get_balance()))
    print("Deposit $2000 for savings account 168444660...")
    savings_acct_objects_dict['168444660'].deposit(2000)
    print("Balance next month for savings account 168444555 with earned interest is: ")
    print('${:,.2f}'.format(savings_acct_objects_dict['168444555'].get_balance_next_month()))
    print("For savings account 168444555 what is the balance with earned interest over X months? Prompt user for months...")
    print('${:,.2f}'.format(savings_acct_objects_dict['168444555'].get_compounded_balance()))
    print("Savings accounts updated: ")
    for k, v in savings_acct_objects_dict.items():
        print(k, ': ', v.get_customer_id(), v.get_account_number(), '${:,.2f}'.format(v.get_balance()))    
    print("Output to csv file...")
    write_savings_accounts_to_file(savings_acct_objects_dict, "sample_output/SavingsAccounts.csv")
            

    print("\n\n\n__________________DEMO CREDIT CARD ACCOUNTS SUBCLASS__________________") 
    #load credit card account objects from file        
    credit_card_acct_objects_dict = load_credit_card_file_to_dict("sample_input/CreditCards.csv")
    print("Credit card accounts initial load: ")
    for k, v in credit_card_acct_objects_dict.items():
        print(k, ': ', v.get_customer_id(), v.get_credit_card_number(), '${:,.2f}'.format(v.get_balance()))
    print("Make a purchase of $365 for credit card 4147-0989-3947-4110...")
    credit_card_acct_objects_dict['4147-0989-3947-4110'].make_purchase(365)
    print("Withdraw cash advance of $2000 for credit card 4147-0989-3995-4678...")
    credit_card_acct_objects_dict['4147-0989-3995-4678'].withdraw_cash(2000)    
    print("Available credit for card 4147-0989-3995-4678 is now ${:,.2f}".format(credit_card_acct_objects_dict['4147-0989-3995-4678'].get_available_credit()))
    print("Now applying interest rate charges for next month...")
    credit_card_acct_objects_dict['4147-0989-3947-4110'].apply_interest()
    credit_card_acct_objects_dict['4147-0989-3995-4678'].apply_interest()
    credit_card_acct_objects_dict['4147-0989-4458-3321'].apply_interest()
    credit_card_acct_objects_dict['4147-0989-4412-9987'].apply_interest()
    
    #### sample code below will raise an exception due to invalid card number and will not create the instance.
    # To demo, uncomment and rerun this file.
    # print("Create a second credit card for customer 600007 using invalid card number: ")
    # credit_card_acct_objects_dict['2222-0989-4412-9987'] = CreditCard('600007','0.180',0,'2222-0989-4412-9987')
    
    print("Credit card accounts updated: ")
    for k, v in credit_card_acct_objects_dict.items():
        print(k, ': ', v.get_customer_id(), v.get_credit_card_number(), '${:,.2f}'.format(v.get_balance()))    
    print("Output to csv file...")
    write_credit_card_accounts_to_file(credit_card_acct_objects_dict,"sample_output/CreditCards.csv")
    

    print("\n\n\n__________________DEMO LOAN ACCOUNTS SUBCLASS__________________") 
    #load loan account objects from file  
    loan_acct_objects_dict = load_loan_file_to_dict("sample_input/LoanAccounts.csv")
    print("Loan accounts initial load: ")
    for k, v in loan_acct_objects_dict.items():
        print(k, ': ', v.get_customer_id(), v.get_loan_account_number(), '${:,.2f}'.format(v.get_balance()), '${:,.2f}'.format(v.get_loan_amount()))   
    print("Monthly payment for loan account 555-678-101 is ${:,.2f}".format(loan_acct_objects_dict['555-678-101'].get_monthly_payment()))
    print("Make payment of $500 on loan account 555-678-101...")
    loan_acct_objects_dict['555-678-101'].make_payment(500)
    print("Loan accounts updated: ")
    for k, v in loan_acct_objects_dict.items():
        print(k, ': ', v.get_customer_id(), v.get_loan_account_number(), '${:,.2f}'.format(v.get_balance()), '${:,.2f}'.format(v.get_loan_amount()))
    print("Output to csv file...")        
    write_loan_accounts_to_file(loan_acct_objects_dict,"sample_output/LoanAccounts.csv")
 
  
    
# driver program
if __name__ == "__main__":
    main()


### EOF