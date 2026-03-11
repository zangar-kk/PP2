class Employee:
    def __init__(self, name, basesalary):
        self.name = name
        self.basesalary = basesalary
    
    def TotalSalary(self):
        return self.basesalary

class Manager(Employee):
    def __init__(self, name, basesalary, bonuspercent):
        super().__init__(name, basesalary)
        self.bonuspercent = bonuspercent
    def TotalSalary(self):
        return self.basesalary +self.basesalary*self.bonuspercent/100

class Developer(Employee):
    def __init__(self, name, basesalary, completedproj):
        super().__init__(name, basesalary)
        self.completedproj = completedproj
    def TotalSalary(self):
        return self.basesalary+self.completedproj*500

class Itern(Employee):
    pass
        
emp = input().split()

job = emp[0]
name = emp[1]
salary =int(emp[2])

if job == "Manager":
    bonus = int(emp[3])
    emp = Manager(name, salary, bonus)
elif job == "Developer":
    bonus = int(emp[3])
    emp = Developer(name, salary, bonus)
    
elif job == "Intern":
    emp = Itern(name,salary)

print(f"Name: {emp.name}, Total: {emp.TotalSalary():.2f}")