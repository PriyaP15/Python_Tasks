def attandance_tracker():
    if len(log_book)==0:
        print("No students available\nAdd students to mark attendance")
        return
    while 1:
        print("Enter 1: To mark attendace")
        print("Enter 2: To view attendance")
        print("Enter 3: To update attendance")
        print("Enter 4: To exit")
        option=input("Enter options: ")
        match option:
            case '1':
                date=input("Enter date in (dd-mm-yyyy): ")
                atd_tracker[date]=[]
                for i in log_book:
                    if input(f"Is {i} present? (y/n): ")=="y":
                        atd_tracker[date].append(i)
                print("Attendance marked")
            case '2':
                print(atd_tracker)
            case '3':
                print("Enter 1: To delete date")
                print("Enter 2: To update attendance")
                print("Enter 3: To exit")
                option=input("Enter option: ")
                match option:
                    case '1':
                        atd_tracker.pop(input("Enter date in (dd-mm-yyyy): "))
                        print("Date deleted")
                    case '2':
                        date=input("Enter date in (dd-mm-yyyy): ")
                        atd_tracker[date]=[]
                        for i in log_book:
                            if input(f"Is {i} present? (y/n): ")=="y":
                                atd_tracker[date].append(i)
                        print("Attendance updated")
                    case '3':
                        print("Exiting")
                        break
                    case _:
                        print("Invalid option")
                        break
            case '4':
                print("Exiting")
                break
            case _:
                print("Invalid option")
                break


def student():
    while 1:
        print()
        print("Enter 1: To view attendance")
        print("Enter 2: To view attendence by rollno")
        print("Enter 3: To exit")
        option=input("Enter option: ")
        match option:
            case '1':
                print(atd_tracker)
            case '2':
                try:
                    date=input("Enter date in (dd-mm-yyyy): ")
                    rollno=input("Enter rollno:")
                    if rollno not in log_book:
                        print("Invalid rollno")
                        continue
                    if rollno in atd_tracker[date]:
                        print("-----Present----")
                    else:
                        print("-----Absent-----")
                except KeyError as e:
                    print("Check the date and rollno")
            case '3':
                print("Exiting")
                break
            case _:
                print("Invalid option")
                break

def teacher(attendance):
    while 1:
        print("Enter 1: To add student")
        print("Enter 2: To delete students")
        print("Enter 3: To view students")
        print("Enter 4: To mark attendance")
        print("Enter 5: To exit")

        option = input("Enter option: ")
        match option:
            case '1':
                attendance.append(input("Enter student regno: "))
                print("Student added")
            case '2':
                attendance.pop(input("Enter student regno: "))
                print("Student deleted")
            case '3':
                print(attendance)
            case '4':
                attandance_tracker()
            case '5':
                print("Exiting")
                break
            case _:
                print("Invalid option")
                break

def analytics():
    total_days=len(atd_tracker)
    total_present_each={}
    total_absent_each={}
    total_present_percent={}

    for i in log_book:
        present=0
        for j in atd_tracker:
            if i in atd_tracker[j]:
                present+=1
        total_present_each[i]=present
        total_absent_each[i]=total_days-present

    for i in total_present_each:
        total_present_percent[i]=int((total_present_each[i]/total_days)*100)

    while 1:
        print("Enter 1: To view total present day for each student")
        print("Enter 2: To view total absent day for each student")
        print("Enter 3: To view total present day for each student in percentage")
        print("Enter 4: To view student greate than percent attendance")
        print("Enter 5: To view student lesser than percent attendance")
        print("Enter 6: To exit")
        option=input("Enter option: ")
        match option:
            case '1':
                for i in total_present_each:
                    print(f"Roll no {i} is present for: {total_present_each[i]}/{total_days}")
                pass
            case '2':
                for i in total_absent_each:
                    print(f"Roll no {i} is absent for: {total_absent_each[i]}/{total_days}")
            case '3':
                for i in total_present_percent:
                    print(f"Roll no {i}'s attendance percentage is: {total_present_percent[i]}/100")
            case '4':
                percent=int(input("Enter percentage: "))
                for i in total_present_percent:
                    if total_present_percent[i]>=percent:
                        print(i,end=" ")
                print()
            case '5':
                percent=int(input("Enter percentage: "))
                print("Roll no: ")
                for i in total_present_percent:
                    if total_present_percent[i]<percent:
                        print(i,end=" ")
                print()
            case '6':
                print("Exiting..")
                break
            case _:
                print("Invalid option")

            
atd_tracker={"28-01-2026":['1','2','3','4','5'],"29-01-2026":['2','3','4','5'],"30-01-2026":['2','3','4','6'],"31-01-2026":['2','3','4','6'],"01-02-2026":['2','3','4','6'],"02-02-2026":['2','3','4','6'],"03-02-2026":['2','3','4','6'],"04-02-2026":['2','3','4','6'],"05-02-2026":['2','3','4','6'],"06-02-2026":['2','3','4','6'],"07-02-2026":['2','3','4','6'],"08-02-2026":['2','3','4','6']}
log_book=['1','2','3','4','5','6']
person=input("Enter 1: To teacher mode\nEnter 2: To student mode\nEnter 3: To view analytics\nEnter 4: To exit\nEnter option: ")
if person=='1':
    print("Enter 1: To update attendance list")
    print("Enter 2: To track attendance")
    print("Enter 3: To exit")
    if input("Enter option :")=="1":
        teacher(log_book)
    elif input("Enter option: ")=="2":
        attandance_tracker()
    elif input("Enter option: ")=="3":
        print("Exiting")
    else:
        print("Invalid option")
    
elif person == '2':
    student()
elif person == '3':
    analytics()
else:
    print("Invalid option")
