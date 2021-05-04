class Matrix:
    def __init__(self, m, n):
        """Initialises (with zeros) a matrix of dimensions m by n."""
        pass

    def __str__(self):
        """Returns a string representation of this matrix as integers in the form:
          a b c
          d e f
          g h i
        Used as follows: s = str(m1)
        """
        return "Not implemented"

    def get(self, key):
        """Returns the (i,j)th entry of the matrix, where key is the tuple (i, j)

        Used as follows: x = matrix.get((0,0))
        * raises IndexError if (i,j) is out of bounds
        """
        pass

    def set(self, key, data):
        """Sets the (i,j)th entry of the matrix, where key is the tuple (i, j)

        and data is the number being added.
        Used as follows: matrix.set((0,0), 1)
        * raises IndexError if (i,j) is out of bounds
        * raises TypeError if data is not an integer
        """
        pass

    def add(self, other):
        """Adds self to another Matrix or integer, returning a new Matrix.

        This method should not modify the current matrix or other.
        Used as follows: m1.add(m2) => m1 + m2
        or: m1.add(3) => m1 + 3
        * raises TypeError if other is not a Matrix object or an integer
        * raises ValueError if the other Matrix does not have the same dimensions
        """
        pass

    def mul(self, other):
        """Multiplies self with another Matrix or integer, returning a new Matrix.

        This method should not modify the current matrix or other.
        Used as follows: m1.mul(m2) m1 x m2 (matrix multiplication, not point-wise)
        or: m1.mul(3) => m1*3
        * raises TypeError if the other is not a Matrix object or an integer
        * raises ValueError if the other Matrix has incorrect dimensions
        """
        pass
