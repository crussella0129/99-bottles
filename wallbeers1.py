a=99
b=a
c="bottle" 
d="of beer"
e="on the wall"
f="Take one down and pass it around,"
g="more"
h="Go to the store and buy some more,"
for i in range(a, -1, -1):
    if i > 2:
       print(f"{b} {c}s {d} {e}, {b} {c}s {d}.\n{f} {b-1} {c}s {d} {e}.\n")
    elif i == 2:
       print(f"{b} {c}s {d} {e}, {b} {c}s {d}.\n{f} {b-1} {c} {d} {e}.\n")
    elif i == 1:
       print(f"{b} {c} {d} {e}, {b} {c}.\n{f} no {g} {c}s {d} {e}.\n")
    else:
       print(f"No {g} {c}s {d} {e}, no {g} {c}s {d}.\n{h} 99 {c}s {d} {e}.")
    b-=1
