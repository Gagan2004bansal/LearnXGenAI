# resources.py
# MCP Resources: read-only data your server exposes (like files or DB records).
# Resources are identified by a URI and returned as text or binary content.

SAMPLE_CODES: dict[str, str] = {

    "bubble_sort": '''\
def bubble_sort(arr):
    """Sort a list using the Bubble Sort algorithm."""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# Example
nums = [64, 34, 25, 12, 22, 11, 90]
print(bubble_sort(nums))
''',

    "binary_search": '''\
def binary_search(arr, target):
    """Search for target in a SORTED list. Returns index or -1."""
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

# Example
sorted_list = [1, 3, 5, 7, 9, 11, 13]
print(binary_search(sorted_list, 7))   # → 3
print(binary_search(sorted_list, 4))   # → -1
''',

    "fibonacci": '''\
def fibonacci(n):
    """Return the first n Fibonacci numbers."""
    sequence = []
    a, b = 0, 1
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence

# Example
print(fibonacci(10))
''',

    "stack_class": '''\
class Stack:
    """A simple stack (LIFO) backed by a list."""

    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek at empty stack")
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)

# Example
s = Stack()
s.push(1)
s.push(2)
print(s.pop())   # → 2
print(s.peek())  # → 1
''',

    "word_frequency": '''\
from collections import Counter

def word_frequency(text):
    """Count how often each word appears in a string."""
    words = text.lower().split()
    # Strip basic punctuation
    words = [w.strip(".,!?;:\\"\'") for w in words]
    return dict(Counter(words).most_common())

# Example
sample = "to be or not to be that is the question to be"
print(word_frequency(sample))
''',
}


def list_sample_codes() -> list[dict]:
    """Return metadata for every available sample."""
    return [
        {
            "uri": f"sample://codes/{name}",
            "name": name,
            "description": f"Sample Python snippet: {name.replace('_', ' ')}",
            "mimeType": "text/plain",
        }
        for name in SAMPLE_CODES
    ]


def get_sample_code(name: str) -> str | None:
    """Return the source text for a named sample, or None if not found."""
    return SAMPLE_CODES.get(name)