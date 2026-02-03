class Product:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.__price = price
        self.__quantity = quantity

    @property
    def price(self):
        return self.__price
    
    @price.setter
    def price(self, value):
        if(value < 0):
            print("Price cannot be negative.")
            return
        self.__price = value
        
    @property
    def quantity(self):
        return self.__quantity
    
    @quantity.setter
    def quantity(self, value):
        if(value < 0):
            print("Quantity cannot be negative.")
            return
        self.__quantity = value

    def restock(self, amount):
        if amount > 0:
            self.quantity += amount
            return True
        return False

    def sell(self, amount):
        if amount > 0 and self.quantity >= amount:
            self.quantity -= amount
            return True
        return False

    def update_price(self, new_price):
        if new_price > 0:
            self.price = new_price
            return True
        return False

    def is_low_stock(self):
        return self.quantity < 10

    def __str__(self):
        status = "Low Stock" if self.is_low_stock() else "In Stock"
        return f"Product ID: {self.product_id} |Product Name: {self.name} |Product Price: {self.price} | Qty: {self.quantity} | Status: {status}"


class Sale:
    def __init__(self, product_id, name, quantity, total_price):
        self.product_id = product_id
        self.name = name
        self.quantity = quantity
        self.total_price = total_price

    def __str__(self):
        return f"Sold {self.quantity} x {self.name} = {self.total_price}"


class Inventory:
    def __init__(self):
        self.products = {}
        self.sales = []
        self.total_revenue = 0

    def add_product(self, product_id, name, price, quantity):
        if product_id in self.products:
            print("Product already exists.")
            return
        self.products[product_id] = Product(product_id, name, price, quantity)
        print("Product added successfully.")

    def get_product(self, product_id):
        return self.products.get(product_id)

    def sell_product(self, product_id, quantity):
        product = self.get_product(product_id)
        if not product:
            print("Product not found.")
            return

        if product.sell(quantity):
            total = quantity * product.price
            self.sales.append(Sale(product_id, product.name, quantity, total))
            self.total_revenue += total
            print(f"Sale successful. Bill Amount: {total}")
        else:
            print("Insufficient stock.")

    def restock_product(self, product_id, quantity):
        product = self.get_product(product_id)
        if product and product.restock(quantity):
            print("Product restocked.")
        else:
            print("Restock failed.")

    def update_product_price(self, product_id, new_price):
        product = self.get_product(product_id)
        if product and product.update_price(new_price):
            print("Price updated.")
        else:
            print("Update failed.")

    def show_products(self):
        for product in self.products.values():
            print(product)

    def show_sales(self):
        for sale in self.sales:
            print(sale)
        print(f"Total Revenue: {self.total_revenue}")

inventory = Inventory()

while True:
    print("1.Add Product")
    print("2.Sell Product")
    print("3.Restock")
    print("4.Update Price")
    print("5.Show Products")
    print("6.Show Sales")
    print("7.Exit")

    option = int(input("Enter option: "))

    match option:
        case 1:
            product_id = input("Enter product id: ")
            name = input("Enter product name: ")
            price = int(input("Enter product price: "))
            quantity = int(input("Enter product quantity: "))
            inventory.add_product(product_id, name, price, quantity)

        case 2:
            product_id = input("Enter product id: ")
            quantity = int(input("Enter product quantity: "))
            inventory.sell_product(product_id, quantity)
            
        case 3:
            product_id = input("Enter product id: ")
            quantity = int(input("Enter product quantity: "))
            inventory.restock_product(product_id, quantity)
            
        case 4:
            product_id = input("Enter product id: ")
            new_price = int(input("Enter new price: "))
            inventory.update_product_price(product_id, new_price)
            
        case 5:
            inventory.show_products()
            
        case 6:
            inventory.show_sales()
            
        case 7:
            print("Exiting...")
            break
            
        case _:
            print("Invalid option.")