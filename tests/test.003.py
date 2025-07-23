import math

for x in range(-10,10):
    if x != 0:
        z = math.atan(x / 10)
    print("arctan(" + str(x / 10) + ") = " + str(z))