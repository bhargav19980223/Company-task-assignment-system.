
'''
Company task assignment system
Total 10 Employees and 2 departments
1) 2 General manager
2) 2 Department manager
4)  6 Workers(3 workers per department)

'''

worker_role = "worker"
manager_role = "manager"
general_manager_role = "general_manager"

task_deletion_requests=[]
task_reassign_requests=[]


class Task():

    def __init__(self, taskName,  department, assignee) -> None:
        self.taskName = taskName
        self.department = department
        self.assignee = assignee

    def get_task_name(self):
        return self.taskName

    def get_task_assignee(self):
        return self.assignee

    def get_task_department(self):
        return self.department

    def set_task_assignee(self, assignee):
        if self.assignee is None:
            self.assignee = assignee
            return True
        else:
            return False



class Department():

    def __init__(self, departmentId, taskList, employeeList) -> None:
        self.departmentId = departmentId
        self.taskList = taskList
        self.employeeList = employeeList

    def add_task(self, task):
        self.taskList.append(task)

    def delete_task(self, task_name):
        for task in self.taskList:
            if task.get_task_name() == task_name:
                self.taskList.remove(task)
                print("Task found and removed")

    def add_employee(self, employee):
        self.employeeList.append(employee)

    def get_department_task_list(self):
        return self.taskList

    def get_department_employee_list(self, empleyee_role):
        worker_list = []

        for employee in self.employeeList:
            if employee.get_employee_role() == empleyee_role:
                worker_list.append(employee.get_employee_username())

        return worker_list

    def get_employee(self, username):
        for employee in self.employeeList:
            if employee.get_employee_username() == username:
                return employee


class Employee():

    def __init__(self, username, password, role, assignedTaskCount, department) -> None:
        self.username = username
        self.password = password
        self.role = role
        self.assignedTaskCount = assignedTaskCount
        self.department = department
        self.assignedTaskList = []

    def get_employee_role(self):
        return self.role

    def get_employee_username(self):
        return self.username

    def get_employee_password(self):
        return self.password

    def get_department(self):
        return self.department

    def check_worker_capacity(self):
        return self.assignedTaskCount < 3

    def update_worker_task_assignment_count(self, task):

        if self.assignedTaskCount < 3:
            self.assignedTaskCount += 1
            self.assignedTaskList.append(task)
            return True
        else:
            return False


    def decrease_worker_task_assignment_count(self, task):
        self.assignedTaskCount -= 1
        self.assignedTaskList.remove(task)

    def perform_role_operations():
        pass


class Worker(Employee):
    
    def perform_role_operations(self):
        print("Please choose any of the below, Press 0 for exit")
        print("1. See the tasks assigned to me")
        print("2. See the department unassigned tasks")
        print("3. Assign task to me")
        print("0. Exit")

        choice = int(input("Your Choice: "))
        while choice != 0:
            if choice == 1:
                task_assigned_to_me = []
                for task in self.assignedTaskList:
                    task_assigned_to_me.append(task.get_task_name())
                print(", ".join(task_assigned_to_me))
            elif choice == 2:
                task_unassigned = []
                for task in self.department.get_department_task_list():
                    if task.get_task_assignee() is None:
                        task_unassigned.append(task.get_task_name())
                print(", ".join(task_unassigned))
            elif choice == 3:
                task_name = input("Enter task name: ")
                task_detail = self.department.get_department_task_list()
                for task in task_detail:
                    if task.get_task_assignee() is None and task.get_task_name() == task_name:
                        task.set_task_assignee(self.username)
                        self.update_worker_task_assignment_count(task)
                        print("task assigned to successfully!!")
                        break

            choice = int(input("Your Choice: "))

