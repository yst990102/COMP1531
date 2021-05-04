def generate(n):
    if n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    elif n >= 3:
        list = [0, 1]
        for i in range(n - 2):
            list.append(list[i] + list[i+1])
        return list
    return []


if __name__ == "__main__":
    for n in range(10):
        print(generate(n))
