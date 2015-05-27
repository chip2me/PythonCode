# Fibonacci numbers module

# return Fibonacci series up to n
def first(n):
    result = []
    a, b = 0, 1
    while b < n:
        result.append(b)
        a, b = b, a+b
        print(b)
    return(result)

print("\nStart fib first")
first(1000)
# This is a commented out line: input(Press<enter>")

input("Press<enter>")