import math

add = lambda x,y: x+y
subtract = lambda x,y: x-y
multiply = lambda x,y: x*y
divide = lambda x,y: print("cannot be divide by zero") if y==0 else x/y
mod = lambda x,y: print("cannot be mod by zero") if y==0 else x%y
power = lambda x,y: x**y
floor = lambda x,y: x//y

square_root = lambda x: math.sqrt(x)
cube_root = lambda x: x**(1/3)
factorial = lambda x: math.factorial(x)
log = lambda x: math.log(x)

while True:
    print("1. Two number operations")
    print("2. One number operations")
    print("3. Exit")

    option = input("Enter option: ")
    match option:
        case '1':
            a=float(input("Enter value 1: "))
            b=float(input("Enter value 2: "))
            print("1. Add")
            print("2. Subtract")
            print("3. Multiply")
            print("4. Divide")
            print("5. Modulo")
            operation = input("Enter operation no: ")
            if operation == '1':
                print(add(a,b))
            elif operation == '2':
                print(subtract(a,b))
            elif operation == '3':
                print(multiply(a,b))
            elif operation == '4':
                print(divide(a,b))
            elif operation == '5':
                print(mod(a,b))
            else:
                print("Invalid operation")
        
        case '2':
            a=int(input("Enter value: "))
            print("1. Square root")
            print("2. Cube root")
            print("3. Factorial")
            print("4. Logarithm")
            operation = input("Enter operation no: ")
            if operation == '1':
                print(square_root(a))
            elif operation == '2':
                print(cube_root(a))
            elif operation == '3':
                print(factorial(a))
            elif operation == '4':
                print(log(a))
            else:
                print("Invalid operation")
        
        case '3':
            print("Exiting")
            break
        
        case _:
            print("Invalid option") 

    print()
