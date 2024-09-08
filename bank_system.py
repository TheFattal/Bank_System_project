import datetime

# Central dictionary to store bank accounts
bank_accounts = {
    1001: {
        "first_name": "Alice",
        "last_name": "Smith",
        "id_number": "123456789",
        "balance": 2500.50,
        "transactions_to_execute": [],
        "transaction_history": []
    },
    1002: {
        "first_name": "Bob",
        "last_name": "Johnson",
        "id_number": "987654321",
        "balance": 3900.75,
        "transactions_to_execute": [],
        "transaction_history": []
    }
}


def current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def trx_perform(bank_dict, account_number):
    account = bank_dict.get(account_number)
    if not account:
        print("Account not found.")
        return

    now = current_time()
    transactions_to_execute = account["transactions_to_execute"]

    for transaction in transactions_to_execute[:]:
        _, src, dest, amount = transaction
        if src == account_number:
            if bank_dict[src]["balance"] >= amount:
                bank_dict[src]["balance"] -= amount
                bank_dict[dest]["balance"] += amount
                execution_time = now
                transaction_history = (transaction[0], transaction[1], transaction[2], transaction[3], execution_time)
                bank_dict[src]["transaction_history"].append(transaction_history)
                bank_dict[dest]["transaction_history"].append(transaction_history)
                account["transactions_to_execute"].remove(transaction)
            else:
                print(f"Insufficient funds in account {src}.")
        else:
            print(f"Transaction from account {src} to account {dest} is not valid for account {account_number}.")


def trx_create(bank_dict, source_account, target_account, amount):
    if source_account not in bank_dict or target_account not in bank_dict:
        print("One or both accounts do not exist.")
        return

    transaction = (current_time(), source_account, target_account, amount)
    bank_dict[source_account]["transactions_to_execute"].append(transaction)
    print("Transaction created successfully.")


def name_by_get(bank_dict, first_name):
    result = []
    first_name_lower = first_name.lower()
    for account in bank_dict.values():
        if first_name_lower in account["first_name"].lower():
            result.append(account)
    return result


# Existing functions remain unchanged
def add_transaction():
    while True:
        source_account = int(input("Enter source account number: "))
        if source_account in bank_accounts:
            break
        print("Account does not exist. Try again.")

    while True:
        destination_account = int(input("Enter destination account number: "))
        if destination_account in bank_accounts:
            break
        print("Account does not exist. Try again.")

    while True:
        try:
            amount = float(input("Enter amount to transfer: "))
            if amount > 0:
                break
            else:
                print("Amount must be positive. Try again.")
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")

    transaction = (current_time(), source_account, destination_account, amount)
    bank_accounts[source_account]["transactions_to_execute"].append(transaction)
    print("Transaction added successfully.")


def execute_transactions():
    while True:
        account_number = int(input("Enter account number to execute transactions: "))
        if account_number in bank_accounts:
            break
        print("Account does not exist. Try again.")

    account = bank_accounts[account_number]
    now = current_time()
    transactions_to_execute = account["transactions_to_execute"]
    for transaction in transactions_to_execute[:]:
        _, src, dest, amount = transaction
        if src == account_number:
            if bank_accounts[src]["balance"] >= amount:
                bank_accounts[src]["balance"] -= amount
                bank_accounts[dest]["balance"] += amount
                execution_time = now
                transaction_history = (transaction[0], transaction[1], transaction[2], transaction[3], execution_time)
                bank_accounts[src]["transaction_history"].append(transaction_history)
                bank_accounts[dest]["transaction_history"].append(transaction_history)
                account["transactions_to_execute"].remove(transaction)
            else:
                print(f"Insufficient funds in account {src}.")
        else:
            print(f"Transaction from account {src} to account {dest} is not valid for account {account_number}.")

    print("All transactions executed.")
    print(bank_accounts[account_number])


def print_reports():
    while True:
        print("\nReports Menu:")
        print("1. Print all bank accounts")
        print("2. Find and print a specific account by account number")
        print("3. Find an account by ID")
        print("4. Find an account by individual name")
        print("5. Print all accounts sorted by balance")
        print("6. Print all transactions sorted by date")
        print("7. Print all transactions that occurred today")
        print("8. Print all accounts with negative balance")
        print("9. Print the sum of balances of all accounts")
        print("10. Back to main menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            for account in bank_accounts.values():
                print(account)

        elif choice == "2":
            account_number = int(input("Enter account number: "))
            if account_number in bank_accounts:
                print(bank_accounts[account_number])
            else:
                print("Account does not exist.")

        elif choice == "3":
            id_number = input("Enter ID number: ")
            found = False
            for account in bank_accounts.values():
                if account["id_number"] == id_number:
                    print(account)
                    found = True
            if not found:
                print("No account found with that ID number.")

        elif choice == "4":
            name = input("Enter first name to search: ").lower()
            found = False
            for account in bank_accounts.values():
                if name in account["first_name"].lower():
                    print(account)
                    found = True
            if not found:
                print("No accounts found with that name.")

        elif choice == "5":
            sorted_accounts = sorted(bank_accounts.values(), key=lambda x: x["balance"])
            for account in sorted_accounts:
                print(account)

        elif choice == "6":
            all_transactions = []
            for account in bank_accounts.values():
                all_transactions.extend(account["transaction_history"])
            sorted_transactions = sorted(all_transactions, key=lambda x: x[4])
            for transaction in sorted_transactions:
                print(transaction)

        elif choice == "7":
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            all_transactions = []
            for account in bank_accounts.values():
                all_transactions.extend(account["transaction_history"])
            today_transactions = [t for t in all_transactions if t[4].startswith(today)]
            for transaction in today_transactions:
                print(transaction)

        elif choice == "8":
            negative_balance_accounts = [account for account in bank_accounts.values() if account["balance"] < 0]
            for account in negative_balance_accounts:
                print(account)

        elif choice == "9":
            total_balance = sum(account["balance"] for account in bank_accounts.values())
            print(f"Total balance of all accounts: {total_balance}")

        elif choice == "10":
            break

        else:
            print("Invalid choice. Try again.")


def open_new_account():
    while True:
        new_account_number = int(input("Enter new account number: "))
        if new_account_number not in bank_accounts:
            break
        print("Account number already exists. Try again.")

    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    id_number = input("Enter ID number: ")
    while True:
        try:
            initial_balance = float(input("Enter initial balance: "))
            if initial_balance >= 0:
                break
            else:
                print("Balance must be non-negative. Try again.")
        except ValueError:
            print("Invalid balance. Please enter a numeric value.")

    bank_accounts[new_account_number] = {
        "first_name": first_name,
        "last_name": last_name,
        "id_number": id_number,
        "balance": initial_balance,
        "transactions_to_execute": [],
        "transaction_history": []
    }
    print("New account created successfully.")


def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Add a new transaction")
        print("2. Execute all pending transactions")
        print("3. Report interface")
        print("4. Open a new account")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_transaction()

        elif choice == "2":
            execute_transactions()

        elif choice == "3":
            print_reports()

        elif choice == "4":
            open_new_account()

        elif choice == "5":
            print("Exiting the system.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main_menu()
