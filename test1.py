from numbers3 import AccurateNumber
from numbers3 import to_accurate_number
from series import *
from math import factorial

def sincoeff(n):
    if n%2==0: return 0
    else: return reciprocal(AccurateNumber.from_int(factorial(n)),500) * (-1)**((n-1)/2)  # this function isn't robust enough

def pi_approx(accuracy):
    pi = AccurateNumber.from_int(0)
    for n in range(1000):
        newterm = AccurateNumber.two_to_the(-n+1)*factorial(n)*factorial(2*n)*(25*n-3)*reciprocal(factorial(3*n),accuracy)
        #print(newterm.positive)

        pi += newterm
        if abs(newterm)<=AccurateNumber.two_to_the(-accuracy): break

    pi.to_accuracy(accuracy)
    pi.error = newterm

    return pi

def reciprocal(n, accuracy=20):
    n = to_accurate_number(n)

    if n.iszero(): raise ZeroDivisionError

    mexp = len("{0:b}".format(n.mantissa))
    expdif = n.exponent-mexp
    # need mexp + exponent = 1

    d = AccurateNumber(n.mantissa, n.exponent-expdif)

    x_old = d*(-1.88235294)+(2.82352941)
    for i in range(100):
        x_old.to_accuracy(accuracy)

        x_new = x_old*(-(d*x_old)+2)
        if abs(x_old-x_new)<=AccurateNumber(1,accuracy): break
        x_old = x_new

    return AccurateNumber(x_new.mantissa, x_new.exponent-expdif)

#print(AccurateNumber.from_float(25325.23529835))

print(series(pi_approx(800),sincoeff,AccurateNumber.two_to_the(-4000)))

