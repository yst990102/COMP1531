def reduce(f, xs):
    xs_list = list(xs)

    if xs_list == []:
        return None
    if len(xs_list) == 1:
        return xs_list[0]
    
    result = f(xs_list[0], xs_list[1])
    
    next_xs = xs_list[2:]
    next_xs.insert(0,result)

    return reduce(f,next_xs)

if __name__ == '__main__':
    print(reduce(lambda x, y: x + y, [1,2,3,4,5]))
    print(reduce(lambda x, y: x * y, [1,2,3,4,5]))