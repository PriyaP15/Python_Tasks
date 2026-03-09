import json
import os
from abc import ABC, abstractmethod

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMPLOYEES_FILE = os.path.join(BASE_DIR, "employee.json")
ATTENDANCE_FILE = os.path.join(BASE_DIR, "attendance.json")

class Person(ABC):
    def __init__(self, emp_id, name, email):
        self.emp_id = emp_id
        self.name = name
        self.email = email
    
    @abstractmethod
    def get_role(self):
        pass
    
    def to_dict(self):
        data = {}
        data['emp_id'] = self.emp_id
        data['name'] = self.name
        data['email'] = self.email
        data['role'] = self.get_role()
        
        if hasattr(self, 'team_ids'):
            data['team_ids'] = self.team_ids
        return data
    
    @classmethod
    def from_dict(cls, data):
        role = data.get('role')
        e_id = data.get('emp_id')
        name = data.get('name')
        mail = data.get('email')

        if role == 'Employee':
            return Employee(e_id, name, mail)
        elif role == 'TL':
            t_ids = data.get('team_ids', [])
            return TL(e_id, name, mail, t_ids)
        elif role == 'Manager':
            t_ids = data.get('team_ids', [])
            return Manager(e_id, name, mail, t_ids)
        elif role == 'HR':
            return HR(e_id, name, mail)
        elif role == 'Admin':
            return Admin(e_id, name, mail)
        return None
    
    def view_own_attendance(self, attendance_data):
        present_count = 0
        total_days = len(attendance_data)
        
        for date in attendance_data:
            day_info = attendance_data[date]
            if self.emp_id in day_info['present']:
                present_count += 1
                
        percentage = 0
        if total_days > 0:
            percentage = (present_count / total_days) * 100
            
        print(f"{self.name} ({self.get_role()}): {present_count}/{total_days} days ({percentage:.1f}%)")


class Employee(Person):
    def get_role(self):
        return 'Employee'

class TL(Person):
    def __init__(self, emp_id, name, email, team_ids=None):
        super().__init__(emp_id, name, email)
        if team_ids is None:
            self.team_ids = []
        else:
            self.team_ids = team_ids
    
    def get_role(self):
        return 'TL'
    
    def view_team_attendance(self, attendance_data):
        print(f"\nTeam Report for TL: {self.name}")
        if not self.team_ids:
            print("No team members assigned")
            return
        
        for member_id in self.team_ids:
            p_days = 0
            for date in attendance_data:
                if member_id in attendance_data[date]['present']:
                    p_days += 1
            print(f"  ID: {member_id} | Present: {p_days}/{len(attendance_data)}")

class Manager(Person):
    def __init__(self, emp_id, name, email, team_ids=None):
        super().__init__(emp_id, name, email)
        self.team_ids = team_ids if team_ids else []
    
    def get_role(self):
        return 'Manager'
    
    def view_department_attendance(self, attendance_data, employees):
        print(f"\n{self.name}'s Department Report")
        ids_to_check = [self.emp_id]
        for tl_id in self.team_ids:
            ids_to_check.append(tl_id)
            for e in employees:
                if e.emp_id == tl_id and hasattr(e, 'team_ids'):
                    for sub_id in e.team_ids:
                        ids_to_check.append(sub_id)
        
        unique_ids = list(set(ids_to_check))
        
        for e_id in unique_ids:
            p_days = 0
            for date in attendance_data:
                if e_id in attendance_data[date]['present']:
                    p_days += 1
            print(f"  ID: {e_id} | Present: {p_days}/{len(attendance_data)}")

class HR(Person):
    def get_role(self):
        return 'HR'
    
    def system_report(self, employees, attendance_data):
        print("\n--- COMPANY REPORT ---")
        total_days = len(attendance_data)
        for emp in employees:
            emp.view_own_attendance(attendance_data)

class Admin(Person):
    def get_role(self):
        return 'Admin'

