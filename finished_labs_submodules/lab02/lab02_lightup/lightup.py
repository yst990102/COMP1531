def board_is_happy(board):
    return check_happy(board)  # TODO


def board_is_solved(board):
    return check_solved(board)  # TODO


def get_board_state(board):
    if board_is_happy(board):
        if board_is_solved(board):
            return "solved"
        else:
            return "happy"
    else:
        return "unhappy"


"""
====================================================================================================
    Here is the overall function for checking solved-condition
    solved -> True, not solved -> False
====================================================================================================
"""


def check_solved(board):

    # solved rule1 : all black cells with numbers must have exactly that many maps as direct NSEW adjacent neighbours
    def check_solved_rule1(board):
        length = get_length(board)
        width = get_width(board)

        result = True
        for i in range(0, width):
            for j in range(0, length):
                # print("check for (%d, %d)" %(i,j))
                num = 0
                if board[i][j].isdigit() == True:
                    num += check_NSEW_N(i, j, board)
                    num += check_NSEW_W(i, j, board)
                    num += check_NSEW_E(i, j, board)
                    num += check_NSEW_S(i, j, board)
                    if int(board[i][j]) != num:
                        result = False
                        break
            if result == False:
                break
        return result

    # solved rule2 : all white cells are illuminated yellow
    def check_solved_rule2(board):
        length = get_length(board)
        width = get_width(board)

        result = True
        for i in range(0, width):
            for j in range(0, length):
                if board[i][j] == ".":
                    result1 = check_solved_rule1_horizontal(i, j, board)
                    result2 = check_solved_rule1_vertical(i, j, board)
                    if result1 == False and result2 == False:
                        # print("result1 == " ,result1, "result2 == ", result2)
                        result = False
                        break
            if result == False:
                break

        return result

    def check_solved_rule1_horizontal(width, length, board):
        j = length

        # check forward
        while j > 0:
            j -= 1
            if board[width][j] == ".":
                continue
            elif board[width][j] == "X" or (board[width][j].isdigit() == True):
                break
            else:
                return True

        j = length
        # check backward
        while j < get_length(board) - 1:
            j += 1
            # print("checking board[%d][%d]" %(width,j))
            if board[width][j] == ".":
                continue
            elif board[width][j] == "X" or (board[width][j].isdigit() == True):
                break
            else:
                # print("returned here")
                return True

        return False

    def check_solved_rule1_vertical(width, length, board):
        j = width

        # print("checking board[%d][%d]" %(j,length))
        # check forward
        while j > 0:
            j -= 1
            if board[j][length] == ".":
                continue
            elif board[j][length] == "X" or (board[j][length].isdigit() == True):
                break
            else:
                return True

        j = width
        # check backward
        while j < get_width(board) - 1:
            j += 1
            if board[j][length] == ".":
                continue
            elif board[j][length] == "X" or (board[j][length].isdigit() == True):
                break
            else:
                return True

        return False

    # ==================================================
    # print(check_solved_rule1(board))
    # print(check_solved_rule2(board))
    return check_solved_rule1(board) and check_solved_rule2(board)


"""
====================================================================================================
    Here is the overall function for checking happy-condition
    happy -> True, unhappy -> False
====================================================================================================
"""


