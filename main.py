
import json
import uuid

from datetime import datetime

from project import Branch,Client,Account,Transaction,Transfer,Withdrawal,Deposit,Transfer

branch = []
while True:
    branch_name = input("Enter branch name: ")
    branch_code = "BR-" + uuid.uuid4().hex[:8].upper()
    print("Generated branch code:", branch_code)
    address = input("Enter branch address: ")
    bank_manager = input("Enter bank manager name: ")
    contact = input("Enter contact : ")

    b1 = Branch(branch_name, branch_code, address, bank_manager, contact)

    new_branch = {
        
        "branch_name": branch_name,
        "branch_code": branch_code,
        "address": address,
        "bank_manager": bank_manager,
        "contact": contact
    }
    try:
        with open("branch.json", "r") as file:
            branch_data = json.load(file)
    except FileNotFoundError:
        branch_data = {}
    branch_data.setdefault("branches", []).append(new_branch)
    with open("branch.json", "w") as file:
        json.dump(branch_data, file, indent=4)
    if input("Do you want to add more branches? (y/n): ").lower() == "y":
        continue
    else:
        break

client = []
while True:
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    address = input("Enter address: ")
    Id = "CL-" + uuid.uuid4().hex[:8].upper()
    print("Generated client ID:", Id)
    contact = input("Enter contact: ")
    gender = input("Enter gender: ")
    account_number = "ACC-" + uuid.uuid4().hex[:8].upper()
    print("Generated account number:", account_number)

    c1 = Client(first_name, last_name, address, Id, contact, gender, account_number)

    new_client = {
        "first_name": first_name,
        "last_name": last_name,
        "address": address,
        "Id": Id,
        "contact": contact,
        "gender": gender,
        "account_number": account_number,
    }
    try:
        with open("client.json", "r") as file:
            client = json.load(file)
    except FileNotFoundError:
        client = []
    client.append(new_client)
    with open("client.json", "w") as file:
        json.dump(client, file, indent=4)
    if input("Do you want to add more clients? (y/n): ").lower() == "y":
        continue
    else:
        break


account = []
while True:
    print("Creating account:", account_number)
    account_type = input("Enter account type: ")
    account_holder = input("Enter account holder: ")
    date = input("Enter date: ")
    account_branch = input("Enter branch name: ")

    a1 = Account(first_name, last_name, address, Id, contact, gender, account_number, account_type, account_holder, date)

    new_account ={
    
            'account_number': account_number,
            'account_type': account_type,
            'account_holder': account_holder,
            'branch': account_branch,
            'balance': 0,
            'status': "in progress",
            'date': date

        }
    try:
        with open("branch.json", "r") as file:
            branch_data = json.load(file)
    except FileNotFoundError:
        branch_data = {}
    branch_data.setdefault("accounts", []).append(new_account)
    with open("branch.json", "w") as file:
        json.dump(branch_data, file, indent=4)
    if input("Do you want to add more accounts? (y/n): ").lower() == "y":
        continue
    else:
        break   
   
transactions = []
while True:
    print("\nChoose a transaction:")
    print("1. Deposit")
    print("2. Withdrawal")
    print("3. Transfer")

    option = input("Enter your choice (1-3): ")
    if option == "1":
        transaction_type = "deposit"
    elif option == "2":
        transaction_type = "withdrawal"
    elif option == "3":
        transaction_type = "transfer"
    else:
        print("Invalid choice. Please choose 1, 2, or 3.")
        continue

    account_number = input("Enter account number: ")
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Please enter a valid amount.")
        continue
    if amount <= 0:
        print("Amount must be greater than zero.")
        continue

    receiver_account = ""
    if transaction_type == "transfer":
        receiver_account = input("Enter receiving account number: ")
        if receiver_account == account_number:
            print("You cannot transfer to the same account.")
            continue

    try:
        with open("branch.json", "r") as file:
            branch_data = json.load(file)
    except FileNotFoundError:
        print("No account data was found.")
        continue

    accounts = branch_data.get("accounts", [])
    source_account = None
    destination_account = None
    for saved_account in accounts:
        if saved_account.get("account_number") == account_number:
            source_account = saved_account
        if saved_account.get("account_number") == receiver_account:
            destination_account = saved_account

    if source_account is None:
        print("Account not found.")
        continue
    if transaction_type == "transfer" and destination_account is None:
        print("Receiving account not found.")
        continue

    balance = float(source_account.get("balance", 0))
    if transaction_type in ("withdrawal", "transfer") and amount > balance:
        print("Not enough money in the account.")
        continue

    if transaction_type == "deposit":
        source_account["balance"] = balance + amount
    else:
        source_account["balance"] = balance - amount
        if transaction_type == "transfer":
            destination_account["balance"] = float(destination_account.get("balance", 0)) + amount

    transaction_id = str(uuid.uuid4())
    receipt_id = str(uuid.uuid4())
    date = datetime.now().isoformat(timespec="seconds")
    transaction = Transaction(
        transaction_id,
        transaction_type,
        date,
        account_number
    )

    transaction_data = {
        "transaction_id": transaction_id,
        "receipt_id": receipt_id,
        "transaction_type": transaction_type,
        "date": date,
        "account_number": account_number,
        "amount": amount
    }

    if transaction_type == "transfer":
        transaction_data["receiver_account"] = receiver_account

    with open("branch.json", "w") as file:
        json.dump(branch_data, file, indent=4)

    try:
        with open("transactions.json", "r") as file:
            transactions = json.load(file)
    except FileNotFoundError:
        transactions = []

    transactions.append(transaction_data)
    with open("transactions.json", "w") as file:
        json.dump(transactions, file, indent=4)

    print("\nTransaction saved.")
    print("Transaction ID:", transaction_id)
    print("Receipt ID:", receipt_id)
    print("New balance:", source_account["balance"])

    if input("Do you want to make another transaction? (y/n): ").lower() != "y":
        break
     