class Manager(Employee):

    def perform_role_operations(self):
        print("Please choose any of the below, Press 0 for exit")
        print("1. See all tasks")
        print("2. Assign task")
        print("3. Delete task")
        print("4. reassign task")
        print("5. See all worker list")
        print("0. Exit")
        department = self.get_department()
        worker_list = department.get_department_employee_list(worker_role)
        choice = int(input("Your Choice: "))
        while choice != 0:
            if choice == 1:
                task_list = department.get_department_task_list()
                print(", ".join([task.get_task_name() for task in task_list]))
            elif choice == 2:
                task_name = input("Enter task name: ")
                worker_usename = input("Enter woker username: ")
                
                worker_user = department.get_employee(worker_usename)
                if worker_usename in worker_list:
                    task_assigned = False
                    for task in department.get_department_task_list():
                        if task.get_task_name() == task_name and task.get_task_department() == department:
                            if task.get_task_assignee() is None and worker_user.check_worker_capacity():
                                task_assigned = True
                                task.set_task_assignee(worker_usename)
                                worker_user.update_worker_task_assignment_count(task)
                            elif not worker_user.check_worker_capacity():
                                print("Cannot assign more than 3 tasks.")
                            else:
                                print("Invalid Operation. Task already assigned, Please perform reassign operation.")
                            continue
                        
                    if not task_assigned:
                        print("Invalid task name.")
                    else:
                        print("Task Assigned successfully.")
                else:
                    print("Please add valid worker username")
            elif choice == 3:
                task_name = input("Enter task name: ")
                task_deletion_request = {}
                task_deletion_request["taskName"] = task_name
                task_deletion_request["department"] = department
                task_deletion_requests.append(task_deletion_request)

                print("Task delete request raised")
            elif choice == 4:
                task_name = input("Enter task name: ")
                worker_usename = input("Enter woker username: ")

                worker_user = department.get_employee(worker_usename)
                if worker_usename in worker_list:
                    task_found = False
                    task_assigned = False
                    for task in department.get_department_task_list():
                        print(task)
                        if task.get_task_name() == task_name and task.get_task_department() == department:
                            task_found = True

                            if not worker_user.check_worker_capacity():
                                print("Can not assign more than 3 tasks")
                                break

                            reassign_request = {}
                            reassign_request["taskName"] = task_name
                            reassign_request["assignee"] = worker_usename
                            reassign_request["department"] = department
                            task_reassign_requests.append(reassign_request)
                            task_assigned = True
                            worker_user.update_worker_task_assignment_count(task)
                            continue
                        
                    if not task_found:
                        print("Invalid task name")
                    elif task_assigned:
                        print("Task reassign request raised")
                else:
                    print("Please add valid worker username")
            elif choice == 5:
                print(", ".join(worker_list))

            choice = int(input("Your Choice: ")) 

class GeneralManager(Employee):
    def perform_role_operations(self):
        print("Please choose any of the below, Press 0 for exit")
        print("1. See all tasks")
        print("2. Assign task")
        print("3. Delete task")
        print("4. See all worker list")
        print("5. See and approve delete task request")
        print("6. See and approve reassign task request")
        print("7. Status Report")
        print("0. Exit")
        department = self.get_department()
        worker_list = department.get_department_employee_list(worker_role) + department.get_department_employee_list(manager_role)
        choice = int(input("Your Choice: "))
        while choice != 0:
            if choice == 1:
                task_list = department.get_department_task_list()
                print(", ".join([task.get_task_name() for task in task_list]))
            elif choice == 2:
                task_name = input("Enter task name: ")
                worker_usename = input("Enter worker username: ")
                
                worker_user = department.get_employee(worker_usename)
                if worker_usename in worker_list:
                    task_assigned = False
                    for task in department.get_department_task_list():
                        if task.get_task_name() == task_name:
                            if worker_user.check_worker_capacity():
                                task_assigned = True
                                task.set_task_assignee(worker_usename)
                                worker_user.update_worker_task_assignment_count(task)
                            elif not worker_user.check_worker_capacity(worker_usename):
                                print("Cannot assign more than 3 tasks.")
                            else:
                                print("Invalid Operation. Task already assigned, Please perform reassign operation.")
                            continue
                        
                    if not task_assigned:
                        print("Invalid task name.")
                    else:
                        print("Task Assigned successfully.")
                else:
                    print("Please add valid employee username")
            elif choice == 3:
                task_name = input("Enter task name: ")
                department.delete_task(task_name)

                print("Task deleted")
            elif choice == 4:
                print(", ".join(worker_list))
            elif choice == 5:
                delete_requested_tasks = []
                for delete_request in task_deletion_requests:
                    if delete_request["department"] == department:
                        delete_requested_tasks.append(delete_request["taskName"])
                print("Below are the tasks send by department manager to be deleted!" )
                print(delete_requested_tasks)
                task_name = input("Enter task name to approve delete: ")
                department.delete_task(task_name)

                for delete_request in task_deletion_requests:
                    if delete_request["department"] == department and delete_request["taskName"] == task_name:
                        task_deletion_requests.remove(delete_request)

                print("Action performed.")
            elif choice == 6:
                reassign_requested_tasks = []
                for reassign_request in task_reassign_requests:
                    if reassign_request["department"] == department:
                        reassign_requested_tasks.append(reassign_request["taskName"])
                print(reassign_requested_tasks)
                task_name = input("Enter task name to approve reassign: ")

                task_assigned = False
                worker_usename = ""
                for reassign_request in task_reassign_requests:
                    if reassign_request["department"] == department and reassign_request["taskName"] == task_name:
                        worker_usename = reassign_request["assignee"]
                        task_reassign_requests.remove(reassign_request)

                worker_user = department.get_employee(worker_usename)
                for task in department.get_department_task_list():
                    if task.get_task_name() == task_name and task.get_task_department() == department:
                        if worker_user.check_worker_capacity():
                            task_assigned = True
                            old_assignee = task.get_task_assignee()
                            old_worker_user = department.get_employee(old_assignee)
                            task.set_task_assignee(worker_usename)
                            old_worker_user.decrease_worker_task_assignment_count(task)
                            worker_user.update_worker_task_assignment_count(task)
                        elif not worker_user.check_worker_capacity():
                            print("Cannot assign more than 3 tasks.")
                        else:
                            print("Invalid Operation. Task already assigned, Please perform reassign operation.")
                        continue
                    
                if not task_assigned:
                    print("Invalid task name.")
                else:
                    print("Task Assigned successfully.")
            elif choice ==7:
                
                task_list = department.get_department_task_list()
                for task in task_list:
                    assignee = "none";
                    if task.get_task_assignee():
                        assignee = task.get_task_assignee()
                    print(task.get_task_name() + ":" + assignee)
            choice = int(input("Your Choice: "))


