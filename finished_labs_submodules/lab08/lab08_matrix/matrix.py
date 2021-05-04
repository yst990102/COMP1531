from decimal import ROUND_DOWN
from types import resolve_bases
from typing import Tuple


class Matrix:
    def __init__(self, m, n):
        """
        Initialises a matrix of dimensions m by n.
        """
        self.row_num = m
        self.col_num = n
        self.matrix = [[0 for i in range(n)] for j in range(m)]

    def __getitem__(self, key):
        """
        Returns the (i,j)th entry of the matrix, where key is the tuple (i,j).
        i or j may be Ellipsis (...) indicating that the entire i-th row
        or j-th column should be selected. In this case, this method returns a
        list of the i-th row or j-th column.
        Used as follows: x = matrix[0,0] || x = matrix[...,1] || x = matrix[0,...]
         * raises IndexError if (i,j) is out of bounds
         * raises TypeError if (i,j) are both Ellipsis
        """
        if (type(key[0]) == int and key[0] > self.row_num) or (type(key[1]) == int and key[1] > self.col_num):
            raise IndexError("(i,j) is out of bounds")
        if (type(key[0]) == int and key[0] < 0) or (type(key[1]) == int and key[1] < 0):
            raise IndexError("(i,j) is out of bounds")
        if key == (..., ...):
            raise TypeError("(i,j) are both Ellipsis")

        if type(key[0]) == int and key[1] == Ellipsis:
            return self.matrix[key[0]][:]
        elif type(key[1]) == int and key[0] == Ellipsis:
            return_col = []
            for i in range(self.row_num):
                return_col.append(self.matrix[i][key[1]])
            return return_col

        elif type(key[0]) == int and type(key[1]) == int:
            return self.matrix[key[0]][key[1]]

    def __setitem__(self, key, data):
        """
        Sets the (i,j)th entry of the matrix, where key is the tuple (i,j)
        and data is the number being added.
        One of i or j may be Ellipsis (...) indicating that the entire i-th row
        or j-th column should be replaced. In this case, data should be a list
        or a tuple of integers of the same dimensions as the equivalent matrix
        row or column. This method then replaces the i-th row or j-th column
        with the contents of the list or tuple
        Used as follows: matrix[0,0] = 1 || matrix[...,1] = [4,5,6] || matrix[0,...] = (1,2)
         * raises IndexError if (i,j) is out of bounds
         * raises TypeError if (i,j) are both Ellipsis
         * if i and j are integral, raises TypeError if data is not an integer
         * if i or j are Ellipsis, raises TypeError if data is not a list or tuple of integers
         * if i or j are Ellipsis, raises ValueError if data is not the correct size
        """
        if (type(key[0]) == int and key[0] > self.row_num) or (type(key[1]) == int and key[1] > self.col_num):
            raise IndexError("(i,j) is out of bounds")
        if (type(key[0]) == int and key[0] < 0) or (type(key[1]) == int and key[1] < 0):
            raise IndexError("(i,j) is out of bounds")
        if type(key[0]) == int and type(key[1]) == int and type(data) != int:
            raise TypeError("data need to be int.")
        if (type(key[0]) == int and key[1] == Ellipsis) or (type(key[1]) == int and key[0] == Ellipsis):
            if type(key[0]) == int and key[1] == Ellipsis:
                col_num = len(data)
                if col_num != self.col_num:
                    raise ValueError("data size is out of bounds")

            if type(key[1]) == int and key[0] == Ellipsis:
                row_num = len(data)
                if row_num != self.row_num:
                    raise ValueError("data size is out of bounds")

            if type(data) != tuple and type(data) != list:
                raise TypeError("data is not a list or tuple of int")
            else:
                for i in data:
                    if type(i) != int:
                        raise TypeError("data is not a list or tuple of int")
        if key[0] == Ellipsis and key[1] == Ellipsis:
            col_num = len(data[0])
            row_num = len(data[1])
            if col_num != self.col_num or row_num != self.row_num:
                raise ValueError("data size is out of bounds")

        if type(key[1]) == int and key[0] == Ellipsis:
            # set col(key[1])
            for i in range(self.row_num):
                self.matrix[i][key[1]] = data[i]
        elif type(key[0]) == int and key[1] == Ellipsis:
            # set row(key[1])
            self.matrix[key[0]] = data
        elif key[0] == Ellipsis and key[1] == Ellipsis:
            self.matrix = data
        elif type(key[0]) == int and type(key[1]) == int and type(data) == int:
            self.matrix[key[0]][key[1]] = data

    def __iadd__(self, other):
        """
        Adds other to this matrix, modifying this matrix object and returning self
        Used as follows: m1 += m2 ||  m1 += 3
         * raises TypeError if other is not a Matrix object or an integer
         * raises ValueError if adding another Matrix and it does not have the same dimensions as this matrix
        """
        if type(other) != int and type(other) != Matrix:
            raise TypeError("other is not a Matrix object or an integer")
        if type(other) == Matrix:
            if (other.row_num != self.row_num) or (other.col_num != self.col_num):
                raise ValueError("Other Matrix does not have the same dimensions")

        if type(other) == int:
            for i in range(self.row_num):
                for j in range(self.col_num):
                    self[i, j] += other
        elif type(other) == Matrix:
            for i in range(self.row_num):
                for j in range(self.col_num):
                    self[i, j] += other[i, j]
        return self

    def __add__(self, other):
        """
        Adds this matrix to other, returning a new matrix object.
        This method should not modify the current matrix or other.
        Used as follows: m1 + m2 ||  m1 + 3
         * raises TypeError if other is not a Matrix object or an integer
         * raises ValueError if adding another Matrix and it does not have the same dimensions as this matrix
        """
        if type(other) != int and type(other) != Matrix:
            raise TypeError("other is not a Matrix object or an integer")
        if type(other) == Matrix:
            if (other.row_num != self.row_num) or (other.col_num != self.col_num):
                raise ValueError("Other Matrix does not have the same dimensions")

        copied_matrix = self.copy()

        if type(other) == int:
            print("what the fuck???")
            for i in range(copied_matrix.row_num):
                for j in range(copied_matrix.col_num):
                    copied_matrix[i, j] += other
        elif type(other) == Matrix:
            for i in range(copied_matrix.row_num):
                for j in range(copied_matrix.col_num):
                    copied_matrix[i, j] += other[i, j]
        return copied_matrix

    def __mul__(self, other):
        """Multiplies self with another Matrix or integer, returning a new Matrix.

        This method should not modify the current matrix or other.
        Used as follows: m1*m2 => m1.__mul__(m2) (matrix multiplication, not point-wise)
        or: m1*3 => m1.__mul__(3)
        * raises TypeError if the other is not a Matrix object or an integer
        * raises ValueError if the other Matrix has incorrect dimensions
        """
        if type(other) != int and type(other) != Matrix:
            raise TypeError("other is not a Matrix object or an integer")
        if type(other) == Matrix:
            if other.row_num != self.col_num:
                raise ValueError("dimensions of other and self do not match!")

        if type(other) == int:
            copy_matrix = self.copy()
            for i in range(copy_matrix.row_num):
                for j in range(copy_matrix.col_num):
                    copy_matrix[i, j] *= other
            return copy_matrix
        elif type(other) == Matrix:
            matrix = Matrix(self.row_num, other.col_num)
            for i in range(self.row_num):
                for j in range(other.col_num):
                    mul_row = self.matrix[i]
                    mul_col = []
                    for k in range(other.row_num):
                        mul_col.append(other.matrix[k][j])
                    matrix[i, j] = sum([a*b for a, b in zip(mul_row, mul_col)])
            return matrix

    def get_dimensions(self):
        return (self.row_num, self.col_num)

    def __str__(self):
        """
        Returns a string representation of this matrix in the form:
          a b c
          d e f
          g h i
        Used as follows: s = str(m1)
        """
        res = []
        for row in self.matrix:
            res.append(' '.join([str(n) for n in row]))
        return "\n".join(res)

    def transpose(self):
        """
        Returns a new matrix that is the transpose of this Matrix object
        This method should not modify the current matrix.
        """
        Transpose_matrix = Matrix(self.col_num, self.row_num)
        for i in range(self.row_num):
            for j in range(self.col_num):
                Transpose_matrix[j, i] = self[i, j]
        return Transpose_matrix

    def copy(self):
        """
        Returns a new Matrix that is an exact and independent copy of this one
        This method should not modify the current matrix.
        """
        copied_matrix = Matrix(self.row_num, self.col_num)
        for i in range(copied_matrix.row_num):
            copied_matrix.matrix[i] = self.matrix[i][:]
        return copied_matrix
