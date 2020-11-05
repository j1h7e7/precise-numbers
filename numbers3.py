# in base 2
from math import frexp, log10, log2

def to_accurate_number(number):
    if type(number)==int:     return AccurateNumber.from_int(number)
    elif type(number)==float: return AccurateNumber.from_float(number)
    else:                     return number

class AccurateNumber:
    def __init__(self, mantissa, exponent=0, error=0, positive=True):
        self.mantissa = int(mantissa)
        self.exponent = int(exponent)
        self.error = error
        self.positive = positive

    @classmethod
    def from_int(cls, value):
        return cls(abs(value), positive= value>=0)

    @classmethod
    def from_float(cls, value):
        if value == 0: return cls(0)

        m = abs(value)
        e = 0
        while m!=int(m):
            e+=1
            m*=2
        
        return cls(m,e,error=(2**(-53+int(log2(abs(value))))),positive=(value>0))

    @classmethod
    def two_to_the(cls, n):
        if type(n)!=int: raise TypeError
        if n>=0: return cls(2**n,0)
        else: return cls(1,-n)

    def __str__(self):
        whole_part = int(self.mantissa/(2**self.exponent))

        decimal_part = self.mantissa%(2**self.exponent)
        decimal_part *= (5**self.exponent)

        whole_part = str(int(whole_part))
        if decimal_part!=0: decimal_part = str(int(decimal_part))
        else: decimal_part = ""

        while len(decimal_part)<self.exponent: decimal_part = "0"+decimal_part

        point = "." if len(decimal_part)>0 else ""
        sign = "" if self.positive else "-"

        error = ""
        if self.error!=0:
            error = " ±"+str(float(self.error))
            decimal_part = decimal_part[:-int(log10(float(self.error)))+2]

        return sign+whole_part+point+decimal_part+error

    def __add__(self, other):
        num2 = to_accurate_number(other)

        newexp = max(self.exponent, num2.exponent)

        final = AccurateNumber(0,newexp)

        final.mantissa += self.mantissa * (2**(newexp-self.exponent)) * (1 if self.positive else -1)
        final.mantissa += num2.mantissa * (2**(newexp-num2.exponent)) * (1 if num2.positive else -1)

        while final.mantissa%2 == 0 and final.mantissa!=0:
            final.mantissa = int(final.mantissa >> 1)
            final.exponent -= 1

        final.positive = final.mantissa>=0
        final.mantissa = abs(final.mantissa)
        if type(self.error)==AccurateNumber: final.error = self.error+num2.error
        else: final.error = num2.error+self.error

        return final

    def __neg__(self):
        return AccurateNumber(self.mantissa,self.exponent,self.error,not self.positive)

    def __sub__(self, other):
        return self + (-other)

    def iszero(self):
        return self.mantissa==0

    def __lt__(self, other):
        num2 = to_accurate_number(other)
        dif = self-num2
        return not(dif.iszero()) and not dif.positive

    def __gt__(self, other):
        num2 = to_accurate_number(other)
        dif = self-num2
        return not(dif.iszero()) and dif.positive

    def __le__(self, other):
        return not self>other

    def __ge__(self, other):
        return not self<other

    def __mul__(self,other):
        num2 = to_accurate_number(other)

        if type(self.error)==AccurateNumber: error = self.error*num2.error
        else: error = num2.error*self.error

        return AccurateNumber(self.mantissa*num2.mantissa,self.exponent+num2.exponent,error,self.positive==num2.positive)

    def __abs__(self):
        return AccurateNumber(self.mantissa, self.exponent, self.error, True)

    def to_accuracy(self, n):
        # in place
        if self.exponent<=n: return

        self.mantissa = (self.mantissa >> self.exponent-n)
        self.exponent = n
        return

    def reduce_mantissa(self, n):
        size = len("{0:#b}".format(self.mantissa))
        self.mantissa = (self.mantissa >> size-n)
        self.exponent -= size-n

    def __float__(self):
        n = AccurateNumber(self.mantissa,self.exponent,positive=self.positive)
        n.reduce_mantissa(20)
        return n.mantissa*2**(-n.exponent)
