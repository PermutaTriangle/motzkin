# In this file we implement the recurrences that prove the forms of the generating function.
import logging

import logzero
from sympy import Expr, Number, ratsimp, sqrt, var

from motzkin import MotzkinPath, MotzkinSpecificationFinder

logzero.loglevel(logging.WARNING)

x = var("x")
y = var("y")

C = var("C")  # 2 / (1 + sqrt(1 - 4 * x ** 2))  # catalan generating function
Cgenf = 2 / (1 + sqrt(1 - 4 * x ** 2))  # (1 - sqrt(1 - 4 * x ** 2)) / (2 * x ** 2)


def gamma(q: MotzkinPath) -> Expr:
    if len(q) == 0:
        return Number(1)
    qprime = MotzkinPath(q[:-1], pattern=True)
    gammaprime = gamma(qprime)
    if q[-1] == "U":
        return ratsimp(
            (x * y / ((1 - x) * (x - y * (1 - x))))
            * (x * gammaprime.subs({y: x / (1 - x)}) - y * (1 - x) * gammaprime)
        )
    if q[-1] == "H":
        return ratsimp(
            # (x / (y - x - x * y ** 2))
            (2 * x / ((y - x * C) * (1 - 2 * x * y + 1 - C * 2 * x ** 2)))
            * (y * gammaprime - x * C * gammaprime.subs({y: x * C}))
        )
    if q[-1] == "D":
        return ratsimp(
            (x / y) * (gammaprime / (1 - x * y - x) - gammaprime.subs({y: 0}) / (1 - x))
        )
    raise ValueError("this isn't a motzkin path")


def delta(q: MotzkinPath) -> Expr:
    if len(q) == 0:
        return Number(0)
    qprime = MotzkinPath(q[:-1], pattern=True)
    gammaprime = gamma(qprime)
    deltaprime = delta(qprime)
    if q[-1] == "D":
        return ratsimp(deltaprime + gammaprime.subs({y: 0}) / (1 - x))
    if q[-1] == "H":
        return ratsimp(deltaprime + C * gammaprime.subs({y: x * C}))
    if q[-1] == "U":
        return ratsimp(deltaprime + gammaprime.subs({y: x / (1 - x)}) / (1 - x))
    raise ValueError("this isn't a motzkin path")


if __name__ == "__main__":
    N = 10
    # ALL:
    msf = MotzkinSpecificationFinder([])
    spec = msf.auto_search()
    for i in range(5, 6):
        for q in spec.generate_objects_of_size(i):
            # print(q, type(q))
            # if sum(1 for l in q if l == "H") == 3:
            #     continue
            # if q in (
            #     MotzkinPath("HHHHH"),
            #     MotzkinPath("HHHUD"),
            #     MotzkinPath("HHUDH"),
            #     # MotzkinPath("HUDHH"),
            #     # MotzkinPath("HHUHD"),
            #     # MotzkinPath("HUDUD"),
            #     # MotzkinPath("HUHDH"),
            #     # MotzkinPath("HUHHD"),
            #     # MotzkinPath("HUHHD"),
            #     # MotzkinPath("HUHHD"),
            #     # MotzkinPath("HUUDD"),
            #     # MotzkinPath("UDHHH"),
            #     # MotzkinPath("UDHUD"),
            #     # MotzkinPath("UDUDH"),
            #     # MotzkinPath("UDUHD"),
            #     # MotzkinPath("UHDHH"),
            #     # MotzkinPath("UHDUD"),
            #     # MotzkinPath("UHHDH"),
            #     # MotzkinPath("UUDDH"),
            #     # MotzkinPath("UHHDH"),
            # ):
            #     continue
            print("Now cheking", q)
            gf = delta(MotzkinPath(q, pattern=True))
            actualgf = gf.subs({C: Cgenf})
            term = actualgf.series(n=None)
            try:
                terms = [next(term) / x ** i for i in range(N)]
            except:
                print(gf)
                print(actualgf)
                print("Skipped", q)
                continue

            # q = "H"
            msf = MotzkinSpecificationFinder([q])
            qspec = msf.auto_search()
            actual = [qspec.count_objects_of_size(i) for i in range(N)]

            # print(spec.get_genf())
            # print(gf)
            # print(actualgf)

            if actual != terms:
                print("===== FAIL ====", q, "==== FAIL ====")
                print(gf)
                print(actualgf)
                print("SPEC:", actual)
                print("RECS:", terms)
