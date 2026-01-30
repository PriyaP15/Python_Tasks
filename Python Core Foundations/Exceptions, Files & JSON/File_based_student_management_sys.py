import json
import os

class NameError (Exception):
    "Raise when length of name is lesser than 3"

class CourseError (Exception):
    "Raise when length of Course is lesser than 2"

class DeptError (Exception):
    "Raise when length of Course is lesser than 2"

def add_student():
    try:
        rollno = input("Enter rollno: ")

        if os.path.exists("student_data.json"):
            try:
                with open("student_data.json", "r") as file:
                    data = json.load(file)
            except json.JSONDecodeError:
                data ={}
        else:
            data = {}

        if rollno in data:
            print("Student already exists\n")
            return
        
        name = input("Enter name: ")

        age = input("Enter age: ")
        if len(name)<3:
            raise NameError
        
        course = input("Enter course: ")
        if len(course)<2 or not course.isalpha():
            raise CourseError
        
        dept = input("Enter department: ")
        if len(dept)<2 or not dept.isalpha():
            raise DeptError
        
        data[rollno]={"rollno":rollno,"name":name, "age":age, "course":course, "department":dept}
        with open("student_data.json", "w") as file:
            json.dump(data, file,indent=4)
        print("Record added\n")

    except NameError:
        print("Name should be greater than 3 characters and should not contain numbers\n")
    except CourseError:
        print("Course should be greater than 2 characters and should not contain numbers\n")
    except DeptError:
        print("Department should be greater than 2 characters and should not contain numbers\n")

        

def modify_data():
    try:
        rollno = input("Enter rollno: ")
        with open("student_data.json", "r") as file:
            data = json.load(file)

        if rollno in data:
            print("Enter 1: To modify name")
            print("Enter 2: To modify age")
            print("Enter 3: To modify course")
            print("Enter 4: To modify department")
            option = int(input("Enter option: "))
            if option == 1:
                data[rollno]["name"]=input("Enter name: ")
            elif option == 2:
                data[rollno]["age"]=input("Enter age: ")
            elif option == 3:
                data[rollno]["course"]=input("Enter course: ")
            elif option == 4:
                data[rollno]["department"]=input("Enter department: ")
            else:
                print("Invalid option\n")

        with open("student_data.json", "w") as file:
            json.dump(data, file,indent=4)
        print("Record modified\n")
    except FileNotFoundError as e:
        print("No students available\n")

def delete_student():
    try:
        rollno = input("Enter rollno: ")
        with open("student_data.json", "r") as file:
            data = json.load(file)

        if rollno in data:
            data.pop(rollno)
            with open("student_data.json", "w") as file:
                json.dump(data, file,indent=4)
            print("Record deleted\n")
        else:
            print("Student not found\n")
    except FileNotFoundError as e:
        print("No students available\n")

def search_student():
    try:
        rollno = input("Enter rollno: ")
        with open("student_data.json", "r") as file:
            data = json.load(file)

        if rollno in data:
            print(data[rollno])
        else:
            print("Student not found\n")
    except FileNotFoundError as e:
        print("No students available\n")

def display_student():
    try:
        with open("student_data.json", "r") as file:
            data = json.load(file)
        for i in data:
            print(data[i])
    except FileNotFoundError as e:
        print("No students available\n")
    

# data={}

while True:
    print("1. Add student")
    print("2. Modify student information")
    print("3. Delete student record")
    print("4. Search student information")
    print("5. Display all student information")
    print("6. Exit")

    option = input("Enter option: ")
    match option:
        case '1':
            add_student()
        case '2':
            modify_data()
        case '3':
            delete_student()
        case '4':
            search_student()
        case '5':
            display_student()
        case '6':
            print("Exiting...\n")
            break
        case _:
            print("Invalid option\n")

    if input("Press 1 to continue... Press any other key to exit...")=="1":
        continue
    else:
        break