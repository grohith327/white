class RingBuffer:
    def __init__(self, size):
        self.size = size
        self.buffer = [None] * size
        self.head = 0
        self.tail = 0
        self.full = False

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.head == self.tail and not self.full

    def is_full(self):
        return self.full

    def enqueue(self, value):
        if self.full:
            # Overwrite the oldest data if the buffer is full
            self.tail = (self.tail + 1) % self.size

        self.buffer[self.head] = value
        self.head = (self.head + 1) % self.size

        # If the buffer is full, update the full flag
        if self.head == self.tail:
            self.full = True

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty buffer")

        value = self.buffer[self.tail]
        self.buffer[self.tail] = None
        self.tail = (self.tail + 1) % self.size
        self.full = False

        return value

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty buffer")
        
        return self.buffer[self.tail]

    def __str__(self):
        return str(self.buffer)

# Example usage:
buffer = RingBuffer(3)
buffer.enqueue(1)
buffer.enqueue(2)
buffer.enqueue(3)

print("Buffer after enqueueing 3 items:", buffer)
print("Dequeueing:", buffer.dequeue())
print("Buffer after dequeue:", buffer)

buffer.enqueue(4)
print("Buffer after enqueueing 4:", buffer)

buffer.enqueue(5)
print("Buffer after enqueueing 5 (overwrites oldest):", buffer)