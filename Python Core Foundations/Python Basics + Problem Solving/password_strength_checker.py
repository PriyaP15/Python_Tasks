password=input("Enter your password: ")

has_num=0
has_upper=0

if len(password)<=3:
    print("Not a strong password")
else:
    for i in password:
        if i.isnumeric():
            has_num+=1
        elif i.isupper():
            has_upper+=1
if has_num<1 and has_upper<1:
    print("Invalid password")
elif has_num<1 or has_upper<1:
    print("weak password")
elif has_num>=1 and has_upper>=1:
    print("medium password")
else:
    print("strong password")
