# Example 1: Using looping technique
def fibo(n):
    a,b = 1,1
    for i in range(n-1):
        a,b = b,a+b
    return a 
print(fibo(10))

# Example 2: Using RecursionError
def fibR(n):
    if n==1 or n==2:
        return 1
    return fibR(n-1)+fibR(n-2)
print(fibR(10))


