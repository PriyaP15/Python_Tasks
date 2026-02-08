import json

FILE_NAME = "bank_dtls.json"

class Bank:
    def __init__(self):
        self.accounts = {}
        self.load()

    def load(self):
        try:
            with open(FILE_NAME, "r") as f:
                content = f.read().strip()
                if content:
                    self.accounts = json.loads(content)
                else:
                    self.accounts = {}
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            self.accounts = {}


    def save(self):
        with open(FILE_NAME, "w") as f:
            json.dump(self.accounts, f, indent=4)

    def account_exists(self, acc_no):
        return str(acc_no) in self.accounts

class Account:
    def __init__(self, bank, acc_no):
        self.bank = bank
        self.acc_no = str(acc_no)
        self.data = bank.accounts[self.acc_no]

    def __check_pin(self, pin):
        return self.data["PIN"] == pin

    def __is_active(self):
        return self.data["Status"]

    def deposit(self, amount):
        if not self.__is_active():
            print("Account closed")
            return

        if amount > 0:
            self.data["Balance"] += amount
            self.data["Statement"].append(f"Deposited  {amount}")
            self.bank.save()
            print(f"Deposited  {amount}")

    def withdraw(self, amount, pin):
        if not self.__is_active():
            print("Account closed")
            return

        if not self.__check_pin(pin):
            print("Wrong PIN")
            return

        if amount <= self.data["Balance"]:
            self.data["Balance"] -= amount
            self.data["Statement"].append(f"Withdrawn  {amount}")
            self.bank.save()
            print(f"Withdrawn  {amount}")
        else:
            print("Insufficient balance")

    def balance(self, pin):
        if self.__check_pin(pin):
            print("Balance:", self.data["Balance"])
        else:
            print("Wrong PIN")

    def change_pin(self, old_pin, new_pin):
        if self.__check_pin(old_pin) and len(new_pin) == 4 and new_pin.isdigit():
            self.data["PIN"] = new_pin
            self.bank.save()
            print("PIN changed")
        else:
            print("Invalid PIN")

    def transfer(self, to_acc, amount, pin):
        if not self.__is_active():
            print("Account closed")
            return

        if not self.__check_pin(pin):
            print("Wrong PIN")
            return

        if not self.bank.account_exists(to_acc):
            print("Receiver not found")
            return

        if not self.bank.accounts[str(to_acc)]["Status"]:
            print("Receiver account closed")
            return

        if amount > self.data["Balance"]:
            print("Insufficient balance")
            return

        self.data["Balance"] -= amount
        self.bank.accounts[str(to_acc)]["Balance"] += amount

        self.data["Statement"].append(f"Transferred  {amount} to {to_acc}")
        self.bank.accounts[str(to_acc)]["Statement"].append(f"Received  {amount} from {self.acc_no}")

        self.bank.save()
        print("Transfer successful")

    def mini_statement(self):
        print("\n Statement ")
        for tx in self.data["Statement"][-5:]:
            print(tx)

    def close_account(self, pin):
        if self.__check_pin(pin):
            self.data["Status"] = False
            self.data["Statement"].append("Account closed by user")
            self.bank.save()
            print("Account closed successfully")
        else:
            print("Wrong PIN")

class Manager:
    def __init__(self, bank):
        self.bank = bank

    def create_account(self, acc_no, name, pin, balance=0):
        acc_no = str(acc_no)
        if acc_no in self.bank.accounts:
            print("Account already exists")
            return

        self.bank.accounts[acc_no] = {
            "Name": name,
            "PIN": pin,
            "Balance": balance,
            "Status": True,
            "Statement": []
        }
        self.bank.save()
        print("Account created")

    def freeze_account(self, acc_no):
        acc_no = str(acc_no)
        if acc_no in self.bank.accounts:
            self.bank.accounts[acc_no]["Status"] = False
            self.bank.save()
            print("Account frozen")

    def close_account(self, acc_no):
        acc_no = str(acc_no)
        if acc_no in self.bank.accounts:
            del self.bank.accounts[acc_no]
            self.bank.save()
            print("Account permanently deleted")

    def view_all_accounts(self):
        for acc, data in self.bank.accounts.items():
            print(acc, data)


bank = Bank()

while True:
    role = int(input("\n1.User  2.Manager  3.Exit : "))

    if role == 1:
        acc_no = input("Account Number: ")
        pin = input("PIN: ")

        if not bank.account_exists(acc_no):
            print("Account not found")
            continue

        acc = Account(bank, acc_no)
        if acc.data["PIN"] != pin:
            print("Wrong PIN")
            continue

        while True:
            print("1. Deposit\n2. Withdraw\n3. Balance\n4. Change PIN\n5. Transfer\n6. Statement\n7. Close Account\n0. Exit")

            ch = int(input("Choice: "))

            if ch == 1:
                acc.deposit(float(input("Amount: ")))

            elif ch == 2:
                acc.withdraw(float(input("Amount: ")), pin)

            elif ch == 3:
                acc.balance(pin)

            elif ch == 4:
                new_pin = input("New PIN: ")
                acc.change_pin(pin, new_pin)
                pin = new_pin

            elif ch == 5:
                to = input("Receiver Acc No: ")
                amt = float(input("Amount: "))
                acc.transfer(to, amt, pin)

            elif ch == 6:
                acc.mini_statement()

            elif ch == 7:
                acc.close_account(pin)
                break

            elif ch == 0:
                break


    elif role == 2:
        manager = Manager(bank)

        while True:
            print("1. Create Account\n2. Freeze Account\n3. Close Account\n4. View All Accounts\n0. Exit")

            ch = int(input("Choice: "))

            if ch == 1:
                manager.create_account(
                    input("Acc No: "),
                    input("Name: "),
                    input("PIN: "),
                    float(input("Balance: "))
                )

            elif ch == 2:
                manager.freeze_account(input("Acc No: "))

            elif ch == 3:
                manager.close_account(input("Acc No: "))

            elif ch == 4:
                manager.view_all_accounts()

            elif ch == 0:
                break

    elif role == 3:
        print("Exiting..")
        print()
        break
