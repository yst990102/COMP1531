def foo1(zid, name, age, suburb):
    print(zid, name, age, suburb)

def foo2(zid=None, name=None, age=None, suburb=None):
    print(zid, name, age, suburb)

if __name__ == '__main__':
    
    foo1('z3418003', 'Hayden', '72', 'Kensington')
    
    foo2('z3418003', 'Hayden')
    foo2(name='Hayden', suburb='Kensington', age='72', zid='z3418003')
    foo2(age='72', zid='z3418003')
    
    foo2('z3418003', suburb='Kensington')
