class Account:
    def __init__(self, account_number, account_holder, balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance
    
    @balance.setter
    def balance(self, value):
        if(value < 0):
            print("Balance cannot be negative.")
            return
        self.__balance = value

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def transfer(self, amount, target_account):
        if self.withdraw(amount):
            target_account.deposit(amount)
            return True
        return False

    def __str__(self):
        return f"Account Number: {self.account_number}, Holder: {self.account_holder}, Balance: {self.balance}"


class Transaction:
    def __init__(self, transaction_id, transaction_type, amount, account_number):
        self.transaction_id = transaction_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.account_number = account_number

    def __str__(self):
        return f"[{self.transaction_id}] {self.transaction_type} - {self.amount} (Account: {self.account_number})"


class Bank:
    def __init__(self):
        self.accounts = {}
        self.transactions = []
        self.transaction_counter = 1

    def create_account(self, account_number, account_holder, initial_balance=0):
        if account_number in self.accounts:
            print("Account already exists!")
            return
        self.accounts[account_number] = Account(account_number, account_holder, initial_balance)
        print("Account created successfully.")

    def get_account(self, account_number):
        return self.accounts.get(account_number)

    def record_transaction(self, transaction_type, amount, account_number):
        transaction = Transaction(
            self.transaction_counter,
            transaction_type,
            amount,
            account_number
        )
        self.transactions.append(transaction)
        self.transaction_counter += 1

    def show_all_accounts(self):
        for account in self.accounts.values():
            print(account)

    def show_all_transactions(self):
        for transaction in self.transactions:
            print(transaction)




bank = Bank()

while True:
    print("\n1.Create  2.Deposit  3.Withdraw  4.Transfer")
    print("5.Account Details  6.All Accounts  7.All Transactions  8.Exit")

    try:
        option = int(input("Enter option: "))
    except ValueError:
        print("Please enter a valid number.")
        continue

    match option:
        case 1:
            acc_no = input("Account number: ")
            name = input("Account holder: ")
            balance = int(input("Initial balance: "))
            bank.create_account(acc_no, name, balance)

        case 2:
            acc_no = input("Account number: ")
            amount = int(input("Amount: "))
            acc = bank.get_account(acc_no)
            if acc and acc.deposit(amount):
                bank.record_transaction("Deposit", amount, acc_no)
                print("Deposit successful.")
            else:
                print("Deposit failed.")

        case 3:
            acc_no = input("Account number: ")
            amount = int(input("Amount: "))
            acc = bank.get_account(acc_no)
            if acc and acc.withdraw(amount):
                bank.record_transaction("Withdraw", amount, acc_no)
                print("Withdrawal successful.")
            else:
                print("Insufficient balance or invalid account.")

        case 4:
            from_acc = input("From account: ")
            to_acc = input("To account: ")
            amount = int(input("Amount: "))
            acc1 = bank.get_account(from_acc)
            acc2 = bank.get_account(to_acc)
            if acc1 and acc2 and acc1.transfer(amount, acc2):
                bank.record_transaction("Transfer", amount, from_acc)
                print("Transfer successful.")
            else:
                print("Transfer failed.")

        case 5:
            acc_no = input("Account number: ")
            acc = bank.get_account(acc_no)
            print(acc if acc else "Account not found.")

        case 6:
            bank.show_all_accounts()

        case 7:
            bank.show_all_transactions()

        case 8:
            print("Exiting...")
            break

        case _:
            print("Invalid option.")
