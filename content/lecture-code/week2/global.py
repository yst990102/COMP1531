myVariable = 5

def printSomething():
  print(myVariable)
  
def writeSomethingBad():
  myVariable = 6
  
def writeSomethingGood():
  global myVariable
  myVariable = 6