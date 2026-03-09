cart={}
print("Enter 1: To add item \nEnter 2: To remove item\nEnter 3: To view cart\nEnter 0: To exit")

option = int(input("Enter option: "))
while option != 0:
    if option == 1:
        print("Menu : \n\tOnion - 30/kg\n\tTomato - 20/kg\n\tPotato - 40/kg\n\tApple - 100/kg\n\tBanana - 50/kg\n\tOrange - 60/kg")
        item = input("Enter item: ").lower()
        if item in cart:
            qty = int(input("Enter quantity: "))
            if item=="onion":
                cart["onion"]+=30*qty
            elif item=="tomato":
                cart["tomato"]+=20*qty
            elif item=="potato":
                cart["potato"]+=40*qty
            elif item=="apple":
                cart["apple"]+=100*qty
            elif item=="banana":
                cart["banana"]+=50*qty
            elif item=="orange":
                cart["orange"]+=60*qty
            else:
                print("Invalid item")
        else:
            qty = int(input("Enter quantity: "))
            if item=="onion":
                cart["onion"]=30*qty
            elif item=="tomato":
                cart["tomato"]=20*qty
            elif item=="potato":
                cart["potato"]=40*qty
            elif item=="apple":
                cart["apple"]=100*qty
            elif item=="banana":
                cart["banana"]=50*qty
            elif item=="orange":
                cart["orange"]=60*qty
            else:
                print("Invalid item")
    elif option == 2:
        item = input("Enter item: ").lower()
        qty = int(input("Enter quantity: "))
        if item in cart:
            if item=="onion":
                cart["onion"]-=30*qty
            elif item=="tomato":
                cart["tomato"]-=20*qty
            elif item=="potato":
                cart["potato"]-=40*qty
            elif item=="apple":
                cart["apple"]-=100*qty
            elif item=="banana":
                cart["banana"]-=50*qty
            elif item=="orange":
                cart["orange"]-=60*qty
        else:
            print("Invalid item")
    elif option == 3:
        print(cart)
    else:
        print("Invalid option")
    option = int(input("Enter option: "))