def draw(tree):
    pass


def Tuple_to_String(tuple):
    str = "".join(tuple)
    return str

def depth(Tup):
    if Tup == () or Tup == []:
        return 1

    Depth_list = []
    for i in Tup:
        Depth_list.append(depth(i))
    
    return max(Depth_list)


