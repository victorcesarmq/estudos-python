# Enter your code here. Read input from STDIN. Print output to STDOUT


n,m = map(int,input().split())

for i in range(1, n, 2):
    pattern = ".|." * i
    print(pattern.center(m, "-"))

print("MESSAGE".center(m, "-"))

for i in range(n-2, -1, -2):
    pattern = ".|." * i
    print(pattern.center(m, "-"))