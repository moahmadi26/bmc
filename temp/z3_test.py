from z3 import *
x = Int('x')
y = Int('y')

r = Real('r')



print(solve(y == 1, x + y == 2, r == RealVal(2)*x))