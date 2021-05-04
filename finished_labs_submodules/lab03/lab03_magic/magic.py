def magic(square):
    # check 01 : check if square is a n*n square
    n = len(square)
    sum_up_list = []
    for i in square:
        if n != len(i):
            return "Invalid data: missing or repeated number"
        else:
            sum_up_list += i

    # check 02 : check if 1-N^2 numbers are all in the square
    for i in range(1, n ** 2 + 1):
        if i not in sum_up_list:
            return "Invalid data: missing or repeated number"

    magic_sum = sum(square[0])
    # check 03 : check the sum of each row if all of them are correct
    for i in square:
        if sum(i) != magic_sum:
            return "Not a magic square"

    # check 04 : check the sum of each column if all of them are correct
    for i in range(0, n):
        column_sum = 0
        for j in square:
            column_sum += j[i]
        if column_sum != magic_sum:
            return "Not a magic square"

    # check 05 : check the sum of diagonal lines if all of them are correct
    diagonal_sum1 = 0
    diagonal_sum2 = 0
    for i in range(0, n):
        j = n - 1 - i
        diagonal_sum1 += square[i][i]
        diagonal_sum2 += square[j][i]
    if diagonal_sum1 != magic_sum or diagonal_sum2 != magic_sum:
        return "Not a magic square"

    return "Magic square"


if __name__ == "__main__":
    print(magic([[8, 1, 6], [3, 5, 7]]))
