# Fibonacci numbers module

# write Fibonacci series up to n
def fib1(n):
    a, b = 0, 1
    while b < n:
        a, b = b, a+b
        print (b)

# return Fibonacci series up to n
def fib2(n):
    result = []
    a, b = 0, 1
    while b < n:
        result.append(b)
        a, b = b, a+b
        print(b)
    return(result)


        

print("\nStart fib1")
fib1(1000)
print("Stop")

print("\nStart fib2")
fib2(1000)
print("Stop")


input("Press<enter>")
