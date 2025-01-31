class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        """Add an item to the top of the stack."""
        self._items.append(item)

    def pop(self):
        """Remove and return the item from the top of the stack."""
        if not self.is_empty():
            return self._items.pop()
        else:
            raise IndexError("Pop from an empty stack")

    def peek(self):
        """Return the item at the top of the stack without removing it."""
        if not self.is_empty():
            return self._items[-1]
        else:
            raise IndexError("Peek from an empty stack")

    def is_empty(self):
        """Check if the stack is empty."""
        return len(self._items) == 0

    def size(self):
        """Return the number of items in the stack."""
        return len(self._items)

    def __str__(self):
        """Return a string representation of the stack."""
        return str(self._items)

# Example usage
stack = Stack()

# Push items onto the stack
stack.push(10)
stack.push(20)
stack.push(30)

print("Stack:", stack)
print("Size of stack:", stack.size())
print("Top item:", stack.peek())

# Pop items from the stack
print("Popped item:", stack.pop())
print("Stack after pop:", stack)

# Check if the stack is empty
print("Is the stack empty?", stack.is_empty())