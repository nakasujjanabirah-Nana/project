class Branch:
    branch_counter = 0

    @classmethod
    def generate_branch_code(cls):
        cls.branch_counter += 1
        return f"BR-{cls.branch_counter:04d}"

    def __init__(self, branch_name, branch_code, address, branch_manager_name, contact):
        self.branch_name = branch_name
        self.branch_code = branch_code
        self.address = address
        self.branch_manager_name = branch_manager_name
        self.contact = contact


    def __str__(self):
        return f"Branch Name: {self.branch_name}, Branch Code: {self.branch_code}, Address: {self.address}, Bank Manager: {self.branch_manager_name}, Contact: {self.contact}"


class Client:
    client_counter = 0

    @classmethod
    def generate_client_id(cls):
        cls.client_counter += 1
        return f"CL-{cls.client_counter:04d}"

    def __init__(self, first_name, last_name, address, Id,branch, contact, gender, account_number):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.Id = Id
        self.branch = branch    
        self.contact = contact
        self.gender = gender
        self.account_number = account_number
        self.branches= []

    def add_branch(self, branch):
        if branch.lient is not self:
            raise ValueError("This account does not belong to this client.")
        if branch not in self.branches:
            self.branches.append(branch)

    def __str__(self):
        return f"Client: {self.first_name} {self.last_name}, ID: {self.Id}, Address: {self.address}, Contact: {self.contact}, Gender: {self.gender}"


class Account:
    account_counter = 0

    @classmethod
    def generate_account_number(cls):
        cls.account_counter += 1
        return f"ACC-{cls.account_counter:04d}"

    def __init__(self, client, account_number, account_type, account_holder, date):
        self.client = client
        self.account_number = account_number
        self.account_type = account_type
        self.account_holder = account_holder
        self.__balance = 0
        self.__status = "in progress"
        self.date = date
    

    def __str__(self):
        return f"Client: {self.client.first_name} {self.client.last_name}, Account Number: {self.account_number}, Account Type: {self.account_type}, Balance: {self.__balance}, status: {self.__status}"
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
    transaction_counter = 0
    receipt_counter = 0

    @classmethod
    def generate_id(cls):
        cls.transaction_counter += 1
        return f"TR-{cls.transaction_counter:04d}"

    @classmethod
    def generate_receipt_id(cls):
        cls.receipt_counter += 1
        return f"RC-{cls.receipt_counter:04d}"

    def __init__(self,t_id=None,transaction_type="Transaction",date=None,account_number=None,account=None):
        self.t_id = t_id if t_id is not None else Transaction.generate_id()
        self.transaction_type = transaction_type
        self.__amount = 0
        self.date = date
        self.__status = "Pending"
        self.account = account
        self.account_number = account.account_number if account is not None else account_number

    def add_account(self, account):
        if self.account_number is not None and account.account_number != self.account_number:
            raise ValueError("This transaction belongs to another account.")
        self.account = account
        self.account_number = account.account_number
        
#override method  
    def update_balance(self,balance):
        print("transaction actions in proccess")
      

    def __str__(self):
        return f"Transaction ID: {self.t_id}, Transaction Type: {self.transaction_type}, Amount: {self.__amount}, Date: {self.date}, Account: {self.account_number}, Status: {self.__status}"

    def get_amount(self):
        return self.__amount
    def set_status(self):
        return self.__status
        
   

class Transfer(Transaction):
    transfer_id=0
    @ classmethod
    def generate_transfer_id(cls):
        cls.transfer_id+=1
        return f"TC-{cls.transfer_id:04d}"
    def __init__(self,transfer_id=None,date=None,reciever_account=None,account=None):
        super().__init__(transfer_id, "Transfer", date, account=account)
        self.transfer_id = self.t_id
        self.__amount = 0
        self.__status = "pending"
        self.reciever_account = reciever_account
        

    def __str__(self):
        return f"Transfer ID: {self.transfer_id}, Amount: {self.amount}, Date: {self.date}, To Account: {self.reciever_account}"    
    
    def get_amount(self,amount,):
        if amount > 500:
            self.__amount +=self.reciever_account
            
        return self.__status
#override method    
    def update_balance(self,account_number, receiver_account, amount):
        self.add_account(account_number)
        if amount <= 0:
            self.__status = "Failed: invalid amount"
            return False      

        if self.account.balance < amount:
            self.__status = "Failed: insufficient funds"
            return False
    
        self.account.update_balance(self.account.balance - amount)
        receiver_account.update_balance(receiver_account.balance + amount)
        self.__amount = amount
        self.reciever_account = receiver_account.account_number
        self.__status = "completed"
        return True
        
        

class Deposit(Transaction):
    deposit_id=0
    @classmethod
    def generate_deposit_id(cls):
        cls.deposit_id+=1
        return f"D.ID-{cls.deposit_id:04d}"
    
    def __init__(self,t_id=None,account_no=None,account=None):
        super().__init__(t_id, "Deposit", account_number=account_no, account=account)
        self.__amount = 0
        self.account_no = account_no
        self.__status = "pending"
    @property
    def get_amount(self,amount):
        if amount > 0:
            self.__amount +=amount
        return "successfull"
    def set_status(self):
        return self.__status
    
    def __str__(self):
        return f"Deposit ID: {self.t_id}, Amount: {self.amount}, Account: {self.account_no}"
#override method    
    def update_balance(self, account_number, amount):
        if amount <= 0:
            self.__status = "Failed: invalid amount"
            return False

        self.add_account(account_number)
        self.account.update_balance(self.account.balance + amount)
        self.__amount = amount
        self.account_no = self.account.account_number
        self.__status = "completed"
        return True

    
    

class Withdrawal(Transaction):
    withdraw_id=0
    @ classmethod
    def generate_withdraw_id(cls):
        cls.withdraw_id+=1
        return f"withdraw_id-{cls.withdraw_id:04d}"
    def __init__(self,t_id=None,account_no=None,account=None):
        super().__init__(t_id, "Withdrawal", account_number=account_no, account=account)
        self.account_no = account_no
        self.__amount = 0
        self.__status = "pending"
    def __str__(self):
        return f"Withdrawal ID: {self.t_id}, Amount: {self.amount}, Account: {self.account}"
    @property
    def set_amount(self):
        self.__amount
    @property
    def get_amount(self,amount):
        
        self.__amount -=amount
    def set_status(self):
        return self.__status      
#override method    
    def update_balance(self, account, amount):
        self.add_account(account)
        if amount <= 0:
            self.__status = "Failed: invalid amount"
            return False

        if self.account.balance < amount:
            self.__status = "Failed: insufficient funds"
            return False

        self.account.update_balance(self.account.balance - amount)
        self.__amount = amount
        self.account_no = self.account.account_number
        self.__status = "completed"
        return True


    
