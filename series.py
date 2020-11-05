from numbers3 import AccurateNumber

def series(x, coeffs, accuracy):
    accuracy = max(accuracy, x.error*0.5)
    result = AccurateNumber.from_int(0)
    lastpower = AccurateNumber.from_int(1)

    for i in range(1000):
        result = result + lastpower * coeffs(i)

        lastpower *= x
        if coeffs(i+1)!=0 and abs(lastpower*coeffs(i+1))<accuracy: break
    
    result.error = max(x.error, abs(lastpower*coeffs(i+1)))

    return result