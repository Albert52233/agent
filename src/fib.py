import sys


def fib(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fib.py <n>")
        sys.exit(1)
    try:
        n = int(sys.argv[1])
        print(fib(n))
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
