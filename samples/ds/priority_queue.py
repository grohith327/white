import heapq

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0  # Used to handle elements with the same priority

    def push(self, item, priority):
        """Add an item to the priority queue with a given priority."""
        # heapq is a min-heap, so we use negative priority to simulate a max-heap
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index = self._index + 1

    def pop(self):
        """Remove and return the item with the highest priority."""
        if not self.is_empty():
            _, _, item = heapq.heappop(self._queue)
            return item
        else:
            raise IndexError("Priority queue is empty")

    def is_empty(self):
        """Check if the priority queue is empty."""
        return len(self._queue) == 0

    def peek(self):
        """Return the item with the highest priority without removing it."""
        if not self.is_empty():
            return self._queue[0][2]  # Return the item part of the tuple
        else:
            raise IndexError("Priority queue is empty")

    def __len__(self):
        """Return the number of items in the priority queue."""
        return len(self._queue)

# Example usage
pq = PriorityQueue()

# Push items with priorities
pq.push("Task 1", 3)
pq.push("Task 2", 1)
pq.push("Task 3", 2)
pq.push("Task 4", 5)

print("Priority Queue Length:", len(pq))

# Pop items in order of priority
while not pq.is_empty():
    print("Processing:", pq.pop())

# Check if the queue is empty
print("Is the priority queue empty?", pq.is_empty())