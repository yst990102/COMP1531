class Stack:
    def __init__(self):
        self.stack = []

    def stack_pop(self):
        if self.stack == []:
            raise IndexError("you can't pop from empty stack!")
        return self.stack.pop()

    def stack_push(self, item):
        return self.stack.append(item)
