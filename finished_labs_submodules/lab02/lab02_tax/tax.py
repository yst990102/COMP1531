income = int(input("Enter your income: "))

tax = 0

if income <= 18200 and income >= 0:
    tax = 0
elif income <= 37000 and income >= 18201:
    tax = 0.19 * (income - 18200)
elif income <= 87000 and income >= 37001:
    tax = 3572 + 0.325 * (income - 37000)
elif income <= 180000 and income >= 87001:
    tax = 19822 + 0.37 * (income - 87000)
elif income >= 180001:
    tax = 54232 + 0.45 * (income - 180000)

print("The estimated tax on your income is $" + '{:,.2f}'.format(tax))
