# BMI = weight in kilograms / (height in meters * height in meters)

weight = float(input("What is your weight in kg? "))
height = float(input("What is your height in m? "))
BMI = weight / (height ** 2)

print("Your BMI is %.1f" % BMI)
