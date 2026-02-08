import json
import os

file="inventory.json"

def load_inventory():
    if not os.path.exists(file):
        return {}
    with open(file,"r") as f:
        return json.load(f)
    
def dump_inventory(inventory):
    with open(file,"w") as f:
        json.dump(inventory,f,indent=4)



class ProductInventory:

    def __init__(self,product_id,product_name,price,quantity,is_active=True):
        self.product_id=product_id
        self.product_name=product_name
        self.price=price
        self.quantity=quantity
        self.is_active=is_active

    def in_stock(self):
        return self.quantity>0
    
    def increase_stock(self,amount):
        if amount<=0:
            raise Exception("Must be positive")
        self.quantity+=amount

    def decrease_stock(self,amount):
        if amount<=0:
            raise Exception("Must be positive")
        if amount>self.quantity:
            raise Exception("Amount should be less than or equal to quantity")
        self.quantity-=amount

    def deactivate(self):
        self.is_active=False      

    def to_dict(self):
        return{
            "product_id":self.product_id,
            "product_name":self.product_name,
            "price":self.price,
            "quantity":self.quantity,
            "is_active":self.is_active
        }
    
    @staticmethod
    def from_dict(data):
        return ProductInventory(data["product_id"],data["product_name"],data["price"],data["quantity"],data["is_active"])

def userSystem():
    while True:
        print("1. View Product Details")
        print("2. Buy Products")
        print("3. Exit")

        choice=input("Enter choice: ")

        inventory=load_inventory()

        try:
            if choice=="1":
                with open("inventory.json","r") as file:
                    a=json.load(file)
                    print(a)
                    print()

            elif choice=="2":
                product_id=input("Enter product id: ")
                if product_id not in inventory:
                    print("Product not found")
                    print()
                    continue

                qty=int(input("Enter quantity: "))

                product=ProductInventory.from_dict(inventory[product_id])
                product.decrease_stock(qty)
                print(f"Amount: {inventory[product_id]["price"]*qty}")
                inventory[product_id]=product.to_dict()
                dump_inventory(inventory)
                

            elif choice=="3":
                print("Exiting....")
                print()
                break

            else:
                print("Invalid choice")
                print()

        except Exception as e:
            print("Error: ",e)
    pass
    
def inventorySystem():
    while True: 
        print("INVENTORY MANAGER")
        print("1. Add Product")
        print("2. View Product Details")
        print("3. Check Stock")
        print("4. Increase Stock")
        print("5. Delete Product")
        print("6. Exit")

        choice=input("Enter choice : ")

        inventory=load_inventory()

        try:
            if choice=="1":
                product_id=input("Enter Product ID: ")
                if product_id in inventory:
                    print("Product already exists")
                    continue

                product_name=input("Enter Product Name: ")
                price=float(input("Enter Price: "))
                quantity=int(input("Enter Quantity: "))
                product=ProductInventory(product_id,product_name,price,quantity)

                inventory[product_id]=product.to_dict()
                dump_inventory(inventory)
                print("Product added")
                print()

            elif choice=="2":
                product_id=input("Enter product ID: ")
                if product_id not in inventory:
                    print("Product not found")
                    continue
                product=ProductInventory.from_dict(inventory[product_id])

                if not product.is_active:
                    print("Product is deactivated")
                    continue
                print(product.to_dict())
                print()

            elif choice=="3":
                product_id=input("Enter product id: ")
                if product_id not in inventory:
                    print("Product not found")
                    continue
                product=ProductInventory.from_dict(inventory[product_id])
                print(f"Product name: {product.product_name}")
                print(f"Price: {product.price}")
                print(f"Quantity: {product.quantity}")
                print()

            elif choice=="4":
                product_id=input("Enter product id: ")
                if product_id not in inventory:
                    print("Product not found")
                    continue

                amount=int(input("Enter amount: "))
                
                product=ProductInventory.from_dict(inventory[product_id])
                product.increase_stock(amount)
                inventory[product_id]=product.to_dict()
                dump_inventory(inventory)
                print("Stock increased")
                print()

            elif choice=="5":
                product_id=input("Enter product id: ")
                if product_id not in inventory:
                    print("Product not found")
                    continue

                product=ProductInventory.from_dict(inventory[product_id])
                product.deactivate()
                inventory[product_id]=product.to_dict()
                dump_inventory(inventory)
                print()

            elif choice=="6":
                print("Exiting....")
                print()
                break

            else:
                print("Invalid choice")
                print()

        except Exception as e:
            print("Error: ",e)


while True:
    print("1. Seller")
    print("2. Buyer")
    print("3. Exit")
    option=input("Enter option: ")
    if option=='1':
        inventorySystem()
    elif option == '2':
        userSystem()
    elif option == '3':
        print("Exiting")
        break
    else:
        print("Invalid option")