def check_happy(board):
    # happy rule1 : no to lamps are in NSEW (North/South/East/West) line-of-sight of each other
    def check_happy_rule1(board):
        length = get_length(board)
        width = get_width(board)

        result = True
        for i in range(0, width):
            for j in range(0, length):
                if board[i][j] == "L":
                    # print("i == %d j = %d" %(i,j))
                    result1 = check_happy_rule1_horizontal(i, j, board)
                    result2 = check_happy_rule1_vertical(i, j, board)
                    if result1 == False or result2 == False:
                        # print("result1 == " ,result1, "result2 == ", result2)
                        result = False
                        break
            if result == False:
                break

        return result

    # happy rule2 : black cells with numbers must have less than or equal to that many lamps as direct NSEW adjacent neighbours
    def check_happy_rule2(board):
        length = get_length(board)
        width = get_width(board)

        result = True
        for i in range(0, width):
            for j in range(0, length):
                # print("check for (%d, %d)" %(i,j))
                num = 0
                if board[i][j].isdigit() == True:
                    num += check_NSEW_N(i, j, board)
                    num += check_NSEW_W(i, j, board)
                    num += check_NSEW_E(i, j, board)
                    num += check_NSEW_S(i, j, board)
                    if int(board[i][j]) < num:
                        result = False
                        break
            if result == False:
                break
        return result

    def check_happy_rule1_horizontal(width, length, board):
        j = length

        # check forward
        while j > 0:
            j -= 1
            if board[width][j] == ".":
                continue
            elif board[width][j] == "X" or (board[width][j].isdigit() == True):
                break
            else:
                return False

        j = length
        # check backward
        while j < get_length(board) - 1:
            j += 1
            # print("checking board[%d][%d]" %(width,j))
            if board[width][j] == ".":
                continue
            elif board[width][j] == "X" or (board[width][j].isdigit() == True):
                break
            else:
                # print("returned here")
                return False

        return True

    def check_happy_rule1_vertical(width, length, board):
        j = width

        # check forward
        while j > 0:
            j -= 1
            if board[j][length] == ".":
                continue
            elif board[j][length] == "X" or (board[j][length].isdigit() == True):
                break
            else:
                return False

        j = width
        # check backward
        while j < get_width(board) - 1:
            j += 1
            if board[j][length] == ".":
                continue
            elif board[j][length] == "X" or (board[j][length].isdigit() == True):
                break
            else:
                return False

        return True

    # ==================================================
    # print(check_happy_rule1(board))
    # print(check_happy_rule2(board))
    return check_happy_rule1(board) and check_happy_rule2(board)


"""
====================================================================================================
    Supplementary functions
====================================================================================================
"""


def get_length(board):
    return len(board[0])


def get_width(board):
    return len(board)


def check_NSEW_N(i, j, board):
    i -= 1
    if i < 0 or j < 0 or i > get_width(board) - 1 or j > get_length(board) - 1:
        return 0
    else:
        if board[i][j] == "L":
            return 1
        else:
            return 0


def check_NSEW_W(i, j, board):
    j -= 1
    if i < 0 or j < 0 or i > get_width(board) - 1 or j > get_length(board) - 1:
        return 0
    else:
        if board[i][j] == "L":
            return 1
        else:
            return 0


def check_NSEW_E(i, j, board):
    j += 1
    if i < 0 or j < 0 or i > get_width(board) - 1 or j > get_length(board) - 1:
        return 0
    else:
        if board[i][j] == "L":
            return 1
        else:
            return 0


def check_NSEW_S(i, j, board):
    i += 1
    if i < 0 or j < 0 or i > get_width(board) - 1 or j > get_length(board) - 1:
        return 0
    else:
        if board[i][j] == "L":
            return 1
        else:
            return 0


# ==================================================
if __name__ == "__main__":
    print(
        get_board_state(
            """
..L1.0.
X...L..
L.X.X.L
X...L.X
..XL3L.
.L....X
L3L2L..""".strip().split(
                "\n"
            )
        )
    )

    print(
        get_board_state(
            """
L..
.X.
..L
""".strip().split(
                "\n"
            )
        )
    )

    print(
        get_board_state(
            """
1L.
..X
L..
""".strip().split(
                "\n"
            )
        )
    )

    print(
        get_board_state(
            """
L....X..L
XXL..X.XX
...L.X.XX
.XX1XX.L.
.X.X.L.X.
.X.XL3LX.
..L2.X.X.
.X.L.XX1L
L........""".strip().split(
                "\n"
            )
        )
    )
