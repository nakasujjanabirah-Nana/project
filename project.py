
import re


class Branch:
    def __init__(self, branch_name, branch_code, address, branch_manager_name, contact):
        self.branch_name = branch_name
        self.branch_code = branch_code
        self.address = address
        self.branch_manager_name = branch_manager_name
        self.contact = contact

    def __str__(self):
        return f"Branch Name: {self.branch_name}, Branch Code: {self.branch_code}, Address: {self.address}, Bank Manager: {self.branch_manager_name}, Contact: {self.contact}"


class Client:
    def __init__(self, first_name, last_name, address, Id, contact, gender, account_number):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.Id = Id
        self.contact = contact
        self.gender = gender
        self.account_number = account_number

    def __str__(self):
        return f"Client: {self.first_name} {self.last_name}, ID: {self.Id}, Address: {self.address}, Contact: {self.contact}, Gender: {self.gender}"


class Account(Client):
    def __init__(self, first_name, last_name, address, Id, contact, gender, account_number, account_type, account_holder, date):
        super().__init__(first_name, last_name, address, Id, contact, gender, account_number)
        self.account_number = account_number
        self.account_type = account_type
        self.account_holder = account_holder
        self.__balance = 0
        self.__status = "in progress"
        self.date = date

    def __str__(self):
        return f"Client: {self.first_name} {self.last_name}, Account Number: {self.account_number}, Account Type: {self.account_type}, Balance: {self.__balance}, status: {self.__status}"
    @property
    def balance(self):
        return self.__balance
     
    @property
    def status(self):
        return self.__status
    def update_balance(self, balance):
        self.__balance = balance
    
    def update_status(self):
        return self.__status =="active"
    



class Transaction:
    def __init__(self,t_id,transaction_type,date,account_number):
        self.t_id = t_id
        self.transaction_type = transaction_type
        self.__amount = 0
        self.date = date
        self.account_number = account_number
        self.__status = "Pending"

    

    def __str__(self):
        return f"Transaction ID: {self.transaction_id}, Transaction Type: {self.transaction_type}, Amount: {self.__amount}, Date: {self.date}, Account: {self.account},staus:{self.__status}"

    def get_amount(self):
        return self.__amount
    def set_status(self):
        return self.__status
        
   

class Transfer:
    def __init__(self,transfer_id,date,reciever_account,):
        
        self.transfer_id = transfer_id
        self.__amount = 0
        self.date = date
        self.__status = "pending"
        self.reciever_account = reciever_account

    def __str__(self):
        return f"Transfer ID: {self.transfer_id}, Amount: {self.amount}, Date: {self.date}, To Account: {self.reciever_account}"    
    
    def get_amount(self,amount,):
        if amount > 500:
            self.__amount +=self.reciever_account
            
        return self.__status
    

class Deposit:
    def __init__(self,t_id,account_no,):
        self.t_id = t_id
        self.__amount = 0
        self.account_no = account_no
    @property
    def get_amount(self,amount):
        if amount > 0:
            self.__amount +=amount
        return "successfull"

    
    def __str__(self):
        return f"Deposit ID: {self.t_id}, Amount: {self.amount}, Account: {self.account_no}"

    

class Withdrawal:
    def __init__(self,t_id,account_no):
        self.t_id = t_id
        self.account_no = account_no
        self.__amount = 0

    def __str__(self):
        return f"Withdrawal ID: {self.t_id}, Amount: {self.amount}, Account: {self.account}"
    @property
    def set_amount(self):
        self.__amount
    @property
    def get_amount(self,amount):
        
        self.__amount -=amount


    
