class Student:
    def __init__(self, zid, name):
        self.zid = zid
        self.name = name
        self.year = 1
        
    def advance_year(self):
        self.year += 1
        
    def email_address(self):
        return self.zid + "@unsw.edu.au"
        
rob = Student("z3254687", "Robert Leonard Clifton-Everest")
hayden = Student("z3418003", "Hayden Smith")