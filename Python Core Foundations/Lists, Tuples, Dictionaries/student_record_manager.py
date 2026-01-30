record={}
count=0
print("Enter 1: To print all the records\nEnter 2: To print a specific record\nEnter 3: To add a record\nEnter 4: To remove a record\nEnter 5: To update a record\nEnter 0: To exit")
option = int(input("\nEnter your option: "))

while option != 0:
    if option == 1:
        print(record)

    elif option == 2:
        rollno = int(input("Enter rollno: "))
        print(record[rollno])

    elif option == 3:
        count+=1
        record[count]={"name" : input("Enter name:"),
                      "age" : int(input("Enter age:")),
                      "course" : input("Enter course:"),
                      "marks" : int(input("Enter marks:"))}
        print("Record added")

    elif option ==4:
        rollno = int(input("Enter rollno to remove :"))
        print(f"Record for {rollno} is removed")
        record.pop(rollno)

    else:
        rollno = int(input("Enter rollno to update:"))
        num=int(input("Enter 1: To update name\nEnter 2: To update age\nEnter 3: To update course\nEnter 4: To update marks\n"))
        if num==1:
            record[rollno]["name"]=input("Enter name to update: ")
        elif num==2:
            record[rollno]["age"]=input("Enter age: ")
        elif num==3:
            record[rollno]["course"]=input("Enter course: ")
        elif num==4:
            record[rollno]["marks"]=input("Enter marks: ")
        else:
            print("Invalid")
    
    option = int(input("\nEnter your option: "))