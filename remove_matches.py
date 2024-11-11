import sys

def remove_matches(a, b, c, d, e, f):
    a = [item for item in a if item not in d]
    b = [item for item in b if item not in e]
    c = [item for item in c if item not in f]
    return a, b, c

extra = []

x = int(input("How many extra routes?"))

a = list(map(str, input().split(' ')))
b = list(map(str, input().split(' ')))
c = list(map(str, input().split(' ')))
for i in range(x):
    d = list(map(str, input().split(' ')))
    e = list(map(str, input().split(' ')))
    f = list(map(str, input().split(' ')))
    a, b, c = remove_matches(a, b, c, d, e, f)

print("Updated:")
print(" ".join(a))
print(" ".join(b))
print(" ".join(c))

input("Press enter to exit")