print("Please login to move ahread..")

d1 = Department("d1", [], [])
d2 = Department("d2", [], [])

worker1 = Worker("worker1", "worker123", worker_role, 0, d1)
worker2 = Worker("worker2", "worker123", worker_role, 0, d1)
worker3 = Worker("worker3", "worker123", worker_role, 0, d1)

worker4 = Worker("worker4", "worker123", worker_role, 0, d2)
worker5 = Worker("worker5", "worker123", worker_role, 0, d2)
worker6 = Worker("worker6", "worker123", worker_role, 0, d2)

manager1 = Manager("m1", "m1", manager_role, 0, d1)
manager2 = Manager("m2", "m2", manager_role, 0, d2)

general_manager1 = GeneralManager("gm1", "gm123", general_manager_role, 0, d1)
general_manager2 = GeneralManager("gm2", "gm123", general_manager_role, 0, d2)

task1 = Task("Task1", d1, None)
task2 = Task("Task2", d1, None)
task3 = Task("Task3", d1, None)
task4 = Task("Task4", d1, None)
task5 = Task("Task5", d1, None)

task6 = Task("Task6", d2, None)
task7 = Task("Task7", d2, None)
task8 = Task("Task8", d2, None)
task9 = Task("Task9", d2, None)


d1.add_employee(worker1)
d1.add_employee(worker2)
d1.add_employee(worker3)

d1.add_employee(manager1)
d1.add_employee(general_manager1)

d1.add_task(task1)
d1.add_task(task2)
d1.add_task(task3)
d1.add_task(task4)
d1.add_task(task5)


d2.add_employee(worker4)
d2.add_employee(worker5)
d2.add_employee(worker6)

d2.add_employee(manager2)
d2.add_employee(general_manager2)

d2.add_task(task6)
d2.add_task(task7)
d2.add_task(task8)
d2.add_task(task9)



while True: 
    print("__________________Welcome to Company Task Assignment System_________________")
    print("LOGIN INFORMATION:")
    print("ROLE                        USERNAME       PASSWORD     ")
    print("Genral manager(dept:1)       gm1             gm123"   )
    print("Genral manager(dept:2)       gm2             gm123"   )
    print("Department manager(dept:1)    m1              m123"   )
    print("Department manager(dept:2)    m2              m123"   )
    print("worker_1(dept:1)           worker1          worker123")
    print("worker_2(dept:1)           worker2          worker123")
    print("worker_1(dept:1)           worker3          worker123")
    print("worker_1(dept:2)           worker4          worker123")
    print("worker_1(dept:2)           worker5          worker123")
    print("worker_1(dept:2)           worker6          worker123")
    username = input("username:")
    password = input("password:")
    user_info = (username, password)

    if d1.get_employee(username):
        user = d1.get_employee(username)
    else:
        user = d2.get_employee(username)

    if user is None:
        print("Please enter valid credentials")
    else:
        print("Hello ", username)
        user.perform_role_operations()

