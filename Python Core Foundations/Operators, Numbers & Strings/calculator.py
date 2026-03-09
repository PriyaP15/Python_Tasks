equ=input().split()


num1=int(equ[0])
operator=equ[1]
num2=int(equ[2])

if operator=='+':
    print("Output: ",num1+num2)
elif operator=='-':
    print("Output: ",num1-num2)
elif operator=='*':
    print("Output: ",num1*num2)
elif operator=='/':
    print("Output: ",num1/num2)
elif operator=='**':
    print("Output: ",num1**num2)
else:
    print("Invalid operator")