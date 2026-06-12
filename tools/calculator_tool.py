# from langchain.tools import tool
# import sympy


# @tool
# def math_solver(expression: str) -> str:
#     """
# Use this tool to solve equations.

# Do NOT solve equations yourself.

# Your job is to translate word problems into equations and send them to the tool.

# The tool is responsible for algebraic manipulation and solving.    """
#     try:

#         expr = sympy.sympify(expression)

#         if expr.free_symbols:
#             return "ERROR: Variables are not allowed."

#         return str(float(expr.evalf()))

#     except Exception as e:
#         return f"ERROR: {e}"
# from langchain.tools import tool
# import sympy as sp
# import string


# @tool
# def math_solver(expression: str) -> str:
#     """
#     SymPy math engine.

#     Supports:
#     - arithmetic
#     - algebra
#     - equations
#     - systems of equations
#     - differentiation
#     - integration
#     - simplification
#     """

#     try:

#         symbols = {
#             ch: sp.Symbol(ch)
#             for ch in string.ascii_lowercase
#         }

#         safe_globals = {
#             "__builtins__": {},
#             **sp.__dict__,
#             **symbols,
#         }

#         result = eval(expression, safe_globals)

#         # If symbolic remains, return symbolic
#         if hasattr(result, "free_symbols") and result.free_symbols:
#             return str(result)

#         # Otherwise return numeric value
#         return str(sp.N(result))

#     except Exception as e:
#         return f"ERROR: {e}"
from langchain.tools import tool
import sympy as sp
import string


@tool
def math_solver(expression: str) -> str:
    """
    Robust SymPy math engine.
    """

    try:
        # define symbols
        symbols = {ch: sp.Symbol(ch) for ch in string.ascii_lowercase}

        local_dict = {
            **symbols,
            "sp": sp,
            "Eq": sp.Eq,
            "solve": sp.solve,
            "diff": sp.diff,
            "integrate": sp.integrate,
            "simplify": sp.simplify,
            "factor": sp.factor,
            "expand": sp.expand,
            "sqrt": sp.sqrt,
        }

        result = eval(expression, {"__builtins__": {}}, local_dict)

        # ---------------------------
        # NORMALIZATION LAYER
        # ---------------------------

        # case 1: list (solve output)
        if isinstance(result, list):
            return str(result)

        # case 2: dict (systems)
        if isinstance(result, dict):
            return str(result)

        # case 3: sympy expressions
        if hasattr(result, "evalf"):
            return str(result.evalf())

        # case 4: fallback numeric
        return str(result)

    except Exception as e:
        return f"ERROR: {e}"