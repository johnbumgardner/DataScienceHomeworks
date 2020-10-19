import math
import timeit
gr = (math.sqrt(5) + 1) / 2

def gss(f, a, b, tol=1e-5):
    c = b - (b - a) / gr
    d = a + (b - a) / gr
    while abs(c - d) > tol:
        if f(c) < f(d):
            b = d
        else:
            a = c

        # We recompute both c and d here to avoid loss of precision which may lead to incorrect results or infinite loop
        c = b - (b - a) / gr
        d = a + (b - a) / gr

    return (b + a) / 2


def main():
    start = timeit.default_timer()
    f = lambda x: (x-2)**2
    x = gss(f, 1, 5)
    stop = timeit.default_timer()
    print("Minimum: " + str(x) + " in time: " + str(stop-start))

main()