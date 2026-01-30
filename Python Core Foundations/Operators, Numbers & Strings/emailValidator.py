mail=input("Enter your email: ")
state=0
for i in range(0,len(mail)):
    if mail[i]=='@':
        state=i
    if mail[i] in '%$!^&*()<>?#:;"\'+=':
        print("Invalid email")
        break
    
if not mail[0:state].isalnum() and not mail[state+1:-1].isalpha():
    print("Invalid email")
else:
    if mail.endswith('.com') or mail.endswith('.in'):
        if '@' in mail:
            print("Valid email")
        else:
            print("Invalid email")
    else:
        print("Invalid email")