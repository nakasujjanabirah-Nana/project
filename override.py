
class Transaction:
    def __init__(self,t_id,date,account_no,amount):
        self.t_id = t_id
        self.date = date
        self.account_no = account_no
        self.amount = 0
    def transaction_action(self,amount):
        print("Transaction successful")    

    def __str__(self):
        return f"Transaction ID: {self.transaction_id}, Amount: {self.amount}, Date: {self.date}, Account: {self.account}"

    

class Deposit(Transaction):
    def __init__(self,t_id,date,account_no):
        super().__init__(t_id,date,account_no)
        self.t_id = t_id
        self.amount = 0
        self.account_no = account_no

    def transaction_action(self,amount):
        if amount > 0:
            self.amount +=amount
        return "successfull"
        

    def __str__(self):
        return f"Deposit ID: {self.t_id}, Amount: {self.amount}, Account: {self.account_no}"

    

class Withdrawal(Transaction):
    def __init__(self,t_id,date,account_no,account_holder):
        super().__init__(t_id,date,account_no)
        self.t_id = t_id
        self.account_holder = account_holder
        self.account_no = account_no
        self.amount = 0
    def transaction_action(self,amount):
        if amount > 0:
            self.amount -= amount
        else:
            return "successful"
    def __str__(self):
        return f"Withdrawal ID: {self.t_id}, Amount: {self.amount}, Account: {self.account}"

   

class Transfer(Transaction):
    def __init__(self,t_id,date,account_no,account_holder,transfer_id,reciever_account,):
        super().__init__(t_id,date,account_no)
        
        self.transfer_id = transfer_id
        self.amount = 0
        self.date = date
        self.status = "pending"
        self.reciever_account = reciever_account
    def transfer_action(self,amount):
        if amount > 500:
            self.reciever_account += amount
        return "transfer successful"
         
                    

    def __str__(self):
        return f"Transfer ID: {self.transfer_id}, Amount: {self.amount}, Date: {self.date}, To Account: {self.reciever_account}"    

    


    
    


        



    
    
