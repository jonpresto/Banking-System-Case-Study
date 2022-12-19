# Banking-System-Case-Study
This simple Bank Model demonstrates Python Object-Oriented Programming (OOP) methodology.

## Prerequisites
Before you continue, ensure you have a basic understanding of Object-Oriented-Programming.
Program was developed using Python 3.9.7, so make sure latest version is installed to prevent potential runtime errors.

## Summary
This bank model defines entities for Bank, Branch(Bank), Customer, Employee, BankAccount, CheckingAccount(BankAaccount), SavingsAccount(BankAccount),
Service, CreditCard(Service), and LoanAccount(Service).  

Refer to the UML Diagram file **UML_Diagram_Bank_System.pdf** to get an overview of the various classes and subclasses.

The following Python scripts are needed to execute the program, along with their brief description:
1. **bank_main.py**  -->  This is the main driver program that demonstrates loading data from csv file to memory, performing updates on certain objects, and writing back the updates to a csv file.
2. **bank_classes_and_io_funcs.py**  -->  This file contains the "meat" of the logic.  This is where Classes are defined, as well as their attributes and methods.  The file also defines some I/O utility functions for loading data to memory and writing data back to file.
3. **bank_data_quality_checks.py**  -->  This file encapulates the functions for checking the validity of credit card numbers and date strings.  In addition, a logger was created to capture I/O events and data quality errors.  Messages are written to the file **main.log**.

Sample datasets using fictitious data have been provided for demonstration purposes.  Refer to folders ***sample_input*** and ***sample_output***.  Do not move these files as the driver program assumes the file locations.
