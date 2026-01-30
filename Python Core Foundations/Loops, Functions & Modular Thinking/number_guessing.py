import random

def developer(level):
    
    while 1:
        print("Enter 1: To update level")
        print("Enter 2: To view level")
        print("Enter 3: To delete level")
        print("Enter 4: To exit")
        print("Enter 5: To play")
        option = input("Enter option: ")
        match option:
            case '1':
                try:
                    lower=int(input("Enter lower limit: "))
                    upper=int(input("Enter upper limit: "))
                    if lower>=upper or lower<0 or upper<0:
                        print("Lower limit should be less than upper limit")
                        continue

                    tries=int(input("Enter number of tries: "))
                    if tries<1 or tries>(upper-lower+1)/2:
                        print("Number of tries should be between 1 and",int((upper-lower+1)/2))
                        continue

                    level[input("Enter level name: ")]=[lower,upper,tries]
                    print("Level added")
                except ValueError as e:
                    print("Invalid input")
            case '2':
                print(level)
            case '3':
                print("Available levels: ",level.keys())
                level.pop(input("Enter level name: "))
                print("Level deleted")
            case '4':
                print("Exiting")
                break
            case '5':
                user(level)
            case _:
                print("\nInvalid option")
        print("-->Press \"Enter\" to continue\n-->Press \"Space and Enter\" to exit")
        if input() != "":
            break

    else:
        print("Invalid option")
        
    

def user(level):
    if len(level)==0:
        print("No levels available\nCreate levels to play")
        return
    else:
        while 1:
            print("-->Press \"Enter\" to continue\n-->Press \"Space and Enter\" to exit")
            mode=input("Press 0 to go fo developer mode, 1 to player mode, 2 to quit :")
            if mode=="0":
                developer(level)
                continue
            elif mode == "1":
                print("Available levels:",level.keys())
                try:
                    lower,upper,tries=level[input("Enter level name: ")]
                except KeyError as e:
                    print("Invalid level")
                num = random.randint(lower,upper)
                for i in range(tries):
                    try:
                        guess = int(input(f"Enter your guess from {lower} to {upper} with {tries} tries:"))
                    except ValueError as e:
                        print("Invalid guess")
                        continue
                    if guess<lower or guess>upper:
                        print("Invalid guess")
                        continue
                    elif guess==num:
                        print("\nYou won\n")
                        break
                    elif guess<num:
                        print(f"The number is greater than {guess}")
                        print("Try again")
                        tries-=1
                        print(f"You have {tries} chances left")
                        if tries==0:
                            print("\nYou lost\n")
                            print(f"The number is {num}")
                            break
                    elif guess>num:
                        print(f"The number is lesser than {guess}")
                        print("Try again")
                        tries-=1
                        print(f"You'r have {tries} chances left")
                        if tries==0:
                            print("\nYou lost\n")
                            print(f"The number is {num}")
                            break
                pass
            elif mode == "2":
                return
            

person=input("Enter 1: To play\nEnter 2: To Developer\n")
level={}
if person=='1':
    user(level)
elif person=='2':
    developer(level)
else:
    print("Invalid option")