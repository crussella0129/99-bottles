a=99
b="bottle"
c=f"{b}s of beer" 
d=f"{c} on the wall"
e="Take one down and pass it around,"
f=f"{b} of beer" 
g=f"{f} on the wall"
h="o more"
i="Go to the store and buy some more,"
for j in range(a, -1, -1):
    if j > 2:
       print(f"{a} {d}, {a} {c}.\n{e} {a-1} {d}.\n")
    elif j == 2:
       print(f"{a} {d}, {a} {c}.\n{e} {a-1} {g}.\n")
    elif j == 1:
       print(f"{a} {g}, {a} {f}.\n{e} n{h} {d}.\n")
    else:
       print(f"N{h} {d}, n{h} {c}. \n{i} 99 {d}.")
    a-=1
