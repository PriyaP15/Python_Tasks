name=input("Enter your name: ")
subject1=int(input("Enter subject1 mark: "))
subject2=int(input("Enter subject2 mark: "))
subject3=int(input("Enter subject3 mark: "))

if subject1<=100 and subject2<=100 and subject3<=100:
    avgMark = (subject1+subject2+subject3)/3
    if avgMark>=80:
        print("Grade A")
    elif avgMark>=50:
        print("Grade B")
    elif avgMark>=30:
        print("Grade C")
    elif avgMark<30 and avgMark>=0:
        print("Fail")
    else:
        print("Invalid mark")
else:
    print("Invalid mark")