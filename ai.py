import sympy as sp
from sympy import symbols

# define symbols for normal math
x, y, z = symbols('x y z')

# define symbols used in research equations
Ps, hk, ht, gk, alpha, beta, ak, sigma2, gamma_th, Ik = symbols(
    'Ps hk ht gk alpha beta ak sigma2 gamma_th Ik'
)

print("FREE AI Math Agent (SymPy)")
print("Type 'exit' to quit")

while True:

    expr = input("\nEnter math expression: ")

    if expr.lower() == "exit":
        break

    try:
        sym_expr = sp.sympify(expr)

        print("\nExpression:")
        print(sym_expr)

        print("\nSimplified:")
        print(sp.simplify(sym_expr))

        print("\nExpanded:")
        print(sp.expand(sym_expr))

        print("\nDerivative (with respect to x):")
        print(sp.diff(sym_expr, x))

    except Exception as e:
        print("Error:", e)