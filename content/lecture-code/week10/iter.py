class Squares:
    def __init__(self, maxBase):
        self.i = 0
        self.max = maxBase

    def __iter__(self):
        return self

    def __next__(self):
        if self.i >= self.max:
            raise StopIteration
        self.i += 1
        return self.i*self.i

S = Squares(50)
for square in S:
    print(square)