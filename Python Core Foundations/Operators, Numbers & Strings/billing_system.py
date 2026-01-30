print("Enter 1: For Vegetables\nEnter 2: For Fruits")

option = int(input("\nEnter your option: "))
if option==1:
    print("Onion - 30/kg\nTomato - 20/kg\nPotato - 40/kg")
    veg = input("Enter the vegetable: ")
    
    if veg.lower()=="onion":
        qty = int(input("Enter the quantity in KG: "))
        print(f"Total: {30*qty}")
    elif veg.lower()=="tomato":
        qty = int(input("Enter the quantity in KG: "))
        print(f"Total: {20*qty}")
    elif veg.lower()=="potato":
        qty = int(input("Enter the quantity in KG: "))
        print(f"Total: {40*qty}")
    else:
        print("Invalid vegetable")
elif option==2:
    print("Apple - 100/kg\nBanana - 50/kg\nOrange - 60/kg")
    fruit = input("Enter the fruit: ")
    
    if fruit.lower()=="apple":
        qty = int(input("Enter the quantity in KG: "))
        print(f"Total: {100*qty}")
    elif fruit.lower()=="banana":
        qty = int(input("Enter the quantity in KG: "))
        print(f"Total: {50*qty}")
    elif fruit.lower()=="orange":
        qty = int(input("Enter the quantity in KG: "))
        print(f"Total: {60*qty}")
    else:
        print("Invalid fruit")
else:
    print("Invalid option")