class EmployeeManager:
    def __init__(self):
        self.employees = []
        self.attendance_data = {}
        
        self.VALID_ROLES = {
            'Admin': ['EMPLOYEE', 'TL', 'MANAGER', 'HR', 'ADMIN'],
            'HR': ['EMPLOYEE', 'TL', 'MANAGER', 'HR'],
            'Manager': ['EMPLOYEE', 'TL'],
            'TL': ['EMPLOYEE'],
            'Employee': []
        }
        self.load_data()

    def load_data(self):
        if os.path.exists(EMPLOYEES_FILE):
            with open(EMPLOYEES_FILE, 'r') as f:
                raw_data = json.load(f)
                for item in raw_data:
                    obj = Person.from_dict(item)
                    if obj:
                        self.employees.append(obj)
        
        if os.path.exists(ATTENDANCE_FILE):
            with open(ATTENDANCE_FILE, 'r') as f:
                self.attendance_data = json.load(f)

    def save_data(self):
        serialized_list = []
        for emp in self.employees:
            serialized_list.append(emp.to_dict())
            
        with open(EMPLOYEES_FILE, 'w') as f:
            json.dump(serialized_list, f, indent=2)
        with open(ATTENDANCE_FILE, 'w') as f:
            json.dump(self.attendance_data, f, indent=2)

    def add_employee(self, e_id, name, email, role, team_ids, creator_role):
        role_upper = role.upper()
        
        allowed = self.VALID_ROLES.get(creator_role, [])
        if role_upper not in allowed:
            print(f"{creator_role} cannot create {role_upper}")
            return
        
        for e in self.employees:
            if e.emp_id == e_id:
                print("ID already exists")
                return

        if role_upper == 'TL': 
            new_emp = TL(e_id, name, email, team_ids)
        elif role_upper == 'MANAGER': 
            new_emp = Manager(e_id, name, email, team_ids)
        elif role_upper == 'HR': 
            new_emp = HR(e_id, name, email)
        elif role_upper == 'ADMIN': 
            new_emp = Admin(e_id, name, email)
        else: 
            new_emp = Employee(e_id, name, email)

        self.employees.append(new_emp)
        self.save_data()
        print(f"Added {name} successfully.")

    def delete_employee(self, e_id):
        target = None
        for e in self.employees:
            if e.emp_id == e_id:
                target = e
                break
        
        if target:
            confirm = input(f"Are you sure you want to delete {target.name}? (y/n): ")
            if confirm.lower() == 'y':
                self.employees.remove(target)
                self.save_data()
                print("Employee removed from system.")
        else:
            print("Employee ID not found.")

    def attendance_tracker(self):
        date = input("Enter date (dd-mm-yyyy): ")
        if date in self.attendance_data:
            print("Date already recorded.")
            return
            
        present_list = []
        for emp in self.employees:
            ans = input(f"Is {emp.name} ({emp.emp_id}) present? (y/n): ")
            if ans.lower() == 'y':
                present_list.append(emp.emp_id)
        
        self.attendance_data[date] = {'present': present_list}
        self.save_data()


    def run_menu(self, user):
        role = user.get_role()
        while True:
            print(f"\n--- {role} Menu: {user.name} ---")
            if role == 'Admin':
                print("1. Add Employee\n2. View List\n3. Mark Attendance\n4. Delete Employee\n5. Logout")
                cmd = input("Select: ")
                if cmd == '1': 
                    self.show_add_menu(role)
                elif cmd == '2': 
                    for e in self.employees: 
                        print(f"{e.emp_id}: {e.name} [{e.get_role()}]")
                elif cmd == '3': 
                    self.attendance_tracker()
                elif cmd == '4':
                    emp = input("Enter ID to delete: ")
                    self.delete_employee(emp)
                elif cmd == '5': 
                    break
            
            elif role == 'HR':
                print("1. Add Employee\n2. Company Report\n3. Logout")
                cmd = input("Select: ")
                if cmd == '1': 
                    self.show_add_menu(role)
                elif cmd == '2': 
                    user.system_report(self.employees, self.attendance_data)
                elif cmd == '3': 
                    break
            
            elif role == 'Manager':
                print("1. Dept Report\n2. My Stats\n3. Logout")
                cmd = input("Select: ")
                if cmd == '1': 
                    user.view_department_attendance(self.attendance_data, self.employees)
                elif cmd == '2': 
                    user.view_own_attendance(self.attendance_data)
                elif cmd == '3':
                    break

            elif role == 'TL':
                print("1. Team Report\n2. My Stats\n3. Logout")
                cmd = input("Select: ")
                if cmd == '1': 
                    user.view_team_attendance(self.attendance_data)
                elif cmd == '2': 
                    user.view_own_attendance(self.attendance_data)
                elif cmd == '3': 
                    break

            else:
                print("1. View My Stats\n2. Logout")
                if input("Select: ") == '1': user.view_own_attendance(self.attendance_data)
                else: break

    def show_add_menu(self, creator_role):
        e_id = input("New ID: ")
        name = input("Name: ")
        mail = input("Email: ")
        role = input("Role: ")
        t_ids = []
        if role.upper() in ['TL', 'MANAGER']:
            t_input = input("Team IDs (comma separated): ")
            if t_input:
                t_ids = t_input.split(',')
        self.add_employee(e_id, name, mail, role, t_ids, creator_role)


manager = EmployeeManager()
if len(manager.employees) == 0:
    manager.add_employee('A01', 'System Admin', 'admin@mail.com', 'Admin', [], 'Admin')

while True:
    print("1. Login")
    print("2. Exit")
    start = input("Choice: ")
    if start == '2': 
        break
    
    e_id = input("Enter Employee ID: ")
    role_choice = input("Enter Role for verification: ")
    
    found_user = None
    for e in manager.employees:
        if e.emp_id == e_id and e.get_role().lower() == role_choice.lower():
            found_user = e
            break
    
    if found_user:
        manager.run_menu(found_user)
    else:
        print("Invalid Login Credentials.")